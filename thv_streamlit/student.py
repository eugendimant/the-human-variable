import json
import streamlit as st
from .common import FORMAT_NAME, option_order, rank_order, store, style
from server import classroom as cl

def response_widgets(c: dict, key: str, code: str = ''):
    f = c['format']
    idx = option_order(c['id'], len(c.get('options') or []), code) if code else list(range(len(c.get('options') or [])))
    if f == 'causal' and c.get('dag'):   # as in the game: the factors in play, the asked-about one masked; links arrive with the reveal
        st.caption('Factors in play: ' + ', '.join('?' if n.get('mask') else n['label'] for n in c['dag']['nodes']) + '. The reveal shows how they connect.')
    if f in ('choice', 'causal'):
        i = st.radio('Your call', idx, format_func=lambda i: c['options'][i], index=None, key=key + 'r')
        return i
    if f == 'multi':
        sel = st.multiselect('Choose two', idx, format_func=lambda i: c['options'][i], max_selections=len(c['multiAnswers']), key=key + 'm')
        return sel if len(sel) == len(c['multiAnswers']) else None
    if f == 'estimate':
        e = c['estimate']; return st.number_input(f"{e['label']} ({e['min']} to {e['max']})", min_value=e['min'], max_value=e['max'], value=None, step=e.get('step', 1), key=key + 'e', placeholder='Your estimate')
    if f == 'forecast':
        st.markdown(f"<div class='thv-claim'>{c['forecast']['claim']}</div>", unsafe_allow_html=True)
        return st.number_input('Probability the claim is true (0 to 100%)', min_value=0, max_value=100, value=None, step=5, key=key + 'f', placeholder='Your probability')
    if f == 'rank':
        st.caption(c['rankLabel'] + '. Pick the top item first.')
        order = st.multiselect('Your order', rank_order(c['id'], len(c['options']), code) if code else idx, format_func=lambda i: c['options'][i], key=key + 'k')
        return order if len(order) == len(c['options']) else None
    if f == 'allocate':
        a = c['allocate']; vals = []
        for i, o in enumerate(c['options']):
            vals.append(st.number_input(o, 0, a['total'], 0, step=a.get('step', 10), key=key + f'a{i}'))
        st.caption(f"{a['label']}: {sum(vals)} of {a['total']} assigned")
        return vals if sum(vals) == a['total'] else None
    if f == 'delegate':
        picks = []
        for i, t in enumerate(c['delegate']['tasks']):
            picks.append(st.radio(t['text'], range(len(c['delegate']['choices'])), format_func=lambda m: c['delegate']['choices'][m], index=None, horizontal=True, key=key + f'd{i}'))
        return picks if all(p is not None for p in picks) else None

def show_reveal(c: dict, a: dict, code: str = ''):
    st.subheader(c['answerTitle'])
    st.write(c['explain'])
    if c.get('dag'):
        lab = {n['id']: n['label'] for n in c['dag']['nodes']}
        st.caption('How they connect: ' + '; '.join(f"{lab[e[0]]} → {lab[e[1]]}" for e in c['dag']['edges']) + '.')
    cols = st.columns(3)
    cols[0].metric('Answers', a['n']); cols[1].metric('Matched the evidence', f"{a['shareCorrect'] or 0}%"); cols[2].metric('Average score', a['meanScore'] if a['meanScore'] is not None else '–')
    if 'counts' in a: st.bar_chart({c['options'][i][:40]: a['counts'][i] for i in option_order(c['id'], len(c['options']), code)} if code else {o[:40]: v for o, v in zip(c['options'], a['counts'])}, horizontal=True)
    ev_txt = (f"{c['estimate']['target']}{c['estimate'].get('unit', '%')}" if c['format'] == 'estimate' else ('true' if c.get('forecast', {}).get('truth') else 'false')) if c['format'] in ('estimate', 'forecast') else ''
    if 'hist' in a and a.get('n'):
        w = (a['hi'] - a['lo']) / len(a['hist'])   # bins labelled by value range, not by index
        st.bar_chart({f"{round(a['lo'] + i * w)} to {round(a['lo'] + (i + 1) * w)}": v for i, v in enumerate(a['hist'])}); st.caption(f"Class median {a['median']}. Evidence: {ev_txt}.")
    elif 'hist' in a: st.caption(f"No answers came in. Evidence: {ev_txt}.")
    if 'meanPosition' in a: st.bar_chart({o[:40]: len(c['options']) + 1 - p for o, p in zip(c['options'], a['meanPosition']) if p is not None}, horizontal=True); st.caption('Higher bar = ranked nearer the top by the room. Measured order: ' + ', '.join(c['options'][i] for i in c['rankAnswer']) + '.')
    if 'meanShare' in a: st.bar_chart({o[:40]: v for o, v in zip(c['options'], a['meanShare']) if v is not None}, horizontal=True); st.caption('Average budget share. Reported effects: ' + '; '.join(f"{o} {l}" for o, l in zip(c['options'], c['allocate'].get('valueLabels', c['allocate']['values']))) + '.')
    if 'taskCounts' in a:
        for t, cnt in zip(c['delegate']['tasks'], a['taskCounts']): st.write(f"**{t['text']}**: {sum(cnt[j] for j in [t['answer'], *t.get('also', [])])} of {a['n']} chose {' or '.join(c['delegate']['choices'][j] for j in [t['answer'], *t.get('also', [])])}. {t['why']}")
    st.info(f"**What a manager does with this.** {c['implication']}\n\n**Where the evidence comes from.** {c['boundary']}")

