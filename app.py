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
from views.legal import render_legal_view
from services.assets import get_logo_base64

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

if "cookie_consent_acknowledged" not in st.session_state:
    st.session_state.cookie_consent_acknowledged = False

init_telemetry()

# ----------------------------------------------------
# 3. Top Navigation Header 🧭
# ----------------------------------------------------
top_bar_c1, top_bar_c2 = st.columns([2.8, 1.4], vertical_alignment="center")

with top_bar_c1:
    logo_icon_b64 = get_logo_base64("icon")
    logo_img_markup = (
        f"<img src='data:image/png;base64,{logo_icon_b64}' class='navbar-brand-logo' alt='BhashaSetu Official Emblem' />"
        if logo_icon_b64 else "<div style='font-size: 2.2rem;'>🎓</div>"
    )
    st.markdown(f"""
        <div style='display: flex; align-items: center; gap: 14px;'>
            {logo_img_markup}
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
    
    # Minimal compact translator dropdown (small, right-aligned)
    st.markdown("<span id='header-lang-marker'></span>", unsafe_allow_html=True)
    _, c_lang = st.columns([1.1, 1.1])
    with c_lang:
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
                <div style='text-align: right; padding-top: 4px;'>
                    <span class='status-badge-live'><span class='status-dot'></span> {st.session_state.user_role}</span>
                    <div style='font-size: 0.76rem; color: #94a3b8;'>User: <b>{st.session_state.username}</b></div>
                </div>
            """, unsafe_allow_html=True)
        with c_out:
            if st.button(t("sign_out"), key="top_logout", use_container_width=True, help="Sign out of active persona session"):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.nav_page_idx = 1
                st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
                st.rerun()
    else:
        st.markdown(f"""
            <div style='text-align: right; margin-top: 8px;'>
                <span class='status-badge-live header-status-badge'><span class='status-dot'></span> {EDITION} {t('portal_live')}</span>
            </div>
        """, unsafe_allow_html=True)

# Navigation Menu (Tab-based switcher with full vernacular localization)
nav_labels = [
    t("nav_home"),
    t("nav_portal"),
    t("nav_faq"),
    t("nav_contact"),
    t("nav_legal")
]

default_tab_idx = st.session_state.get("nav_page_idx", 0)
if default_tab_idx >= len(nav_labels) or default_tab_idx < 0:
    default_tab_idx = 0

nav_ver = st.session_state.get("nav_ver", 0)
try:
    tabs = st.tabs(
        nav_labels,
        default=nav_labels[default_tab_idx],
        key=f"main_nav_{st.session_state.portal_ui_language}_{nav_ver}"
    )
except TypeError:
    tabs = st.tabs(nav_labels)

tab_home, tab_portal, tab_faq, tab_contact, tab_legal = tabs

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

with tab_legal:
    render_legal_view()

# ----------------------------------------------------
# 5. Global Sticky Footer with Legal Links & Disclosures 🌐
# ----------------------------------------------------
st.markdown(f"""
    <div class='portal-footer'>
        <div style='display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 14px;'>
            <div>
                <b style='color: #e2e8f0;'>{PROJECT_NAME} Platform</b> • {EDITION}
                <div style='font-size: 0.8rem; color: #94a3b8; margin-top: 3px;'>
                    {t('footer_empower')}
                </div>
                <div style='display: flex; gap: 10px; margin-top: 8px; flex-wrap: wrap;'>
                    <span class='compliance-badge'>🛡️ DPDP Act 2023 Compliant</span>
                    <span class='compliance-badge'>♿ WCAG 2.1 AA Accessible</span>
                    <span class='compliance-badge'>🔒 Zero Biometric Retention</span>
                </div>
            </div>
            <div class='footer-links' style='text-align: right;'>
                <span class='status-badge-live'><span class='status-dot'></span> {t('footer_pipelines')}</span>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Quick footer action bar for immediate legal & grievance navigation
foot_col1, foot_col2, foot_col3, foot_col4 = st.columns(4)
with foot_col1:
    if st.button("🔒 Privacy Policy", key="foot_priv", use_container_width=True, help="Read our DPDP Act 2023 compliant privacy policy"):
        st.session_state.nav_page_idx = 4
        st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
        st.session_state.legal_subtab_idx = 0
        st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
        st.rerun()
with foot_col2:
    if st.button("📜 Terms of Use", key="foot_terms", use_container_width=True, help="Read platform educational terms & AI disclaimer"):
        st.session_state.nav_page_idx = 4
        st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
        st.session_state.legal_subtab_idx = 1
        st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
        st.rerun()
with foot_col3:
    if st.button("🍪 Cookie Policy", key="foot_cookies", use_container_width=True, help="Inspect session cookies and storage policy"):
        st.session_state.nav_page_idx = 4
        st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
        st.session_state.legal_subtab_idx = 2
        st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
        st.rerun()
with foot_col4:
    if st.button("🏛️ Grievance Officer", key="foot_grievance", use_container_width=True, help="Statutory Grievance Redressal Officer contact"):
        st.session_state.nav_page_idx = 4
        st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
        st.session_state.legal_subtab_idx = 4
        st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
        st.rerun()

# ----------------------------------------------------
# 6. Privacy & Necessary Cookies Notice (Modal Dialog Popup) 🍪
# ----------------------------------------------------
@st.dialog("🍪 Privacy & Necessary Cookies Notice", width="small")
def show_cookie_consent_modal():
    st.markdown("""
        <div style='font-size: 0.92rem; color: #cbd5e1; line-height: 1.6; margin-bottom: 14px;'>
            <b style='color: #f8fafc; font-size: 1rem;'>BhashaSetu Educational LMS</b><br/>
            We process strictly necessary session tokens for vernacular dialect switching and secure persona authentication.
        </div>
        <div style='background: rgba(56, 189, 248, 0.08); border: 1px solid rgba(56, 189, 248, 0.3); border-radius: 12px; padding: 12px 14px; margin-bottom: 18px; font-size: 0.83rem; color: #94a3b8; line-height: 1.5;'>
            🛡️ <b>DPDP Act 2023 Compliant:</b> Classroom voice streams and queries are processed strictly in-memory with <b>zero permanent biometric storage</b> and zero third-party advertising trackers.
        </div>
    """, unsafe_allow_html=True)

    col_acc, col_pol = st.columns([1.4, 1.0])
    with col_acc:
        if st.button("Accept Necessary", key="modal_ack_cookies", type="primary", use_container_width=True, help="Acknowledge and accept necessary session cookies"):
            st.session_state.cookie_consent_acknowledged = True
            st.rerun()
    with col_pol:
        if st.button("Cookie Policy", key="modal_view_policy", use_container_width=True, help="Inspect full cookie & storage policy"):
            st.session_state.cookie_consent_acknowledged = True
            st.session_state.nav_page_idx = 4
            st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
            st.session_state.legal_subtab_idx = 2
            st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
            st.rerun()

if not st.session_state.cookie_consent_acknowledged:
    show_cookie_consent_modal()