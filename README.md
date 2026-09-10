# 🎓 BhashaSetu — AI-Driven Vernacular Pedagogy & Classroom LMS
### Smart India Hackathon 2026 | Team INNOVEXA

[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![MeitY Bhashini](https://img.shields.io/badge/Powered%20By-MeitY%20Bhashini-0284c7)](https://bhashini.gov.in/)
[![Adi Vaani](https://img.shields.io/badge/Tribal%20Affairs-Adi%20Vaani-16a34a)](https://adivaani.tribal.gov.in/)
[![NEP 2020](https://img.shields.io/badge/Aligned-NEP%202020-f59e0b)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**BhashaSetu** is an AI-powered vernacular pedagogy and classroom learning management platform designed to eliminate linguistic barriers in Indian education. Aligned with the **National Education Policy (NEP 2020)** mandate for mother-tongue instruction, it provides real-time speech-to-speech translation, multilingual transcription, and classroom engagement telemetry across **22 Eighth Schedule Indian languages** and **9 indigenous tribal dialects**.

---

## 🌟 Key Features

- **🌐 22 Scheduled Indian Languages**: Integrated via MeitY Digital India Bhashini (ULCA).
- **🌿 9 Indigenous Tribal Dialects**: Integrated via the Ministry of Tribal Affairs *Adi Vaani* engine (*Santali, Mundari, Bhili, Gondi, Garo, Bettakuruba, Kokborok, Koya, Kui*).
- **⚡ Multi-Directional Indic Translation**: Seamless routing between regional languages (e.g. Hindi ↔ Bengali, Marathi ↔ Tamil) with automatic bridge translation for tribal dialects.
- **🛡️ Multi-Tier Institutional Fallback**:
  - **NMT (Text)**: AI4Bharat (IndicTrans-v2) ➔ IIIT Hyderabad ➔ IIT Bombay.
  - **TTS (Voice)**: IIT Madras ➔ AI4Bharat (IndicTTS) ➔ High-Res Acoustic Fallback.
- **🎙️ Dual-Mode Audio Input**: Live microphone STT (15+ Indian locales) + Audio File Upload (WAV/MP3).
- **🎵 Interactive Audio Visualizer**: HTML5 audio player featuring live animated CSS equalizer visualizers and repeat pronunciation controls.
- **📈 Persistent Classroom Telemetry**: Teacher analytics tracking student vernacular questions, dialect distribution, and one-click CSV export.
- **👨‍🏫 Dual-Persona Portal with 1-Click Demo Login**: Tailored workspaces for teachers and students, with instant evaluator access for hackathon judges.

---

## 📂 Project Architecture

```text
SIH/
├── .streamlit/
│   └── secrets.toml.example  # Secrets template (never commit real secrets.toml)
├── config.py                 # Central language maps, pipeline IDs, & metadata
├── services/
│   ├── bhashini.py           # Multi-tier Bhashini ULCA API & institutional fallback
│   ├── adivaani.py           # Ministry of Tribal Affairs Adi Vaani API & bridging
│   ├── tts.py                # Dual-tier speech synthesis engine
│   └── telemetry.py          # Persistent JSON storage in data/ + CSV exporter
├── components/
│   ├── audio_player.py       # Animated equalizer visualizer & audio player
│   └── translator_ui.py      # Voice/text/audio upload translation workspace
├── views/
│   ├── home.py               # Landing page (Hero, stats, matrix, 4-step pipeline)
│   ├── portal.py             # Classroom Portal (1-click demo logins, telemetry)
│   ├── faq.py                # FAQ, NEP 2020 alignment, and technical specs
│   └── contact.py            # Contact tab with INNOVEXA and SIT Sitamarhi details
├── app.py                    # Main Streamlit application entrypoint
├── style.css                 # Glassmorphism cyber-pedagogy dark CSS design
└── requirements.txt          # Python dependencies
```

---

## 🚀 Quickstart Guide

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Secrets
Create a `.streamlit/secrets.toml` file from the example template:
```bash
mkdir .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```
Open `.streamlit/secrets.toml` and add your Bhashini credentials:
```toml
BHASHINI_API_KEY = "your_api_key_here"
BHASHINI_USER_ID = "your_user_id_here"
```

### 4. Run the Application
```bash
streamlit run app.py
```

---

## 🔑 Demo Accounts for Evaluators

| Role | Username | Password | Notes |
| :--- | :--- | :--- | :--- |
| **Teacher (Admin)** | `teacher1` | `admin` | Access to translation & real-time telemetry |
| **Student** | `student1` | `pass` | Clean vernacular learning workspace |

> *Tip: You can also use the **1-Click Evaluator Access** buttons on the login page for instant demo access without typing!*

---

## 🏛️ Team & Institutional Hub

- **Team Name**: **`INNOVEXA`**
- **Hackathon Edition**: **Smart India Hackathon 2026**
- **Institution**: **Sitamarhi Institute of Technology**
- **Address**: Village: Gosainpur, Post Office: Rasulpur, Sitamarhi, Bihar – 843302, India
- **Contact Email**: `contact@bhashasetu.gov.in`

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).
