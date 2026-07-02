"""
Curated lists of company slugs for Greenhouse, Lever, Ashby, and Workday ATS platforms.
All are direct company career page APIs — no aggregator middleman.
Ashby source discovered via github.com/santifer/career-ops.
"""

GREENHOUSE_COMPANIES = {
    # ── Verified live w/ London roles (auto-audited) ──
    # Fintech & payments
    "monzo": "Monzo",
    "tide": "Tide",
    "gocardless": "GoCardless",
    "sumup": "SumUp",
    "ebury": "Ebury",
    "stripe": "Stripe",
    "adyen": "Adyen",
    "marqeta": "Marqeta",
    "truelayer": "TrueLayer",
    "form3": "Form3",
    "liberis": "Liberis",
    "complyadvantage": "ComplyAdvantage",

    # Trading / quant / market makers
    "janestreet": "Jane Street",
    "point72": "Point72",
    "mangroup": "Man Group",
    "winton": "Winton",
    "imc": "IMC Trading",
    "schonfeld": "Schonfeld",
    "flowtraders": "Flow Traders",
    "aqr": "AQR Capital",

    # Data / analytics / consulting
    "databricks": "Databricks",
    "dunnhumby": "dunnhumby",
    "teneo": "Teneo",
    "capco": "Capco",

    # Crypto / digital assets
    "coinbase": "Coinbase",
    "blockchain": "Blockchain.com",
    "fireblocks": "Fireblocks",
    "bybit": "Bybit",
    "okx": "OKX",
}

# ── Lever ATS companies (verified live w/ London roles) ──
# Note: most finance firms have migrated off Lever; only a few remain active.
LEVER_COMPANIES = {
    "zopa": "Zopa",
    "palantir": "Palantir",
}

# ── Ashby ATS companies ──
# Endpoint: https://api.ashbyhq.com/posting-api/job-board/{slug}
ASHBY_COMPANIES = {
    # Fintech / Payments
    "cleo": "Cleo",
    "moneybox": "Moneybox",
    "plum": "Plum",
    "freetrade": "Freetrade",
    "chip": "Chip",
    "ziglu": "Ziglu",
    "wagestream": "Wagestream",
    "monevium": "Monevium",
    "tickr": "Tickr",
    "habito": "Habito",
    "moneyfarm": "Moneyfarm",
    "saltedge": "Salt Edge",
    "bud": "Bud Financial",
    "open-banking-excellence": "Open Banking Excellence",
    "finbourne": "FINBOURNE Technology",
    "broadridge": "Broadridge",
    "enfuce": "Enfuce",
    "deko": "Deko",
    "allica-bank": "Allica Bank",
    "griffin": "Griffin Bank",
    "kroo": "Kroo Bank",
    "atom-bank": "Atom Bank",
    # Data / Analytics
    "quantcast": "Quantcast",
    "signal-ai": "Signal AI",
    "primer": "Primer",
    "data-reply": "Data Reply",
    "profusion": "Profusion",
    "cervest": "Cervest",
    "eigen-technologies": "Eigen Technologies",
    "solidatus": "Solidatus",
    "hazeltree": "HazelTree",
    # Consulting / Advisory
    "advisory-board": "The Advisory Board Company",
    "manifold": "Manifold",
    "fincrime": "FinCrime",
    # Investment / Asset Management
    "circa5000": "Circa5000",
    "clim8": "Clim8 Invest",
    "wealthkernel": "WealthKernel",
    "seccl": "Seccl",
    "hub71": "Hub71",
    "mj-hudson": "MJ Hudson",
    # Insurance / Risk
    "cytora": "Cytora",
    "concirrus": "Concirrus",
    "dinghy": "Dinghy",
    "superscript": "Superscript",
    "qover": "Qover",
    # Regulatory / Compliance tech
    "encompass": "Encompass Corporation",
    "neotas": "Neotas",
    "acin": "ACIN",
    "muinmos": "Muinmos",
    "corlytics": "Corlytics",
}

