# Handover for Claude: The Human Variable

You are taking over **The Human Variable**, an evidence-based decision game on behavioral science, AI and business for MBA students, graduate students and executives. **Original concept: Professor Eugen Dimant** (University of Pennsylvania). He will use it in his teaching and publish it on GitHub and Streamlit. Read this file in full before touching anything.

## 1. What Eugen wants, in his words (binding)

- "It can absolutely not look like AI slop… nothing that looks cheap and nothing that looks just vibe coded." It should look like "a million bucks".
- "Really AI and business orientation, merged with psychology and behavioral science… drawing from my own research."
- "Always backed up with real science": peer-reviewed publications or scholarly books only. A preprint or working paper may only **verify a number** when the published text is paywalled; it is labelled as such in `src/evidence.json` and never appears in player-facing text. When a paper is paywalled, find a preprint (his website links all of his papers) rather than marking a number unverified.
- "Enough variation that people can be engaged." Predict, then see the truth, then learn it with good visuals. Accuracy and scores can be compared later.
- Students can click predefined follow-up questions. An optional Gemini tutor must survive 30 or more simultaneous students on a free key, must be grounded in the lab's knowledge, and must never break the game.
- "Remove all clutter, move stuff elsewhere if not absolutely needed to be front and center." The UX should be best-in-class.
- "Remove all AI design markers from every page" and ask on every page "what would Tufte do?": the title states the finding, the moment that matters is annotated, the source sits inside the figure, and only the mark that proves the headline is coloured. The rules are `qa/DESIGN_RULES.md` (31 rules with detectors in `tools/design_lint.js`) and `qa/TUFTE_PASS.md`.
- "Find a way to not introduce new major problems as you fix them." See section 4: invariants, regression audits and frozen tutor batteries exist for this.
- **Keep iterating until an independent reviewer scores the product at 95/100 or higher.** "Whatever the reviewers suggest, you improve." A score you give yourself does not count.
- **Do not publish the repository or deploy publicly without his explicit approval.**

House rules that apply to anything you write for Eugen:
- Keep prose short, plain and specific, with no generic AI phrasing.
- Never write a sentence that downplays his research contribution. For his studies, state scope as what the study covers, never as what it "did not" do.
- Any correction he makes applies to every place the same defect occurs, not just the one he named.

## 2. Current state (1 November 2026)

| Area | State |
|---|---|
| Content | <!--n:decisions-->112<!--/n--> decisions and <!--n:sources-->109<!--/n--> peer-reviewed sources, each checked against Crossref and against the text the checker read (full text or abstract, recorded per source). Corrections, retirements and replication decisions are logged in `docs/audit/`. <!--n:dimant_decisions-->18<!--/n--> decisions draw on <!--n:dimant_papers-->15<!--/n--> of Eugen Dimant's published papers. |
| Formats | choice, causal (DAG, mediator masked until reveal), multi (pick two), estimate, forecast (1 − 2 × Brier, unclamped), rank (with `rankTies`), allocate (points spread over which option worked best, scored with the same proper rule), delegate. Two multi-step cases. |
| Structure | <!--n:paths-->8<!--/n--> curated paths, Library (<!--n:principles-->10<!--/n--> principles plus all decisions), personal record with calibration, live classes. |
| UX | Focus mode during play with a fixed action bar. Reveal: verdict, gap figure, finding, one manager action, and tabs for Questions, Scope, Source and Note. |
| Classroom | Standard-library server, SQLite WAL, versioned cache. Instructor console with QR code. Phones use the same option order as the projector. Served pages carry no answers. Evidence is released after lock, and held during a live question. |
| Tutor | Presets and a decision's own follow-up questions answer from the summaries; otherwise cache, then Gemini, then the curated router. Without a key the router answers only on a clear match (a route, or a follow-up whose question shares two distinctive words); anything weaker gives the finding plus the decision's own questions as buttons. The routing table is `tools/tutor_routes_2026_10_31.py`; the page (`src/app.js curated`) and the server (`server/tutor.py curated`) must agree word for word. See `docs/TUTOR.md`. |
| Deployment | Offline file, Docker (Render or Fly configs), Streamlit multipage. See `docs/DEPLOYMENT.md`. |
| Tests | Content gates, scoring parity, classroom, tutor, HTTP load, Playwright browser tests and axe. Run `python -m pytest -q`; all must pass. |
| Quality | Independent reviews are logged in `qa/reviews/` and `qa/LOOP_LEDGER.md`. The latest independent score is in `qa/QUALITY_ASSESSMENT.md`. |

