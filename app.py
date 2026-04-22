"""
London Graduate Job Search Platform
Aggregates jobs directly from company career pages via Greenhouse, Lever, and Adzuna APIs.
"""

from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os

load_dotenv()

from sources.greenhouse import fetch_greenhouse_jobs
from sources.lever import fetch_lever_jobs
from sources.adzuna import fetch_adzuna_jobs

app = Flask(__name__)


@app.route("/")
def index():
    adzuna_configured = bool(os.getenv("ADZUNA_APP_ID") and os.getenv("ADZUNA_APP_KEY"))
    return render_template("index.html", adzuna_configured=adzuna_configured)


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json() or {}
    keywords = data.get("keywords", [])
    filters = data.get("filters", {})

    all_jobs = []
    errors = []

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = {
            executor.submit(fetch_greenhouse_jobs, keywords): "Greenhouse",
            executor.submit(fetch_lever_jobs, keywords): "Lever",
            executor.submit(fetch_adzuna_jobs, keywords): "Adzuna",
        }
        for future in as_completed(futures):
            source = futures[future]
            try:
                jobs = future.result(timeout=20)
                all_jobs.extend(jobs)
            except Exception as e:
                errors.append(f"{source}: {str(e)}")

    # Apply tag filters
    if filters.get("tags"):
        selected_tags = filters["tags"]
        all_jobs = [
            j for j in all_jobs
            if any(tag in j.get("tags", []) for tag in selected_tags)
        ]

    # Apply source system filter
    if filters.get("source"):
        all_jobs = [j for j in all_jobs if j.get("source_system") == filters["source"]]

    # Deduplicate by URL
    seen_urls = set()
    unique_jobs = []
    for job in all_jobs:
        url = job.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)
        elif not url:
            unique_jobs.append(job)

    # Sort: newest first, then by company name
    unique_jobs.sort(key=lambda x: (x.get("days_ago", 999), x.get("company", "")))

    return jsonify({
        "jobs": unique_jobs,
        "total": len(unique_jobs),
        "errors": errors,
    })


@app.route("/api/sources")
def sources():
    from sources.company_lists import GREENHOUSE_COMPANIES, LEVER_COMPANIES
    return jsonify({
        "greenhouse_count": len(GREENHOUSE_COMPANIES),
        "lever_count": len(LEVER_COMPANIES),
        "adzuna_enabled": bool(os.getenv("ADZUNA_APP_ID")),
        "total_companies": len(GREENHOUSE_COMPANIES) + len(LEVER_COMPANIES),
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    print(f"\n  London Job Finder running at http://localhost:{port}\n")
    app.run(debug=True, port=port)
