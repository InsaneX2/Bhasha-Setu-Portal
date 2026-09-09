"""
BhashaSetu — AI-Driven Vernacular Pedagogy & Classroom LMS
Smart India Hackathon 2026 | Team INNOVEXA
"""

import os
import streamlit as st
from config import PROJECT_NAME, EDITION
from services.telemetry import init_telemetry
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

if "nav_page" not in st.session_state:
    st.session_state.nav_page = "🏠 Home & Overview"

init_telemetry()

# ----------------------------------------------------
# 3. Top Navigation Header 🧭
# ----------------------------------------------------
top_bar_c1, top_bar_c2 = st.columns([3, 1])

with top_bar_c1:
    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 12px;'>
            <div style='font-size: 2.2rem;'>🎓</div>
            <div>
                <div style='font-size: 1.6rem; font-weight: 800; background: linear-gradient(90deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                    {PROJECT_NAME}
                </div>
                <div style='font-size: 0.82rem; color: #94a3b8; font-weight: 500;'>
                    AI-Driven Vernacular Pedagogy & Classroom Learning Management System
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with top_bar_c2:
    if st.session_state.authenticated:
        st.markdown(f"""
            <div style='text-align: right;'>
                <span class='status-badge-live'><span class='status-dot'></span> {st.session_state.user_role} Session</span>
                <div style='font-size: 0.8rem; color: #94a3b8;'>User: <b>{st.session_state.username}</b></div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚪 Sign Out", key="top_logout"):
            st.session_state.authenticated = False
            st.session_state.user_role = None
            st.session_state.username = None
            st.session_state.nav_page = "🎓 Classroom Portal"
            st.rerun()
    else:
        st.markdown(f"""
            <div style='text-align: right; padding-top: 8px;'>
                <span class='status-badge-live'><span class='status-dot'></span> {EDITION} Portal Live</span>
            </div>
        """, unsafe_allow_html=True)

# Navigation Menu (Tab-based switcher matching design)
nav_options = [
    "🏠 Home & Overview",
    "🎓 Classroom Portal",
    "❓ FAQ & Documentation",
    "🏛️ Contact & Institutions"
]

current_nav = st.session_state.get("nav_page", nav_options[0])
if current_nav not in nav_options:
    current_nav = nav_options[0]

try:
    tabs = st.tabs(nav_options, default=current_nav, key="main_nav_tabs")
except TypeError:
    tabs = st.tabs(nav_options)

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
                    Empowering vernacular pedagogy across 22 Scheduled Indian languages & 9 indigenous tribal dialects.
                </div>
            </div>
            <div class='footer-links'>
                <span class='status-badge-live'><span class='status-dot'></span> All 4 Institutional AI Pipelines Operational</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)