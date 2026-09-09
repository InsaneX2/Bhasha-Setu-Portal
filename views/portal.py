"""
Classroom Portal View
Smart India Hackathon 2026 | BhashaSetu
"""

from datetime import datetime
import streamlit as st
from config import ALL_LANGUAGES
from components.translator_ui import render_translation_interface
from services.telemetry import (
    get_all_logs,
    clear_logs,
    get_logs_dataframe,
    get_csv_export
)


def render_portal_view():
    """Render the role-based classroom portal."""
    if not st.session_state.authenticated:
        st.markdown("### 🔐 Classroom Portal Access")
        st.caption("Sign in to your role-based pedagogical dashboard or use quick 1-click evaluator access below.")

        login_col1, login_col2 = st.columns([1.1, 0.9])

        with login_col1:
            with st.container(border=True):
                st.markdown("#### ⚡ 1-Click Evaluator Access (SIH 2026 Demo Mode)")
                st.caption("Instant preview for Smart India Hackathon jury and evaluators without typing:")

                demo_c1, demo_c2 = st.columns(2)
                with demo_c1:
                    if st.button("👨‍🏫 Login as Teacher (Admin)", key="quick_teacher", use_container_width=True):
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Teacher"
                        st.session_state.username = "teacher1"
                        st.rerun()
                with demo_c2:
                    if st.button("🎓 Login as Student", key="quick_student", use_container_width=True):
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Student"
                        st.session_state.username = "student1"
                        st.rerun()

                st.markdown("<hr style='margin: 16px 0; border-color: rgba(255,255,255,0.08);'>", unsafe_allow_html=True)
                st.markdown("#### 🔑 Standard Credentials Login")
                role = st.radio("Select Persona", ["Student", "Teacher (Admin)"], horizontal=True)
                username_input = st.text_input("User ID", placeholder="e.g., teacher1 or student1")
                password_input = st.text_input("Password", type="password", placeholder="Enter password")

                if st.button("Sign In to Portal", key="btn_signin", use_container_width=True):
                    if role == "Teacher (Admin)" and username_input == "teacher1" and password_input == "admin":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Teacher"
                        st.session_state.username = username_input
                        st.rerun()
                    elif role == "Student" and username_input == "student1" and password_input == "pass":
                        st.session_state.authenticated = True
                        st.session_state.user_role = "Student"
                        st.session_state.username = username_input
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
                "🗣️ Live Translation Workspace",
                "📈 Student Engagement & Learning Telemetry"
            ])

            with tab_translate:
                render_translation_interface("Teacher")

            with tab_telemetry:
                st.markdown("### 📈 Real-Time Classroom Telemetry")
                st.caption("Live persistent monitoring of student vernacular queries, topic trends, and dialect distribution")

                logs = get_all_logs()
                total_searches = len(logs)
                unique_students = len(set([log.get("Student", "") for log in logs])) if total_searches > 0 else 0

                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Translations Logged", total_searches)
                m2.metric("Active Students Tracked", unique_students)
                m3.metric("Supported Dialects", len(ALL_LANGUAGES))
                m4.metric("Pipeline Health", "100% Operational")

                with st.container(border=True):
                    header_col, btn_col1, btn_col2 = st.columns([3, 1, 1])
                    with header_col:
                        st.markdown("#### 📋 Persistent Activity Stream")

                    with btn_col1:
                        if logs:
                            csv_data = get_csv_export()
                            st.download_button(
                                "📥 Export CSV",
                                data=csv_data,
                                file_name=f"bhashasetu_telemetry_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                mime="text/csv",
                                use_container_width=True
                            )

                    with btn_col2:
                        if st.button("🗑️ Clear Logs", use_container_width=True):
                            clear_logs()
                            st.rerun()

                    if logs:
                        df = get_logs_dataframe()
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.info("No activity recorded yet. Conduct a translation in the workspace to see real-time telemetry populate here.")

        elif st.session_state.user_role == "Student":
            render_translation_interface("Student")
