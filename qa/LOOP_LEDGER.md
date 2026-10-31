# Loop ledger

Method: Eugen Dimant's loop (eugen-ops, `the-loop.md`). Each iteration: (1) verify the previous iteration's fixes first, (2) run every gate, (3) read adversarially through ten reviewer lenses, (4) triage into Blocking / Major / Minor / Optional, (5) fix, (6) count Blocking + Major found. The ten lenses are simulated reviewers, run by the model. They are not independent human reviewers.

The lenses: MBA student (M), executive (E), behavioral scientist (S), learning scientist (L), game designer (G), creative director (C), UX and accessibility (U), engineer (N), instructor (I), skeptic (K).

---

## Iteration 1: baseline, audit, architecture, visual system

**Verify previous:** the handover package. All 24 handover tests passed. A browser run at 1440 and 375 px found the logo mark broken: "H·V" wrapped, and the V overflowed below the box.

**Gates run:** unittest 24/24 and pytest 24/24 (old suite). A Playwright run had 0 console errors. The source audit covered 28 sources with four agents: Crossref metadata plus the published text.

**Findings, by lens:**
- S: Blocking. Nine challenges misdescribe a design or a number. Noy & Zhang was called a firm rollout. biz11 contradicts Tversky & Kahneman on incentives. judg02 presents a contested reversal as settled. social15 was called a "workplace study". social19 said "stranger" where the peers were anonymous. social04/05 claimed behavior change. biz05/06 said "utility bill".
- S: Major. Two Dimant years are wrong: Hate Trumps Love is 2024, 70(1); the norms paper in Management Science is 2025, 71(3).
- K: Major. The bank says every source was "checked" without evidence. The verification fields were placeholders.
- C: Major. The visual language matches three generic AI-design defaults: cream paper with a serif display and a coral accent; dark bands with an acid accent; hairline broadsheet rules with ALL-CAPS eyebrows.
- G: Major. 50 of 60 items are single choice, and the conceptual charts decorate rather than inform.
- N: Major. The game is one 168 KB HTML file edited by regex, with no module boundaries or build check.
- U: Minor. The logo overflows and the mobile hero figure labels overlap.
- L: Major. The reveal does not show the distance between the player's call and the evidence.
- M/E: Major. Too little AI × Business. The questions are conceptual ("which assumption is dangerous?"), not predictions about measured outcomes.
- I: Major. The classroom is a JSON dump in a `<pre>`.

**Fixes:**
- Applied 25 logged corrections (`docs/audit/corrections_2026-10-31.json`). judg02/loss15 are quarantined from scored play.
- Every source now has a real verification record: status, date, text read, URL. Volumes and pages were added.
- The front end was split into `src/app.js`, `src/app.css`, `src/scoring.js` and `src/shell.html`. `src/build.py` assembles one offline file with embedded OFL fonts and has a `--check` mode.
- New visual system. Two semantic colors: blue for the player's call, amber for the evidence. Faces are Schibsted Grotesk and Newsreader. No ALL-CAPS eyebrows, no arrow glyphs on buttons.
- New hero: a live prediction on Noy & Zhang, so the first screen is the product.
- New scoring engine with eight formats and partial credit. Forecasts use the Brier rule. There is a calibration module.

**Count:** 1 Blocking + 8 Major. Iterate.

## Iteration 2: classroom, tutor, server, tests

**Verify previous:** the audit corrections were checked by script against the bank (25 entries, all present). A browser re-shot of the home page found two regressions from iteration 1: `.hero` and `.section` padding overrode `.wrap` gutters, so the fact row was misaligned; and the hero showed an empty axis above the slider. Both fixed.

**Gates run:** the new pytest suite, bank gates and an HTTP load test. Results: classroom 6/8 and tutor 12/12 (two classroom tests wait for formats not yet in the bank); HTTP 5/5. Load: 50 clients polling and submitting, p95 poll latency 2 ms.

**Findings:**
- I: Blocking. No instructor-controlled flow. No open/close/reveal, no phone join, no projected view.
- N: Blocking. Session creation is open to anyone; there are no rate limits, no CSP and no retention. The old server bound 0.0.0.0.
- N: Major. A per-IP rate limit would block a whole class behind one campus NAT. Found while writing the limiter; fixed with per-client buckets plus a high per-IP ceiling.
- K: Major. The tutor endpoint returned canned text and had no grounding check.
- E: Major. The Gemini free tier would be exhausted by 30 students. There were no budgets or cache.
- U: Major. On mobile, the "See your record" button appeared in room mode because `.next-row{display:flex}` overrode `[hidden]`. Found in the end-to-end screenshot; fixed globally.
- S: Major. Participant data left the server with nicknames. Now participants are numbers only.
- L: Minor. Students saw the reveal before the instructor revealed it. Room mode now holds the reveal.
- G: Minor. Students could not tell how many classmates had answered. A live count was added.
- M: Optional. A QR code for joining. Added.

**Fixes:**
- `server/classroom.py`: SQLite WAL with a versioned in-memory cache. Five-character codes with no ambiguous glyphs. Hashed instructor keys and participant tokens. Server-side validation for all eight formats, using the Python scorer mirrored from JS. Per-format aggregates, CSV export with formula escaping, a 48-hour retention purge, and end-and-delete.
- `server/tutor.py`: lookup in a fixed order: presets, then cache, then Gemini, then curated answers. BM25 retrieval over the checked bank. Answers that cite nothing retrieved are discarded. There are global RPM and RPD caps, a per-client daily cap and a concurrency cap; a 429 triggers a cooldown, and daily quota exhaustion triggers a shutdown until reset. Configuration errors are not retried. The question is quoted as data.
- `server/app.py`: CSP, nosniff, no-referrer, rate limits, an 8 KB body cap, an optional instructor passcode, `THV_TRUST_PROXY`, and a default bind of 127.0.0.1.
- Room mode in the game (`?room=CODE`), and an instructor console (`classroom.html`) with a QR code, a decision picker, a live count and a per-format reveal.

