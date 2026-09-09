"""
Text-to-Speech (TTS) Service
Supports primary Bhashini synthesis and phonetic script-aware fallback gTTS generation.
Specialized support for Kashmiri, Sindhi, Santali (Ol Chiki), Mundari, and all Indian dialects.
"""

import io
import re
import base64
from gtts import gTTS

# Comprehensive language map for standard and regional codes
GTTS_LANG_MAP = {
    # 22 Scheduled Indic Languages + English
    "en": "en", "English": "en",
    "hi": "hi", "Hindi": "hi",
    "bn": "bn", "Bengali": "bn",
    "ta": "ta", "Tamil": "ta",
    "te": "te", "Telugu": "te",
    "mr": "mr", "Marathi": "mr",
    "gu": "gu", "Gujarati": "gu",
    "kn": "kn", "Kannada": "kn",
    "ml": "ml", "Malayalam": "ml",
    "ur": "ur", "Urdu": "ur",
    "pa": "pa", "Punjabi": "pa",
    "ne": "ne", "Nepali": "ne",
    "ks": "ur", "Kashmiri": "ur",    # Kashmiri Perso-Arabic phonetic acoustics
    "sd": "ur", "Sindhi": "ur",      # Sindhi Perso-Arabic phonetic acoustics
    "as": "bn", "Assamese": "bn",    # Assamese uses Eastern Indic/Bengali acoustic base
    "or": "hi", "Odia": "hi",        # Odia phonetic synthesis
    "sa": "hi", "Sanskrit": "hi",    # Classical Sanskrit Devanagari synthesis
    "bho": "hi", "Bhojpuri": "hi",   # Bhojpuri Devanagari
    "gom": "mr", "Konkani": "mr",    # Konkani / Marathi acoustics
    "doi": "hi", "Dogri": "hi",      # Dogri Devanagari
    "brx": "hi", "Bodo": "hi",       # Bodo Devanagari
    "mai": "hi", "Maithili": "hi",   # Maithili Devanagari
    "mni": "bn", "Manipuri": "bn",   # Manipuri Bengali script acoustics

    # 9 Indigenous Tribal Dialects (Ministry of Tribal Affairs)
    "sat": "hi", "Santali": "hi",
    "mun": "hi", "Mundari": "hi",
    "bhili": "hi", "Bhili": "hi",
    "gnd": "hi", "Gondi": "hi",
    "garo": "bn", "Garo": "bn",
    "bettakuruba": "kn", "Bettakuruba": "kn",
    "kokborok": "bn", "Kokborok": "bn",
    "koya": "te", "Koya": "te",
    "kui": "te", "Kui": "te"
}

# Ol Chiki (Santali native script U+1C50 - U+1C7F) to Devanagari phonetic transliteration map
OL_CHIKI_TO_DEVA = {
    '\u1c5a': '\u0913',  # LA (o / a)
    '\u1c5b': '\u0924',  # AT (t)
    '\u1c5c': '\u0917',  # AG (g)
    '\u1c5d': '\u0919',  # ANG (ng)
    '\u1c5e': '\u0932',  # AL (l)
    '\u1c5f': '\u093e',  # LAA (aa)
    '\u1c60': '\u0915',  # AAK (k)
    '\u1c61': '\u091c',  # AAJ (j)
    '\u1c62': '\u092e',  # AAM (m)
    '\u1c63': '\u0935',  # AAW (w)
    '\u1c64': '\u093f',  # LI (i)
    '\u1c65': '\u0938',  # IS (s)
    '\u1c66': '\u0939',  # IH (h)
    '\u1c67': '\u091e',  # INY (ny)
    '\u1c68': '\u0930',  # IR (r)
    '\u1c69': '\u0941',  # LU (u)
    '\u1c6a': '\u091a',  # UC (ch)
    '\u1c6b': '\u0926',  # UD (d)
    '\u1c6c': '\u0923',  # UNN (nn)
    '\u1c6d': '\u092f',  # UY (y)
    '\u1c6e': '\u0947',  # LE (e)
    '\u1c6f': '\u092a',  # EP (p)
    '\u1c70': '\u0921',  # EDD (dd)
    '\u1c71': '\u0928',  # EN (n)
    '\u1c72': '\u095c',  # ER (rh)
    '\u1c73': '\u094b',  # LO (o)
    '\u1c74': '\u091f',  # OTT (tt)
    '\u1c75': '\u092c',  # OB (b)
    '\u1c76': '\u0935',  # OV (v)
    '\u1c77': '\u094d\u0939', # OH (aspirant h)
    '\u1c78': '\u0902',  # Anusvara (nasal)
    '\u1c79': '',        # Tone dot
    '\u1c7a': '',
    '\u1c7b': '',
    '\u1c7c': '\u094d',  # Virama / glottal stop
    '\u1c7d': '',
    '\u1c7e': '\u0964',  # Danda (।)
    '\u1c7f': '\u0965'   # Double Danda (॥)
}


