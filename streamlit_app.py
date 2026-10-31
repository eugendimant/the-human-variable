import streamlit as st
from pathlib import Path
st.set_page_config(page_title='The Human Variable',layout='wide',initial_sidebar_state='collapsed')
st.markdown('<style>header[data-testid="stHeader"], footer {display:none} .block-container{padding:0;max-width:100%}</style>',unsafe_allow_html=True)
import streamlit.components.v1 as components
html=(Path(__file__).parent/'index.html').read_text()
components.html(html,height=940,scrolling=True)
st.caption('For best full-screen experience, use the standalone browser edition. Browser storage inside embedded components can vary by hosting environment.')
