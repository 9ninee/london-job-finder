"""
Fetches jobs from The Muse public API (www.themuse.com/developers/api/v2).
No API key required. Aggregates from many employers (Bank of America, Uber, etc.).
Filtered to London + finance/data/consulting categories.
"""

import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import RELEVANT_TITLE_KEYWORDS, is_uk_location

BASE_URL = "https://www.themuse.com/api/public/jobs"
TIMEOUT = 8
LOCATION = "London, United Kingdom"

# The Muse's own category taxonomy — pick the finance/data/consulting relevant ones
CATEGORIES = [
    "Finance",
    "Accounting and Finance",
    "Data Science",
    "Business & Strategy",
]
PAGES_PER_CATEGORY = 2   # 20 results per page


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


def _extract_tags(title: str, categories: list[str]) -> list[str]:
    tags = []
    combined = (title + " " + " ".join(categories)).lower()
    if any(k in combined for k in ["graduate", "grad", "entry level", "trainee", "junior", "intern"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "insight", "science"]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "treasury", "investment", "credit", "risk", "accounting"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank", "capital markets"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult", "advisory", "strategy"]):
        tags.append("Consulting")
    if any(k in combined for k in ["quant", "quantitative", "trading"]):
        tags.append("Quantitative")
    return tags or ["Finance"]


def _fetch_page(category: str, page: int, user_keywords: list[str]) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL,
            params={"location": LOCATION, "category": category, "page": page},
            timeout=TIMEOUT,
            headers={"User-Agent": "LondonJobFinder/1.0"},
        )
        if resp.status_code != 200:
            return []

        results = []
        for job in resp.json().get("results", []):
            title = job.get("name", "")
            company = (job.get("company") or {}).get("name", "Unknown")
            locations = [l.get("name", "") for l in job.get("locations", [])]
            loc_str = ", ".join(locations)

            # Muse location filter can be loose — enforce UK/London
            if not any(is_uk_location(l) for l in locations):
                continue

            # Relevance by title keyword
            cats = [c.get("name", "") for c in job.get("categories", [])]
            if not any(kw in (title + " " + " ".join(cats)).lower() for kw in RELEVANT_TITLE_KEYWORDS):
                continue

            if user_keywords:
                combined = (title + " " + company + " " + loc_str).lower()
                if not any(kw.lower() in combined for kw in user_keywords):
                    continue

            published = job.get("publication_date", "")
            days = _days_ago(published)
            if days > 90:
                continue

            results.append({
                "id":            f"muse_{job.get('id', '')}",
                "title":         title,
                "company":       company,
                "location":      loc_str or "London, UK",
                "department":    cats[0] if cats else "",
                "posted_date":   _parse_date(published),
                "days_ago":      days,
                "url":           (job.get("refs") or {}).get("landing_page", ""),
                "source":        "Company Career Page",
                "source_system": "TheMuse",
                "tags":          _extract_tags(title, cats),
            })

        return results

    except Exception:
        return []


def fetch_themuse_jobs(user_keywords: list[str] = None) -> list[dict]:
    user_keywords = user_keywords or []
    all_jobs = []
    seen_ids: set[str] = set()

    tasks = [(cat, p) for cat in CATEGORIES for p in range(PAGES_PER_CATEGORY)]

    with ThreadPoolExecutor(max_workers=len(tasks)) as executor:
        futures = [
            executor.submit(_fetch_page, cat, page, user_keywords)
            for cat, page in tasks
        ]
        for future in as_completed(futures):
            try:
                for job in future.result():
                    if job["id"] not in seen_ids:
                        seen_ids.add(job["id"])
                        all_jobs.append(job)
            except Exception:
                pass

    return all_jobs
