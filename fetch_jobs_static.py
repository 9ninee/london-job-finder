"""
Standalone job fetcher for GitHub Pages static hosting.
Run by GitHub Actions every 6 hours.
Writes all jobs to docs/data/jobs.json.
"""

import json
import os
import sys
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from sources.greenhouse import fetch_greenhouse_jobs
from sources.lever import fetch_lever_jobs
from sources.ashby import fetch_ashby_jobs
from sources.workday import fetch_workday_jobs
from sources.adzuna import fetch_adzuna_jobs
from sources.findajob import fetch_findajob_jobs
from sources.company_lists import (
    GREENHOUSE_COMPANIES, LEVER_COMPANIES,
    ASHBY_COMPANIES, WORKDAY_COMPANIES,
)

FETCHERS = {
    "Greenhouse": fetch_greenhouse_jobs,
    "Lever":      fetch_lever_jobs,
    "Ashby":      fetch_ashby_jobs,
    "Workday":    fetch_workday_jobs,
    "Adzuna":     fetch_adzuna_jobs,
    "FindAJob":   fetch_findajob_jobs,
}

OUTPUT_PATH = Path(__file__).parent / "docs" / "data" / "jobs.json"


def main():
    print("Fetching jobs from all sources...")
    all_jobs = []
    errors = []

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {executor.submit(fn): name for name, fn in FETCHERS.items()}
        for future in as_completed(futures, timeout=60):
            source = futures[future]
            try:
                jobs = future.result(timeout=60)
                print(f"  ✓ {source}: {len(jobs)} jobs")
                all_jobs.extend(jobs)
            except Exception as e:
                print(f"  ✗ {source}: {e}", file=sys.stderr)
                errors.append(f"{source}: {str(e)}")

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

    output = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total": len(unique_jobs),
        "errors": errors,
        "meta": {
            "greenhouse_count": len(GREENHOUSE_COMPANIES),
            "lever_count":      len(LEVER_COMPANIES),
            "ashby_count":      len(ASHBY_COMPANIES),
            "workday_count":    len(WORKDAY_COMPANIES),
            "total_companies": (
                len(GREENHOUSE_COMPANIES) + len(LEVER_COMPANIES)
                + len(ASHBY_COMPANIES) + len(WORKDAY_COMPANIES)
            ),
            "adzuna_enabled": bool(os.getenv("ADZUNA_APP_ID")),
        },
        "jobs": unique_jobs,
    }

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, indent=2, ensure_ascii=False))

    print(f"\nDone: {len(unique_jobs)} unique jobs → {OUTPUT_PATH}")
    if errors:
        print(f"Errors: {errors}")


if __name__ == "__main__":
    main()
