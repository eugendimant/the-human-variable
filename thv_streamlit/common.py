import os
from pathlib import Path
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
FORMAT_NAME = {'choice': 'Call it', 'causal': 'Find the cause', 'multi': 'Pick two', 'estimate': 'Estimate', 'forecast': 'Forecast',
               'rank': 'Rank', 'allocate': 'Allocate', 'delegate': 'Delegate'}

def secret(name: str, default: str = '') -> str:
    try:
        v = st.secrets.get(name)
        if v: return str(v)
    except Exception:
        pass
    return os.environ.get(name, default)

@st.cache_resource
def store():
    for k in ('GEMINI_API_KEY', 'GOOGLE_API_KEY', 'THV_INSTRUCTOR_PASSCODE', 'GEMINI_RPM', 'GEMINI_RPD', 'TUTOR_PER_CLIENT_DAY', 'GEMINI_MODELS'):
        v = secret(k)
        if v: os.environ.setdefault(k, v)
    from server.classroom import Store
    d = Path(secret('THV_DATA_DIR', str(ROOT / 'server' / 'data'))); d.mkdir(parents=True, exist_ok=True)
    return Store(d / 'classroom.sqlite3')

@st.cache_resource
def tutor():
    store()  # copies secrets into the environment first
    from server.tutor import Tutor
    d = Path(secret('THV_DATA_DIR', str(ROOT / 'server' / 'data')))
    return Tutor(str(d / 'tutor_cache.sqlite3'))

STYLE = """<style>
html, body, [class*="css"] { font-family: 'Schibsted Grotesk', ui-sans-serif, system-ui, sans-serif; }
.block-container { padding-top: 1.2rem; max-width: 1180px; }
h1, h2, h3 { letter-spacing: -0.02em; }
.thv-code { font-size: 64px; font-weight: 800; letter-spacing: .12em; color: #1f3cc2; line-height: 1; }
.thv-claim { border-left: 3px solid #14203a; background: #e2e7ed; padding: 12px 16px; border-radius: 0 10px 10px 0; font-size: 18px; }
.thv-ev { color: #7d5200; font-weight: 700; }
</style>"""

def style(): st.markdown(STYLE, unsafe_allow_html=True)