# ── Workday ATS companies ──
# Used by Goldman Sachs, JP Morgan, Morgan Stanley, Barclays, HSBC,
# McKinsey, BCG, Bain, Deloitte, PwC, EY, KPMG, Accenture, and more.
# Format: {company_slug, shard (number), site (career page name)}
WORKDAY_COMPANIES = {
    # ── Investment Banks ──
    "Goldman Sachs": {
        "company_slug": "goldmansachs",
        "shard": "1",
        "site": "GS",
    },
    "JP Morgan Chase": {
        "company_slug": "jpmc",
        "shard": "1",
        "site": "campus_triage",
    },
    "Morgan Stanley": {
        "company_slug": "morganstanley",
        "shard": "3",
        "site": "Experienced_Jobs",
    },
    "Barclays": {
        "company_slug": "barclays",
        "shard": "3",
        "site": "Barclays",
    },
    "HSBC": {
        "company_slug": "hsbc",
        "shard": "3",
        "site": "ExternalCareers",
    },
    "Deutsche Bank": {
        "company_slug": "db",
        "shard": "3",
        "site": "deutschebank_ext",
    },
    "UBS": {
        "company_slug": "ubs",
        "shard": "3",
        "site": "UBS",
    },
    "Credit Suisse": {
        "company_slug": "creditsuisse",
        "shard": "5",
        "site": "Non-FAs",
    },
    "Citigroup": {
        "company_slug": "citi",
        "shard": "5",
        "site": "Citi",
    },
    "BNP Paribas": {
        "company_slug": "bnpparibasgroup",
        "shard": "3",
        "site": "BNP_Paribas_External_Jobs",
    },
    "Santander": {
        "company_slug": "santander",
        "shard": "3",
        "site": "SantanderCareers",
    },
    "NatWest Group": {
        "company_slug": "natwestgroup",
        "shard": "3",
        "site": "Careers",
    },
    "Lloyds Banking Group": {
        "company_slug": "lloydsbankinggroup",
        "shard": "3",
        "site": "Careers",
    },
    "Standard Chartered": {
        "company_slug": "standardchartered",
        "shard": "3",
        "site": "SCB_Ext",
    },
    # ── Consulting ──
    "McKinsey & Company": {
        "company_slug": "mckinsey",
        "shard": "12",
        "site": "mckinsey",
    },
    "Boston Consulting Group": {
        "company_slug": "bcg",
        "shard": "1",
        "site": "BCG",
    },
    "Bain & Company": {
        "company_slug": "bain",
        "shard": "1",
        "site": "Bain",
    },
    "Deloitte": {
        "company_slug": "deloitte",
        "shard": "1",
        "site": "Deloitte_Careers",
    },
    "PwC": {
        "company_slug": "pwc",
        "shard": "3",
        "site": "Global",
    },
    "EY": {
        "company_slug": "ey",
        "shard": "5",
        "site": "EY",
    },
    "KPMG": {
        "company_slug": "kpmg",
        "shard": "3",
        "site": "KPMG",
    },
    "Accenture": {
        "company_slug": "accenture",
        "shard": "3",
        "site": "AccentureCareers",
    },
    "Capgemini": {
        "company_slug": "capgemini",
        "shard": "1",
        "site": "Capgemini",
    },
    "Oliver Wyman": {
        "company_slug": "oliverwyman",
        "shard": "1",
        "site": "OliverWyman",
    },
    "Roland Berger": {
        "company_slug": "rolandberger",
        "shard": "3",
        "site": "RolandBerger",
    },
    "L.E.K. Consulting": {
        "company_slug": "lek",
        "shard": "3",
        "site": "LEK",
    },
    "Marsh McLennan": {
        "company_slug": "mmc",
        "shard": "5",
        "site": "mmc",
    },
    # ── Asset Management ──
    "BlackRock": {
        "company_slug": "blackrock",
        "shard": "3",
        "site": "Global",
    },
    "Vanguard": {
        "company_slug": "vanguard",
        "shard": "1",
        "site": "vanguard",
    },
    "Fidelity International": {
        "company_slug": "fidelityinternational",
        "shard": "3",
        "site": "FIL",
    },
    "Legal & General": {
        "company_slug": "landg",
        "shard": "3",
        "site": "LegalandGeneral",
    },
    "Prudential": {
        "company_slug": "prudentialplc",
        "shard": "5",
        "site": "Prudential",
    },
    "Aviva": {
        "company_slug": "aviva",
        "shard": "5",
        "site": "Aviva",
    },
    "Abrdn": {
        "company_slug": "abrdn",
        "shard": "3",
        "site": "External",
    },
    "Man Group": {
        "company_slug": "mangroup",
        "shard": "3",
        "site": "ManGroup",
    },
    # ── Exchanges & Market Infrastructure ──
    "LSEG": {
        "company_slug": "lseg",
        "shard": "3",
        "site": "LSEG",
    },
    "CME Group": {
        "company_slug": "cmegroup",
        "shard": "5",
        "site": "CME_Group",
    },
    "Intercontinental Exchange": {
        "company_slug": "intercontinentalexchange",
        "shard": "3",
        "site": "ICE",
    },
}

