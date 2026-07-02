"""
Fetches jobs from Adzuna API (aggregates from UK company career pages).
Requires free API credentials from https://developer.adzuna.com/
Set ADZUNA_APP_ID and ADZUNA_APP_KEY in your .env file.
Queries run in parallel to stay within Render's 30s request limit.
"""

import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import (
    RELEVANT_TITLE_KEYWORDS, is_foreign_role, requires_experience,
)

BASE_URL = "https://api.adzuna.com/v1/api/jobs/gb/search/{page}"
TIMEOUT = 5

# Exclude clearly-irrelevant sectors that share words like "analyst"/"consultant"
EXCLUDE_KEYWORDS = [
    "recruitment", "recruiter", "sales executive", "sales manager", "estate agent",
    "cyber security", "security analyst", "soc analyst", "penetration",
    "nurse", "care assistant", "carer", "teacher", "teaching", "tutor",
    "warehouse", "driver", "delivery", "retail assistant", "hospitality",
    "chef", "cleaner", "receptionist", "beauty", "mechanic", "electrician",
]


def _is_relevant(title: str, category: str) -> bool:
    text = (title + " " + category).lower()
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return False
    return any(kw in text for kw in RELEVANT_TITLE_KEYWORDS)

# Adzuna ANDs all words in `what`, so keep queries SHORT (2 words max) and
# never include "london" here — location is handled by the `where` param.
# Each query returns up to 50 results, all run in parallel.
SEARCH_QUERIES = [
    "graduate analyst",
    "graduate scheme",
    "data analyst",
    "investment analyst",
    "financial analyst",
    "consulting analyst",
    "business analyst",
    "risk analyst",
]


def _parse_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return dt.strftime("%d %b %Y")
    except Exception:
        return ""


def _days_ago(date_str: str) -> int:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", ""))
        return (datetime.now() - dt).days
    except Exception:
        return 999


def _extract_tags(title: str, category: str) -> list[str]:
    tags = []
    combined = (title + " " + category).lower()
    if any(k in combined for k in ["graduate", "grad", "entry"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "bi"]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "investment"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult"]):
        tags.append("Consulting")
    return tags or ["Finance"]


def _fetch_query(query: str, app_id: str, app_key: str) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL.format(page=1),
            params={
                "app_id": app_id,
                "app_key": app_key,
                "what": query,
                "where": "London",
                "distance": 15,
                "results_per_page": 50,
                "sort_by": "date",
                "max_days_old": 60,
            },
            timeout=TIMEOUT,
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        results = []
        for job in data.get("results", []):
            title    = job.get("title", "")
            company  = job.get("company", {}).get("display_name", "Unknown")
            location = job.get("location", {}).get("display_name", "London, UK")
            url      = job.get("redirect_url", "")
            created  = job.get("created", "")
            category = job.get("category", {}).get("label", "")
            description = job.get("description", "")

            if not _is_relevant(title, category):
                continue

            # Focus on graduate/entry-level: drop foreign & experienced roles.
            # (Senior *titles* are handled by the client-side toggle.)
            if is_foreign_role(title, location):
                continue
            if requires_experience(description):
                continue

            days = _days_ago(created)
            if days > 90:
                continue

            results.append({
                "id":            f"az_{job.get('id', '')}",
                "title":         title,
                "company":       company,
                "location":      location,
                "department":    category,
                "posted_date":   _parse_date(created),
                "days_ago":      days,
                "url":           url,
                "source":        "Company Career Page",
                "source_system": "Adzuna",
                "tags":          _extract_tags(title, category),
            })

        return results

    except Exception:
        return []


def fetch_adzuna_jobs(user_keywords: list[str] = None) -> list[dict]:
    app_id  = os.getenv("ADZUNA_APP_ID", "")
    app_key = os.getenv("ADZUNA_APP_KEY", "")

    if not app_id or not app_key:
        return []

    queries = SEARCH_QUERIES.copy()
    if user_keywords:
        queries.insert(0, " ".join(user_keywords) + " london")

    all_jobs = []
    seen_ids = set()

    # Run all queries in parallel instead of sequentially
    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        futures = [executor.submit(_fetch_query, q, app_id, app_key) for q in queries]
        for future in as_completed(futures):
            try:
                for job in future.result():
                    if job["id"] not in seen_ids:
                        seen_ids.add(job["id"])
                        all_jobs.append(job)
            except Exception:
                pass

    return all_jobs
