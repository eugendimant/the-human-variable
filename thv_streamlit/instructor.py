import streamlit as st
import json
from .common import FORMAT_NAME, ROOT, secret, store, style

def join_url(code: str) -> str:
    """The student page with the code filled in, built from the address this page was opened at."""
    try:
        u = st.context.url or ''
    except Exception:
        return ''
    base = u.split('?')[0].rstrip('/')
    base = base.rsplit('/teach', 1)[0]
    return f"{base}/join?code={code}" if base.startswith('http') else ''

def qr_block(text: str):
    """QR code drawn with the vendored MIT qrcode.js, the same generator the instructor console uses."""
    js = (ROOT / 'src/vendor/qrcode.js').read_text(encoding='utf-8')
    html = f"""<div id=q style="background:#fff;padding:8px;display:inline-block;border-radius:10px"></div><script>{js}
    const q = qrcode(0, 'M'); q.addData({json.dumps(text)}); q.make(); document.getElementById('q').innerHTML = q.createSvgTag(5, 0);</script>"""
    import streamlit.components.v1 as components
    components.html(html, height=200)
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
    join = join_url(I['code'])
    a, b = st.columns([3, 1])
    a.markdown(f"Students open **Join a class** and enter <div class='thv-code'>{I['code']}</div>" + (f"<p>Or scan, or open <code>{join}</code></p>" if join else ''), unsafe_allow_html=True)
    if join:
        with b: qr_block(join)
    left, right = st.columns([3, 2])
    with right:
        q = st.text_input('Search decisions', '')
        opts = [c for c in cl.CHALLENGES.values() if q.lower() in (c['title'] + ' ' + c['question'] + ' ' + c['concept']).lower()]
        pick = st.selectbox('Decision', [c['id'] for c in opts], format_func=lambda i: f"{cl.CHALLENGES[i]['title']} ({FORMAT_NAME[cl.CHALLENGES[i]['format']]})") if opts else None
        if st.button('Open for answers', type='primary', disabled=not pick): S.control(I['code'], I['secret'], 'open', pick); st.rerun()
        joining = S.state(I['code']).get('joining', True)
        if st.button('Close joining' if joining else 'Reopen joining'):
            S.control(I['code'], I['secret'], 'lockjoin' if joining else 'unlockjoin'); st.rerun()
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
            if c.get('options') and s['phase'] in ('open', 'closed'):
                from .common import option_order
                st.markdown('\n'.join(f"{k + 1}. {c['options'][i]}" for k, i in enumerate(option_order(c['id'], len(c['options']), I['code']))))
            st.metric('Answered', f"{s['responses']} of {s['participants']}")
            b1, b2 = st.columns(2)
            if s['phase'] == 'open' and b1.button('Stop answers'): S.control(I['code'], I['secret'], 'close'); st.rerun()
            if s['phase'] in ('open', 'closed') and b2.button('Reveal to the room', type='primary'): S.control(I['code'], I['secret'], 'reveal'); st.rerun()
            if s['phase'] == 'revealed' and s.get('aggregate'):
                from .student import show_reveal
                show_reveal(c, s['aggregate'], I['code'])
        live()
