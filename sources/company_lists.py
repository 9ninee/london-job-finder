"""
Curated lists of company slugs for Greenhouse and Lever ATS platforms.
These are direct company career page APIs — no aggregator middleman.
"""

GREENHOUSE_COMPANIES = {
    # Fintech & Neobanks
    "monzo": "Monzo",
    "starlingbank": "Starling Bank",
    "wise": "Wise",
    "checkout": "Checkout.com",
    "pensionbee": "PensionBee",
    "oaknorth": "OakNorth Bank",
    "tide": "Tide",
    "zopa": "Zopa",
    "funding-circle": "Funding Circle",
    "iwoca": "iwoca",
    "curve": "Curve",
    "modulrfinance": "Modulr Finance",
    "weavr": "Weavr",
    "yapily": "Yapily",
    "truelayer": "TrueLayer",
    "paymentcloud": "PaymentCloud",
    "form3": "Form3",
    "tink": "Tink",
    # Data / Analytics / Tech for Finance
    "palantir": "Palantir",
    "simcorp": "SimCorp",
    "murex": "Murex",
    "finastra": "Finastra",
    "temenos": "Temenos",
    "quantexa": "Quantexa",
    "eigen": "Eigen Technologies",
    "behavox": "Behavox",
    "amenity": "Amenity Analytics",
    "kensho": "Kensho",
    # Investment & Asset Management
    "schroders": "Schroders",
    "aberdeenstandardinvestments": "abrdn",
    "janus-henderson": "Janus Henderson",
    "hermes-investment": "Federated Hermes",
    "polar-capital": "Polar Capital",
    "liontrust": "Liontrust",
    # Banks & Insurance
    "barclays": "Barclays",
    "lloyds-banking-group": "Lloyds Banking Group",
    "natwest-group": "NatWest Group",
    "santander-uk": "Santander UK",
    "hsbc": "HSBC",
    "aon": "Aon",
    "wtwco": "WTW",
    "aviva": "Aviva",
    # Consulting & Professional Services
    "deloitte": "Deloitte",
    "pwc": "PwC",
    "ey": "EY",
    "kpmg": "KPMG",
    "accenture": "Accenture",
    "capgemini": "Capgemini",
    "oliverwyman": "Oliver Wyman",
    "mckinsey": "McKinsey & Company",
    "bcg": "Boston Consulting Group",
    "rolandberger": "Roland Berger",
    "arthurdalittle": "Arthur D. Little",
    "lek": "L.E.K. Consulting",
    "frontier-economics": "Frontier Economics",
    "nera": "NERA Economic Consulting",
    "analysisgroup": "Analysis Group",
    # Exchanges & Market Infrastructure
    "londonstockexchange": "London Stock Exchange Group",
    "euronext": "Euronext",
    "ice": "Intercontinental Exchange",
    "cboe": "Cboe Global Markets",
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

# Location strings that indicate a London-based role
LONDON_LOCATION_KEYWORDS = [
    "london", "uk", "united kingdom", "england", "gb", "great britain",
    "canary wharf", "city of london", "ec", "e14", "wc", "sw1",
    "remote", "hybrid",  # often UK-based remote counts
]
