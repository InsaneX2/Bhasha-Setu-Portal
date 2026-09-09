"""
Adi Vaani Service (Ministry of Tribal Affairs)
Handles translation for 9 indigenous tribal dialects.
"""

import requests
from config import TRIBAL_LANG_CODES

ADIVAANI_URL = "https://adivaani.tribal.gov.in/api/translation/translate"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/152.0.0.0 Safari/537.36"
}


def get_tribal_translation(input_text: str, src_code: str, tgt_code: str) -> str:
    """
    Call Adi Vaani translation API.
    src_code: 'hin', 'eng', or tribal code ('sat', 'mun', etc.)
    tgt_code: tribal code or 'hin'/'eng'
    """
    if not input_text or not input_text.strip():
        return ""

    # Normalize codes to 3-letter codes expected by Adi Vaani
    code_map = {
        "hi": "hin", "Hindi": "hin", "hin": "hin",
        "en": "eng", "English": "eng", "eng": "eng"
    }
    # Check if src is tribal
    for name, code in TRIBAL_LANG_CODES.items():
        if src_code in (name, code):
            src_code = code
            break
    else:
        src_code = code_map.get(src_code, "eng")

    # Check if tgt is tribal
    for name, code in TRIBAL_LANG_CODES.items():
        if tgt_code in (name, code):
            tgt_code = code
            break
    else:
        tgt_code = code_map.get(tgt_code, "hin")

    payload = {
        "text": input_text.strip(),
        "source_language": src_code,
        "target_language": tgt_code,
        "user_id": ""
    }

    try:
        response = requests.post(ADIVAANI_URL, json=payload, headers=HEADERS, timeout=12)
        response.raise_for_status()
        data = response.json()
        translated = data.get("translated_text", "")
        if translated:
            return translated
        return "Translation returned empty result."
    except requests.exceptions.Timeout:
        return "Adi Vaani gateway timeout. Please retry."
    except Exception as e:
        return f"Tribal Translation Error: {e}"
