"""
Legal, Privacy, Terms, Cookies & Compliance Views
Smart India Hackathon 2026 | BhashaSetu (Team INNOVEXA)
Compliant with DPDP Act 2023 (India), IT Act 2000, and WCAG 2.1 AA Accessibility Standards.
"""

import streamlit as st
from config import (
    PROJECT_NAME,
    EDITION,
    TEAM_NAME,
    CONTACT_EMAIL,
    INSTITUTION_DETAILS,
    GRIEVANCE_OFFICER,
    LEGAL_ENTITY
)


def render_legal_view(active_subtab: str = "privacy"):
    """Render the full legal, privacy, terms, cookie, and compliance portal."""
    st.markdown(f"### ⚖️ {PROJECT_NAME} Legal & Regulatory Compliance Hub")
    st.caption(
        f"Official disclosures, privacy mandates under the **Digital Personal Data Protection Act (DPDP Act 2023)**, "
        f"Terms of Use, and Accessibility commitments for {EDITION}."
    )

    legal_tab_labels = [
        "🔒 Privacy Policy (DPDP Act)",
        "📜 Terms & Conditions",
        "🍪 Cookie Policy",
        "💳 Refund & Pilot Policy",
        "🏛️ Business & Regulatory Details",
        "♿ Accessibility Statement"
    ]

    legal_ver = st.session_state.get("legal_nav_ver", 0)
    legal_idx = st.session_state.get("legal_subtab_idx", 0)
    if legal_idx >= len(legal_tab_labels) or legal_idx < 0:
        legal_idx = 0

    try:
        legal_tabs = st.tabs(
            legal_tab_labels,
            default=legal_tab_labels[legal_idx],
            key=f"legal_subtabs_{legal_ver}"
        )
    except TypeError:
        legal_tabs = st.tabs(legal_tab_labels)

    tab_privacy, tab_terms, tab_cookies, tab_refund, tab_business, tab_a11y = legal_tabs

    # ----------------------------------------------------
    # 1. Privacy Policy
    # ----------------------------------------------------
    with tab_privacy:
        with st.container(border=True):
            st.markdown("#### 🔒 Privacy Notice & Policy")
            st.caption("Last Updated: September 2026 | In Compliance with the Digital Personal Data Protection Act, 2023 (India)")

            st.markdown(f"""
            ##### 1. Identity of the Data Fiduciary
            The Data Fiduciary responsible for processing personal data on this platform is **{LEGAL_ENTITY['entity_name']}**, 
            located at {INSTITUTION_DETAILS['full_address']}. Official communication should be directed to `{CONTACT_EMAIL}`.

            ##### 2. Purpose of Data Collection & Processing
            Under Section 4 and Section 6 of the DPDP Act 2023, personal and academic data is collected strictly for specified, lawful purposes:
            * **Classroom Vernacular Learning**: Facilitating real-time speech-to-text, neural translation, and speech synthesis between scheduled Indian languages and indigenous tribal dialects.
            * **Pedagogical Telemetry**: Enabling educators to analyze classroom comprehension, language usage patterns, and engagement metrics via the Teacher Dashboard.
            * **Institutional Pilot Onboarding**: Responding to school administration requests submitted via our Pilot Form.

            ##### 3. Categories of Data Collected
            We enforce the principle of **Data Minimization** (collecting only what is strictly necessary):
            * **Voice & Audio Streams (Ephemeral)**: Audio inputs captured via the browser microphone or uploaded audio files (MP3, MP4, WAV) are converted into standard PCM WAV in volatile memory. **No biometric voiceprints, voice models, or raw audio files are stored permanently** on our servers.
            * **Classroom Activity Telemetry**: User role (`Teacher` or `Student`), session identifier, source language, target dialect, input query string, translated response, and timestamp.
            * **Pilot Contact Information**: School/institution name, nodal contact email, target regional dialect, and institutional notes provided voluntarily via the pilot form.
            * **Authentication Credentials**: Ephemeral session credentials (`teacher1`, `student1`) used solely for role-based interface demonstration.

            ##### 4. Third-Party Sub-Processors & Data Flow
            To deliver AI vernacular capabilities, specific non-identifiable query payloads are routed through verified national gateways:
            * **Digital India Bhashini Mission (MeitY, Government of India)**: Universal Language Contribution API (ULCA) inference endpoints.
            * **Adi Vaani Linguistic Service (Ministry of Tribal Affairs, Government of India)**: Indigenous tribal dialect translation API.
            * **Google Speech Recognition Service**: Acoustic speech-to-text decoding.
            * *Data Protection Guarantee*: We do not sell, rent, monetize, or disclose student or teacher data to private advertising networks or data brokers.

            ##### 5. Protection of Children & Students (Section 9, DPDP Act 2023)
            Because BhashaSetu is deployed in primary and secondary educational environments:
            * We **do not engage in behavioral tracking, profiling, or targeted marketing** directed at children or students.
            * Institutional deployments must be authorized by the school administration, acting *in loco parentis* or pursuant to parental/guardian consent protocols.
            * All telemetry logging in the student interface can be disabled or anonymized by the school administrator.

            ##### 6. Rights of Data Principals
            Under Chapter III of the DPDP Act 2023, you and your institution have the following rights:
            * **Right to Access Information**: You may inspect all logged telemetry at any time via the Teacher Dashboard.
            * **Right to Correction & Erasure**: You may wipe all stored telemetry logs instantly using the *Clear Telemetry Logs* button.
            * **Right to Grievance Redressal**: You may address any privacy inquiries or complaints to our designated Grievance Officer.
            * **Right to Nominate**: Right to designate a representative in case of incapacity.

            ##### 7. Statutory Grievance Redressal Officer
            In accordance with Section 8(9) of the DPDP Act 2023:
            * **Officer Name:** {GRIEVANCE_OFFICER['name']}
            * **Designation:** {GRIEVANCE_OFFICER['designation']}
            * **Institution:** {GRIEVANCE_OFFICER['institution']}
            * **Official Email:** `{GRIEVANCE_OFFICER['email']}`
            * **Postal Address:** {GRIEVANCE_OFFICER['address']}
            * **Turnaround SLA:** We acknowledge all privacy grievances within 48 hours and provide complete resolution within **{GRIEVANCE_OFFICER['turnaround_days']} working days**.
            """)

    # ----------------------------------------------------
    # 2. Terms and Conditions
    # ----------------------------------------------------
    with tab_terms:
        with st.container(border=True):
            st.markdown("#### 📜 Terms & Conditions of Use")
            st.caption("Standard Educational & Pedagogical License Terms | Smart India Hackathon 2026")

            st.markdown(f"""
            ##### 1. Acceptance of Terms
            By accessing or using the {PROJECT_NAME} platform, you agree to comply with and be bound by these Terms and Conditions. 
            If you represent a school, university, or academic organization, you warrant that you have the institutional authority to bind that entity.

            ##### 2. Permitted Use & Academic Integrity
            * The platform is intended exclusively for educational, pedagogical, research, and classroom comprehension assistance.
            * You agree **not** to:
              * Transmit unlawful, defamatory, obscene, or infringing content through the translation engine.
              * Attempt to reverse-engineer, overload, launch denial-of-service attacks, or tamper with institutional API keys.
              * Use the platform to train proprietary competitive models without prior institutional authorization from MeitY or the project authors.

            ##### 3. AI & Linguistic Translation Disclaimer (Important Notice)
            * **Probabilistic Nature of AI**: Neural Machine Translation (NMT) and Text-to-Speech (TTS) models are probabilistic AI systems. While calibrated against leading academic benchmarks (AI4Bharat IndicTrans-v2, IIIT Hyderabad, and Adi Vaani), translations may occasionally contain dialectical variations or nuances.
            * **Human Teacher Oversight**: BhashaSetu is an *educator-assistive* tool. Human teacher verification is strongly advised for high-stakes examinations, formal grade assessments, or legal compliance notices.
            * **No Academic Guarantee**: {PROJECT_NAME} does not warrant that translation outputs are 100% error-free in every regional colloquial idiom.

            ##### 4. Intellectual Property & Attribution
            * Platform interface design, telemetry dashboards, and orchestration pipelines are copyrighted by **{TEAM_NAME}** under the {EDITION} Open Innovation framework.
            * Underlying foundational models and linguistic corpora remain the property of their respective creators:
              * *Bhashini ULCA*: Ministry of Electronics and IT (MeitY).
              * *Adi Vaani*: Ministry of Tribal Affairs.
              * *IndicTrans & IndicTTS*: AI4Bharat (IIT Madras), IIIT Hyderabad, IIT Bombay.

            ##### 5. Limitation of Liability
            To the maximum extent permitted by Indian Law:
            * {PROJECT_NAME}, its developers, and {INSTITUTION_DETAILS['name']} shall not be liable for any direct, indirect, incidental, or consequential damages resulting from the use or inability to use the platform, including translation inaccuracies during live classroom lectures.

            ##### 6. Governing Law & Jurisdiction
            These Terms shall be governed by and construed in accordance with the **laws of India**. Any dispute arising under these Terms shall be subject to the exclusive jurisdiction of the competent courts in **Sitamarhi / Patna High Court, Bihar, India**.
            """)

    # ----------------------------------------------------
    # 3. Cookie Policy
    # ----------------------------------------------------
    with tab_cookies:
        with st.container(border=True):
            st.markdown("#### 🍪 Cookie & Local Storage Policy")
            st.caption("Transparent disclosure on how cookies and browser storage are utilized")

            st.markdown("""
            ##### 1. What Are Cookies?
            Cookies and browser storage objects are small text files placed on your device to ensure web applications function smoothly.

            ##### 2. How BhashaSetu Uses Cookies
            We adhere to a **strict privacy-first standard**:
            * **100% Strictly Necessary Cookies Only**: We do not deploy third-party advertising cookies, marketing tracking pixels, or cross-site tracking scripts.
            
            | Cookie / Key Name | Type | Purpose | Retention |
            | :--- | :--- | :--- | :--- |
            | `_streamlit_session` | Essential Session Token | Manages the WebSocket connection between your browser and the Streamlit app. | Browser Session (Deleted upon closing tab) |
            | `portal_ui_language` | Functional State | Remembers your chosen vernacular interface language. | Browser Session |
            | `authenticated` | Security Token | Maintains active logged-in persona (Teacher or Student). | Browser Session |
            | `cookie_consent_acknowledged` | Compliance Token | Stores your acknowledgment of this privacy and cookie policy. | Persistent Session |

            ##### 3. Third-Party Analytics & Web Beacons
            * **No Third-Party Ad-Trackers**: There are zero Google Analytics, Meta Pixel, or commercial ad-tech trackers embedded in this codebase.
            * **Fonts & Audio APIs**: Fonts are served via Google Fonts CDN (`fonts.googleapis.com`), which processes standard HTTP requests for font delivery.

            ##### 4. How to Manage or Disable Cookies
            You can modify your browser settings to decline or clear cookies at any time. If you disable session cookies, the application may require re-authenticating or re-selecting your vernacular language upon page refresh.
            """)

    # ----------------------------------------------------
    # 4. Refund & Pilot Policy
    # ----------------------------------------------------
    with tab_refund:
        with st.container(border=True):
            st.markdown("#### 💳 Refund & Institutional Pilot Policy")
            st.caption("Terms governing educational access, school pilot onboarding, and cancellation")

            st.markdown(f"""
            ##### 1. Zero-Fee Public Good Model
            * **Free Educational Access**: {PROJECT_NAME} is an educational research and social-inclusion initiative developed for **{EDITION}**.
            * Individual teachers, students, and classrooms can access the portal and its vernacular translation pipelines **at zero financial charge**.
            * No credit card, bank details, or monetary transactions are required to use the service.

            ##### 2. Institutional Pilot Program Terms
            * Primary, secondary, and tribal welfare schools may apply for custom classroom pilot onboarding via the [Contact Hub](#).
            * Pilot onboarding, integration documentation, and teacher demonstration sessions are provided free of cost by **{TEAM_NAME}**.

            ##### 3. Pilot Cancellation & Data Purging
            * Participating schools may terminate their pilot participation at any time without penalty or notice period.
            * Upon pilot termination, the school may request complete erasure of any localized institutional logs and school records within 48 hours by emailing `{CONTACT_EMAIL}`.

            ##### 4. Commercial Deployments & Future Refund Terms
            * Should any specialized private-cloud enterprise tier or dedicated hardware-accelerated instance be commissioned in the future:
              * All fees, billing milestones, and service level agreements (SLAs) will be governed by a separate written Institutional Service Agreement.
              * A standard 30-day money-back guarantee will apply to any prepaid enterprise server hosting fees if technical uptime falls below 99.5%.
            """)

    # ----------------------------------------------------
    # 5. Business & Regulatory Entity Disclosures
    # ----------------------------------------------------
    with tab_business:
        with st.container(border=True):
            st.markdown("#### 🏛️ Business, Statutory & Institutional Disclosures")
            st.caption("Official entity details pursuant to Indian Consumer Protection & IT Rules")

            b_c1, b_c2 = st.columns(2)
            with b_c1:
                st.markdown(f"""
                **Initiative Name:** `{PROJECT_NAME}`  
                **Parent Institution:** **{INSTITUTION_DETAILS['name']}**  
                **Innovation Team:** `{TEAM_NAME}` ({EDITION})  
                **Registered Address:**  
                {INSTITUTION_DETAILS['village']}, Post Office: {INSTITUTION_DETAILS['post_office']},  
                District: {INSTITUTION_DETAILS['district']}, State: {INSTITUTION_DETAILS['state']} – {INSTITUTION_DETAILS['pincode']}, {INSTITUTION_DETAILS['country']}.  
                **Official Communication Email:** `{CONTACT_EMAIL}`  
                """)
            with b_c2:
                st.markdown(f"""
                **Applicable Statutory Frameworks:**  
                * Digital Personal Data Protection Act (DPDP Act), 2023  
                * Information Technology Act, 2000 (Sections 43A, 72A & SPDI Rules)  
                * Rights of Persons with Disabilities Act, 2016  
                * National Education Policy (NEP 2020) Guidelines on Mother-Tongue Pedagogy  

                **Nodal Hackathon Organizer:**  
                Ministry of Education Innovation Cell (MIC), AICTE, Government of India.
                """)

    # ----------------------------------------------------
    # 6. Accessibility Statement (WCAG 2.1 AA)
    # ----------------------------------------------------
    with tab_a11y:
        with st.container(border=True):
            st.markdown("#### ♿ Accessibility Statement (WCAG 2.1 AA Compliance)")
            st.caption("Commitment to inclusive education under the Accessible India Campaign (Sugamya Bharat Abhiyan)")

            st.markdown("""
            ##### 1. Our Commitment
            {PROJECT_NAME} is committed to ensuring digital accessibility for all users, including students and teachers with visual, auditory, motor, or cognitive impairments. We continuously optimize our portal to conform with the **Web Content Accessibility Guidelines (WCAG) 2.1 Level AA** and the **Guidelines for Indian Government Websites (GIGW)**.

            ##### 2. Accessibility Measures Implemented
            * **High-Contrast Color System**: Muted and body text elements satisfy a minimum contrast ratio of 4.5:1 against dark backgrounds for optimal readability.
            * **Full Keyboard Operability**: All buttons, form inputs, language selectors, and tab panels are traversable and operable using standard keyboard navigation (`Tab`, `Shift+Tab`, `Enter`, `Space`).
            * **Visible Focus Indicators**: High-visibility cyan focus rings (`2px outline with offset`) are applied to all interactive controls during keyboard navigation.
            * **Screen Reader Support**: Semantic HTML headings (`h1` through `h4`), input field labels, and descriptive tooltips accompany all voice recording and playback tools.
            * **Dual-Modality Output**: Every voice translation is simultaneously delivered as high-contrast written text and synthesized audio, accommodating both hearing and visually impaired learners.

            ##### 3. Feedback & Accessibility Contact
            If you encounter any accessibility barrier or require content in an alternative format, please contact our team at `{CONTACT_EMAIL}` with the subject line *"Accessibility Assistance"*. We are committed to responding within 3 working days.
            """.format(PROJECT_NAME=PROJECT_NAME, CONTACT_EMAIL=CONTACT_EMAIL))
