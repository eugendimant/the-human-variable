import streamlit as st
from .common import FORMAT_NAME, store, style, tutor
from server import classroom as cl
from server.tutor import PRESETS

def run():
    style(); T = tutor(); ss = st.session_state
    ss.setdefault('client', __import__('secrets').token_hex(6))
    st.title('Ask the tutor')
    st.caption(('Answers come from Gemini, restricted to the lab’s checked sources, with citations. ' if T.enabled else 'No AI key is configured, so answers come from the lab’s checked summaries. ') + 'Verify details in the source.')
    locked, allowed = store().class_lock(); held = store().open_challenges()   # an open question stays held even if the console went quiet
    srcs = lambda i: set(cl.CHALLENGES.get(i, {}).get('sources', []))
    blocked = lambda i: (locked and i not in allowed) or i in held or any(srcs(i) & srcs(h) for h in held)   # same-paper siblings stay held, as on the server
    ids = [i for i in cl.CHALLENGES if not blocked(i)]
    if locked: st.info('A live class is running, so the tutor covers only decisions your class has already revealed.')
    if not ids: return
    cid = st.selectbox('Decision', ids, format_func=lambda i: f"{cl.CHALLENGES[i]['title']} ({cl.CHALLENGES[i]['track']})")
    c = cl.CHALLENGES[cid]
    with st.expander('Show the finding (play the decision first if you want to predict it)'):
        st.write(f"**{c['answerTitle']}.** {c['explain']}")
    cols = st.columns(3); q = None
    for col, p in zip(cols, PRESETS.values()):
        if col.button(p, use_container_width=True): q = p
    for f in c['follow']:
        with st.expander(f['q']): st.write(f['a'])
    typed = st.chat_input('Your question about this study')
    q = typed or q
    if q:
        with st.chat_message('user'): st.write(q)
        r = T.ask(q, cid, ss.client, exclude=blocked if (locked or held) else None)
        with st.chat_message('assistant'):
            st.write(r['answer'])
            if r.get('citations'): st.caption('Sources: ' + '; '.join(x['label'] for x in r['citations']))
            if r.get('note'): st.caption(r['note'])
    if T.enabled: st.caption(f"AI questions left today for you: {T.budget.remaining(ss.client)}")
