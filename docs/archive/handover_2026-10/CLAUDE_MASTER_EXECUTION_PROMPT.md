# CLAUDE: THE HUMAN VARIABLE — EXECUTION BRIEF

You are taking over a real existing application, not beginning a greenfield design. Originator: Professor Eugen Dimant. Target: MBA, executive MBA, business professionals. Goal: a premium interactive evidence-based learning game at the intersection of AI, business, behavioral economics, and psychology, ultimately deployable on Streamlit.

## First actions (execute, do not just plan)
1. Extract the package. Read `README.md`, `docs/TECHNICAL_HANDOVER.md`, `qa/STATUS_CURRENT.md`, and inspect every source file.
2. Run `python -m unittest discover -s tests -v` and `python -m pytest -q` (install pytest if needed). Report actual results.
3. Run `python start_classroom.py`; check `/api/health`, open `/`, `/classroom`, and `START_HERE.html` in a real browser. Inspect desktop and mobile screenshots. Correct any failures before feature work.
4. Run `python src/build.py`; verify generated content and tests remain consistent.
5. Make meaningful commits after tested changes. Do not claim any unavailable tool or human review was used.

## Nonnegotiable product outcomes
- Premium, restrained editorial visual identity. No generic gradient/card AI aesthetic. Rich, accurate, animated data reveals with reduced-motion support. Real browser screenshots, including 375px, 768px and 1440px.
- Engaging *varied* mechanics: multiple choice, numeric estimation, multi-select, ranking, probabilistic forecasts, confidence calibration, sequential managerial scenarios, AI delegation, budget allocation, causal inference and boundary-condition questions. Do not invent study outcomes to populate game mechanics.
- Prediction → commitment → visual evidence → mechanism → limitations → business application → short predefined follow-ups → next relevant concept. Keep visible text concise. Show depth on demand.
- Build a trustworthy research almanac. Independently verify all 28 carried-forward references, each game claim, exact numerical result, study population and conditions. `docs/VERIFICATION_LEDGER.json` is NOT a completed scientific audit. Only peer-reviewed publications or scholarly books support scored claims. Unverified entries must be excluded from scored play or clearly quarantined until verified. Integrate published Dimant research naturally.
- Real classroom functionality: instructor session creation, access control, participant joins, submissions, controlled reveal, cohort distributions, export, recovery, privacy and 40–50-user concurrency. Existing SQLite server is an early local prototype, not a production-grade shared backend.
- Optional server-side Gemini tutor: retrieval over verified records, citations, caching, budgets, per-user limits, concurrency caps, timeout, key protection, prompt-injection defenses, deterministic curated fallback. Never make the core game depend on the API. Check current Gemini quotas against official docs before promising free capacity.
- Streamlit deployment: do not confuse a Streamlit HTML iframe with a publicly reachable multiuser backend. Propose and implement a working deployment architecture. Streamlit Community Cloud is not by itself a durable shared SQLite hosting solution. Document actual persistence, authentication, secrets and hosting constraints. Preserve a standalone browser build.

## 35 substantive improvement cycles
Perform 35 actual cycles if execution resources permit. For each: identify defect → ten explicitly *simulated* reviewer critiques (MBA, executive, scientist, learning scientist, game designer, creative director, UX, engineer, instructor, skeptic) → prioritize ten candidate improvements → implement valuable changes → execute tests → log file diffs and results. A cycle counts only with an actual code/content/test change. Do not inflate counts or replace work with planning. If interrupted, preserve a working checkpoint and state exact count.

## Verification gates
- Run unit, integration, browser interaction, accessibility, responsive, and load tests. Verify all content/source IDs and scoring paths. Include actual rendered screenshots and a source-by-source scientific ledger.
- Score with weights: science 15, learning 15, visual 15, gameplay 15, AI/business 10, content 10, technical 10, classroom 5, accessibility 5. Target >=95/100 but never manufacture a score. Independent human assessment requires actual humans. No critical defects.
- Report implemented vs tested vs not tested. Do not claim production readiness until backend, security, browser and load checks actually pass.

## Engineering concerns already found
- Existing `streamlit_app.py` embeds a monolithic HTML file at fixed 940px iframe height; not equivalent to a fully responsive Streamlit-native or full-viewport app.
- Existing server listens on 0.0.0.0 and has no TLS, authentication for session creation, persistent production-grade identity, CORS policy, rate limits or data retention. Do not deploy publicly as-is.
- Existing source verification is pending. Source ledger records are not proof of verification.
- SQLite database must not be shipped with classroom participant data; `.gitignore` excludes it.
- Previous live Chromium attempts timed out. No successful screenshot audit is established.
- Prior `python -m unittest` passed 24 tests. A prior pytest invocation outside project root failed on module imports; this handover adds `pytest.ini` to make project-root test discovery explicit. Re-run both.

## Deliverables
One clean GitHub-ready repository and a verified ZIP with runnable code, research bank, verification ledger, instructor backend, offline fallback, optional Gemini integration, tests, Streamlit configuration, reproducible setup, screenshots, quality report, iteration log and honest limitations. Include a succinct final changelog. Do not publish to GitHub or Streamlit without the user's explicit approval and relevant credentials.

## Operating principle
Implement, run, inspect, correct, repeat. Prioritize scientific integrity, actual functioning software, and educational value over feature quantity or lengthy reports. Preserve user voice and concise editorial copy. Do not stop at a beautiful static mockup.
