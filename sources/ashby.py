"""
Fetches jobs from Ashby ATS company career boards.
Uses the public REST API (discovered from santifer/career-ops).
No API key required.
Endpoint: https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true
"""

import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import ASHBY_COMPANIES, RELEVANT_TITLE_KEYWORDS, is_uk_location

BASE_URL = "https://api.ashbyhq.com/posting-api/job-board/{slug}"
TIMEOUT = 5


def _is_relevant(title: str, department: str, location: str) -> bool:
    combined = (title + " " + department).lower()
    has_keyword = any(kw in combined for kw in RELEVANT_TITLE_KEYWORDS)
    is_london = is_uk_location(location)
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
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 999


def _extract_tags(title: str, department: str) -> list[str]:
    tags = []
    combined = (title + " " + department).lower()
    if any(k in combined for k in ["graduate", "grad", "entry level", "trainee", "junior"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "insight", "bi ", "intelligence"]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "treasury", "investment", "credit", "risk"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank", "capital markets"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult", "advisory", "adviser"]):
        tags.append("Consulting")
    if any(k in combined for k in ["quant", "quantitative", "trading", "algo"]):
        tags.append("Quantitative")
    return tags or ["Finance"]


def _fetch_one(slug: str, company_name: str, user_keywords: list[str]) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL.format(slug=slug),
            params={"includeCompensation": "true"},
            timeout=TIMEOUT,
            headers={"User-Agent": "LondonJobFinder/1.0"},
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        postings = data.get("jobPostings", [])
        results = []

        for job in postings:
            title = job.get("title", "")
            department = job.get("departmentName", "") or ""
            location = job.get("locationName", "") or ""
            job_url = job.get("jobUrl", "") or ""
            published = job.get("publishedDate", "") or ""
            employment_type = job.get("employmentType", "") or ""

            if not _is_relevant(title, department, location):
                continue

            if user_keywords:
                combined = (title + " " + department + " " + location).lower()
                if not any(kw.lower() in combined for kw in user_keywords):
                    continue

            days = _days_ago(published)
            if days > 90:
                continue

            results.append({
                "id": f"ash_{slug}_{job.get('id', '')}",
                "title": title,
                "company": company_name,
                "location": location or "London, UK",
                "department": department,
                "commitment": employment_type,
                "posted_date": _parse_date(published),
                "days_ago": days,
                "url": job_url,
                "source": "Company Career Page",
                "source_system": "Ashby",
                "tags": _extract_tags(title, department),
            })

        return results

    except Exception:
        return []


def fetch_ashby_jobs(user_keywords: list[str] = None) -> list[dict]:
    all_jobs = []
    user_keywords = user_keywords or []

    with ThreadPoolExecutor(max_workers=30) as executor:
        futures = {
            executor.submit(_fetch_one, slug, name, user_keywords): (slug, name)
            for slug, name in ASHBY_COMPANIES.items()
        }
        for future in as_completed(futures):
            try:
                all_jobs.extend(future.result())
            except Exception:
                pass

    return all_jobs
