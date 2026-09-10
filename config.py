"""
BhashaSetu — Central Configuration & Linguistic Constants
Smart India Hackathon 2026 | INNOVEXA
"""

# ----------------------------------------------------
# 1. Linguistic Registries
# ----------------------------------------------------

# 22 Eighth Schedule Indian Languages (MeitY Bhashini)
LANG_CODES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Bhojpuri": "bho",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Tamil": "ta",
    "Telugu": "te",
    "Assamese": "as",
    "Punjabi": "pa",
    "Odia": "or",
    "Urdu": "ur",
    "Sanskrit": "sa",
    "Kashmiri": "ks",
    "Nepali": "ne",
    "Sindhi": "sd",
    "Konkani": "gom",
    "Dogri": "doi",
    "Bodo": "brx",
    "Maithili": "mai",
    "Manipuri": "mni"
}

# Speech-to-Text (STT) Recognition Locales
STT_LANG_CODES = {
    "English": "en-IN",
    "Hindi": "hi-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Tamil": "ta-IN",
    "Telugu": "te-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Urdu": "ur-IN",
    "Punjabi": "pa-Guru-IN",
    "Odia": "or-IN",
    "Assamese": "as-IN",
    "Nepali": "ne-NP",
    "Sanskrit": "sa-IN"
}

# 9 Indigenous Tribal Dialects (Ministry of Tribal Affairs - Adi Vaani)
TRIBAL_LANG_CODES = {
    "Santali": "sat",
    "Mundari": "mun",
    "Bhili": "bhili",
    "Gondi": "gnd",
    "Garo": "garo",
    "Bettakuruba": "bettakuruba",
    "Kokborok": "kokborok",
    "Koya": "koya",
    "Kui": "kui"
}

# Unified Language List
ALL_LANGUAGES = list(LANG_CODES.keys()) + list(TRIBAL_LANG_CODES.keys())

# Linguistic Taxonomy Groups
LANG_FAMILIES = {
    "Indo-Aryan": [
        "Hindi", "Marathi", "Bengali", "Gujarati", "Punjabi", "Odia",
        "Bhojpuri", "Assamese", "Urdu", "Nepali", "Sindhi", "Konkani",
        "Dogri", "Maithili", "Sanskrit"
    ],
    "Dravidian": [
        "Tamil", "Telugu", "Kannada", "Malayalam"
    ],
    "Tribal & Indigenous": [
        "Santali", "Mundari", "Bhili", "Gondi", "Garo", "Bettakuruba",
        "Kokborok", "Koya", "Kui"
    ],
    "Tibeto-Burman & Others": [
        "Bodo", "Manipuri", "Kashmiri", "English"
    ]
}

# ----------------------------------------------------
# 2. Institutional AI Pipeline Registry (MeitY Bhashini)
# ----------------------------------------------------
PIPELINES = {
    "iiith": "660f866443e53d4133f65317",       # IIIT Hyderabad (Broad translation / NMT)
    "ai4bharat": "64392f96daac500b55c543cd",  # AI4Bharat (IndicTrans-v2 & IndicTTS)
    "iit_madras": "660fa5bec7fb5b0328229016", # IIT Madras (TTS dialect coverage)
    "iit_bombay": "660f8130413087224435d2c"   # IIT Bombay (Trilingual fallback)
}

# ----------------------------------------------------
# 3. Project, Institutional & Legal Entity Metadata
# ----------------------------------------------------
PROJECT_NAME = "BhashaSetu"
EDITION = "Smart India Hackathon 2026"
TEAM_NAME = "INNOVEXA"
CONTACT_EMAIL = "contact@bhashasetu.gov.in"

INSTITUTION_DETAILS = {
    "name": "Sitamarhi Institute of Technology",
    "village": "Gosainpur",
    "post_office": "Rasulpur",
    "district": "Sitamarhi",
    "state": "Bihar",
    "pincode": "843302",
    "country": "India",
    "full_address": "Sitamarhi Institute of Technology, Village: Gosainpur, Post Office: Rasulpur, Sitamarhi, Bihar – 843302, India"
}

# DPDP Act 2023 Statutory Grievance Redressal Officer
GRIEVANCE_OFFICER = {
    "name": "Grievance Redressal Officer, BhashaSetu Initiative",
    "designation": "Data Protection & Grievance Officer",
    "institution": "Sitamarhi Institute of Technology",
    "email": "grievance@bhashasetu.gov.in",
    "address": "Sitamarhi Institute of Technology Campus, Gosainpur, Sitamarhi, Bihar – 843302, India",
    "turnaround_days": 7
}

# Legal Entity Disclosures
LEGAL_ENTITY = {
    "entity_name": "Team INNOVEXA / Sitamarhi Institute of Technology",
    "initiative_type": "Educational & Pedagogical Open Innovation Project (Smart India Hackathon 2026)",
    "jurisdiction": "Sitamarhi / Patna High Court, Bihar, India",
    "governing_laws": [
        "Digital Personal Data Protection Act, 2023 (India)",
        "Information Technology Act, 2000 & SPDI Rules, 2011",
        "Rights of Persons with Disabilities Act, 2016 (WCAG 2.1 AA Standards)",
        "Consumer Protection Act, 2019"
    ]
}

# Preset Demo Prompts for Quick Testing
QUICK_CLASSROOM_PROMPTS = [
    "Explain photosynthesis in simple words.",
    "Please submit your science assignments by Friday.",
    "Water boils at 100 degrees Celsius.",
    "Who can explain Newton's first law of motion?"
]

