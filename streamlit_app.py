"""Streamlit entry point. Run: streamlit run streamlit_app.py

Pages: the full game (embedded), a native live classroom (instructor and student) and a grounded tutor.
On Streamlit Community Cloud everything runs in one process, so classroom state is shared across
browser sessions through one SQLite file. See docs/DEPLOYMENT.md for durability limits.
"""
import streamlit as st

st.set_page_config(page_title='The Human Variable', page_icon='◐', layout='wide', initial_sidebar_state='collapsed')
from thv_streamlit import play, student, instructor, tutor_page

pages = [
    st.Page(play.run, title='Play', default=True),
    st.Page(student.run, title='Join a class', url_path='join'),
    st.Page(instructor.run, title='Run a class', url_path='teach'),
    st.Page(tutor_page.run, title='Ask the tutor', url_path='tutor'),
]
st.navigation(pages, position='sidebar').run()   # the game has its own top navigation; class pages sit in the sidebar
