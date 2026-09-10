"""
Contact & Institutions View
Smart India Hackathon 2026 | BhashaSetu
"""

import streamlit as st
from config import (
    ALL_LANGUAGES,
    TEAM_NAME,
    CONTACT_EMAIL,
    EDITION,
    INSTITUTION_DETAILS
)


def render_contact_view():
    """Render the institutional hub and contact information."""
    st.markdown("### 🏛️ Institutional Hub & Project Information")
    st.caption(f"{EDITION} project details, nodal ministries, and institutional support")

    inst_c1, inst_c2 = st.columns([1.1, 0.9])

    with inst_c1:
        with st.container(border=True):
            st.markdown("#### 🤝 Participating Ministries & Institutional Pillars")
            st.markdown("""
            * **Ministry of Electronics and Information Technology (MeitY)**:
              * *Digital India Bhashini Mission* — Providing national foundational AI models for 22 scheduled Indian languages.
            * **Ministry of Tribal Affairs**:
              * *Adi Vaani Initiative* — Enabling linguistic inclusion for indigenous tribal student communities.
            * **Ministry of Education**:
              * *Department of School Education & Literacy* — Aligning classroom tools with the NEP 2020 national curriculum.
            * **Academic Research Partners**:
              * AI4Bharat (IIT Madras) • IIIT Hyderabad • IIT Bombay
            """)

        with st.container(border=True):
            st.markdown(f"#### 📍 Project Location & {EDITION} Hub")
            st.markdown(f"""
            **Project Team:** `{TEAM_NAME}`  
            **Institution:** **{INSTITUTION_DETAILS['name']}**  
            **Address:** {INSTITUTION_DETAILS['full_address']}  
            **District / State:** {INSTITUTION_DETAILS['district']}, {INSTITUTION_DETAILS['state']} – {INSTITUTION_DETAILS['pincode']}  
            **Contact Email:** `{CONTACT_EMAIL}` (Demo Portal)  
            **Hackathon Edition:** {EDITION} Innovation Cell  
            """)

    with inst_c2:
        with st.container(border=True):
            st.markdown("#### ✉️ School Pilot Request & Feedback")
            st.caption("Interested in piloting BhashaSetu in your regional school or classroom?")

            with st.form("pilot_request_form"):
                school_name = st.text_input(
                    "School / Institution Name *",
                    placeholder="e.g., Kendriya Vidyalaya No. 1, Ranchi",
                    help="Official registered name of the educational institution."
                )
                contact_email = st.text_input(
                    "Institutional Contact Email *",
                    placeholder="e.g., principal@school.edu.in",
                    help="Official institutional email for pilot onboarding communication."
                )
                target_region = st.selectbox(
                    "Primary Dialect or Regional Language Needed *",
                    ALL_LANGUAGES,
                    index=0,
                    help="Primary student vernacular dialect required for classroom translation."
                )
                feedback_notes = st.text_area(
                    "Classroom Requirements / Project Notes",
                    placeholder="Describe student demographics, grade levels, and specific pedagogical requirements...",
                    help="Optional details regarding student cohort size and language needs."
                )

                # DPDP Act 2023 Statutory Consent Checkbox
                dpdp_consent = st.checkbox(
                    "I consent to the collection and processing of the institutional contact information provided above strictly for pilot onboarding and pedagogical review, in accordance with the BhashaSetu Privacy Policy.",
                    value=False,
                    help="Mandatory consent pursuant to Section 6 of the Digital Personal Data Protection Act, 2023."
                )

                submitted = st.form_submit_button("Submit Pilot Application", use_container_width=True)
                if submitted:
                    if not school_name or not school_name.strip():
                        st.error("Please enter a valid School or Institution name.")
                    elif not contact_email or "@" not in contact_email or "." not in contact_email:
                        st.error("Please provide a valid institutional contact email address.")
                    elif not dpdp_consent:
                        st.warning("Consent required: Please acknowledge the DPDP Act privacy consent checkbox above before submitting your application.")
                    else:
                        st.success(f"Thank you, {school_name.strip()}! Your pilot onboarding application for {target_region} instruction has been registered. The {TEAM_NAME} nodal team will contact `{contact_email.strip()}`.")

