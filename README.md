# The Human Variable

A decision lab on behavioral science, AI and business for MBA students, graduate students and executives. Original concept by **Eugen Dimant**.

Players commit to a prediction about a published experiment, state how sure they are, and then see the evidence placed on the same axis as their call. Each reveal shows what a manager does with the finding, where the evidence comes from, three follow-up questions, the source, and an optional tutor.

- **Decisions:** <!--n:decisions-->117<!--/n-->, drawn from <!--n:sources-->108<!--/n--> peer-reviewed papers and scholarly books (<!--n:fulltext-->48<!--/n--> checked against the full text, the rest against the published abstract). Each source has a recorded check against its DOI record and its published text; see [`docs/SCIENTIFIC_AUDIT.md`](docs/SCIENTIFIC_AUDIT.md).
- **Formats:** eight ways to commit: forecast (proper Brier-based score), estimate, rank, allocate a budget, delegate tasks to AI, find the cause (with a causal diagram), pick one, pick two.
- **Structure:** multi-step cases, <!--n:paths-->8<!--/n--> curated paths, a playbook of <!--n:principles-->10<!--/n--> principles, a personal calibration record, and live classes with an instructor console.
- **Research by Eugen Dimant:** <!--n:dimant_decisions-->18<!--/n--> decisions from <!--n:dimant_papers-->14<!--/n--> of his published papers. Working papers are excluded.

## Run it

| What | How | Needs |
|---|---|---|
| Play offline | Open `index.html` in any modern browser | Nothing |
| Game, live classroom and tutor on one machine | `python start_classroom.py`, then open http://localhost:8502/ (game) and http://localhost:8502/classroom (instructor) | Python 3.10+ (standard library only) |
| Streamlit | `pip install -r requirements.txt` then `streamlit run streamlit_app.py` | Streamlit |
| Production host (recommended for classes) | `Dockerfile` (Render, Fly.io, Railway, any container host) | See [`docs/DEPLOYMENT.md`](docs/DEPLOYMENT.md) |

Optional Gemini tutor: set `GEMINI_API_KEY` (environment variable or Streamlit secret). Without it the tutor answers from the lab’s checked summaries. Details, budgets and privacy: [`docs/TUTOR.md`](docs/TUTOR.md).

## Develop

```bash
python src/build.py            # assemble index.html and classroom.html from src/
python src/build.py --check    # fail if the built pages are stale
python -m pytest -q            # content gates, scoring parity (JS vs Python), classroom, tutor, HTTP load, real browser + axe
python tools/make_audit_doc.py # regenerate docs/SCIENTIFIC_AUDIT.md after content changes
```

Content lives in `src/bank.json` (decisions, sources, themes, paths) with supporting quotes in `src/evidence.json`. Content changes are made by scripts in `tools/` so every edit is logged and repeatable. The writing and evidence rules for new items are in [`docs/CONTENT_GUIDE.md`](docs/CONTENT_GUIDE.md).

| Path | Role |
|---|---|
| `src/app.js`, `src/app.css`, `src/scoring.js`, `src/shell.html` | The game (vanilla JS, no framework, no network calls except the optional tutor and live class) |
| `src/classroom.js`, `src/classroom.css` | Instructor console |
| `server/` | Standard-library HTTP server: classroom store (SQLite WAL), tutor (retrieval + Gemini + budgets), Python mirror of the scorer |
| `thv_streamlit/`, `streamlit_app.py` | Streamlit pages: embedded game, native live class, native tutor |
| `tests/` | 150+ automated checks, including Playwright browser tests |
| `qa/` | Loop ledger, quality assessment, change log, screenshots |

## Status and limits

See [`qa/QUALITY_ASSESSMENT.md`](qa/QUALITY_ASSESSMENT.md) for the scored assessment and its evidence. These items remain unverified:

- No live Gemini call has been made from this environment. The tutor's request format follows Google's documentation as of October 2026 and is exercised in tests with a simulated transport.
- No classroom pilot with real students has been run.
- The Docker image was not built here because no container daemon was available. Its file set was run directly and passed.

No university endorsement implied.
