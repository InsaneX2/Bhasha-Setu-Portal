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
top_bar_c1, top_bar_c2 = st.columns([3.8, 1.2], gap="medium", vertical_alignment="center")

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
            if st.button(t("sign_out"), key="top_logout", use_container_width=True, help="Sign out of active persona session"):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.nav_page_idx = 1
                st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
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
# 6. Bottom Floating Cookie Consent Overlay (Standard Web Pattern) 🍪
# ----------------------------------------------------
if not st.session_state.cookie_consent_acknowledged:
    with st.container(key="cookie_popup_bar"):
        st.markdown("""
            <div class='cookie-overlay-anchor'></div>
            <style>
            .st-key-cookie_popup_bar,
            div[data-testid="stVerticalBlockBorderWrapper"]:has(.cookie-overlay-anchor),
            div[data-testid="stVerticalBlock"]:has(.cookie-overlay-anchor) {
                position: fixed !important;
                bottom: 0 !important;
                left: 0 !important;
                right: 0 !important;
                width: 100vw !important;
                max-width: 100vw !important;
                margin: 0 !important;
                padding: 14px 36px 16px 36px !important;
                background: #000000 !important;
                background: rgba(5, 8, 14, 0.98) !important;
                border-top: 1px solid rgba(255, 255, 255, 0.16) !important;
                border-left: none !important;
                border-right: none !important;
                border-bottom: none !important;
                border-radius: 0 !important;
                box-shadow: 0 -10px 36px rgba(0, 0, 0, 0.88) !important;
                z-index: 999999999 !important;
                backdrop-filter: blur(16px) !important;
                -webkit-backdrop-filter: blur(16px) !important;
            }
            .st-key-cookie_btn_customise button {
                background: #0d121d !important;
                color: #f8fafc !important;
                border: 1px solid rgba(255, 255, 255, 0.38) !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                font-size: 0.86rem !important;
                padding: 6px 12px !important;
                min-height: 38px !important;
                transition: all 0.2s ease !important;
            }
            .st-key-cookie_btn_customise button:hover {
                background: rgba(255, 255, 255, 0.12) !important;
                border-color: rgba(255, 255, 255, 0.7) !important;
            }
            .st-key-cookie_btn_reject button {
                background: #1d4ed8 !important;
                color: #ffffff !important;
                border: 1px solid #2563eb !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                font-size: 0.86rem !important;
                padding: 6px 12px !important;
                min-height: 38px !important;
                transition: all 0.2s ease !important;
            }
            .st-key-cookie_btn_reject button:hover {
                background: #1e40af !important;
                border-color: #3b82f6 !important;
            }
            .st-key-cookie_btn_accept button {
                background: #2563eb !important;
                color: #ffffff !important;
                border: 1px solid #3b82f6 !important;
                border-radius: 6px !important;
                font-weight: 600 !important;
                font-size: 0.86rem !important;
                padding: 6px 12px !important;
                min-height: 38px !important;
                box-shadow: 0 2px 12px rgba(37, 99, 235, 0.4) !important;
                transition: all 0.2s ease !important;
            }
            .st-key-cookie_btn_accept button:hover {
                background: #1d4ed8 !important;
                border-color: #60a5fa !important;
            }
            @media (prefers-color-scheme: light) {
                .st-key-cookie_popup_bar,
                div[data-testid="stVerticalBlockBorderWrapper"]:has(.cookie-overlay-anchor),
                div[data-testid="stVerticalBlock"]:has(.cookie-overlay-anchor) {
                    background: rgba(255, 255, 255, 0.98) !important;
                    border-top: 1px solid rgba(0, 0, 0, 0.12) !important;
                    box-shadow: 0 -8px 30px rgba(0, 0, 0, 0.12) !important;
                }
                .cookie-popup-title {
                    color: #0f172a !important;
                }
                .cookie-popup-text {
                    color: #334155 !important;
                }
                .st-key-cookie_btn_customise button {
                    background: #f1f5f9 !important;
                    color: #0f172a !important;
                    border-color: #cbd5e1 !important;
                }
            }
            </style>
        """, unsafe_allow_html=True)
        c_text, c_actions = st.columns([3.1, 1.4], gap="medium", vertical_alignment="center")
        with c_text:
            st.markdown("""
                <div>
                    <div class='cookie-popup-title' style='font-size: 1.15rem; font-weight: 700; color: #ffffff; margin-bottom: 3px;'>
                        We value your privacy
                    </div>
                    <div class='cookie-popup-text' style='font-size: 0.82rem; color: #cbd5e1; line-height: 1.45;'>
                        We use cookies to enhance your browsing experience, maintain language preferences, and ensure seamless classroom translation. 
                        By clicking "Accept All", you consent to our use of cookies pursuant to India's <b>DPDP Act 2023</b>. 
                        Learn more in our educational 
                        <a href='#cookie-policy' style='color: #60a5fa; text-decoration: underline;' title='Read Cookie Policy'>Cookie Policy</a>.
                    </div>
                </div>
            """, unsafe_allow_html=True)
        with c_actions:
            b1, b2, b3 = st.columns(3, gap="small", vertical_alignment="center")
            with b1:
                if st.button("Customise", key="cookie_btn_customise", use_container_width=True, help="Configure cookie preferences"):
                    st.session_state.nav_page_idx = 4
                    st.session_state.nav_ver = st.session_state.get("nav_ver", 0) + 1
                    st.session_state.legal_subtab_idx = 2
                    st.session_state.legal_nav_ver = st.session_state.get("legal_nav_ver", 0) + 1
                    st.rerun()
            with b2:
                if st.button("Reject All", key="cookie_btn_reject", use_container_width=True, help="Reject optional tracking tokens"):
                    st.session_state.cookie_consent_acknowledged = True
                    st.rerun()
            with b3:
                if st.button("Accept All", key="cookie_btn_accept", use_container_width=True, help="Accept all session cookies"):
                    st.session_state.cookie_consent_acknowledged = True
                    st.rerun()