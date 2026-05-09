"""
Curated lists of company slugs for Greenhouse, Lever, Ashby, and Workday ATS platforms.
All are direct company career page APIs — no aggregator middleman.
Ashby source discovered via github.com/santifer/career-ops.
"""

GREENHOUSE_COMPANIES = {
    # ── Verified active ✓ (confirmed returning London finance roles) ──
    "monzo": "Monzo",
    "tide": "Tide",
    "gocardless": "GoCardless",
    "complyadvantage": "ComplyAdvantage",
    "form3": "Form3",
    "truelayer": "TrueLayer",
    "modulrfinance": "Modulr Finance",
    "behavox": "Behavox",
    "cleo": "Cleo",
    "salaryfinance": "Salary Finance",
    "n26": "N26",

    # ── Fintech & Neobanks (Greenhouse-confirmed) ──
    "starlingbank": "Starling Bank",
    "wise": "Wise",
    "pensionbee": "PensionBee",
    "oaknorth": "OakNorth Bank",
    "zopa": "Zopa",
    "funding-circle": "Funding Circle",
    "iwoca": "iwoca",
    "curve": "Curve",
    "yapily": "Yapily",
    "checkout": "Checkout.com",
    "railsr": "Railsr",
    "payhawk": "Payhawk",
    "pleo": "Pleo",
    "soldo": "Soldo",
    "wagestream": "Wagestream",
    "coconut": "Coconut",
    "moneyhub": "Moneyhub",
    "snyk": "Snyk",

    # ── Payments & Infrastructure ──
    "verifone": "Verifone",
    "token-io": "Token.io",

    # ── Data / Analytics / RegTech ──
    "palantir": "Palantir",
    "quantexa": "Quantexa",
    "eigen": "Eigen Technologies",
    "onfido": "Onfido",
    "sumsub": "Sumsub",
    "callsign": "Callsign",
    "featurespace": "Featurespace",
    "amenity": "Amenity Analytics",
    "fenergo": "Fenergo",
    "neotas": "Neotas",
    "acin": "ACIN",

    # ── Investment & Asset Management ──
    "schroders": "Schroders",
    "janus-henderson": "Janus Henderson",
    "polar-capital": "Polar Capital",
    "liontrust": "Liontrust",

    # ── FinTech Infrastructure / Capital Markets Tech ──
    "simcorp": "SimCorp",
    "murex": "Murex",
    "finastra": "Finastra",
    "temenos": "Temenos",
    "broadridge": "Broadridge",
    "kensho": "Kensho",
    "tradeweb": "Tradeweb",

    # ── Insurance / Risk ──
    "cytora": "Cytora",
    "hyperexponential": "Hyperexponential",
    "concirrus": "Concirrus",
    "superscript": "Superscript",

    # ── Consulting & Advisory ──
    "nera": "NERA Economic Consulting",
    "analysisgroup": "Analysis Group",
    "cornerstone-research": "Cornerstone Research",

    # ── Exchanges & Market Infrastructure ──
    "euronext": "Euronext",
    "ice": "Intercontinental Exchange",
    "cboe": "Cboe Global Markets",
    "marex": "Marex",
}

LEVER_COMPANIES = {
    # Quant / Trading
    "citadel": "Citadel",
    "jane-street": "Jane Street",
    "virtu": "Virtu Financial",
    "hrt": "Hudson River Trading",
    "imc": "IMC Trading",
    "optiver": "Optiver",
    "akuna-capital": "Akuna Capital",
    "drwtrading": "DRW",
    "sig": "SIG",
    # Fintech
    "revolut": "Revolut",
    "sumup": "SumUp",
    "paysafe": "Paysafe",
    "worldremit": "WorldRemit",
    "caxton": "Caxton",
    "currencycloud": "CurrencyCloud",
    "airwallex": "Airwallex",
    "transfermate": "TransferMate",
    # Data / Analytics
    "dunnhumby": "dunnhumby",
    "datasparq": "Data SparQ",
    "satalia": "Satalia",
    "feedzai": "Feedzai",
    # Consulting / Advisory
    "cornerstone-research": "Cornerstone Research",
    "cfra": "CFRA Research",
    "ihs-markit": "S&P Global Market Intelligence",
    # Banks / Finance
    "lazard": "Lazard",
    "evercore": "Evercore",
    "stifel": "Stifel",
    "berenberg": "Berenberg",
    "numis": "Numis",
    "liberum": "Liberum",
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
