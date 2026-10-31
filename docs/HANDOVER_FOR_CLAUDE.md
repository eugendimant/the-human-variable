# Handover for Claude: The Human Variable

You are taking over **The Human Variable**, an evidence-based decision game on behavioral science, AI and business for MBA students, graduate students and executives. **Original concept: Professor Eugen Dimant** (University of Pennsylvania). He will use it in his teaching and publish it on GitHub and Streamlit. Read this file in full before touching anything.

## 1. What Eugen wants, in his words (binding)

- "It can absolutely not look like AI slop… nothing that looks cheap and nothing that looks just vibe coded." It should look like "a million bucks".
- "Really AI and business orientation, merged with psychology and behavioral science… drawing from my own research."
- "Always backed up with real science": peer-reviewed publications or scholarly books only. **No preprints and no working papers.** That includes his own working papers.
- "Enough variation that people can be engaged." Predict, then see the truth, then learn it with good visuals. Accuracy and scores can be compared later.
- Students can click predefined follow-up questions. An optional Gemini tutor must survive 30 or more simultaneous students on a free key, must be grounded in the lab's knowledge, and must never break the game.
- "Remove all clutter, move stuff elsewhere if not absolutely needed to be front and center." The UX should be best-in-class.
- **Keep iterating until an independent reviewer scores the product at 95/100 or higher.** "Whatever the reviewers suggest, you improve." A score you give yourself does not count.
- **Do not publish the repository or deploy publicly without his explicit approval.**

House rules that apply to anything you write for Eugen:
- Keep prose short, plain and specific, with no generic AI phrasing.
- Never write a sentence that downplays his research contribution. For his studies, state scope as what the study covers, never as what it "did not" do.
- Any correction he makes applies to every place the same defect occurs, not just the one he named.

## 2. Current state (31 October 2026)

| Area | State |
|---|---|
| Content | <!--n:decisions-->112<!--/n--> decisions and <!--n:sources-->103<!--/n--> peer-reviewed sources, each checked against Crossref and against the text the checker read (full text or abstract, recorded per source). Corrections, retirements and replication decisions are logged in `docs/audit/`. <!--n:dimant_decisions-->18<!--/n--> decisions draw on <!--n:dimant_papers-->14<!--/n--> of Eugen Dimant's published papers. |
| Formats | choice, causal (DAG, mediator masked until reveal), multi (pick two), estimate, forecast (1 − 2 × Brier, unclamped), rank (with `rankTies`), allocate, delegate. Two multi-step cases. |
| Structure | <!--n:paths-->8<!--/n--> curated paths, Library (<!--n:principles-->10<!--/n--> principles plus all decisions), personal record with calibration, live classes. |
| UX | Focus mode during play with a fixed action bar. Reveal: verdict, gap figure, finding, one manager action, and tabs for Questions, Scope, Source and Note. |
| Classroom | Standard-library server, SQLite WAL, versioned cache. Instructor console with QR code. Phones use the same option order as the projector. Served pages carry no answers. Evidence is released after lock, and held during a live question. |
| Tutor | Presets, then cache, then Gemini, then curated answers. Budgets and grounding are enforced. See `docs/TUTOR.md`. |
| Deployment | Offline file, Docker (Render or Fly configs), Streamlit multipage. See `docs/DEPLOYMENT.md`. |
| Tests | 175+ checks, including Playwright browser tests and axe. Run `python -m pytest -q`. |
| Quality | Independent reviews are logged in `qa/reviews/` and `qa/LOOP_LEDGER.md`. The latest independent score is in `qa/QUALITY_ASSESSMENT.md`. |

## 3. First actions

1. Run `python -m pytest -q`. All tests must pass. Install Playwright browsers if they are missing (`python -m playwright install chromium`).
2. Open `index.html` directly. Then run `python start_classroom.py` and open http://localhost:8502/ and http://localhost:8502/classroom. Play one path at 1440 px and at 390 px, then run a three-phone live class.
3. Read `qa/LOOP_LEDGER.md` (what was found and fixed, and why), `docs/SCIENTIFIC_AUDIT.md`, and `docs/CONTENT_GUIDE.md`.

## 4. How to work: the loop (binding)

Each iteration does the following, in order:
1. **Verify the previous iteration's fixes first,** with a reader who did not write them: a fresh agent or a test.
2. **Run every gate:** `python src/build.py --check`, `python -m pytest -q`, and `python tools/make_audit_doc.py` after content changes.
3. **Get an independent adversarial review.** Use a fresh agent that copies the tree to a snapshot and reviews only that copy. Give it real browser play at two widths, a live class, axe, content reading through ten lenses (MBA student, executive, behavioral scientist, learning scientist, game designer, creative director, UX and accessibility, engineer, instructor, skeptic), a server audit, and a 100-point score: science 15, learning 15, visual 15, gameplay 15, AI/business 10, content 10, technical 10, classroom 5, accessibility 5. The previous review prompts are in the ledger.
4. **Triage** into Blocking, Major, Minor and Optional.
5. **Fix** in this order: the fact, then the number, then the calibration, then the wording. Turn every new defect class into a test.
6. **Count** Blocking plus Major. With two or more, iterate again. Do not stop below a 95 independent score.

Record each iteration in `qa/LOOP_LEDGER.md`: what was verified, the findings by lens, the fixes, and the count. Never inflate counts, and never claim a check you did not run.

## 5. Content rules

These come from `docs/CONTENT_GUIDE.md`; read the full guide.
- Every number must appear in text you read. Store the quote in `src/evidence.json`, and record full text or abstract in the source's `verification` block.
- A contested finding enters only as an item about the contest. Examples: `bz10` (choice overload), `bz11` (sign-first), `biz04` (towel replication) and `social10` (collective intelligence).
- Non-significant differences are never scored as evidence. Use `rankTies`, zero payoffs, or drop the task.
- Content changes go through scripts in `tools/`, so every edit is logged and repeatable. Do not hand-edit `index.html`; it is built.

## 6. Ideas the next rounds should push on

Run each through the loop and an independent reviewer before calling it done.

- **More allocate and delegate items** (only 2 allocate so far). Use papers that report comparable effects per option.
- **More AI × Business field evidence** as journal versions appear. Candidates must be versions of record. Eloundou et al. (2024, Science) was dropped because its text could not be read; retry.
- **A live Gemini test** with Eugen's key, on a paid or billing-enabled project for EEA, UK or Swiss classes. Confirm the model IDs in `GEMINI_MODELS` against Google's current list. Consider migrating to the Interactions API with `store: false`.
- **A pilot** with 5 or more MBA students and 2 instructors: task completion, comprehension, willingness to continue. Record it honestly in `qa/`.
- **Instructor extras:** a post-class debrief export (class calibration, biggest surprise) and timed rounds.
- **Visual:** a richer illustration per theme drawn as inline SVG, never stock imagery, and dark mode once every chart uses CSS tokens.

## 7. Publishing (only after Eugen approves)

1. Create the GitHub repository (private first) and push. Add a license chosen by Eugen. Fonts are OFL, and their licenses are in `src/fonts/`.
2. GitHub Pages for the offline game, a Render or Fly container for live classes (set `THV_INSTRUCTOR_PASSCODE`), and/or Streamlit Community Cloud. Follow `docs/DEPLOYMENT.md`.
3. Never commit secrets or SQLite data. `.gitignore` covers both.
