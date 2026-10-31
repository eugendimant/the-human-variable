import streamlit as st
from .common import ROOT, embed, secret, store

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
    # The embedded game is the self-study file, which carries its answers. A deployment set up for classes
    # (instructor passcode configured) leaves solo play off unless THV_STREAMLIT_SOLO=1 asks for it.
    solo = secret('THV_STREAMLIT_SOLO', '0' if secret('THV_INSTRUCTOR_PASSCODE') else '1') == '1'
    if not solo:
        st.title('The Human Variable')
        st.write('This deployment runs live classes. Open **Join a class** and enter the code on the instructor screen. Self-study play is available in the offline game your instructor shares.')
        return
    if store().class_lock()[0] or store().open_challenges():   # any class with an unrevealed decision also pauses solo play
        st.info('A live class is running on this app. Solo play pauses until it ends, so the evidence stays hidden until your instructor reveals it. Use "Join a class" to take part.')
        return
    embed(page_html(), height=900)
