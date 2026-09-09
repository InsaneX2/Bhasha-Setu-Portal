"""
Home & Overview Page View
Smart India Hackathon 2026 | BhashaSetu
"""

import streamlit as st
from config import ALL_LANGUAGES, LANG_FAMILIES, TRIBAL_LANG_CODES


def render_home_view():
    """Render the landing home & overview page."""
    # 1. Hero Section
    st.markdown("""
        <div class='hero-badge'>
            <span>🚀 Smart India Hackathon 2026</span> • <span>MeitY Bhashini & Adi Vaani Powered</span> • <span>NEP 2020 Aligned</span>
        </div>
        <div class='hero-title'>
            Empowering Every Student in Their Mother Tongue
        </div>
        <div class='hero-subtitle'>
            BhashaSetu bridges language barriers between teachers and students through real-time multilingual speech translation, intelligent neural fallback across 4 premier Indian institutes, and indigenous tribal dialect support.
        </div>
    """, unsafe_allow_html=True)

    # 2. Key Stat Cards
    s1, s2, s3, s4 = st.columns(4)
    with s1:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>22+</div>
                <div class='stat-label'>Scheduled Indian Languages (Bhashini)</div>
            </div>
        """, unsafe_allow_html=True)
    with s2:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>9+</div>
                <div class='stat-label'>Indigenous Tribal Dialects (Adi Vaani)</div>
            </div>
        """, unsafe_allow_html=True)
    with s3:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>4</div>
                <div class='stat-label'>Premier AI Fallbacks (IIIT, AI4Bharat, IITs)</div>
            </div>
        """, unsafe_allow_html=True)
    with s4:
        st.markdown("""
            <div class='stat-card'>
                <div class='stat-number'>&lt;500ms</div>
                <div class='stat-label'>Low-Latency Speech & Telemetry Processing</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # 3. Call to Actions
    cta1, cta2 = st.columns(2)
    with cta1:
        with st.container(border=True):
            st.markdown("### 🎓 Launch Classroom Portal")
            st.write("Instant access for educators and students to conduct live vernacular lectures, record voice queries, and monitor comprehension metrics.")
            if st.button("Open Portal Workspace ➔", key="cta_portal", use_container_width=True):
                st.session_state.nav_page = "🎓 Classroom Portal"
                st.rerun()
    with cta2:
        with st.container(border=True):
            st.markdown("### 🏛️ NEP 2020 Pedagogical Mandate")
            st.write("The National Education Policy prioritizes mother-tongue education. BhashaSetu implements this mandate directly in classrooms without burdening teachers.")
            if st.button("Read Architecture & FAQs ➔", key="cta_faq", use_container_width=True):
                st.session_state.nav_page = "❓ FAQ & Documentation"
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # 4. Interactive Language Matrix
    st.markdown("### 🗺️ Multilingual Coverage & Dialect Matrix")
    st.caption("Interactive taxonomy of all supported national and indigenous languages across India")

    tab_all, tab_indo, tab_drav, tab_tribal, tab_others = st.tabs([
        f"All Languages ({len(ALL_LANGUAGES)})",
        f"Indo-Aryan ({len(LANG_FAMILIES['Indo-Aryan'])})",
        f"Dravidian ({len(LANG_FAMILIES['Dravidian'])})",
        f"Tribal & Indigenous ({len(LANG_FAMILIES['Tribal & Indigenous'])})",
        f"Tibeto-Burman & Others ({len(LANG_FAMILIES['Tibeto-Burman & Others'])})"
    ])

    def render_chips(langs, is_tribal=False):
        chips_html = "<div style='display: flex; flex-wrap: wrap; gap: 4px; padding: 8px 0;'>"
        for l in langs:
            cls = "lang-chip tribal" if is_tribal or l in TRIBAL_LANG_CODES else "lang-chip"
            icon = "🌿" if is_tribal or l in TRIBAL_LANG_CODES else "🇮🇳"
            chips_html += f"<span class='{cls}'>{icon} {l}</span>"
        chips_html += "</div>"
        st.markdown(chips_html, unsafe_allow_html=True)

    with tab_all:
        render_chips(ALL_LANGUAGES)
    with tab_indo:
        render_chips(LANG_FAMILIES["Indo-Aryan"])
    with tab_drav:
        render_chips(LANG_FAMILIES["Dravidian"])
    with tab_tribal:
        render_chips(LANG_FAMILIES["Tribal & Indigenous"], is_tribal=True)
    with tab_others:
        render_chips(LANG_FAMILIES["Tibeto-Burman & Others"])

    st.markdown("<br>", unsafe_allow_html=True)

    # 5. 4-Step Technical Pipeline Flow
    st.markdown("### ⚡ End-to-End System Architecture")
    st.caption("How BhashaSetu processes live classroom speech with zero friction")

    f1, f2, f3, f4 = st.columns(4)
    with f1:
        with st.container(border=True):
            st.markdown("#### 1. Ingestion 🎙️")
            st.write("**Acoustic Capture**")
            st.caption("Live microphone or uploaded audio with ambient noise reduction and Google STT multi-lingual acoustic engine.")
    with f2:
        with st.container(border=True):
            st.markdown("#### 2. Neural NMT 🧠")
            st.write("**Multi-Tier Fallback**")
            st.caption("Cascaded routing through AI4Bharat IndicTrans-v2, IIIT Hyderabad, IIT Bombay, or Ministry of Tribal Affairs Adi Vaani.")
    with f3:
        with st.container(border=True):
            st.markdown("#### 3. Native TTS 🔊")
            st.write("**Waveform Synthesis**")
            st.caption("Generates speech streams via IIT Madras / AI4Bharat IndicTTS, paired with animated visualizer equalizers.")
    with f4:
        with st.container(border=True):
            st.markdown("#### 4. Telemetry 📊")
            st.write("**Pedagogy Insights**")
            st.caption("Logs real-time student vernacular queries and engagement metrics with persistent JSON storage and CSV export.")