def run():
    style(); S = store(); ss = st.session_state
    st.title('Join a live class')
    if 'room' not in ss:
        code = st.text_input('Session code', value=str(st.query_params.get('code', ''))[:8], max_chars=8, placeholder='K7QPM').strip().upper()
        if st.button('Join', type='primary') and code:
            try: ss.room = S.join(code); st.rerun()
            except cl.ClassroomError as e: st.error(str(e))
        st.caption('No name or account needed. The instructor sees participant numbers only.')
        return

    @st.fragment(run_every='2s')
    def live():
        R = ss.room
        try: s = S.state(R['code'])
        except cl.NotFound: st.warning('This session has ended.'); ss.pop('room', None); return
        st.caption(f"Live class {R['code']}, participant {R['number']}. {s['participants']} joined.")
        if s['phase'] == 'lobby' or not s['challenge']:
            st.subheader('You are in. The first decision appears when your instructor opens it.'); return
        c = cl.CHALLENGES[s['challenge']]; done = ss.get('done', {})
        if s['phase'] == 'revealed' and s.get('aggregate'):
            mine = ss.get('mine', {}).get(c['id'])
            if mine is not None:   # the student's own result, as on the game's reveal
                from server import scoring
                sc = scoring.score(c, mine); st.success(f"Your call scored {round(100 * sc['score'])}{' and matched the evidence' if sc['correct'] else ''}.")
            show_reveal(c, s['aggregate'], R['code']); return
        if c['id'] in done:
            st.subheader(done[c['id']]); st.write('The evidence appears for everyone when your instructor reveals it.'); return
        if s['phase'] == 'closed': st.subheader('Answers are closed. Waiting for the reveal.'); return
        st.caption(f"{FORMAT_NAME[c['format']]}, {c['track']}")
        st.write(c['scene']); st.subheader(c['question'])
        with st.form(key='f' + c['id']):
            r = response_widgets(c, c['id'], R['code'])
            conf = None if c['format'] in ('forecast', 'allocate') else st.number_input((f"How sure are you that you land within {c['estimate']['tolerance']}{' points' if c['estimate'].get('unit', '%') == '%' else c['estimate'].get('unit', '')} of the study value? (0 to 100%)" if c['format'] == 'estimate' else 'How sure are you that you got it right? (0 to 100%)'), min_value=0, max_value=100, value=None, step=5, placeholder='Your confidence')
            if st.form_submit_button('Lock my answer', type='primary'):
                if r is None or (c['format'] not in ('forecast', 'allocate') and conf is None): st.error('Give your answer and your confidence first.')
                else:
                    try: m = S.submit(R['code'], R['token'], r, conf)['message']
                    except cl.ClassroomError as e: m = str(e)
                    done[c['id']] = m; ss.done = done; ss.setdefault('mine', {})[c['id']] = r; st.rerun(scope='fragment')
    live()
    if st.button('Leave the class'): ss.pop('room', None); st.rerun()
