"""
Fetches jobs directly from Lever ATS company career boards.
API is public — no API key required.
Docs: https://github.com/lever/lever-postings-api
"""

import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import LEVER_COMPANIES, RELEVANT_TITLE_KEYWORDS, LONDON_LOCATION_KEYWORDS

BASE_URL = "https://api.lever.co/v0/postings/{slug}"
TIMEOUT = 8


def _is_relevant(title: str, team: str, location: str) -> bool:
    combined = (title + " " + team).lower()
    location_lower = location.lower()
    has_keyword = any(kw in combined for kw in RELEVANT_TITLE_KEYWORDS)
    is_london = any(loc in location_lower for loc in LONDON_LOCATION_KEYWORDS) or location == ""
    return has_keyword and is_london


def _days_ago(timestamp_ms: int) -> int:
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 999


def _format_date(timestamp_ms: int) -> str:
    try:
        dt = datetime.fromtimestamp(timestamp_ms / 1000, tz=timezone.utc)
        return dt.strftime("%d %b %Y")
    except Exception:
        return ""


def _extract_tags(title: str, team: str) -> list[str]:
    tags = []
    combined = (title + " " + team).lower()

    if any(k in combined for k in ["graduate", "grad", "entry level", "trainee"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "insight", "bi "]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "treasury", "credit", "risk", "investment"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank", "capital markets"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult", "advisory"]):
        tags.append("Consulting")
    if any(k in combined for k in ["quant", "quantitative", "trading"]):
        tags.append("Quantitative")

    return tags or ["Finance"]


def _fetch_one(slug: str, company_name: str, user_keywords: list[str]) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL.format(slug=slug),
            params={"mode": "json"},
            timeout=TIMEOUT,
            headers={"User-Agent": "LondonJobFinder/1.0"},
        )
        if resp.status_code != 200:
            return []

        postings = resp.json()
        if not isinstance(postings, list):
            return []

        results = []
        for job in postings:
            title = job.get("text", "")
            categories = job.get("categories", {})
            team = categories.get("team", "")
            location = categories.get("location", "")
            commitment = categories.get("commitment", "")
            created_ms = job.get("createdAt", 0)
            url = job.get("hostedUrl", "")

            if not _is_relevant(title, team, location):
                continue

            if user_keywords:
                combined = (title + " " + team + " " + location).lower()
                if not any(kw.lower() in combined for kw in user_keywords):
                    continue

            days = _days_ago(created_ms)
            if days > 90:
                continue

            results.append({
                "id": f"lv_{slug}_{job.get('id', '')}",
                "title": title,
                "company": company_name,
                "location": location or "London, UK",
                "department": team,
                "commitment": commitment,
                "posted_date": _format_date(created_ms),
                "days_ago": days,
                "url": url,
                "source": "Company Career Page",
                "source_system": "Lever",
                "tags": _extract_tags(title, team),
            })

        return results

    except Exception:
        return []


def fetch_lever_jobs(user_keywords: list[str] = None) -> list[dict]:
    all_jobs = []
    user_keywords = user_keywords or []

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(_fetch_one, slug, name, user_keywords): (slug, name)
            for slug, name in LEVER_COMPANIES.items()
        }
        for future in as_completed(futures):
            try:
                all_jobs.extend(future.result())
            except Exception:
                pass

    return all_jobs
