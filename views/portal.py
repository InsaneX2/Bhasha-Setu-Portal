"""
Classroom Portal View
Smart India Hackathon 2026 | BhashaSetu
"""

from datetime import datetime
import streamlit as st
from config import ALL_LANGUAGES
from services.i18n import t
from components.translator_ui import render_translation_interface
from services.telemetry import (
    get_all_logs,
    clear_logs,
    get_logs_dataframe,
    get_csv_export,
    is_telemetry_enabled,
    set_telemetry_enabled
)


def render_portal_view():
    """Render the role-based classroom portal."""
    if not st.session_state.authenticated:
        st.markdown(f"### {t('portal_access_title')}")
        st.caption(t("portal_access_sub"))

        login_col1, login_col2 = st.columns([1.1, 0.9])

        with login_col1:
            with st.container(border=True):
                st.markdown(f"#### {t('demo_eval_title')}")
                st.caption(t("demo_eval_sub"))

                demo_c1, demo_c2 = st.columns(2)
                with demo_c1:
                    if st.button(t("btn_login_teacher"), key="quick_teacher", use_container_width=True):
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Teacher"
                        st.session_state.username = "teacher1"
                        st.session_state.nav_page_idx = 1
                        st.rerun()
                with demo_c2:
                    if st.button(t("btn_login_student"), key="quick_student", use_container_width=True):
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Student"
                        st.session_state.username = "student1"
                        st.session_state.nav_page_idx = 1
                        st.rerun()

                st.markdown("<hr style='margin: 16px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
                st.markdown(f"#### {t('standard_login_title')}")
                role = st.radio(t("select_persona"), ["Student", "Teacher (Admin)"], horizontal=True)
                username_input = st.text_input(t("user_id"), placeholder="e.g., teacher1 or student1")
                password_input = st.text_input(t("password"), type="password", placeholder="Enter password")

                if st.button(t("btn_signin"), key="btn_signin", use_container_width=True):
                    if role == "Teacher (Admin)" and username_input == "teacher1" and password_input == "admin":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Teacher"
                        st.session_state.username = username_input
                        st.session_state.nav_page_idx = 1
                        st.rerun()
                    elif role == "Student" and username_input == "student1" and password_input == "pass":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Student"
                        st.session_state.username = username_input
                        st.session_state.nav_page_idx = 1
                        st.rerun()
                    else:
                        st.error("Invalid credentials. Try `teacher1`/`admin` or `student1`/`pass`, or use 1-Click Access above.")

        with login_col2:
            with st.container(border=True):
                st.markdown("#### 💡 Presentation & Testing Guide")
                st.markdown("""
                * **👨‍🏫 Teacher (Admin) Account**:
                  * **Translation Tool**: Real-time microphone, audio upload & text translator with live audio playback.
                  * **Telemetry Dashboard**: Persistent logging of student questions, popular dialects, and one-click CSV export.
                * **🎓 Student Account**:
                  * Distraction-free vernacular learning assistant designed for easy classroom interaction.
                * **🔑 Demo Credentials**:
                  * Teacher: `teacher1` / `admin`
                  * Student: `student1` / `pass`
                """)
                st.info("💡 Tip: Use the Quick Classroom Prompts once logged in to test instant multi-directional translations with zero typing!")

    else:
        # Authenticated Workspace
        if st.session_state.user_role == "Teacher":
            tab_translate, tab_telemetry = st.tabs([
                t("tab_workspace"),
                t("tab_telemetry")
            ])

            with tab_translate:
                render_translation_interface("Teacher")

            with tab_telemetry:
                st.markdown(f"### {t('telemetry_title')}")
                st.caption(t("telemetry_sub"))

                logs = get_all_logs()
                total_searches = len(logs)
                unique_students = len(set([log.get("Student", "") for log in logs])) if total_searches > 0 else 0

                m1, m2, m3, m4 = st.columns(4)
                m1.metric(t("metric_translations"), total_searches)
                m2.metric(t("metric_students"), unique_students)
                m3.metric(t("metric_dialects"), len(ALL_LANGUAGES))
                m4.metric(t("metric_health"), "Active (MeitY & Adi Vaani)")

                with st.container(border=True):
                    # Privacy & Data Governance Controls
                    st.markdown("##### 🛡️ Privacy & Classroom Data Governance (DPDP Act 2023)")
                    gov_col1, gov_col2 = st.columns([2.2, 1.8])
                    with gov_col1:
                        current_telemetry_state = is_telemetry_enabled()
                        new_telemetry_state = st.toggle(
                            "Enable Pedagogical Telemetry Logging",
                            value=current_telemetry_state,
                            help="When disabled, student queries will not be saved to disk or shown in the activity stream."
                        )
                        if new_telemetry_state != current_telemetry_state:
                            set_telemetry_enabled(new_telemetry_state)
                            st.rerun()
                    with gov_col2:
                        st.caption("🔒 **Right to Erasure:** As a school administrator, you may purge all localized telemetry at any time below.")

                    st.markdown("<hr style='margin: 12px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)

                    header_col, btn_col1, btn_col2 = st.columns([2.5, 1.2, 1.3])
                    with header_col:
                        st.markdown(f"#### {t('activity_stream')}")

                    with btn_col1:
                        if logs:
                            csv_data = get_csv_export()
                            st.download_button(
                                t("btn_export_csv"),
                                data=csv_data,
                                file_name=f"bhashasetu_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    with btn_col2:
                        if st.button(f"🗑️ {t('btn_clear_logs')}", use_container_width=True, help="Permanently erase all activity logs (DPDP Right to Erasure)"):
                            clear_logs()
                            st.success("All activity telemetry erased successfully.")
                            st.rerun()

                    if logs:
                        df = get_logs_dataframe()
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No activity recorded yet. Conduct a translation in the workspace to see real-time telemetry populate here.")

        elif st.session_state.user_role == "Student":
            render_translation_interface("Student")
