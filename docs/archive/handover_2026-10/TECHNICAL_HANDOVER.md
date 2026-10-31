# Technical handover and known risks

## Entry points
- `START_HERE.html`: offline navigation landing page. Open `index.html` directly for individual game.
- `index.html`: monolithic playable browser application with embedded content.
- `src/bank.json`: editable challenge/source content; `src/build.py`: content embed step.
- `classroom.html`: browser classroom interface, requires server.
- `start_classroom.py`: starts local HTTP classroom server on port 8502.
- `server/app.py`: stdlib threaded HTTP server and SQLite persistence.
- `streamlit_app.py`: embeds offline game in Streamlit iframe; does not launch classroom server.
- `tests/`: Python unittest suite.
- `docs/VERIFICATION_LEDGER.json`: verification tracking, not certified primary-source audit.

## Run locally
```bash
python -m unittest discover -s tests -v
python -m pytest -q  # requires pytest installed
python start_classroom.py
# http://localhost:8502/classroom
```
For standalone game, open `index.html`. For Streamlit, `pip install -r requirements.txt && streamlit run streamlit_app.py`.

## Important architectural gaps
1. Classroom server is local HTTP only. Public deployment needs TLS, proper auth, abuse controls, persistent hosted DB, lifecycle management, backups and monitoring.
2. Streamlit launcher is an iframe. It does not integrate classroom server or durable multiuser state.
3. Gemini tutor is not implemented. Curated offline answers exist.
4. Publication metadata and associated claims have not been independently checked against all primary papers.
5. No successful full browser interaction and visual regression audit is established.
6. Tests are not a production security or concurrency certification.

## Next actions
First establish a reproducible clean install and browser automation. Then independently audit the evidence, isolate game UI modules, implement diverse challenge formats and classroom backend, and validate an actual Streamlit-hosted deployment path.

## Data handling
Do not commit `server/classroom.sqlite3` or secrets. Existing SQLite data was intentionally excluded from this package. Ensure no student personal data is sent to Gemini without explicit consent and a defined retention policy.
