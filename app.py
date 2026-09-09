"""
BhashaSetu — AI-Driven Vernacular Pedagogy & Classroom LMS
Smart India Hackathon 2026 | Team INNOVEXA
"""

import os
import streamlit as st
from config import PROJECT_NAME, EDITION
from services.telemetry import init_telemetry
from services.i18n import t, get_available_ui_languages
from views.home import render_home_view
from views.portal import render_portal_view
from views.faq import render_faq_view
from views.contact import render_contact_view

# ----------------------------------------------------
# 1. Page Configuration & Custom CSS 🎨
# ----------------------------------------------------
st.set_page_config(
    page_title=f"{PROJECT_NAME} | Vernacular Classroom LMS",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)


def load_css(file_name="style.css"):
    """Inject custom stylesheet if available."""
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css("style.css")

# ----------------------------------------------------
# 2. Session State & Telemetry Initialization 🗄️
# ----------------------------------------------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None
    st.session_state.username = None

if "portal_ui_language" not in st.session_state:
    st.session_state.portal_ui_language = "English (Default)"

if "nav_page_idx" not in st.session_state:
    st.session_state.nav_page_idx = 0

init_telemetry()

# ----------------------------------------------------
# 3. Top Navigation Header 🧭
# ----------------------------------------------------
top_bar_c1, top_bar_c2 = st.columns([2.3, 1.2])

with top_bar_c1:
    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='font-size: 2.2rem;'>🎓</div>
            <div>
                <div style='font-size: 1.6rem; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; line-height: 1.25;'>
                    {PROJECT_NAME}
                </div>
                <div style='font-size: 0.82rem; color: #94a3b8; font-weight: 500; line-height: 1.3;'>
                    {t('top_subtitle')}
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with top_bar_c2:
    avail_langs = get_available_ui_languages()
    cur_lang_idx = avail_langs.index(st.session_state.portal_ui_language) if st.session_state.portal_ui_language in avail_langs else 0
    selected_lang = st.selectbox(
        "🌐 UI Language",
        avail_langs,
        index=cur_lang_idx,
        key="portal_ui_language",
        label_visibility="collapsed",
        help="Translate entire portal into tribal dialects (Santali, Gondi, Bhili, etc.) or Indian languages"
    )
    if st.session_state.authenticated:
        c_user, c_out = st.columns([1.1, 0.9])
        with c_user:
            st.markdown(f"""
                <div style='text-align: right; padding-top: 6px;'>
                    <span class='status-badge-live'><span class='status-dot'></span> {st.session_state.user_role}</span>
                    <div style='font-size: 0.76rem; color: #94a3b8;'>User: <b>{st.session_state.username}</b></div>
                </div>
            """, unsafe_allow_html=True)
        with c_out:
            if st.button(t("sign_out"), key="top_logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.nav_page_idx = 1
                st.rerun()
    else:
        st.markdown(f"""
            <div style='text-align: right; margin-top: 4px;'>
                <span class='status-badge-live'><span class='status-dot'></span> {EDITION} {t('portal_live')}</span>
            </div>
        """, unsafe_allow_html=True)

# Navigation Menu (Tab-based switcher with full vernacular localization)
nav_labels = [
    t("nav_home"),
    t("nav_portal"),
    t("nav_faq"),
    t("nav_contact")
]

default_tab_idx = st.session_state.get("nav_page_idx", 0)
if default_tab_idx >= len(nav_labels):
    default_tab_idx = 0

try:
    tabs = st.tabs(nav_labels, default=nav_labels[default_tab_idx], key=f"main_nav_{st.session_state.portal_ui_language}")
except TypeError:
    tabs = st.tabs(nav_labels)

tab_home, tab_portal, tab_faq, tab_contact = tabs

# ----------------------------------------------------
# 4. View Routing 🔀
# ----------------------------------------------------
with tab_home:
    render_home_view()

with tab_portal:
    render_portal_view()

with tab_faq:
    render_faq_view()

with tab_contact:
    render_contact_view()

# ----------------------------------------------------
# 5. Global Sticky Footer 🌐
# ----------------------------------------------------
st.markdown(f"""
    <div class='portal-footer'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px;'>
            <div>
                <b style='color: #e2e8f0;'>{PROJECT_NAME} Platform</b> • {EDITION}
                <div style='font-size: 0.78rem; color: #64748b; margin-top: 2px;'>
                    {t('footer_empower')}
                </div>
            </div>
            <div class='footer-links'>
                <span class='status-badge-live'><span class='status-dot'></span> {t('footer_pipelines')}</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)