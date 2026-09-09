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

            with st.form("feedback_form"):
                school_name = st.text_input("School / Institution Name", placeholder="e.g., Kendriya Vidyalaya No. 1")
                contact_email = st.text_input("Contact Email", placeholder="e.g., principal@school.edu.in")
                target_region = st.selectbox("Primary State / Dialect Needed", ALL_LANGUAGES, index=0)
                feedback_notes = st.text_area("Notes or Questions", placeholder="Describe your classroom student language requirements...")

                submitted = st.form_submit_button("Submit Pilot Application", use_container_width=True)
                if submitted:
                    if school_name and contact_email:
                        st.success(f"Thank you, {school_name}! Your pilot request for {target_region} instruction has been recorded for the {TEAM_NAME} review team.")
                    else:
                        st.warning("Please provide your institution name and contact email.")
