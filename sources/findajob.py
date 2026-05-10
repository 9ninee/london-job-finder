"""
Fetches jobs from Find a Job (findajob.dwp.gov.uk) — the UK Government's official job board.
Scrapes HTML search results (no API key required, public site).
London location code: 86384
Runs multiple targeted searches in parallel.
"""

import re
import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_URL = "https://findajob.dwp.gov.uk/search"
LONDON_LOC = "86384"
TIMEOUT = 8

# Targeted searches for relevant graduate roles
SEARCH_QUERIES = [
    "graduate analyst",
    "graduate finance",
    "junior analyst",
    "data analyst",
    "investment analyst",
    "banking analyst",
    "financial analyst",
    "consulting analyst",
    "graduate consultant",
]

SENIOR_KEYWORDS = [
    "senior", "lead", "principal", "head of", "director",
    "manager", "vp ", "vice president", "chief", "partner",
    "managing", " sr ", "sr.", "svp", "evp", "avp",
]


def _is_senior(title: str) -> bool:
    t = title.lower()
    return any(kw in t for kw in SENIOR_KEYWORDS)


def _parse_date(date_str: str) -> str:
    """Parse '07 May 2026' → '07 May 2026' (already formatted)."""
    return date_str.strip()


def _days_ago(date_str: str) -> int:
    """Convert '07 May 2026' to days since today."""
    try:
        dt = datetime.strptime(date_str.strip(), "%d %b %Y")
        dt = dt.replace(tzinfo=timezone.utc)
        return (datetime.now(timezone.utc) - dt).days
    except Exception:
        return 999


def _extract_tags(title: str) -> list[str]:
    tags = []
    t = title.lower()
    if any(k in t for k in ["graduate", "grad", "entry level", "trainee", "junior"]):
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


def _fetch_query(query: str, user_keywords: list[str]) -> list[dict]:
    try:
        resp = requests.get(
            BASE_URL,
            params={
                "q":   query,
                "loc": LONDON_LOC,
                "pp":  50,
            },
            timeout=TIMEOUT,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; LondonJobFinder/1.0)",
                "Accept":     "text/html,application/xhtml+xml",
            },
        )
        if resp.status_code != 200:
            return []

        html = resp.text

        # Parse job blocks: id, url, title, date, company, location
        jobs_raw = re.findall(
            r'<div class="search-result" data-aid="(\d+)">'
            r'.*?<a class="govuk-link" href="(https://findajob\.dwp\.gov\.uk/details/\d+)">'
            r'\s*(.*?)\s*</a>'
            r'.*?<li>\s*(\d{1,2} \w+ \d{4})\s*</li>'
            r'.*?<strong>(.*?)</strong> - <span>(.*?)</span>',
            html,
            re.DOTALL,
        )

        results = []
        for job_id, url, title, date_str, company, location in jobs_raw:
            # Strip HTML tags from title/company (occasionally contain entities)
            title   = re.sub(r"<[^>]+>", "", title).strip()
            company = re.sub(r"<[^>]+>", "", company).strip()

            # Skip senior roles upfront
            if _is_senior(title):
                continue

            # Apply user keyword filter
            if user_keywords:
                combined = (title + " " + company).lower()
                if not any(kw.lower() in combined for kw in user_keywords):
                    continue

            days = _days_ago(date_str)
            if days > 90:
                continue

            results.append({
                "id":           f"faj_{job_id}",
                "title":        title,
                "company":      company.title(),   # normalise ALL-CAPS company names
                "location":     location.strip() or "London, UK",
                "department":   "",
                "posted_date":  _parse_date(date_str),
                "days_ago":     days,
                "url":          url,
                "source":       "Find a Job (Gov.uk)",
                "source_system": "FindAJob",
                "tags":         _extract_tags(title),
            })

        return results

    except Exception:
        return []


def fetch_findajob_jobs(user_keywords: list[str] = None) -> list[dict]:
    user_keywords = user_keywords or []
    all_jobs = []
    seen_ids: set[str] = set()

    with ThreadPoolExecutor(max_workers=len(SEARCH_QUERIES)) as executor:
        futures = [
            executor.submit(_fetch_query, q, user_keywords)
            for q in SEARCH_QUERIES
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
