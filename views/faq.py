"""
FAQ & Documentation View
Smart India Hackathon 2026 | BhashaSetu
"""

import streamlit as st


def render_faq_view():
    """Render the FAQ and technical architecture documentation."""
    st.markdown("### ❓ Frequently Asked Questions & System Documentation")
    st.caption("Everything you need to know about BhashaSetu's pedagogical architecture and AI pipelines")

    with st.expander("📚 1. How does BhashaSetu support the National Education Policy (NEP 2020)?", expanded=True):
        st.write("""
        NEP 2020 explicitly advocates for instruction in home languages and mother tongues wherever possible, particularly in primary and secondary schooling. 
        BhashaSetu empowers educators to teach complex STEM and humanities concepts without language barriers by converting classroom lectures into 22 scheduled national languages and 9 indigenous tribal dialects on-the-fly.
        """)

    with st.expander("🌐 2. How does the Bhashini API integration work?"):
        st.write("""
        BhashaSetu connects to the **MeitY ULCA (Universal Language Contribution API)** gateway. When a query is initiated:
        1. It contacts the ULCA Pipeline discovery endpoint using the institutional ID.
        2. Retrieves the dynamic inference authorization token and callback endpoint.
        3. Cascades through premier institutional models (IIIT Hyderabad for broad NMT, AI4Bharat for IndicTrans-v2, and IIT Madras for regional speech synthesis).
        """)

    with st.expander("🌿 3. How are Indigenous Tribal Dialects supported?"):
        st.write("""
        Standard translation platforms overlook indigenous dialects. BhashaSetu features dedicated routing to the **Ministry of Tribal Affairs' Adi Vaani engine**, enabling real-time translations for Santali, Mundari, Bhili, Gondi, Garo, Bettakuruba, Kokborok, Koya, and Kui, with automatic bridging for Indic source languages.
        """)

    with st.expander("⚡ 4. What is the Multi-Tier Institutional Fallback Engine?"):
        st.write("""
        Classrooms cannot afford server downtime during a live lecture. BhashaSetu implements automatic fallback routing:
        * **NMT (Text)**: Dynamically routes Indic-to-Indic through **AI4Bharat IndicTrans-v2** $\rightarrow$ **IIIT Hyderabad** $\rightarrow$ **IIT Bombay**.
        * **TTS (Voice)**: Tries **IIT Madras** $\rightarrow$ **AI4Bharat IndicTTS** $\rightarrow$ **High-Res Acoustic Fallback**.
        If any single university node experiences high traffic or downtime, the query seamlessly shifts to the next node with zero disruption.
        """)

    with st.expander("🔒 5. What about student data privacy and security?"):
        st.write("""
        All voice inputs are processed in-memory. No student biometric audio or personal credentials are permanently stored on remote public servers. Activity logs recorded in the teacher dashboard are saved locally and can be exported or purged instantly by the school administrator.
        """)

    st.markdown("<br>", unsafe_allow_html=True)

    # Technical Stack Card
    with st.container(border=True):
        st.markdown("#### 🛠️ Technical Specifications & Stack")
        tc1, tc2, tc3 = st.columns(3)
        with tc1:
            st.markdown("**Frontend & Dashboard**")
            st.caption("• Streamlit Framework (Wide Layout)\n• Glassmorphism CSS Design System\n• HTML5 WebAudio & Base64 Streaming\n• Interactive Equalizer Component")
        with tc2:
            st.markdown("**AI & Linguistic Backends**")
            st.caption("• MeitY Bhashini ULCA Pipeline\n• Ministry of Tribal Affairs (Adi Vaani)\n• Google Multi-Lingual Speech STT\n• Resilient Audio File Decoder")
        with tc3:
            st.markdown("**Institutional AI Models**")
            st.caption("• AI4Bharat IndicTrans-v2 & IndicTTS\n• IIIT-H Indic NMT Engine\n• IIT Madras Dialect Nodes\n• IIT Bombay Trilingual Fallback")
