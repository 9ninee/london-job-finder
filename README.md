# London Graduate Job Finder

A job search platform that aggregates graduate roles in **Finance, Banking, Data Analytics, and Consulting** directly from company career pages and major UK job boards — no job board middlemen.

## 🚀 Just want to use it? Open the live site — no setup required

### 👉 **[https://9ninee.github.io/london-job-finder/](https://9ninee.github.io/london-job-finder/)**

It's free and hosted for everyone. Open the link, filter by category, and apply
directly — the job list refreshes automatically every 6 hours with 1,000+ live
London roles. Nothing to install, no account, no API keys.

> 💛 **Contributions welcome!** This is an open project — if you know of a company
> career board we're missing or want to add a new job source, please jump in.
> See [Contributing](#contributing) below. No contribution is too small.

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

Pulls **1,000+ live London roles** at a time by combining direct company career
boards with major UK aggregators, across:
- Fintech & Payments (Monzo, Stripe, Adyen, SumUp, GoCardless, Ebury…)
- Quant / Trading (Jane Street, Point72, Man Group, IMC, Flow Traders…)
- Banks & Big Names via aggregators (JPMorgan, Bank of America…)
- Consulting & Data (Capco, Teneo, Databricks, dunnhumby…)
- Crypto / Digital Assets (Coinbase, Fireblocks, OKX, Bybit…)

All results are filtered to **London-based** roles matching graduate / analyst / consulting / finance / banking criteria.

---

## How to use it

### Option 1 — Use the live site (recommended for everyone)

Just open **[https://9ninee.github.io/london-job-finder/](https://9ninee.github.io/london-job-finder/)**.

That's it. The site is hosted and maintained for you, refreshes every 6 hours, and
requires zero setup. This is the right choice for the vast majority of users — you
only need the options below if you want to run your *own* independent copy.

### Option 2 — Host your own copy

Prefer to self-host (your own company lists, your own refresh schedule)? You can run
it three ways:

<details>
<summary><strong>2a. Your own GitHub Pages site (free, no server)</strong></summary>

The `docs/` folder is a fully static build. A GitHub Actions cron fetches fresh jobs
every 6 hours and commits them to `docs/data/jobs.json`.

1. **Fork** this repo.
2. Go to your fork's **Settings → Pages** → source **Deploy from branch** → `main` → `/docs`.
3. (Optional, for Adzuna + Reed results) **Settings → Secrets and variables → Actions**, add:
   - `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` — free from [developer.adzuna.com](https://developer.adzuna.com/)
   - `REED_API_KEY` — free from [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker)
4. Your copy goes live at `https://<your-username>.github.io/london-job-finder`.

Trigger a manual refresh anytime from the **Actions** tab → **Fetch & Update Jobs** → **Run workflow**.
</details>

<details>
<summary><strong>2b. Run locally (Flask, live search)</strong></summary>

```bash
git clone https://github.com/9ninee/london-job-finder.git
cd london-job-finder
pip install -r requirements.txt

# Optional — API keys for Adzuna & Reed
echo "ADZUNA_APP_ID=your_id"   >> .env
echo "ADZUNA_APP_KEY=your_key" >> .env
echo "REED_API_KEY=your_key"   >> .env

python app.py
open http://localhost:5050
```
</details>

<details>
<summary><strong>2c. Render (cloud, always-on Flask)</strong></summary>

Render auto-deploys on every push to `main`. The `render.yaml` and `Procfile` are
already configured — connect the repo in your Render dashboard and add the same API
keys as environment variables.
</details>

---

## Features

- **Instant load** on GitHub Pages — jobs pre-fetched, all filtering client-side
- **"Updated X ago"** badge shows freshness of the data
- Filter by category: Graduate / Data & Analytics / Finance / Banking / Consulting / Quantitative
- **Hide Senior / Management roles** toggle (on by default)
- Filter by source platform (Greenhouse / Lever / Adzuna / The Muse / Reed / Gov.uk)
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

## Optional: API keys (all free)

Some aggregator sources need a free API key. The app works without them — those
sources simply return nothing until a key is provided.

| Provider | Where to register | Env vars |
|----------|-------------------|----------|
| **Adzuna** | [developer.adzuna.com](https://developer.adzuna.com/) | `ADZUNA_APP_ID`, `ADZUNA_APP_KEY` |
| **Reed** | [reed.co.uk/developers](https://www.reed.co.uk/developers/jobseeker) | `REED_API_KEY` |

Add them to a local `.env` file (for local/Render use) or as GitHub Actions
repository secrets (for the GitHub Pages auto-refresh).

---

## Contributing

**This project is open to everyone — contributions of any size are genuinely welcome.**
Whether you're fixing a typo, adding a company, or building a whole new job source,
your help makes the tool better for every job seeker who uses it. 💛

### Good first contributions

- **➕ Add a company** — the single most useful thing you can do. If you know a
  company hiring in London on Greenhouse, Lever, or Ashby, add its slug to the
  relevant dict in [`sources/company_lists.py`](sources/company_lists.py).
  - Greenhouse slug: the `xxx` in `boards.greenhouse.io/xxx`
  - Lever slug: the `xxx` in `jobs.lever.co/xxx`
  - Ashby slug: the `xxx` in `jobs.ashbyhq.com/xxx`
- **🔌 Add a new source** — build a new fetcher in `sources/` that returns the
  standard job dict (see any existing source for the shape), then register it in
  both `app.py` and `fetch_jobs_static.py`. Ideas: Workable, SmartRecruiters,
  Recruitee, Otta, Welcome to the Jungle.
- **🏷️ Improve filtering** — better role tagging, senior-role detection, or
  relevance keywords in `company_lists.py`.
- **🎨 UI/UX** — design tweaks, accessibility, mobile layout, dark mode.
- **🐛 Report bugs / dead sources** — open an issue if a source stops returning
  results or a company slug 404s.

### How to contribute

1. **Fork** the repo and clone your fork.
2. Create a branch: `git checkout -b add-my-company`.
3. Make your change. To sanity-check a new source or company list locally:
   ```bash
   pip install -r requirements.txt
   python fetch_jobs_static.py      # prints per-source job counts
   ```
4. **Commit** with a clear message and **open a Pull Request** describing what you
   added and, for new companies, confirming they had London roles when you checked.

### Contribution guidelines

- Keep sources **key-free where possible** — prefer public ATS APIs so the tool
  works out of the box.
- Every source must **fail gracefully** (return `[]` on error/timeout) so one dead
  source never breaks a search.
- Match the existing job-dict shape and the ~5s per-request timeout budget.
- Be kind in issues and reviews. We're all here to help people find jobs.

New to open source? That's perfect — open a draft PR or an issue and we'll help you
get it merged.