def transliterate_ol_chiki(text: str) -> str:
    """Transliterate Ol Chiki (Santali) text into Devanagari phonetics for speech synthesis."""
    return ''.join(OL_CHIKI_TO_DEVA.get(ch, ch) for ch in text)


def detect_text_script(text: str) -> str:
    """Identify script category to route to the most natural acoustic engine."""
    if re.search(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]', text):
        return "perso_arabic"
    if re.search(r'[\u1C50-\u1C7F]', text):
        return "ol_chiki"
    if re.search(r'[\u0900-\u097F]', text):
        return "devanagari"
    if re.search(r'[\u0980-\u09FF]', text):
        return "bengali"
    if re.search(r'[\u0B80-\u0BFF]', text):
        return "tamil"
    if re.search(r'[\u0C00-\u0C7F]', text):
        return "telugu"
    if re.search(r'[\u0C80-\u0CFF]', text):
        return "kannada"
    if re.search(r'[\u0D00-\u0D7F]', text):
        return "malayalam"
    if re.search(r'[\u0A80-\u0AFF]', text):
        return "gujarati"
    if re.search(r'[\u0A00-\u0A7F]', text):
        return "gurmukhi"
    return "latin"


def generate_fallback_tts(text: str, lang_code: str) -> tuple[str | None, str]:
    """
    Generate speech audio via script-aware gTTS.
    Handles Kashmiri, Sindhi, Santali (Ol Chiki), Mundari, and tribal dialects.
    Validates output buffer size (> 2800 bytes) to prevent empty/silent audio dummy headers.
    Returns: (audio_b64, mime_type) or (None, "")
    """
    if not text or not text.strip():
        return None, ""

    clean_text = text.strip()

    # 1. Handle Ol Chiki transliteration for Santali
    script = detect_text_script(clean_text)
    if script == "ol_chiki":
        clean_text = transliterate_ol_chiki(clean_text)
        script = "devanagari"

    # 2. Build acoustic candidates prioritized by script and language hint
    candidates = []

    if script == "perso_arabic":
        # Kashmiri, Sindhi, and Urdu in Nastaliq/Perso-Arabic script
        candidates = ["ur", "ar"]
    elif script == "devanagari":
        # Mundari, Santali (Devanagari), Hindi, Marathi, Nepali, Sanskrit, Bhojpuri, Dogri, etc.
        preferred = GTTS_LANG_MAP.get(lang_code, "hi")
        candidates = [preferred, "hi", "mr", "ne"]
    elif script == "bengali":
        # Bengali, Assamese, Manipuri, Garo
        candidates = ["bn", "hi"]
    elif script == "tamil":
        candidates = ["ta"]
    elif script == "telugu":
        candidates = ["te", "hi"]
    elif script == "kannada":
        candidates = ["kn", "hi"]
    elif script == "malayalam":
        candidates = ["ml", "hi"]
    elif script == "gujarati":
        candidates = ["gu", "hi"]
    elif script == "gurmukhi":
        candidates = ["pa", "hi"]
    else:
        # Default or Latin script
        mapped = GTTS_LANG_MAP.get(lang_code, "en")
        candidates = [mapped, "en", "hi"]

    # Deduplicate while preserving order
    seen = set()
    deduped_candidates = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            deduped_candidates.append(c)

    # 3. Iterate through candidates and verify that real audio waveform was synthesized
    for cand in deduped_candidates:
        try:
            tts = gTTS(text=clean_text, lang=cand, slow=False)
            buffer = io.BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            audio_bytes = buffer.read()

            # Google TTS writes ~2092-2304 bytes when it cannot vocalize the script (silent dummy MP3).
            # Legitimate spoken audio is > 2800 bytes.
            if len(audio_bytes) > 2800:
                audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                return audio_b64, "audio/mp3"
        except Exception:
            continue

    # 4. Final safety fallback: English acoustic synthesis
    try:
        tts = gTTS(text=clean_text, lang="en", slow=False)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_bytes = buffer.read()
        if len(audio_bytes) > 2500:
            return base64.b64encode(audio_bytes).decode("utf-8"), "audio/mp3"
    except Exception:
        pass

    return None, ""
