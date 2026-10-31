import streamlit as st
from .common import ROOT

@st.cache_data
def page_html() -> str:
    return (ROOT / 'index.html').read_text(encoding='utf-8')

def run():
    # Let the embedded game fill the window instead of a fixed-height box.
    st.markdown("""<style>
      .block-container{padding:3.4rem 0 0 0 !important;max-width:100% !important}
      header[data-testid="stHeader"]{background:#eceff3;border-bottom:1px solid #cbd3dd}
      iframe{width:100% !important;height:calc(100vh - 3.5rem) !important;border:0}
      footer{display:none}
    </style>""", unsafe_allow_html=True)
    st.iframe(page_html(), height=900)
