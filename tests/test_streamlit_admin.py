"""Owner, 2026-11-18: on Streamlit nothing about running a class is shown before the passcode, and the sidebar menu of internal pages is hidden."""
import pytest
pytest.importorskip('streamlit')
from pathlib import Path
from streamlit.testing.v1 import AppTest
ROOT = Path(__file__).resolve().parents[1]

def _app():
    import sys, os; sys.path.insert(0, os.environ['THV_ROOT'])
    from thv_streamlit import instructor; instructor.run()

def test_admin_page_shows_only_the_passcode_until_it_is_right(tmp_path, monkeypatch):
    monkeypatch.setenv('THV_ROOT', str(ROOT)); monkeypatch.setenv('THV_DATA_DIR', str(tmp_path)); monkeypatch.setenv('THV_INSTRUCTOR_PASSCODE', 'pw-123')
    at = AppTest.from_function(_app, default_timeout=30).run()
    assert [b.label for b in at.button] == ['Open admin'] and [t.label for t in at.text_input] == ['Passcode']
    at.text_input[0].set_value('wrong'); at.button[0].click(); at.run()
    assert any('Wrong passcode' in e.value for e in at.error) and [t.label for t in at.text_input] == ['Passcode']
    at.text_input[0].set_value('pw-123'); at.button[0].click(); at.run()
    assert [b.label for b in at.button] == ['Create a new class'] and not at.exception
    at.button[0].click(); at.run()
    assert any('Join a class' in m.value for m in at.markdown) and not at.exception

def test_admin_page_is_off_without_a_passcode(tmp_path, monkeypatch):
    monkeypatch.setenv('THV_ROOT', str(ROOT)); monkeypatch.setenv('THV_DATA_DIR', str(tmp_path)); monkeypatch.delenv('THV_INSTRUCTOR_PASSCODE', raising=False)
    at = AppTest.from_function(_app, default_timeout=30).run()
    assert any('switched off' in e.value for e in at.error) and not at.button

def test_every_page_hides_the_sidebar_and_links_to_join_and_admin():
    from thv_streamlit import common
    assert 'stSidebar' in common.STYLE and 'display: none' in common.STYLE
    assert all(f'href="{h}"' in common.LINKS for h in ('./', 'join', 'tutor', 'teach'))
