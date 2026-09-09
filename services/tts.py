"""
Text-to-Speech (TTS) Service
Supports primary Bhashini synthesis and fallback gTTS generation.
"""

import io
import base64
from gtts import gTTS

# gTTS supported Indian language codes
GTTS_LANG_MAP = {
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
    "pa": "pa", "Punjabi": "pa"
}


def generate_fallback_tts(text: str, lang_code: str) -> tuple[str | None, str]:
    """
    Generate speech audio via gTTS as a resilient fallback.
    Returns: (audio_b64, mime_type) or (None, "")
    """
    if not text or not text.strip():
        return None, ""

    # Normalize code
    code = GTTS_LANG_MAP.get(lang_code, "hi")
    try:
        tts = gTTS(text=text.strip(), lang=code, slow=False)
        buffer = io.BytesIO()
        tts.write_to_fp(buffer)
        buffer.seek(0)
        audio_b64 = base64.b64encode(buffer.read()).decode("utf-8")
        return audio_b64, "audio/mp3"
    except Exception:
        # If specific language fails, attempt english fallback
        try:
            tts = gTTS(text=text.strip(), lang="en", slow=False)
            buffer = io.BytesIO()
            tts.write_to_fp(buffer)
            buffer.seek(0)
            return base64.b64encode(buffer.read()).decode("utf-8"), "audio/mp3"
        except Exception:
            return None, ""