# Keywords that indicate a relevant role for the user's criteria
RELEVANT_TITLE_KEYWORDS = [
    "graduate", "grad programme", "grad program", "entry level", "junior",
    "trainee", "associate", "analyst", "analytics", "data", "insight",
    "finance", "financial", "investment", "banking", "bank",
    "consulting", "consultant", "advisory", "adviser", "advisor",
    "quantitative", "quant", "economic", "economist",
    "risk", "credit", "portfolio", "treasury", "capital markets",
    "business intelligence", "bi ", "reporting",
]

# Location strings that indicate a UK-based role (London or UK-remote)
# Note: "remote" alone is too broad; we include it as many UK fintechs post "Remote (UK)"
LONDON_LOCATION_KEYWORDS = [
    "london", "united kingdom", "england", "great britain",
    "canary wharf", "city of london",
    # Substring matches that indicate UK scope
    "(uk)", "uk,", ", uk", " uk ", " uk\n",
    # Common UK region strings
    "birmingham", "manchester", "edinburgh", "bristol", "leeds", "oxford", "cambridge",
    # Bare "UK" — match case-insensitively as standalone or in compound strings
    "\buk\b",
]

def is_uk_location(location_str: str) -> bool:
    """Return True if the location string indicates a UK-based role."""
    loc = (location_str or "").lower().strip()
    if not loc:
        return True  # no location = assume UK for UK-focused companies
    for kw in LONDON_LOCATION_KEYWORDS:
        if kw.lower() in loc:
            return True
    # Catch bare "uk" as a whole word
    import re
    if re.search(r'\buk\b', loc):
        return True
    return False


# Non-UK cities/countries that sometimes leak into titles or locations from
# aggregators (e.g. "Analyst - Base in Beijing", "…Abu Dhabi Public Sector").
FOREIGN_LOCATION_KEYWORDS = [
    "beijing", "shanghai", "hong kong", "singapore", "tokyo", "seoul", "mumbai",
    "bangalore", "bengaluru", "delhi", "dubai", "abu dhabi", "doha", "riyadh",
    "new york", "san francisco", "chicago", "boston", "toronto", "sydney",
    "melbourne", "paris", "berlin", "munich", "frankfurt", "madrid", "milan",
    "amsterdam", "dublin", "zurich", "geneva", "warsaw", "lisbon", "prague",
    "dallas", "austin", "seattle", "los angeles", "atlanta", "washington",
    "shenzhen", "guangzhou", "kuala lumpur", "jakarta", "manila", "bangkok",
]


def is_foreign_role(title: str, location: str = "") -> bool:
    """Return True if the title/location clearly points to a non-UK city.

    A foreign city named in the *title* is a strong signal (e.g. "Analyst -
    Abu Dhabi Public Sector" mislabelled as London), so it wins even if the
    location says London. For the location, a London/UK anchor keeps the role
    (many genuine multi-city listings read "Dubai, London, Paris").
    """
    t = (title or "").lower()
    if any(city in t for city in FOREIGN_LOCATION_KEYWORDS) and "london" not in t:
        return True
    loc = (location or "").lower()
    if "london" in loc or "united kingdom" in loc:
        return False
    return any(city in loc for city in FOREIGN_LOCATION_KEYWORDS)


import re as _re
# Matches "3+ years", "3-5 years", "minimum of 4 years", "at least 5 years'
# experience", "5 yrs experience", etc. Captures the leading number.
_EXPERIENCE_RE = _re.compile(
    r'(\d+)\s*(?:\+|\-\s*\d+)?\s*(?:years?|yrs?)[\s\S]{0,20}?(?:experience|exp\b|in\b)',
    _re.IGNORECASE,
)


def requires_experience(text: str, max_years: int = 2) -> bool:
    """Return True if the text demands more than `max_years` years of experience."""
    if not text:
        return False
    for m in _EXPERIENCE_RE.finditer(text):
        try:
            if int(m.group(1)) > max_years:
                return True
        except (ValueError, TypeError):
            continue
    return False


# Senior / management title markers (kept in sync with the frontend toggle).
SENIOR_TITLE_KEYWORDS = [
    "senior", "sr.", " sr ", "lead ", " lead", "principal", "head of", "head,",
    "director", " manager", "managing director", "vp ", " vp", "svp", "evp", "avp",
    "vice president", "chief", "partner", "c-suite", "managing partner",
    "managing consultant", "expert", "staff ",
]


def is_senior_title(title: str) -> bool:
    """Return True if the job title indicates a senior/management role."""
    t = " " + (title or "").lower() + " "
    return any(kw in t for kw in SENIOR_TITLE_KEYWORDS)