## 3. First actions

1. Run `python -m pytest -q`. All tests must pass. Install Playwright browsers if they are missing (`python -m playwright install chromium`).
2. Open `index.html` directly. Then run `python start_classroom.py` and open http://localhost:8502/ and http://localhost:8502/classroom. Play one path at 1440 px and at 390 px, then run a three-phone live class.
3. Read `qa/LOOP_LEDGER.md` (what was found and fixed, and why), `docs/SCIENTIFIC_AUDIT.md`, and `docs/CONTENT_GUIDE.md`.

## 4. How to work: the loop (binding)

Each iteration does the following, in order:
1. **Verify the previous iteration's fixes first,** with a reader who did not write them: a fresh agent or a test.
1a. **Before any fix, name the invariants it touches** (`qa/INVARIANTS.md`, I1 to I16). After the fix, run the full gates, then a **regression audit** with a fresh agent (`qa/AUDIT_PROMPT.md`, given the diff and a snapshot). Fix what it finds and audit again until it finds no introduced Major or Blocking; only then send the snapshot to an independent reviewer. Every new Major class becomes an invariant with a test.
1b. **The tutor is frozen** behind `tests/tutor_golden.json` and `tests/tutor_golden_wide.json` (about 24,000 question and decision pairs). A routing change ships only with the diff `tools/tutor_golden.py` produces, read line by line or by class.
2. **Run every gate:** `python src/build.py --check`, `python -m pytest -q`, and `python tools/make_audit_doc.py` after content changes.
3. **Get an independent adversarial review.** Use a fresh agent that copies the tree to a snapshot and reviews only that copy. Give it real browser play at two widths, a live class, axe, content reading through ten lenses (MBA student, executive, behavioral scientist, learning scientist, game designer, creative director, UX and accessibility, engineer, instructor, skeptic), a server audit, and a 100-point score: science 15, learning 15, visual 15, gameplay 15, AI/business 10, content 10, technical 10, classroom 5, accessibility 5. The review prompt is in `qa/REVIEW_PROMPT.md`.
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

## Where it stands (2026-11-01, after iteration 35)

- Independent scores: 62 at review 1, 82 at review 10, 86 to 87 at reviews 15 to 28 (latest 86 at review 28, with 0 Blocking and 0 Major for the first time since review 21). The target is 95 and it has not been reached.
- The categories have not moved for six reviews: science 13/15, learning 12/15, visual 12/15, gameplay 13/15, AI and business 9/10, content 8/10, technical 9/10, classroom 5/5, accessibility 5/5. Each review finds about a dozen new Minors; all were fixed in the following iteration.
- What reviewers still ask for: a more distinctive visual identity ("a well-made product template rather than a million bucks"), a filled right column on wide reveals before the player has two calls on a principle (the theme strip covers it after that), and a contest item that held up (most contest items resolve to "the famous result failed"). One large drawing per theme was deliberately not added: it would be decoration that encodes nothing, against the Tufte instruction.
- The key-less tutor is a grounded router, not a generator. Extend `tools/tutor_routes_2026_10_31.py` and the golden batteries; never let it borrow an answer on one shared word (see the ledger, iterations 30 to 33).
- Open verification items: bz01's 73%, 222% and 316% figures need the published Marketing Science PDF; dimant-opioid-forecast figures should be rechecked against the Health Economics version of record; the polarized-norms "most chose extremes" line follows the abstract while the body reports 46% above the midpoint.
- Nothing has been published or deployed.
