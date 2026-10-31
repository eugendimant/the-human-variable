import streamlit as st
from .common import FORMAT_NAME, secret, store, style
from server import classroom as cl

def run():
    style(); S = store(); ss = st.session_state
    st.title('Run a live class')
    if 'inst' not in ss:
        st.write('Students join on the **Join a class** page with a code. You open one decision at a time and reveal the class picture next to the evidence.')
        with st.form('create'):
            title = st.text_input('Session name', max_chars=80, placeholder='Leading with AI, week 3')
            pw = st.text_input('Instructor passcode', type='password') if secret('THV_INSTRUCTOR_PASSCODE') else ''
            if st.form_submit_button('Create the session', type='primary'):
                if secret('THV_INSTRUCTOR_PASSCODE') and pw != secret('THV_INSTRUCTOR_PASSCODE'): st.error('Wrong passcode.')
                else: ss.inst = S.create(title); st.rerun()
        st.caption('Answers are stored by participant number only and deleted when you end the session or after 48 hours.')
        return
    I = ss.inst
    st.markdown(f"Students open **Join a class** and enter <div class='thv-code'>{I['code']}</div>", unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with right:
        q = st.text_input('Search decisions', '')
        opts = [c for c in cl.CHALLENGES.values() if q.lower() in (c['title'] + ' ' + c['question'] + ' ' + c['concept']).lower()]
        pick = st.selectbox('Decision', [c['id'] for c in opts], format_func=lambda i: f"{cl.CHALLENGES[i]['title']} ({FORMAT_NAME[cl.CHALLENGES[i]['format']]})") if opts else None
        if st.button('Open for answers', type='primary', disabled=not pick): S.control(I['code'], I['secret'], 'open', pick); st.rerun()
        st.download_button('Download answers (CSV)', S.export_csv(I['code'], I['secret']), file_name=f"human-variable-{I['code']}.csv", mime='text/csv')
        if st.button('End session and delete data'):
            S.control(I['code'], I['secret'], 'end'); ss.pop('inst'); st.rerun()
    with left:
        @st.fragment(run_every='2s')
        def live():
            s = S.state(I['code'], admin=True)
            if not s['challenge']: st.info('Nothing open yet. Pick a decision on the right.'); return
            c = cl.CHALLENGES[s['challenge']]
            st.caption(f"{c['track']} · {FORMAT_NAME[c['format']]} · {s['phase']}")
            st.subheader(c['question'])
            st.metric('Answered', f"{s['responses']} of {s['participants']}")
            b1, b2 = st.columns(2)
            if s['phase'] == 'open' and b1.button('Stop answers'): S.control(I['code'], I['secret'], 'close'); st.rerun()
            if s['phase'] in ('open', 'closed') and b2.button('Reveal to the room', type='primary'): S.control(I['code'], I['secret'], 'reveal'); st.rerun()
            if s['phase'] == 'revealed' and s.get('aggregate'):
                from .student import show_reveal
                show_reveal(c, s['aggregate'])
        live()
