"""
Fetches jobs from Workday ATS — used by Goldman Sachs, JP Morgan, McKinsey,
BCG, Bain, Deloitte, PwC, EY, KPMG, Barclays, HSBC, Morgan Stanley, and more.

Workday uses a POST JSON API:
POST https://{company}.wd{shard}.myworkdayjobs.com/wday/cxs/{company}/{site}/jobs
Body: {"appliedFacets":{},"limit":20,"offset":0,"searchText":"..."}

Each company has a unique (company, shard, site) triple — configured in company_lists.py
"""

import requests
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from .company_lists import WORKDAY_COMPANIES, is_uk_location

TIMEOUT = 5
SEARCH_TERMS = [
    "analyst", "graduate", "associate", "consultant", "finance", "data",
]


def _build_url(cfg: dict) -> str:
    company = cfg["company_slug"]
    shard   = cfg["shard"]
    site    = cfg["site"]
    return (
        f"https://{company}.wd{shard}.myworkdayjobs.com"
        f"/wday/cxs/{company}/{site}/jobs"
    )


def _days_ago(date_str: str) -> int:
    """Workday returns dates like '01/12/2025' or ISO strings."""
    if not date_str:
        return 999
    for fmt in ("%m/%d/%Y", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - dt).days
        except Exception:
            continue
    return 999


def _format_date(date_str: str) -> str:
    if not date_str:
        return ""
    for fmt in ("%m/%d/%Y", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%d %b %Y")
        except Exception:
            continue
    return date_str


def _extract_tags(title: str, category: str) -> list[str]:
    tags = []
    combined = (title + " " + category).lower()
    if any(k in combined for k in ["graduate", "grad", "entry", "trainee", "associate"]):
        tags.append("Graduate")
    if any(k in combined for k in ["data", "analytics", "insight", "bi ", "quantitative analysis"]):
        tags.append("Data & Analytics")
    if any(k in combined for k in ["finance", "financial", "treasury", "credit", "risk", "investment"]):
        tags.append("Finance")
    if any(k in combined for k in ["banking", "bank", "capital markets", "markets"]):
        tags.append("Banking")
    if any(k in combined for k in ["consult", "advisory", "adviser", "strategy"]):
        tags.append("Consulting")
    if any(k in combined for k in ["quant", "quantitative", "trading", "algo"]):
        tags.append("Quantitative")
    return tags or ["Finance"]


def _fetch_one(
    company_name: str,
    cfg: dict,
    user_keywords: list[str],
) -> list[dict]:
    url = _build_url(cfg)
    results = []
    seen_ids = set()

    search_terms = user_keywords if user_keywords else SEARCH_TERMS

    for term in search_terms:
        try:
            resp = requests.post(
                url,
                json={
                    "appliedFacets": {},
                    "limit": 20,
                    "offset": 0,
                    "searchText": term,
                },
                timeout=TIMEOUT,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "LondonJobFinder/1.0",
                    "Accept": "application/json",
                },
            )
            if resp.status_code != 200:
                continue

            data = resp.json()
            job_postings = data.get("jobPostings", [])

            for job in job_postings:
                job_id = job.get("externalPath", "") or job.get("bulletFields", [""])[0]

                if job_id in seen_ids:
                    continue
                seen_ids.add(job_id)

                title = job.get("title", "")

                # Location — Workday nests this differently per version
                location = ""
                loc_data = job.get("locationsText", "") or job.get("location", "")
                if isinstance(loc_data, str):
                    location = loc_data
                elif isinstance(loc_data, dict):
                    location = loc_data.get("descriptor", "")

                if not is_uk_location(location):
                    continue

                posted_on = job.get("postedOn", "") or ""
                days = _days_ago(posted_on)
                if days > 90:
                    continue

                category = job.get("jobFamilyGroup", {})
                if isinstance(category, dict):
                    category = category.get("descriptor", "")
                elif not isinstance(category, str):
                    category = ""

                # Build the job URL
                ext_path = job.get("externalPath", "")
                base_domain = (
                    f"https://{cfg['company_slug']}.wd{cfg['shard']}.myworkdayjobs.com"
                )
                job_url = base_domain + ext_path if ext_path else base_domain

                results.append({
                    "id": f"wd_{cfg['company_slug']}_{job_id}",
                    "title": title,
                    "company": company_name,
                    "location": location or "London, UK",
                    "department": category,
                    "posted_date": _format_date(posted_on),
                    "days_ago": days,
                    "url": job_url,
                    "source": "Company Career Page",
                    "source_system": "Workday",
                    "tags": _extract_tags(title, category),
                })

        except Exception:
            continue

    return results


def fetch_workday_jobs(user_keywords: list[str] = None) -> list[dict]:
    all_jobs = []
    user_keywords = user_keywords or []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(_fetch_one, name, cfg, user_keywords): name
            for name, cfg in WORKDAY_COMPANIES.items()
        }
        for future in as_completed(futures):
            try:
                all_jobs.extend(future.result())
            except Exception:
                pass

    # Deduplicate across search terms
    seen = set()
    unique = []
    for job in all_jobs:
        if job["id"] not in seen:
            seen.add(job["id"])
            unique.append(job)

    return unique
