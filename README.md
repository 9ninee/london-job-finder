# London Graduate Job Finder

A local job search platform that aggregates graduate roles in **Finance, Banking, Data Analytics, and Consulting** directly from company career pages — no job board middlemen.

## What it searches

| Source | How | API Key? |
|--------|-----|----------|
| **Greenhouse ATS** | Direct company board API | No |
| **Lever ATS** | Direct company posting API | No |
| **Adzuna UK** | Aggregates from company sites | Optional (free) |

Queries **91 company career pages** simultaneously across:
- Fintech & Neobanks (Monzo, Wise, Checkout.com, Starling, Revolut…)
- Investment Banks & Asset Managers (Barclays, Lloyds, Schroders, Janus Henderson…)
- Consulting (Deloitte, PwC, EY, KPMG, McKinsey, BCG, Oliver Wyman…)
- Quant / Trading (Citadel, Jane Street, Optiver, IMC Trading…)
- Data & Analytics (Palantir, Quantexa, dunnhumby…)

All results are filtered to **London-based** roles matching graduate / analyst / consulting / finance / banking criteria.

## Quick Start

```bash
# 1. Clone & enter the directory
git clone <repo-url>
cd london-job-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Add Adzuna API key for more results
cp .env.example .env
# Edit .env and add your free key from https://developer.adzuna.com/

# 4. Run
python app.py

# 5. Open browser
open http://localhost:5050
```

## Optional: Adzuna API (free)

Register at [developer.adzuna.com](https://developer.adzuna.com/) for a free API key and add to `.env`:

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```

## Features

- Auto-searches on page load with your preset filters
- Filter by category: Graduate / Data & Analytics / Finance / Banking / Consulting / Quantitative
- Filter by source platform (Greenhouse / Lever / Adzuna)
- Sort by newest, company name, or job title
- Direct links to the original job posting on each company's own career site
- Pagination (24 jobs per page)

## Project Structure

```
├── app.py                 Flask server
├── sources/
│   ├── company_lists.py   Curated company slugs
│   ├── greenhouse.py      Greenhouse ATS fetcher
│   ├── lever.py           Lever ATS fetcher
│   └── adzuna.py          Adzuna API fetcher
├── templates/index.html   UI
├── static/css/style.css
└── static/js/app.js
```
