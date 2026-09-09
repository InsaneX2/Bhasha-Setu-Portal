"""
Interactive Vernacular Classroom Translator UI Component
Handles voice recording, audio file upload, prompt presets, translation routing, and output playback.
"""

import io
import streamlit as st
import speech_recognition as sr
from config import (
    LANG_CODES,
    STT_LANG_CODES,
    TRIBAL_LANG_CODES,
    ALL_LANGUAGES,
    QUICK_CLASSROOM_PROMPTS
)
from services.bhashini import run_bhashini_pipeline_smart
from services.adivaani import get_tribal_translation
from services.tts import generate_fallback_tts
from services.telemetry import log_activity
from services.i18n import t
from components.audio_player import render_audio_player


def render_translation_interface(user_type_label: str):
    """Render the full vernacular learning assistant interface."""
    st.markdown(f"### {t('asst_title')}")
    st.caption(f"{t('asst_sub')} **{user_type_label} Mode**")

    # 1. Language Selection Row
    col1, col2 = st.columns(2)
    with col1:
        src_lang = st.selectbox(
            t("src_lang_label"),
            ALL_LANGUAGES,
            index=0,
            key=f"src_{user_type_label}"
        )
    with col2:
        default_target_idx = ALL_LANGUAGES.index("Hindi") if "Hindi" in ALL_LANGUAGES else 1
        target_lang = st.selectbox(
            t("tgt_lang_label"),
            ALL_LANGUAGES,
            index=default_target_idx,
            key=f"tgt_{user_type_label}"
        )

    # 2. Preset Prompt Chips for Quick Demo
    st.markdown(f"<div style='margin-top: 10px; margin-bottom: 6px; font-size: 0.85rem; color: #94a3b8;'>{t('quick_prompts')}</div>", unsafe_allow_html=True)
    p_cols = st.columns(4)
    selected_preset = None

    for i, p_text in enumerate(QUICK_CLASSROOM_PROMPTS):
        with p_cols[i]:
            if st.button(f"📌 {p_text[:24]}...", key=f"chip_{user_type_label}_{i}", help=p_text):
                selected_preset = p_text

    # 3. Translation Orchestrator Function
    def run_translation(input_query: str):
        if not input_query or not input_query.strip():
            st.warning("Please enter or record some text first.")
            return

        is_target_tribal = target_lang in TRIBAL_LANG_CODES
        is_src_tribal = src_lang in TRIBAL_LANG_CODES

        audio_b64_to_play = None
        mime_type = "audio/wav"
        translated_output = ""

        with st.spinner(f"Translating to {target_lang}..."):
            # Scenario A: Target is an indigenous tribal dialect
            if is_target_tribal:
                tgt_c = TRIBAL_LANG_CODES[target_lang]
                if src_lang == "Hindi":
                    src_c = "hin"
                    intermediate_text = input_query
                elif src_lang == "English":
                    src_c = "eng"
                    intermediate_text = input_query
                else:
                    # Bridge translation: Translate source Indic language to Hindi first
                    src_code_bhashini = LANG_CODES.get(src_lang, "en")
                    intermediate_text, _, _ = run_bhashini_pipeline_smart(input_query, src_code_bhashini, "hi")
                    src_c = "hin"

                translated_output = get_tribal_translation(intermediate_text, src_c, tgt_c)
                if translated_output and not translated_output.startswith("Error") and not translated_output.startswith("Adi Vaani"):
                    audio_b64_to_play, mime_type = generate_fallback_tts(translated_output, tgt_c)

            # Scenario B: Source is tribal dialect, Target is standard language
            elif is_src_tribal:
                src_c = TRIBAL_LANG_CODES[src_lang]
                tgt_c = "hin" if target_lang == "Hindi" else "eng"
                translated_output = get_tribal_translation(input_query, src_c, tgt_c)
                if translated_output and not translated_output.startswith("Error") and not translated_output.startswith("Adi Vaani"):
                    tgt_std_code = LANG_CODES.get(target_lang, "hi")
                    audio_b64_to_play, mime_type = generate_fallback_tts(translated_output, tgt_std_code)

            # Scenario C: Multi-Directional Bhashini Translation (Indic-to-Indic, English-to-Indic, Indic-to-English)
            else:
                src_code = LANG_CODES.get(src_lang, "en")
                tgt_code = LANG_CODES.get(target_lang, "hi")
                try:
                    translated_output, audio_b64_to_play, mime_type = run_bhashini_pipeline_smart(
                        input_query, src_code, tgt_code
                    )
                except Exception as e:
                    st.error(f"Bhashini Pipeline Error: {e}")
                    translated_output = "Error in translation pipeline."

        # Telemetry Logging
        username = st.session_state.get("username") or user_type_label
        log_activity(username, src_lang, target_lang, input_query, translated_output)

        # Output Presentation Container
        with st.container(border=True):
            st.markdown(f"#### {t('output_title')} ({target_lang})")
            st.markdown(
                f"<div style='font-size: 1.25rem; font-weight: 600; color: #38bdf8; padding: 8px 0;'>"
                f"{translated_output}</div>",
                unsafe_allow_html=True
            )

            if audio_b64_to_play:
                render_audio_player(audio_b64_to_play, mime_type)
            else:
                st.caption("🎙️ Voice output unavailable for this query.")

    # 4. Input Controls: Voice, Text, and Audio Upload
    input_tab_voice, input_tab_text, input_tab_file = st.tabs([
        t("tab_mic_input"),
        t("tab_text_input"),
        t("tab_file_input")
    ])

    with input_tab_voice:
        with st.container(border=True):
            st.markdown(f"#### {t('mic_head')}")
            st.caption(f"{t('mic_sub')} • Configured for: **{src_lang}** ({STT_LANG_CODES.get(src_lang, 'en-IN')})")

            # Native browser microphone input (works seamlessly in Streamlit Cloud, Mobile, and Desktop browsers)
            voice_recording = st.audio_input(
                t("mic_record_prompt"),
                key=f"browser_mic_{user_type_label}"
            )

            if voice_recording is not None:
                audio_bytes = voice_recording.getvalue()
                audio_hash = str(hash(audio_bytes))
                processed_flag_key = f"processed_audio_hash_{user_type_label}"

                is_new_speech = (st.session_state.get(processed_flag_key) != audio_hash)
                manual_retrans = False

                if not is_new_speech:
                    manual_retrans = st.button(t("btn_retranslate"), key=f"retrans_btn_{user_type_label}", use_container_width=True)

                if is_new_speech or manual_retrans:
                    st.session_state[processed_flag_key] = audio_hash
                    recognizer = sr.Recognizer()
                    try:
                        with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                            audio_data = recognizer.record(source)
                            stt_code = STT_LANG_CODES.get(src_lang, "en-IN")
                            spoken = recognizer.recognize_google(audio_data, language=stt_code)
                            st.session_state[f"last_spoken_{user_type_label}"] = spoken
                            st.success(f"{t('recognized_voice')} **{spoken}**")
                            run_translation(spoken)
                    except sr.UnknownValueError:
                        st.warning("Could not understand the audio. Please speak clearly into your mic and try again.")
                    except sr.RequestError as e:
                        st.error(f"Speech recognition service error: {e}")
                    except Exception as e:
                        st.error(f"Audio processing error: {e}")
                elif f"last_spoken_{user_type_label}" in st.session_state:
                    st.info(f"🎙️ Current Speech: **{st.session_state[f'last_spoken_{user_type_label}']}**")

            # Local PC Hardware Sound Card Fallback (Only useful for local offline testing)
            with st.expander("⚙️ Advanced: Local PC Sound Card (Localhost Only)", expanded=False):
                st.caption("Direct PyAudio hardware capture. Only functions when running Python locally on your machine with a sound card, not in cloud containers.")
                if st.button("🔴 Local Host Hardware Mic", key=f"local_mic_btn_{user_type_label}", use_container_width=True):
                    status_placeholder = st.empty()
                    status_placeholder.markdown("""
                        <div style='background: linear-gradient(90deg, #dc2626, #ef4444); color: white; border-radius: 8px; padding: 10px 20px; text-align: center; font-weight: 600; margin-bottom: 10px;'>
                            🎙️ Listening on host hardware... (Speak clearly)
                        </div>
                    """, unsafe_allow_html=True)

                    recognizer = sr.Recognizer()
                    try:
                        with sr.Microphone() as source:
                            recognizer.adjust_for_ambient_noise(source, duration=0.4)
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
                            status_placeholder.empty()

                            stt_code = STT_LANG_CODES.get(src_lang, "en-IN")
                            spoken = recognizer.recognize_google(audio, language=stt_code)
                            st.session_state[f"last_spoken_{user_type_label}"] = spoken
                            st.success(f"{t('recognized_voice')} **{spoken}**")
                            run_translation(spoken)
                    except sr.WaitTimeoutError:
                        status_placeholder.empty()
                        st.warning("Listening timed out. No speech was detected.")
                    except sr.UnknownValueError:
                        status_placeholder.empty()
                        st.warning("Could not understand the audio. Please speak clearly.")
                    except Exception as e:
                        status_placeholder.empty()
                        st.error(f"Host microphone unavailable: {e}. When running on the web, please use the Browser WebAudio mic above.")

    with input_tab_text:
        with st.container(border=True):
            st.markdown(f"#### {t('text_input_head')}")
            st.caption(t("text_input_sub"))

            default_val = selected_preset if selected_preset else ""
            typed_query = st.text_input(
                "Enter concept or sentence:",
                value=default_val,
                key=f"txt_{user_type_label}",
                placeholder="e.g., Photosynthesis is the process by which plants make food..."
            )

            if st.button(t("btn_translate_synth"), key=f"trans_btn_{user_type_label}", use_container_width=True):
                run_translation(typed_query)

    with input_tab_file:
        with st.container(border=True):
            st.markdown(f"#### {t('file_input_head')}")
            st.caption("Upload recorded lecture snippets or oral student responses (WAV, MP3, M4A)")

            uploaded_audio = st.file_uploader(
                "Select classroom audio clip:",
                type=["wav", "mp3", "m4a"],
                key=f"uploader_{user_type_label}"
            )
            if uploaded_audio:
                st.audio(uploaded_audio)
                if st.button(t("btn_translate_clip"), key=f"file_btn_{user_type_label}", use_container_width=True):
                    with st.spinner("Processing audio with acoustic recognizer..."):
                        recognizer = sr.Recognizer()
                        try:
                            # Convert uploaded file bytes into AudioFile
                            audio_bytes = uploaded_audio.read()
                            with sr.AudioFile(io.BytesIO(audio_bytes)) as source:
                                audio_data = recognizer.record(source)
                                stt_code = STT_LANG_CODES.get(src_lang, "en-IN")
                                transcribed_text = recognizer.recognize_google(audio_data, language=stt_code)
                                st.success(f"Transcribed Audio: **{transcribed_text}**")
                                run_translation(transcribed_text)
                        except Exception as e:
                            st.error(f"Audio file decoding failed: {e}. Please ensure the file is an uncompressed WAV or standard MP3.")

    # If preset was selected, trigger translation immediately
    if selected_preset:
        run_translation(selected_preset)
