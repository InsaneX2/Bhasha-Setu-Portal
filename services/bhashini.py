"""
MeitY Bhashini Institutional Pipeline Engine
Handles multi-directional Indic translation and multi-tier institutional fallbacks.
"""

import requests
import streamlit as st
from config import PIPELINES
from services.tts import generate_fallback_tts


def execute_bhashini_task(task_type: str, source_lang: str, target_lang: str, text: str, pipeline_id: str):
    """Query a specific institutional pipeline for translation or TTS."""
    config_url = "https://meity-auth.ulcacontrib.org/ulca/apis/v0/model/getModelsPipeline"
    
    user_id = st.secrets.get("BHASHINI_USER_ID", "")
    api_key = st.secrets.get("BHASHINI_API_KEY", "")

    if not user_id or not api_key:
        return None

    headers = {
        "userID": user_id,
        "ulcaApiKey": api_key,
        "Content-Type": "application/json"
    }

    if task_type == "translation":
        task_config = {
            "taskType": "translation",
            "config": {
                "language": {
                    "sourceLanguage": source_lang,
                    "targetLanguage": target_lang
                }
            }
        }
    else:
        task_config = {
            "taskType": "tts",
            "config": {
                "language": {
                    "sourceLanguage": target_lang
                }
            }
        }

    config_payload = {
        "pipelineTasks": [task_config],
        "pipelineRequestConfig": {"pipelineId": pipeline_id}
    }

    try:
        config_res = requests.post(config_url, json=config_payload, headers=headers, timeout=10).json()
        if "pipelineInferenceAPIEndPoint" not in config_res:
            return None

        callback_url = config_res["pipelineInferenceAPIEndPoint"]["callbackUrl"]
        auth_ticket = config_res["pipelineInferenceAPIEndPoint"]["inferenceApiKey"]["value"]

        config_list = config_res["pipelineResponseConfig"][0].get("config", [])
        if not config_list:
            return None
        service_id = config_list[0]["serviceId"]

        compute_headers = {
            "Authorization": auth_ticket,
            "Content-Type": "application/json",
            "Accept": "*/*"
        }

        if task_type == "translation":
            compute_payload = {
                "pipelineTasks": [{
                    "taskType": "translation",
                    "config": {
                        "language": {
                            "sourceLanguage": source_lang,
                            "targetLanguage": target_lang
                        },
                        "serviceId": service_id
                    }
                }],
                "inputData": {"input": [{"source": text}]}
            }
        else:
            compute_payload = {
                "pipelineTasks": [{
                    "taskType": "tts",
                    "config": {
                        "language": {
                            "sourceLanguage": target_lang
                        },
                        "serviceId": service_id,
                        "gender": "female"
                    }
                }],
                "inputData": {"input": [{"source": text}]}
            }

        compute_res = requests.post(callback_url, json=compute_payload, headers=compute_headers, timeout=12).json()

        if task_type == "translation" and "pipelineResponse" in compute_res:
            return compute_res["pipelineResponse"][0]["output"][0]["target"]
        elif task_type == "tts" and "pipelineResponse" in compute_res:
            return compute_res["pipelineResponse"][0]["audio"][0]["audioContent"]

    except Exception:
        pass

    return None


def run_bhashini_pipeline_smart(text: str, source_lang_code: str, target_lang_code: str):
    """
    Multi-Directional & Multi-Tier Institutional Fallback Translation & TTS Engine.
    Dynamically routes source_lang_code -> target_lang_code without hardcoding.
    Returns: (translated_text, audio_b64, mime_type)
    """
    if not text or not text.strip():
        return "", None, "audio/wav"

    # If source and target are identical, skip translation
    if source_lang_code == target_lang_code:
        translated_text = text.strip()
    else:
        # Dynamic fallback ordering:
        # For Indic-to-Indic, AI4Bharat (IndicTrans-v2) is optimized, followed by IIIT-H
        if source_lang_code != "en":
            translation_order = [
                ("ai4bharat", PIPELINES["ai4bharat"]),
                ("iiith", PIPELINES["iiith"]),
                ("iit_bombay", PIPELINES["iit_bombay"])
            ]
        else:
            translation_order = [
                ("iiith", PIPELINES["iiith"]),
                ("ai4bharat", PIPELINES["ai4bharat"]),
                ("iit_bombay", PIPELINES["iit_bombay"])
            ]

        translated_text = None
        for provider_name, pipeline_id in translation_order:
            translated_text = execute_bhashini_task("translation", source_lang_code, target_lang_code, text, pipeline_id)
            if translated_text:
                break

        if not translated_text:
            return "Translation failed across all institutional pipelines. Please verify language pair or connection.", None, "audio/wav"

    # Speech Synthesis (TTS) Fallback Chain
    tts_order = [
        ("iit_madras", PIPELINES["iit_madras"]),
        ("ai4bharat", PIPELINES["ai4bharat"])
    ]
    audio_b64 = None
    mime_type = "audio/wav"

    for provider_name, pipeline_id in tts_order:
        audio_b64 = execute_bhashini_task("tts", source_lang_code, target_lang_code, translated_text, pipeline_id)
        if audio_b64:
            break

    # If Bhashini TTS fails or is unavailable for this dialect, engage high-res fallback TTS
    if not audio_b64:
        fallback_b64, fallback_mime = generate_fallback_tts(translated_text, target_lang_code)
        if fallback_b64:
            audio_b64 = fallback_b64
            mime_type = fallback_mime

    return translated_text, audio_b64, mime_type
