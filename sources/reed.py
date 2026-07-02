"""
Fetches jobs from the Reed.co.uk API — the UK's largest job board.
Requires a free API key from https://www.reed.co.uk/developers/jobseeker
Set REED_API_KEY in your .env file (or as a GitHub Actions secret).
Auth: HTTP Basic — API key as username, blank password.
Queries run in parallel.
"""

import os
import requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import RELEVANT_TITLE_KEYWORDS

BASE_URL = "https://www.reed.co.uk/api/1.0/search"
TIMEOUT = 6

# Reed does keyword AND matching too — keep queries short, no "london".
SEARCH_QUERIES = [
    "graduate analyst",
    "graduate scheme",
    "data analyst",
    "investment analyst",
    "financial analyst",
    "consulting analyst",
    "risk analyst",
    "business analyst",
]

EXCLUDE_KEYWORDS = [
    "recruitment", "recruiter", "sales executive", "sales manager", "estate agent",
    "cyber security", "security analyst", "soc analyst", "penetration",
    "nurse", "care assistant", "carer", "teacher", "teaching", "tutor",
    "warehouse", "driver", "delivery", "retail assistant", "hospitality",
    "chef", "cleaner", "receptionist", "beauty", "mechanic", "electrician",
]


def _is_relevant(title: str) -> bool:
    text = title.lower()
    if any(bad in text for bad in EXCLUDE_KEYWORDS):
        return False
    return any(kw in text for kw in RELEVANT_TITLE_KEYWORDS)


def _parse_date(date_str: str) -> str:
    """Reed dates come as DD/MM/YYYY."""
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return dt.strftime("%d %b %Y")
    except Exception:
        return ""


def _days_ago(date_str: str) -> int:
    try:
        dt = datetime.strptime(date_str, "%d/%m/%Y")
        return (datetime.now() - dt).days
    except Exception:
        return 999


def _extract_tags(title: str) -> list[str]:
    tags = []
    t = title.lower()
    if any(k in t for k in ["graduate", "grad", "entry level", "trainee", "junior", "intern"]):
        tags.append("Graduate")
    if any(k in t for k in ["data", "analytics", "insight", "bi "]):
        tags.append("Data & Analytics")
    if any(k in t for k in ["finance", "financial", "treasury", "investment", "credit", "risk"]):
        tags.append("Finance")
    if any(k in t for k in ["banking", "bank", "capital markets"]):
        tags.append("Banking")
    if any(k in t for k in ["consult", "advisory", "adviser"]):
        tags.append("Consulting")
    if any(k in t for k in ["quant", "quantitative", "trading"]):
        tags.append("Quantitative")
    return tags or ["Finance"]


def _fetch_query(query: str, api_key: str) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL,
            params={
                "keywords": query,
                "locationName": "London",
                "distanceFromLocation": 10,
                "resultsToTake": 100,
            },
            auth=(api_key, ""),
            timeout=TIMEOUT,
            headers={"User-Agent": "LondonJobFinder/1.0"},
        )
        if resp.status_code != 200:
            return []

        results = []
        for job in resp.json().get("results", []):
            title    = job.get("jobTitle", "")
            company  = job.get("employerName", "Unknown")
            location = job.get("locationName", "London")
            url      = job.get("jobUrl", "")
            created  = job.get("date", "")   # DD/MM/YYYY

            if not _is_relevant(title):
                continue

            days = _days_ago(created)
            if days > 90:
                continue

            results.append({
                "id":            f"reed_{job.get('jobId', '')}",
                "title":         title,
                "company":       company,
                "location":      location or "London, UK",
                "department":    "",
                "posted_date":   _parse_date(created),
                "days_ago":      days,
                "url":           url,
                "source":        "Company Career Page (via Reed)",
                "source_system": "Reed",
                "tags":          _extract_tags(title),
            })

        return results

    except Exception:
        return []


def fetch_reed_jobs(user_keywords: list[str] = None) -> list[dict]:
    api_key = os.getenv("REED_API_KEY", "")
    if not api_key:
        return []

    queries = SEARCH_QUERIES.copy()
    if user_keywords:
        queries.insert(0, " ".join(user_keywords))

    all_jobs = []
    seen_ids: set[str] = set()

    with ThreadPoolExecutor(max_workers=len(queries)) as executor:
        futures = [executor.submit(_fetch_query, q, api_key) for q in queries]
        for future in as_completed(futures):
            try:
                for job in future.result():
                    if job["id"] not in seen_ids:
                        seen_ids.add(job["id"])
                        all_jobs.append(job)
            except Exception:
                pass

    return all_jobs
