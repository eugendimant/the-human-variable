

def test_abandoned_open_decision_is_released_after_the_hold(tmp_path):
    """Review 53, m-6: a room left open and never ended holds its decision for two quiet hours, not six."""
    from server import classroom as cl
    st = cl.Store(tmp_path / 'hold.sqlite3'); r = st.create('t'); cid = next(iter(cl.CHALLENGES))
    st.control(r['code'], r['secret'], 'open', cid)
    assert cid in st.open_challenges()
    st.db().execute("UPDATE sessions SET beat = ?", (__import__('time').time() - 3 * 3600,)); st.db().commit(); st._open = None
    assert cid not in st.open_challenges()
