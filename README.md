# London Graduate Job Finder

A job search platform that aggregates graduate roles in **Finance, Banking, Data Analytics, and Consulting** directly from company career pages — no job board middlemen.

**Live (GitHub Pages):** `https://9ninee.github.io/london-job-finder`
**Live (Render):** `https://london-job-finder.onrender.com`

---

## What it searches

| Source | Type | API Key? |
|--------|------|----------|
| **Greenhouse ATS** | Direct company board API | No |
| **Lever ATS** | Direct company posting API | No |
| **Ashby ATS** | Direct company board API | No |
| **Workday ATS** | Direct company jobs API | No |
| **Adzuna UK** | Aggregates from company sites | Optional (free) |
| **Find a Job (Gov.uk)** | UK Government official job board | No |
| **The Muse** | Aggregator (JPMorgan, BofA, TikTok…) | No |
| **Reed.co.uk** | UK's largest job board | Optional (free) |

Queries **182 company career pages** simultaneously across:
- Fintech & Neobanks (Monzo, Wise, Checkout.com, Starling, Revolut…)
- Investment Banks & Asset Managers (Barclays, Lloyds, Schroders, Janus Henderson…)
- Consulting (Deloitte, PwC, EY, KPMG, McKinsey, BCG, Oliver Wyman…)
- Quant / Trading (Citadel, Jane Street, Optiver, IMC Trading…)
- Data & Analytics (Palantir, Quantexa, dunnhumby…)

All results are filtered to **London-based** roles matching graduate / analyst / consulting / finance / banking criteria.

---

## Hosting Options

### Option A — GitHub Pages (recommended, free, no server)

The `docs/` folder contains a fully static version of the site. GitHub Actions fetches fresh jobs every 6 hours and commits them as `docs/data/jobs.json`.

**Setup:**
1. Go to repo **Settings → Pages**
2. Set source to **Deploy from branch** → `main` → `/docs`
3. Go to **Settings → Secrets and variables → Actions** and add:
   - `ADZUNA_APP_ID` = your Adzuna app ID
   - `ADZUNA_APP_KEY` = your Adzuna app key
   - `REED_API_KEY` = your Reed API key (free from [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker))
4. Your site goes live at `https://<username>.github.io/london-job-finder`

Jobs refresh automatically every 6 hours via `.github/workflows/fetch-jobs.yml`.
You can also trigger a manual refresh from the **Actions** tab → **Fetch & Update Jobs** → **Run workflow**.

### Option B — Run locally (Flask)

```bash
# 1. Clone
git clone https://github.com/9ninee/london-job-finder.git
cd london-job-finder

# 2. Install dependencies
pip install -r requirements.txt

# 3. (Optional) Add Adzuna API key
echo "ADZUNA_APP_ID=your_id" >> .env
echo "ADZUNA_APP_KEY=your_key" >> .env

# 4. Run
python app.py

# 5. Open
open http://localhost:5050
```

### Option C — Render (cloud, always-on)

Render auto-deploys on every push to `main`. The `render.yaml` and `Procfile` are already configured.

---

## Features

- **Instant load** on GitHub Pages — jobs pre-fetched, all filtering client-side
- **"Updated X ago"** badge shows freshness of the data
- Filter by category: Graduate / Data & Analytics / Finance / Banking / Consulting / Quantitative
- **Hide Senior / Management roles** toggle (on by default)
- Filter by source platform (Greenhouse / Lever / Ashby / Workday / Adzuna / Gov.uk)
- Sort by newest, company name, or job title
- Direct **Apply Now** links to the original job posting on each company's career site
- Pagination (24 jobs per page, Load More)

---

## Project Structure

```
├── app.py                        Flask server (for local / Render hosting)
├── fetch_jobs_static.py          Standalone fetcher (used by GitHub Actions)
├── requirements.txt
├── Procfile                      Render start command
├── render.yaml                   Render deployment config
│
├── sources/
│   ├── company_lists.py          Curated company slugs (182 companies)
│   ├── greenhouse.py             Greenhouse ATS fetcher
│   ├── lever.py                  Lever ATS fetcher
│   ├── ashby.py                  Ashby ATS fetcher
│   ├── workday.py                Workday ATS fetcher
│   ├── adzuna.py                 Adzuna API fetcher
│   └── findajob.py               Gov.uk Find a Job scraper
│
├── templates/index.html          Flask template (Render / local)
├── static/
│   ├── css/style.css
│   └── js/app.js                 Frontend logic (Flask version)
│
├── docs/                         GitHub Pages static site
│   ├── index.html                Static HTML (no Jinja2)
│   ├── data/jobs.json            Pre-fetched jobs (auto-updated)
│   └── static/
│       ├── css/style.css
│       └── js/app.js             Frontend logic (static version)
│
└── .github/
    └── workflows/
        └── fetch-jobs.yml        Cron job: fetch + commit every 6 hours
```

---

## Optional: Adzuna API (free)

Register at [developer.adzuna.com](https://developer.adzuna.com/) for a free key. Adds ~20 extra aggregated job results per search beyond the direct ATS sources.

```
ADZUNA_APP_ID=your_app_id
ADZUNA_APP_KEY=your_app_key
```
