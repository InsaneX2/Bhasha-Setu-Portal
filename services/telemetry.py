"""
Classroom Telemetry Service for BhashaSetu
Handles in-memory and persistent JSON storage of student queries, dialect usage, and engagement metrics.
"""

import os
import json
from datetime import datetime
import pandas as pd
import streamlit as st

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
LOG_FILE = os.path.join(DATA_DIR, "telemetry_logs.json")


def _ensure_storage_dir():
    """Ensure data directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)


def load_logs():
    """Load activity logs from local disk or return empty list."""
    _ensure_storage_dir()
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []


def save_logs(logs):
    """Save activity logs to local disk."""
    _ensure_storage_dir()
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception:
        pass


def init_telemetry():
    """Hydrate st.session_state.activity_logs from disk if not present."""
    if "activity_logs" not in st.session_state:
        st.session_state.activity_logs = load_logs()


def log_activity(student_name, src, dest, query, translated):
    """Record a translation query into telemetry state and persist to disk."""
    init_telemetry()
    entry = {
        "Timestamp": datetime.now().strftime("%I:%M %p"),
        "Date": datetime.now().strftime("%Y-%m-%d"),
        "Student": student_name or "Anonymous",
        "Source": src,
        "Target": dest,
        "Query": query,
        "Translated": translated
    }
    st.session_state.activity_logs.append(entry)
    save_logs(st.session_state.activity_logs)


def get_all_logs():
    """Retrieve all logged activity."""
    init_telemetry()
    return st.session_state.activity_logs


def clear_logs():
    """Purge all logged activity from session state and disk."""
    st.session_state.activity_logs = []
    save_logs([])


def get_logs_dataframe():
    """Return activity logs as a pandas DataFrame."""
    logs = get_all_logs()
    if logs:
        return pd.DataFrame(logs)
    return pd.DataFrame(columns=["Timestamp", "Date", "Student", "Source", "Target", "Query", "Translated"])


def get_csv_export():
    """Generate CSV encoded bytes for download."""
    df = get_logs_dataframe()
    return df.to_csv(index=False).encode("utf-8")
