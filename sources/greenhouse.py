"""
Fetches jobs directly from Greenhouse ATS company career boards.
API is public — no API key required.
Docs: https://developers.greenhouse.io/job-board.html
"""

import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import GREENHOUSE_COMPANIES, RELEVANT_TITLE_KEYWORDS, LONDON_LOCATION_KEYWORDS

BASE_URL = "https://boards-api.greenhouse.io/v1/boards/{slug}/jobs"
TIMEOUT = 8


def _is_relevant(title: str, location: str) -> bool:
    title_lower = title.lower()
    location_lower = location.lower()
    has_keyword = any(kw in title_lower for kw in RELEVANT_TITLE_KEYWORDS)
    is_london = any(loc in location_lower for loc in LONDON_LOCATION_KEYWORDS) or location == ""
    return has_keyword and is_london


def _parse_date(date_str: str) -> str:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.strftime("%d %b %Y")
    except Exception:
        return ""


def _days_ago(date_str: str) -> int:
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        delta = datetime.now(timezone.utc) - dt
        return delta.days
    except Exception:
        return 999


def _fetch_one(slug: str, company_name: str, user_keywords: list[str]) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL.format(slug=slug),
            params={"content": "true"},
            timeout=TIMEOUT,
            headers={"User-Agent": "LondonJobFinder/1.0"},
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        jobs = data.get("jobs", [])
        results = []

        for job in jobs:
            title = job.get("title", "")
            location = job.get("location", {}).get("name", "")
            updated = job.get("updated_at", "")
            url = job.get("absolute_url", "")
            departments = [d.get("name", "") for d in job.get("departments", [])]

            if not _is_relevant(title, location):
                continue

            if user_keywords:
                combined = (title + " " + location + " " + " ".join(departments)).lower()
                if not any(kw.lower() in combined for kw in user_keywords):
                    continue

            # Skip very old postings (> 90 days)
            if _days_ago(updated) > 90:
                continue

            results.append({
                "id": f"gh_{slug}_{job.get('id', '')}",
                "title": title,
                "company": company_name,
                "location": location or "London, UK",
                "department": departments[0] if departments else "",
                "posted_date": _parse_date(updated),
                "days_ago": _days_ago(updated),
                "url": url,
                "source": "Company Career Page",
                "source_system": "Greenhouse",
                "tags": _extract_tags(title, departments),
            })

        return results

    except Exception:
        return []


def _extract_tags(title: str, departments: list[str]) -> list[str]:
    tags = []
    title_lower = title.lower()
    dept_str = " ".join(departments).lower()
    combined = title_lower + " " + dept_str

    if any(k in combined for k in ["graduate", "grad", "entry level", "trainee"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "insight", "bi"]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "treasury", "credit", "risk", "investment"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank", "capital markets"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult", "advisory", "adviser"]):
        tags.append("Consulting")
    if any(k in combined for k in ["quant", "quantitative"]):
        tags.append("Quantitative")

    return tags or ["Finance"]


def fetch_greenhouse_jobs(user_keywords: list[str] = None) -> list[dict]:
    all_jobs = []
    user_keywords = user_keywords or []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(_fetch_one, slug, name, user_keywords): (slug, name)
            for slug, name in GREENHOUSE_COMPANIES.items()
        }
        for future in as_completed(futures):
            try:
                all_jobs.extend(future.result())
            except Exception:
                pass

    return all_jobs