**Count:** 2 Blocking + 5 Major. Iterate.

## Iteration 3: deployment

**Verify previous:** I re-ran the HTTP and classroom tests (5/5 and 6/8; the two failures need formats that were not yet in the bank). A Playwright end-to-end class with one instructor and three phones passed with 0 console errors.

**Findings:**
- N: Blocking. A Streamlit iframe cannot host the classroom API. Phones cannot reach a second port on Community Cloud.
- I: Major. There was no documented path to a durable shared backend.
- N: Major. `st.components.v1.html` is deprecated and slated for removal. The Streamlit log warned about it.
- U: Major. Streamlit's header overlapped the game's header. Opening `/play` showed a "Page not found" toast, because the default page was given a URL path.
- E: Minor. The Deploy toolbar showed to students.
- N: Minor. No container recipe.
- K: Minor. A broad `pkill` killed the shell during testing. Process rule: never use it.

**Fixes:**
- Native Streamlit pages: Join a class, Run a class, and Ask the tutor. They share one classroom store in-process through `st.cache_resource`, with `st.fragment(run_every=2s)` for live updates.
- The embedded game uses `st.iframe` with full-window CSS. Join controls are hidden inside the frame, where the API is unreachable.
- Added a Dockerfile, `render.yaml` and `fly.toml`, with a volume at `/data`.
- The container file set was run directly (no Docker daemon here): health OK, classroom 200.

**Count:** 1 Blocking + 3 Major. Iterate.

## Iteration 4: content depth and AI × Business orientation

**Verify previous:** the Streamlit e2e passed. The instructor created a session, a phone joined and saw the open decision, and the Play page rendered the game.

**Findings:**
- M/E: Blocking. 29 legacy items asked players to name a concept, with throwaway distractors ("Conservation of momentum", "Room temperature", "An inability to identify colors"). That does not fit an MBA audience.
- S: Major. Classic items gave no measured numbers. Framing, defaults, anchoring and prospect theory now carry verified figures: 72/78%, 37 vs 86%, 25 vs 45, and 80/92%.
- G: Major. There was no structure beyond random rounds. Added seven curated paths and a playbook of ten principles.
- L: Major. No round summary; a "best call" and "biggest surprise" summary was added.
- S: Major. Legacy follow-ups repeated the implication and boundary verbatim. Gate `test_followups_add_information` added; it fires on 31 items. Rewrite agent dispatched.
- K: Major. Dimant items stated limits as "X was not studied". Under RULE 0 they were restated as what each study covers.
- C: Minor. The rank reveal slope chart had labels colliding with lines. Replaced with a two-badge comparison list.
- U: Minor. Disabled delegate chips were unreadable at 45% opacity in the reveal. Fixed.
- U: Minor. The DAG text was 7.5 px on phones. Enlarged.
- S: Minor. The Kristal et al. correction (June 2026) was checked. It fixes table details; the null result stands.

**Fixes:**
- Four drafting agents (clusters A–D) each verified every source against Crossref and the published text, then drafted items with evidence quotes. A fifth agent verified classic numbers.
- Merged with `tools/merge_content_2026_10_31.py`; every change is logged in `docs/audit/merge_log_2026-10-31.json`.
- Result: 95 decisions and 82 sources. Costello et al. was added at Eugen Dimant's instruction.

**Count:** 1 Blocking + 5 Major. Iterate.

## Iteration 5: UX declutter (Eugen: "remove all clutter")

**Verify previous:** the full suite passed (145/146; the 1 failure is the follow-up gate, waiting on the rewrite agent). The browser suite covered every format at 1440 and 390 px with 0 overflow. axe found a serious contrast violation on path cards, now fixed.

**Findings:**
- C/U: Major. The play screen showed a two-column layout with four side panels: confidence, study facts, gap, source and tutor. Too much at once.
- C: Major. The reveal stacked lessons, follow-ups, a note, the source and the tutor in one long scroll.
- G: Major. The primary action was not always in the same place.
- U: Major. The Playbook and Studies pages overlapped in purpose.
- C: Minor. The home page had six sections, including a formats explainer and a facts row.
- U: Minor. The record page showed eight blocks of similar weight.
- C: Minor. The forecast asked a generic question, while the claim sat in a quote box below it.
- S: Minor. A forecast scoring 51 on the wrong side of 50% was labelled "Close".

**Fixes:**
- Focus mode. The site chrome is hidden during a round. The top bar holds only Exit, progress and count. One column of 820 px holds the scene, a one-line study context, the question, the instrument and inline confidence. A fixed bottom action bar carries one primary button, as in Duolingo's Check pattern.
- The reveal shows the verdict, the result headline, the gap figure, the finding and one manager action. Everything else moved into tabs: Questions, Where the evidence comes from, Source, Your note.
- The home page now has a hero with one CTA, a live widget, paths (with a featured case), a custom round behind a link, and the Dimant research band. The Library has Principles and All decisions. The nav is Play, Library, Your record and Join a class.
- The record page shows one big score, three quiet metrics and two summary cards; the explanation sits behind "How scoring works".
- In forecasts the claim is now the headline. The "Close" label applies only when the score is 75 or higher.

**Count:** 0 Blocking + 4 Major. Iterate.
