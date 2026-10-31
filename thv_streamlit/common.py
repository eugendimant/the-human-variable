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

# Same option order as the projector console and the phone page (src/classroom.js order()):
# FNV-1a hash of the decision id and session code seeds a mulberry32 shuffle.
_M = 0xFFFFFFFF
def _fnv(s: str) -> int:
    h = 2166136261
    for ch in s: h = ((h ^ ord(ch)) * 16777619) & _M
    return h
def _imul(a: int, b: int) -> int: return (a * b) & _M
def _rng(seed: int):
    x = seed & _M
    def nxt():
        nonlocal x
        x = (x + 0x6D2B79F5) & _M; t = x
        t = _imul(t ^ (t >> 15), t | 1)
        t = (t ^ ((t + _imul(t ^ (t >> 7), t | 61)) & _M)) & _M
        return ((t ^ (t >> 14)) & _M) / 4294967296
    return nxt
def option_order(cid: str, n: int, code: str) -> list:
    """Indices 0..n-1 in the room's shared display order."""
    a = list(range(n)); r = _rng(_fnv(cid + '-' + str(_fnv(code))))
    for i in range(n - 1, 0, -1):
        j = int(r() * (i + 1)); a[i], a[j] = a[j], a[i]
    return a

def embed(html: str, height: int = 900):
    """st.iframe on current Streamlit; components.html on older releases."""
    if hasattr(st, 'iframe'): return st.iframe(html, height=height)
    import streamlit.components.v1 as components
    return components.html(html, height=height, scrolling=True)
