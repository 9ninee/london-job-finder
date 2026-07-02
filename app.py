"""
London Graduate Job Search Platform
Aggregates jobs directly from company career pages via:
  - Greenhouse ATS  (public API, no key needed)
  - Lever ATS       (public API, no key needed)
  - Ashby ATS       (public API, no key needed) — discovered via github.com/santifer/career-ops
  - Workday ATS     (public POST API, no key needed) — Goldman, JP Morgan, McKinsey, BCG…
  - Adzuna UK       (optional free API key)
  - Find a Job Gov  (UK Government official job board, no key needed)
"""

from flask import Flask, render_template, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from dotenv import load_dotenv
import os

load_dotenv()

from sources.greenhouse import fetch_greenhouse_jobs
from sources.lever import fetch_lever_jobs
from sources.ashby import fetch_ashby_jobs
from sources.workday import fetch_workday_jobs
from sources.adzuna import fetch_adzuna_jobs
from sources.findajob import fetch_findajob_jobs
from sources.themuse import fetch_themuse_jobs

app = Flask(__name__)

FETCHERS = {
    "Greenhouse": fetch_greenhouse_jobs,
    "Lever":      fetch_lever_jobs,
    "Ashby":      fetch_ashby_jobs,
    "Workday":    fetch_workday_jobs,
    "Adzuna":     fetch_adzuna_jobs,
    "FindAJob":   fetch_findajob_jobs,
    "TheMuse":    fetch_themuse_jobs,
}


@app.route("/")
def index():
    adzuna_configured = bool(os.getenv("ADZUNA_APP_ID") and os.getenv("ADZUNA_APP_KEY"))
    return render_template("index.html", adzuna_configured=adzuna_configured)


@app.route("/api/search", methods=["POST"])
def search():
    data = request.get_json() or {}
    keywords = data.get("keywords", [])
    filters  = data.get("filters", {})

    all_jobs = []
    errors   = []

    with ThreadPoolExecutor(max_workers=7) as executor:
        futures = {
            executor.submit(fn, keywords): name
            for name, fn in FETCHERS.items()
        }
        for future in as_completed(futures, timeout=22):
            source = futures[future]
            try:
                jobs = future.result(timeout=22)
                all_jobs.extend(jobs)
            except Exception as e:
                errors.append(f"{source}: {str(e)}")

    # Apply tag filters (only if user deselected some)
    if filters.get("tags"):
        selected_tags = set(filters["tags"])
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

    # Sort: newest first
    unique_jobs.sort(key=lambda x: (x.get("days_ago", 999), x.get("company", "")))

    return jsonify({
        "jobs":   unique_jobs,
        "total":  len(unique_jobs),
        "errors": errors,
    })


@app.route("/api/sources")
def sources():
    from sources.company_lists import (
        GREENHOUSE_COMPANIES, LEVER_COMPANIES,
        ASHBY_COMPANIES, WORKDAY_COMPANIES,
    )
    return jsonify({
        "greenhouse_count": len(GREENHOUSE_COMPANIES),
        "lever_count":      len(LEVER_COMPANIES),
        "ashby_count":      len(ASHBY_COMPANIES),
        "workday_count":    len(WORKDAY_COMPANIES),
        "adzuna_enabled":   bool(os.getenv("ADZUNA_APP_ID")),
        "total_companies": (
            len(GREENHOUSE_COMPANIES) + len(LEVER_COMPANIES)
            + len(ASHBY_COMPANIES) + len(WORKDAY_COMPANIES)
        ),
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    print(f"\n  London Job Finder running at http://localhost:{port}\n")
    app.run(debug=True, port=port)
