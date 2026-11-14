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

## Iteration 6: first independent review (fresh agent; did not build the product)

**Verify previous:** all 146 tests passed before the review started. The reviewer ran its own browser rounds, axe and server probes on a snapshot.

**Independent score: 62/100.** Reviewer findings, verbatim severity: 2 Blocking, 15 Major, 14 Minor. Full report: `qa/reviews/review1.md`.

**Blocking:**
- B1: in a live class, pressing N stranded the student on the record page.
- B2: the answer key shipped to every browser, including live-class phones. Estimate items also carried stale options that stated the answer.

**Major:**
- Calibration was computed on a default confidence the player never set.
- Midpoint guesses scored about 80, and a 50% forecast scored 75.
- "Close" appeared on wrong-side forecasts.
- The preset tutor question returned an unrelated retracted study.
- The home page overstated full-text checks.
- Non-significant differences were scored as evidence.
- The causal diagram drew the answer.
- Strawman distractors, and the correct option was often the longest.
- The projector and the phones numbered options differently.
- The instructor console stole focus.
- A join flood was possible, with a spoofable X-Forwarded-For.
- The 48-hour deletion never ran.
- The logo broke the offline file.
- Rank and allocate could be locked without being touched.
- On phones, the gap chart sat below the Next button. This was already fixed in iteration 5.

**Fixes (each verified by a test or a re-run):**
- **Answer-free served pages.** The server rewrites the embedded bank to public fields only. Evidence comes from `/api/reveal/<id>` after a call is locked, and is refused (409) while that decision is open in any live class. Live-class phones get the evidence only in the revealed state. The instructor console loads the full bank with its key. `window.THV` exists only in the offline file. New tests: `test_served_pages_carry_no_answers`, `test_reveal_blocked_while_open_in_a_class`, `test_instructor_bank_needs_key`.
- **Room mode.** N is ignored in a room, and the poll returns the student to play on every new decision. The option order is seeded by the session code, so phones and projector match. The score is finalized from the server's evidence at reveal.
- **Confidence is required before locking** for every format except forecasts. Rank and allocate must be touched. New test: `test_lock_requires_confidence_and_touch`.
- **Scoring.** Estimates reach zero at three tolerances. Percentage ranges were standardized to 0–100 (42 items). Forecasts use the Brier skill against 50%, so hedging scores 0. "Close" never applies to forecasts. Rank ties (`rankTies`) cover differences the studies did not separate. Allocation payoffs set non-significant arms to zero. The parity test (JS against Python) passed.
- **Content.**
  - 15 option sets rewritten to be plausible and length-balanced.
  - The causal mediator is masked until the reveal (`test_causal_diagram_hides_answer_until_reveal`).
  - Stale options were removed from estimate and forecast items.
  - The ai02 scene now stands alone.
  - axb06 wording now matches its observational design.
  - axb01 dropped a task that rested on g = 0.19 (n.s.).
- **Tutor.** The client curated answer gained a size branch scoped to the current item, and no longer borrows unrelated items.
- **Server.**
  - Right-most X-Forwarded-For.
  - Join rate limit per IP per room.
  - A passcode is required for session creation off loopback.
  - Background purge every 10 minutes, with `touched` refreshed on join and submit.
  - Tutor cache purge after 30 days.
- **Console.** Polling uses the etag, re-renders only on change, restores focus and selection, and has page headings.
- **Streamlit.** Charts for every format. Estimate and confidence inputs start empty and are required.
- **Cluster E merged.** 17 AI × Business items from 17 newly checked sources (7 read in full), including the 3-step case "Generative AI in your content team". genai2 was converted from an allocation to an estimate so that small gaps are not scored as evidence.

**Count:** 2 Blocking + 15 Major found. Iterate.

## Iteration 7 (2026-10-31)

**Verified first:** iteration-6 fixes, by independent review 2 (fresh agent, snapshot copy) and by a blind fact-check of 32 randomly drawn decisions against their sources (26 correct, 6 correctable, 0 wrong; `docs/audit/factcheck_sample32_2026-10-31.json`).

**Independent score:** 59/100 (review 2, `qa/reviews/review2.md`). 2 Blocking, 15 Major.

**Fixes:**
- **Class lock (B2).** While any class with participants was active in the last 3 hours, `/api/reveal`, `/api/library` and the tutor release only decisions that class has revealed. Instructors can close and reopen joining. Tests: `test_class_lock_holds_evidence_until_revealed`, `test_join_can_be_closed`. The Streamlit Play and tutor pages follow the same lock.
- **Proper forecast score (M1).** Score = 1 − 2 × Brier, unclamped (−100 to 100), in JS and Python; parity test passes. Copy explains that a confident miss goes below zero.
- **Confidence (M2).** The question now states what "right" means for each format (for example "within ±7 of the true value", "the exact order").
- **Content (M3–M10).** `tools/content_review2_2026_10_31.py` and `tools/content_review2b_2026_10_31.py`: all six fact-check corrections and author lists; bz07 became an estimate of the overall quit-rate drop (33%) with subgroups as a chart; rollout3 offers only the routes the study compared; the Costello boundary states the expression of concern and the reanalysis; 30 titles neutralized; 31 options rewritten. Two unverified numbers (agent count, subgroup P values) were removed rather than kept.
- **New gates.** Correct option longest in at most 35% of choice items (now well under), the two correct pick-two options are never the two longest, no absolute words in distractors, titles may not state the finding.
- **Classroom (M11, M12).** Streamlit phones and instructor use the projector's option order (Python port of the JS shuffle, parity-tested against the console code). Console rank chart: longer bar = nearer the top, labelled with the average rank. Decision list hides while answers are live. CSV export includes readable answer text.
- **Interaction (M13–M15).** Confidence row no longer overflows; lock hint shows on phones; tabs wrap; Enter on an option selects it and no longer locks; scroll padding keeps focus above the action bar. Lifetime stats count first tries only.

**Gates:** build check, 178 tests passed (163 non-browser, 15 browser), audit doc regenerated.

**Count:** 2 Blocking + 15 Major found and addressed. Next: independent review 3.

**Update (2026-10-31, Eugen Dimant):** the expression of concern on Costello et al. (2024) has been officially removed. Every mention was removed from the bank, the Source tab and the docs (`tools/content_costello_notice_2026_10_31.py`); review 2's M6 is superseded.

**Content addition (2026-10-31).** Five new decisions from five newly checked peer-reviewed sources (`tools/merge_allocate_2026_10_31.py`, draft and quotes in `docs/audit/draft_allocate_2026_10_31.json`): axf01 allocate (Köbis et al. 2025, Nature, delegation and dishonesty), axf02 forecast (Milkman et al. 2022, PNAS, scientists' predictions r = 0.03), axf04 delegate (Garvey, Kim & Duhachek 2023, J. Marketing), axf05 rank with ties (Jabbour et al. 2023, JAMA), axf06 allocate with an n.s. arm at zero (Goh et al. 2024, JAMA Netw Open). Dropped: an AMIE item (overlap, untested key comparison) and two follow-ups that rested on partial web excerpts. Played in Chromium at 1440 and 390 px with no errors or overflow; 185 tests pass.

## Iteration 8 (2026-10-31)

**Verified first:** iteration-7 fixes, by independent review 3 (fresh agent, snapshot `snap_r3`): Enter-select, lock rules, class lock on reveal/library/tutor, phone and projector order, console rank chart, forecast parity, join lock and CSV key all held. Partial: the class lock leaked through source takeaways, diagram alt text and bank order; the 390 px overflow persisted before confidence was touched.

**Independent score:** 70/100 (review 3, `qa/reviews/review3.md`). 1 Blocking, 7 Major.

**Fixes:**
- **B1 answers in served sources.** The served bank carries bibliographic records only; takeaways, flags, notes and theme principles travel with the evidence (`/api/reveal`, `/api/library`, both under the class lock). The leak test now walks every decision and fails if any answer title, explanation, implication, follow-up answer, source takeaway, diagram text, masked label or principle appears in the page bytes; it was live-fired by restoring the takeaway and failed as intended.
- **M1 diagram.** The public diagram has no written explanation and no masked label; before the reveal the accessible description lists boxes and arrows only.
- **M2 order.** Option order in the bank was shuffled per item with every index remapped (`tools/permute_options_2026_10_31.py`); the console lists rank items in the phones' starting order. Gate: no position holds more than 45% of answers, no rank item is stored in answer order.
- **M3/M4 tutor.** `exclude` accepts a callable or a set; source records of locked decisions are left out of retrieval; the cache is neither read nor written while a class is locked; a locked decision returns a locked message. Tests added.
- **M5 midpoint.** Six estimates fixed (tolerances, axis ranges, one question flipped to the other anchor group, three converted to forecasts). Gate: the axis midpoint scores at most 50 on every estimate.
- **M6 allocate.** axe04 asks where the budget buys most agreement; axb08 is now a choice item with a chart of all four arms.
- **M7 ties and titles.** The rank reveal marks rows the study did not separate and says those pairs are not scored; two answer titles narrowed; one title neutralized.
- **Minors.** Overflow root cause (a generic `.empty` class added 40 px padding) fixed and tested in the predict state; percentage-point wording; chart legend for study charts; 16 scope lines rewritten positively with a gate; forecast reveal restates the claim and labels the end "Claim true/false"; Brier labelled as a calibration score; one "Start here" flag and a path grid without orphans; Record layout; five distractors and one cross-item leak fixed; tutor label tied to a configured model; free preset answers skip the per-network tutor limit; class lock engages when a decision is open and requires every running class to reveal; Library filter labels, heading order and page titles; constant-time passcode check; Streamlit tutor crash, instructor QR code and join link, prefilled code, join lock.
- **Visual.** A small drawing per principle in the game's blue/amber code (frontier, error, gap, norm shape, default path, and so on) on every path card and principle card.
- **Content.** Five new decisions (see the content addition above).

**Gates:** build check, 190 tests, audit doc and doc counts regenerated.

**Count:** 1 Blocking + 7 Major found and addressed. Next: independent review 4.

## Iteration 9 (2026-10-31)

**Verified first:** iteration-8 fixes, by independent review 4 (fresh agent, snapshot `snap_r4`): served pages carry no answers (full scan), the class lock held on every route probed, midpoint guesses capped at 50, rank ties shown and unscored, axe 0 violations on 21 states, keyboard-only path, 50-student load.

**Independent score:** 76/100 (review 4, `qa/reviews/review4.md`). 0 Blocking, 7 Major.

**Fixes:**
- **M1 path leaks.** Reveals and follow-ups that answered later items on the same path were rewritten (rollout3, rollout2, dimant-polarizednorms-choice, social01, dimant-hate-choice, social15, social16); the Dimant path and the design path were reordered. Gate: an item's key numbers may not appear in the reveal of an earlier item on its path.
- **M2 versions of record (swept across the whole bank).** Every evidence quote located in a working paper was removed; content that rested on them was rewritten or re-sourced (social13, social12, biz02, ai01, ai02, biz01 now cites Cribb & Emmerson 2020 for the 86% and 37% figures). Gates: no working-paper material in decisions or evidence locations.
- **M3 allocate.** Points are spread over which option worked best and scored with the same proper rule as forecasts (1 − sum of squared gaps); splitting pays under uncertainty. No separate confidence; the allocation itself enters calibration. The reveal shows points per option with the reported values as labels, no mixed axes.
- **M4 class lock.** A class holds the lock only while active: the instructor console refreshes it, 20 idle minutes release it, an ended class never holds it. Solo players see a note before they answer. Reopening a decision takes it out of the released set.
- **M5 contested and exploratory results.** bz06 and social13 became items about the strength of the evidence; axf06 became a forecast about the measured physician result; axe03 retired (routings rested on author suggestions); axe02 keeps only measured routings; axe08's forecast now claims the opposite of the suggestive result (false).
- **M6 phone rank chart.** HTML bars with "#average rank" labels, matching the projector.
- **M7 explanations.** 44 explanations rewritten from the versions of record with their key numbers (30 with effect sizes or samples; 13 abstract-only where full texts were unreadable, listed in the gate's allow-list). social03 retired as a duplicate of social01. Gate: a number in every explanation outside the allow-list, and no generic phrasing.
- **Minors.** axf04 task order no longer alternates; pick-two items have four options with no logical negations; record strip shows only measures where higher is better plus the calibration gap; plain forecast caption; quiet "Slide to answer" prompts and faint untouched thumbs; projector view on the console; Streamlit tutor hides findings until asked, forecasts need an entered probability, rank start order matches the phones (parity-tested); CSV guard covers tab and carriage return; HEAD supported; docs state that the offline file carries answers and how to confirm Gemini model ids.

**Gates:** build check, 194 tests, audit doc and counts regenerated.

**Count:** 0 Blocking + 7 Major found and addressed. Next: independent review 5.

## Iteration 10 (2026-10-31)

**Verified first:** iteration-9 fixes, by independent review 5 (snapshot `snap_r5`): no answers in served pages or APIs, class lock on every route, phone and projector rank charts agree, idle lock release, proper allocate rule, midpoint cap, numbers in explanations. Not held: two path leaks, social01's options, axe02's routings, projector layout.

**Independent score:** 78/100 (review 5, `qa/reviews/review5.md`). 0 Blocking, 7 Major.

**Fixes:**
- **M1.** rollout1's follow-up and rollout3's delegate reasons rewritten; the path-leak gate now scans answer titles, chart notes and delegate reasons of earlier items too.
- **M2.** Delegate tasks can list equally supported routes (`also`), scored in JS and Python, shown on reveal, console and Streamlit; axe01's hedonic task accepts the hybrid and the human recommender.
- **M3.** axe02 retired (routings not compared).
- **M4.** The class lock follows instructor activity only (`beat`, refreshed by control and the open console; 5 idle minutes release it); student joins no longer revive it. Test added.
- **M5.** Allocate sliders rebalance automatically so the total stays fixed; only a real change unlocks; a hint says how it works. Browser test added.
- **M6.** Four forecast claims stated neutrally; axf06 became an estimate (median 76%, axis 40–100). Gate: no strong qualifiers in claims.
- **M7.** Before the reveal, causal diagrams show dotted, undirected links with a one-line explanation; arrows appear at the reveal. Test: no arrowheads before the reveal.
- **Minors.** social01 has four options with no negation pair, bz15 became a rank with a tie, gate requires four options in pick-two items; three distractors replaced; social13 asks how the authors described their own estimates; auditor-voice follow-ups and thin scope lines rewritten; axf04 reduced to its two distinct tasks; Isoni, Loomes & Sugden (2011) added as a source; dimant-notalie scene describes the experiment; allocate ties at the top no longer count as a hit; offline and server tutors decline off-topic questions and give a practical reading of effect size; projector view in two columns with the class chart beside the question; console notes pairs a study did not separate; diagrams fit their boxes; record calibration card no longer stretches; hero unit hidden until a call; record headings in order; README file map and `qa/QUALITY_ASSESSMENT.md` added.

**Gates:** build check, 198 tests, audit doc, counts and reference screenshots regenerated.

**Count:** 0 Blocking + 7 Major found and addressed. Next: independent review 6.

## Iteration 11 (2026-10-31)

**Verified first:** iteration-10 fixes, by independent review 6 (snapshot `snap_r6`): student joins cannot keep the lock alive, allocate rebalancing and real-change rule, no arrowheads before the reveal, ties unscored, no answers served, tutor declines off-topic and injection. Partly held: negation gate (dimant-contagion-multi). Not held: projector polish, Streamlit double navigation.

**Independent score:** 79/100 (review 6, `qa/reviews/review6.md`). 0 Blocking, 7 Major.

**Fixes:**
- **M1.** dimant-requiem-forecast states the paper's own measure: misreporting around 30 percentage points above the 16.67% honest rate.
- **M2.** Verification records now match what was read: 15 sources read in the published article are recorded as such; four read in authors' accepted manuscripts carry a new status, `verified_accepted_manuscript`, shown to players; quotes from news releases, project pages, annotated copies and working papers were removed, and the content that rested on them was rewritten (civic-wallet-rank, misperceived-norms items, biz07, biz08, social10).
- **M3.** Estimate credit now reaches zero at twice the band; tolerances are about a fifth of each target (with stated exceptions). Gate: the best constant guess across all estimates averages at most 0.35 (was 0.44).
- **M4.** Scenes no longer state the mechanism (social04, dimant-conspiracy-choice, social07, axb10); strawman and negation distractors replaced with rival mechanisms (dimant-notalie-causal, ai12, biz02, ai07, dimant-contagion-multi).
- **M5.** Allocate supports arms the study did not separate (`allocate.best`); axe04 treats the original and GPT-3 as tied best; splitting evenly across tied best arms counts as a hit.
- **M6.** On a deployment set up for classes (passcode configured), the Streamlit Play page points to Join a class unless `THV_STREAMLIT_SOLO=1`; documented.
- **M7.** Console null-scroll bug fixed; the class test fails on any error toast.
- **Minors.** ai04 explanation states the 15%; bz10 scene wording; axe11 no longer ties a significant pair; tutor says a study opens after the reveal during a lock; projector lists delegate routing choices; live-class phones show the class code instead of "1 of 1"; calibration plot margins; delegate buttons name their task for screen readers.
- **Visual.** Tighter home rhythm, path colour now encodes AI-first paths (blue) versus behavior and business (ink), larger theme drawings, and the Dimant band states 17 decisions from 14 published papers with a sticky heading.

**Gates:** build check, 200 tests, audit doc and counts regenerated.

**Count:** 0 Blocking + 7 Major found and addressed. Next: independent review 7.

## Iteration 12 (2026-10-31)

**Verified first:** iteration-11 fixes, by independent review 7 (snapshot `snap_r7`): no arrowheads before reveal, ties unscored, midpoint cap, lock follows the instructor, tutor locked and off-topic handling, no console toast, Streamlit Play gated, allocate rebalancing, served takeaways and principles gated. Not held: allocate structured fields leaked; strawman distractors; Streamlit double navigation; scope gate too weak.

**Independent score:** 79/100 (review 7, `qa/reviews/review7.md`). 0 Blocking, 5 Major.

**Fixes:**
- **M1.** The public allocate block is an allow-list (total, step, label, prefix, suffix). The leak test now fails on any answer-bearing key (best, valueName, also, why, rankTies, rankValues, chart, follow and more) anywhere in the served bank.
- **M2.** axf01 asks which of the three machine interfaces kept people most honest (self-reporting moved to the scene); axe04 became an estimate. Gate: an even split scores at most 0.6 on every allocate item.
- **M3.** Two fresh agents rebuilt the evidence for 40 decisions with verbatim quotes and page or section from published texts (accepted manuscripts labelled). One wrong number fixed (lies-in-disguise: about 20% full liars, not 22%); numbers without a published source removed or rewritten (bz01's 73%/222%/316% appear only in a 2018 authors' copy; accuracy-prompt's 4.8% and 2.1% are behind the paywall; bz10, meta-perception, civic-wallet-experts, dimant-masks, opposing-views-bot sign, bz12). Gate: no paraphrased or summarized evidence entries.
- **M4.** The measurement path now includes randomized trials that confirmed their claims (bz05, bz07), with a neutral blurb.
- **M5.** Neutral scenes (biz07, bz06), rival distractors (misperceived-norms-action, biz02, social07, social13), social20 rewritten as a measurement choice with rival methods; ai04 retired as a repeat of rollout1; ai11 has two options and a neutral title.
- **Minors.** axb01 count; internal study notes removed; sibling leak gate across decisions that share a paper, with fixes; forecasting principle grounded; 23 scope lines rewritten and the scope gate widened; tutor finds studies by author; allocate reveal shows player bars with a "Worked best" tag; chart legend wording; lock button label; Streamlit passcode warning and constant-time check.
- **Visual.** Dark research band; reveal titles balanced to fewer lines.

**Gates:** build check, full suite, audit doc and counts regenerated.

**Count:** 0 Blocking + 5 Major found and addressed. Next: independent review 8.

**Needs the owner:** bz01's original figures (73% randomized lift, 222% to 316% observational) can return once checked against the published Marketing Science PDF, which requires library access.

## Iteration 13 (2026-10-31)

**Verified first:** iteration-12 fixes, by independent review 8 (snapshot `snap_r8`): no answer fields served on any route while open or closed, allocate rule and even-split cap, lock follows the instructor (60 students alone released it). Partly held: verbatim evidence (six entries the gate's wording missed) and the measurement path.

**Independent score:** 78/100 (review 8, `qa/reviews/review8.md`). 0 Blocking, 4 Major.

**Fixes:**
- **M1.** Forecast calibration is folded to the side the player leaned to (10% on a false claim is a 90% call that was right; 50% is excluded). Test added.
- **M2.** Estimate axes for effect sizes were re-ranged within plausible bounds so targets spread along their axes, and bands on high shares tightened (`tools/estimate_axes_2026_10_31.py`). Gate: no fixed slider position averages more than 0.35 (was 0.45); the constant-value gate still holds (0.33).
- **M3.** The measurement path interleaves tests where the intervention worked (bz09, accuracy-prompt, bz05, bz07).
- **M4.** Nodes that name the asked-about mechanism stay masked until the reveal (dimant-notalie, axe12, meta-perception). Gate: no visible node label repeats the correct option's key words; the served-page leak test checks masked labels exactly.
- **Minors.** Remaining non-verbatim evidence relabelled or removed and the gate widened (condensed, summarized, transcribed, fetch tool); biz06 retired as a repeat of biz05; civic-wallet-experts no longer states the rank item's order; social15's action no longer states dimant-hate-choice's answer; axb08 is a second allocation item with one separated arm; join burst covers 120 students per network with client retries; offline tutor matches authors with accents and handles transfer questions; axe11 scores only the tested pairs; the mask item says intentions and pledges; forecasting principle states the open debate; limiter buckets pruned; biz02 distractor; compact path list on phones.

**Gates:** build check, 205 tests, audit doc and counts regenerated.

**Count:** 0 Blocking + 4 Major found and addressed. Next: independent review 9.

## Iteration 14 (2026-10-31)

**Verified first:** iteration-13 fixes, by independent review 9 (snapshot `snap_r9`): folded forecast calibration, midpoint and fixed-position gates, ties unscored, lock follows the instructor, 120 joins from one IP, no arrowheads before reveal, allocate rebalancing, tutor locked and off-topic handling; no answer text on any route at open or closed stages.

**Independent score:** 79/100 (review 9, `qa/reviews/review9.md`). 0 Blocking, 3 Major.

**Fixes:**
- **M1.** Every number in an explanation or answer title now appears in a quote for that decision (`tools/evidence_numbers_2026_10_31.py`; table and figure values read from published texts are their own entries, marked as printed). judg09 and axb15 have quotes; axb15's sample is the 2,044 believers in the version-of-record abstract (was 2,190 from another passage). Four explanations trimmed to quoted numbers (social15, axb14, bz04, dimant-motivated). Duplicates and retired ids removed from the evidence file; ai10's source recorded as read in full. Gates: every live decision has evidence; every explained number is quoted (allowing rounding, percent versus share, number words).
- **M2.** The record's headline and area bars show skill above guessing: each score is rescaled so a no-information strategy for that format (50% forecast, random order, even split, random pick) is 0 and a perfect call 100. Per-decision scores keep their proper rules. Test: hedges and even splits have zero skill.
- **M3.** Masked diagram nodes are served with neutral ids (n0, n1...), and the unshown `concept` field is no longer served.
- **Minors.** Tutor picks the sibling that matches the question's topic; social20's keyed option is the paper's belief-elicitation method and both long questions shortened; axe12 rewritten without the "Correct:" cue or a manager's conclusion; social01 option shortened; biz07 strawman replaced; length-cue gate covers causal items; solo play during a lock offers "Next decision"; projector exit button moved; allocate legend; record grid.
- **Visual.** On wide screens the reveal reads in two columns, the finding beside the evidence figure, which stays in view.

**Gates:** build check, 207 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 3 Major found and addressed. Next: independent review 10.

## Iteration 15 (2026-10-31)

**Verified first:** iteration-14 fixes, by independent review 10 (snapshot `snap_r10`): quoted-numbers gate, skill headline, neutral diagram ids, two-column reveal.

**Independent score:** 82/100 (review 10, `qa/reviews/review10.md`). 0 Blocking, 2 Major.

**Fixes:**
- **M1.** The skill headline pools first and rescales once (mean raw score against mean baseline), so one confident forecast miss no longer erases a round of right calls. Recent calls are labelled as decision scores before the chance adjustment.
- **M2.** The tutor request carries the client id in a header and the per-client limit keys on it, so a class behind one network address is not throttled. Test: 30 tutor requests from one address all answered.
- **Minors.** dimant-enforcers is a forecast on the contrast the paper tests (norm information raised reporting of inequity-creating bribes), not a rank with untested cross-cell pairs; axe01 offers only the two routes the studies compared; bz01 quotes come only from the version of record; opioid26 lists Dimant among its authors and the Dimant count reads full author lists (18 decisions, 15 papers); null and absolute distractors replaced with rival claims in bz12, bz14, biz03, biz05; the tutor stays on the decision on screen unless the question names another study, answers design questions from the study record, maps junior and senior to experience, and no longer reads "experiment" as a pilot question; projector bars scale to the room size or 100% and show "2 of 3"; the projector exit sits beside the QR code; estimate and forecast reveals open with your number against the study's, large, and the gap between them; record reads in two columns (calibration beside recent calls and areas) and has an empty state; unknown `?play=` links say so; provenance links to third-party re-hosts and working-paper PDFs removed (5 sources) with a gate; social13, ai12, meta-perception copy.

**Gates:** build check, 209 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 2 Major found and addressed. Next: independent review 11.

## Iteration 16 (2026-10-31)

**Verified first:** iteration-15 fixes, by independent review 11 (snapshot `snap_r11`): pooled skill headline, tutor header, enforcers forecast, axe01 routes, projector delegate and allocate scaling, record layout and empty state, unknown play link, numeric reveal head. Not held: choice and multi projector bars; offline tutor misrouting.

**Independent score:** 81/100 (review 11, `qa/reviews/review11.md`). 0 Blocking, 4 Major.

**Fixes:**
- **M1.** dimant-contagion-multi cites only the 2019 contagion paper; its action now says close peers copy more and bad conduct most. Both Dimant items carry a follow-up that reconciles the 2019 and 2022 designs (closeness to the observed peer versus a shared-identity cue that made good examples spread too). Rule recorded in the content guide.
- **M2.** axb14 says 33.9% with GPT-4 and a prompt-engineering overview, 29.9% with GPT-4 alone, quoting the full sentence. The quoted-numbers gate now covers follow-up answers (14 numbers fixed: six quotes added from the papers, six follow-ups rewritten, names excluded), and a new gate fails quotes that stop mid-sentence.
- **M3.** The home card no longer states ai02's answer; a gate fails any page code that hard-codes a decision's result. A source's takeaway travels only when every decision on that source is open (class) or played (solo dialog). Test: revealing one sibling does not release the paper's takeaway.
- **M4.** Offline tutor (server and page): light stemming and number tokens, follow-ups need two shared words, ethics and "should we" questions get scope and action, siblings on the same paper are fair answers, a named author whose decisions are all locked returns "locked". Regression tests for the reviewer's questions.
- **Minors.** Library principles and findings open only after a call on that theme; forecasts with true-resolving predictions and a famous result that held (axb13, opioid, axe10, bz08); causal diagrams show only the factors before the call and draw the links one by one at the reveal; distractors in biz05, genai1, judg02, social13; choice, multi and histogram projector bars scale to the room; an open or closed-unrevealed question stays held even if the console goes quiet (test); share bars on a 0 to 100 scale; provenance labels (plural24 rechecked verbatim, OpenAlex abstracts, one more re-host link); padding quote removed; study line reads as sentences; Streamlit navigation moved to the sidebar so the game's own header is the only top bar; ids kept as permanent keys (content guide).
- **Visual.** On wide screens the questions, scope and tutor sit under the finding, beside the sticky evidence figure, so the reveal has no dead column.

**Gates:** build check, 218 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 4 Major found and addressed. Next: independent review 12.

## Iteration 17 (2026-10-31)

**Verified first:** iteration-16 fixes, by independent review 12 (snapshot `snap_r12`): M1 to M3 held; M4 mostly held (two imprecise tutor answers).

**Independent score:** 84/100 (review 12, `qa/reviews/review12.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** biz03 retired: it keyed the original towel-sign effect with an unconditional action, while biz04 (same source) teaches the failed German replication. Contested findings enter only as items about the contest.
- **Minors.** Absolute and null distractors replaced with rival claims in 11 items, with a gate (at most 3 left across choice and causal items); every call with stated confidence now shows a confidence score on the forecast rule, explained in "How scoring works"; sibling spoilers removed (civic-wallet-experts, misperceived-norms-support); allocate options shuffle with the seed (phones and console agree), steps allow a true even split, remainders follow the display order; axe11 is a pick-two over the two tested contrasts (both significant per the paper's quotes); duplicate and mirror distractors removed (bz14, dimant-contagion-multi); social20's keyed option names the spread of views; eight scenes rewritten to the real designs; two estimate targets moved to 0.40 to 0.41 of their axes (the per-item midpoint gate keeps targets 1.5 tolerances off centre); record puts areas under calibration, shows area skill after 3 calls and gives the headline its call count; evidence entries all name a source of their decision, processing notes removed, gate added; a failed class join shows a message that stays; Streamlit student page lists the causal factors before the call and the links after; tutor answers subgroup questions from the item's who-gained follow-up, and a clear follow-up match beats generic routes.

**Gates:** build check, 219 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 13.

## Iteration 18 (2026-10-31)

**Verified first:** iteration-17 fixes, by independent review 13 (snapshot `snap_r13`): biz03 retired, absolute-word gate, confidence score, allocate order and even split, axe11 pick-two, scenes, evidence hygiene, join message. Not held: two sibling spoilers in civic-wallet-experts.

**Independent score:** 83/100 (review 13, `qa/reviews/review13.md`). 0 Blocking, 3 Major.

**Fixes:**
- **M1.** Paper titles are private fields, served with the evidence and gated like takeaways (during a class, only once every decision on the paper is open). The page shows a title once every decision built on the paper has been played; until then the source dialog shows authors and year and the home Dimant list shows a decision's title. The served-page leak test now probes titles.
- **M2.** Method and replication words never pick another study: they answer from the decision on screen (design and sample, scope), and with no decision the tutor asks which study is meant. Subgroup questions use only follow-ups about who gained. Regression tests added.
- **M3.** A class poll that returns an error (429 or other) keeps the phone's card and pending answer; only real state updates the screen.
- **Minors.** Sibling spoilers removed (civic-wallet-experts question, claim, title and follow-up; social15 action; forecast-training and rollout1 follow-ups); prediction forecasts now resolve both ways (civic-wallet-experts and axf02 true); invented expectations removed from four scenes; axb05 scene no longer states the cost proxy; social13's keyed option is no longer the only hedged one; axf04 asks which messenger drew the better response; projector rank reveal shows the measured order as large numbered badges with the room's average beside each, "1 answer" grammar, causal factors on the open stage, exit button at full contrast; plain-language explanations for the two forecasting-tournament items; one score per decision, with the confidence result on its own line; Streamlit tutor holds open questions; deployment note on Streamlit without a passcode; location strings and quotes from a non-source replication paper removed from evidence (gate extended), and its unsourced follow-up replaced.

**Gates:** build check, 221 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 3 Major found and addressed. Next: independent review 14.

## Iteration 19 (2026-10-31)

**Verified first:** iteration-18 fixes, by independent review 14 (snapshot `snap_r14`): titles gated on both builds, poll errors survived, rank projector, class lock routes. Not held: tutor routing (M1) and evidence annotations.

**Independent score:** 85/100 (review 14, `qa/reviews/review14.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** One routing table (`tutorRoutes` in `src/bank.json`, written by `tools/tutor_routes_2026_10_31.py`) drives both the server tutor and the page's offline tutor, in the same order: the item's own follow-up (exact, then near), a named study by author surname, ethics, subgroup, design, pilot, size and transfer routes, a two-word follow-up match, then the decision on screen. Generic words ("answer", "result", "numbers", "matter") never pick another study; another study answers only when named or when the question shares nothing with the decision on screen and strongly matches the other. Tests: every live decision answers ten generic questions with its own source and all 335 own follow-ups exactly (server), and the same on the page through Playwright.
- **Minors.** Evidence split into verbatim prose quotes (`quote`) and values read from tables or figures (`printed`); 16 annotations removed; gate extended. Sample lines no longer say "not stated"; the observability scene includes taking from the charity; axe12's diagram drops the visible work-quality node, dimant-notalie's distractor names a candidate for the masked node, bz01 is a plain choice; dimant-conspiracy scene and two weak distractors rewritten; four forecasts reworded to resolve false so each path mixes true and false claims; confidence line reads "Confidence score N (from −100 to 100). You were X% sure and missed"; the forecast head shows the distance from the truth instead of repeating the score; the action bar shows the average score; the projector shows the live answer count large before the reveal; the console retries throttled requests; phone reveal tabs scroll sideways; punctuation.

**Gates:** build check, 224 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 15.

## Iteration 20 (2026-10-31)

**Verified first:** iteration-19 fixes, by independent review 15 (snapshot `snap_r15`): shared routing table, evidence split, causal and forecast fixes, projector count, console retry, phone tabs. Not held: the tutor answered its test list but declined or misrouted ordinary phrasings; some annotations survived as printed values.

**Independent score:** 86/100 (review 15, `qa/reviews/review15.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** With a decision on screen the tutor answers about it unless the question names another study by a whole author surname; it never switches study on word overlap and declines only clear off-topic requests (poems, jokes, weather and the like). New routes in the shared table: who was studied, catch or backfire, summary or explain simply, how long it lasted, which AI models. Thirty natural phrasings, including the reviewer's, are tested on every decision, server and page.
- **Minors.** Printed values must name a table or figure; annotations replaced by verbatim sentences or table cells found in the papers (eight decisions; norms24's n = 1,203 from the published article); lees20 recorded as checked on the version-of-record abstract and figure legend, DASH quotes removed; quarantined judg02 evidence cleaned; axb03, axb14 and axe06 axes widened, with a gate that a random slider guess earns at most 0.3; social13 rival option; sibling spoilers in axb14 and rollout2 follow-ups; biz05 action adds a pilot check for low users; axe14 action recommends disclosure at the start of the call; the confidence line says a 50% hedge scores 50; the questioned link in causal reveals is drawn thick in amber; diagram labels larger on phones; open-question hold window follows instructor activity.
- **Deeper visual pass.** 22 more decisions show the paper's own numbers as an evidence figure ("What the study measured"), every value checked against that decision's evidence (gate extended to chart values); the figure is the reveal's centrepiece, with larger bars and the evidence in amber, and appears under forecast, estimate, delegate and allocate views where the paper reports comparable numbers; path grid is one featured card plus paper cards with a blue or amber marker; delegate reveal opens with "tasks routed as the evidence suggests"; record headline has a call-by-call history line; Library principles show how many of their decisions the player has opened; causal diagrams sit on a faint lab grid; projector is a dark stage around white cards.

**Gates:** build check, 229 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 16.

## Iteration 21 (2026-10-31)

**Verified first:** iteration-20 fixes, by independent review 16 (snapshot `snap_r16`): tutor grounding (216 of 216 own-source answers), evidence figures, class leak probes, lock, load, Streamlit. New regression found: estimate prompt on the served page.

**Independent score:** 83/100 (review 16, `qa/reviews/review16.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** The public bank serves the estimate tolerance (it defines a hit and says nothing about the target); the Streamlit student prompt names the band. Tests: the served bank carries a tolerance for every estimate, and a browser test on the served page finds no "undefined", "null" or "NaN" in any format's play screen.
- **Minors.** Three forecasts reworded so claim wording no longer predicts truth, with a gate (a wording-only rule cannot beat 0.55); axe10 title; dimant-hate-choice "dropped by a similar amount"; tutor declines a wider set of off-topic requests, answers "what should I do" with the action, matches follow-ups whose words all appear in the question (fix ~ fixed), and uses only who-gained follow-ups for subgroup questions; biz07, biz08 and overconfidence-hard-task scenes describe the real tasks; axe12 scene no longer restates the answer and the keyed option names the mechanism; genai3 follow-up no longer states axe12's answer; ai09 says how its design differs from algorithm-appreciation studies; axb02 and bz15 are plain calls instead of ranks that scored one or two pairs; bz09 action adds a consumer-protection caveat; verdict says "Close" from a score of 50; class lock idle window 20 minutes; verdict set as a statement; projector stat labels do not wrap.

**Gates:** build check, 232 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 17.

## Iteration 22 (2026-10-31)

**Verified first:** iteration-21 fixes, by independent review 17 (snapshot `snap_r17`): served estimate prompt, wording gate, scenes, tutor routes, lock window, leak probes, load, Streamlit. Not held: the per-path truth balance on the trust-algo path.

**Independent score:** 86/100 (review 17, `qa/reviews/review17.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** dimant-enforcers-rank now says what Dimant and Gesche (2023) did: participants learned that most previous participants objected to taking bribes, and chose how much evidence to submit, which set the probability that the coworker is punished. Scene, claim, title, explanation, action and figure note rewritten; the two defining sentences quoted from the full text.
- **Minors.** Title punctuation on the phone wait screen; repeated study lines removed; tutor answers subgroup questions it cannot answer with "the lab's summary does not break results down that way", and duration questions with design and sample; the estimate baseline in "skill above guessing" is a random slider position (copy updated); ai10's claim resolves false so every path mixes true and false forecasts, with a gate; numbers in scenes and scope lines are quoted (six quotes added from the papers, two scenes reworded, one invented scenario removed from rollout1) and the number gate covers scenes and scope lines; sparkline label, diagram margin; projector allocate caption reads "(baseline)" and "not significant"; social13 rivals; dimant-proximity action says even a minimal shared-identity cue helped.

**Gates:** build check, 233 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 18.

## Iteration 23 (2026-10-31)

**Verified first:** iteration-22 fixes, by independent review 18 (snapshot `snap_r18`): enforcers item (fact-checked correct against the full text), quoted scene numbers, estimate baseline, path balance, leak probes, lock, load, Streamlit.

**Independent score:** 86/100 (review 18, `qa/reviews/review18.md`). 0 Blocking, 1 Major.

**Also applied this iteration:** an in-house design-fidelity audit (`docs/audit/design_fidelity_2026_10_31.json`) corrected how 14 items describe their study's manipulation, measure or population (misperceived-norms-action, dimant-observability-choice, social07, social01, social15, dimant-notalie-causal, dimant-contagion-multi, biz05, social13, biz11, ai11, ai12, accuracy-prompt).

**Fixes:**
- **M1.** bz16 is now an item about the contest: Benartzi and Thaler's menu effect set against Huberman and Jiang's (2006) real-plan records (new source, three verbatim abstract quotes), as a forecast that resolves false, with follow-ups on how the designs differ.
- **Minors.** rollout1 asks which agents gained most, with plausible rivals; neutral titles for bz04, rollout4, judg09; rank items added to the Trust, Measure and People paths; three claims reworded and the wording gate now also covers positive verbs; volume rendered only when present; plain negative numbers in the CSV are not prefixed; reveal tab "Scope"; Streamlit class reveal labels bins by value, handles no answers and shows each student's own score; open decisions hold their same-paper siblings (test); "Calibration points" on the verdict line; stale editorial rule removed; Library counts decisions.
- **Visual.** Allocate reveal shows the player's points and the study's measured result per option, with non-significant effects drawn striped.

**Gates:** build check, 234 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 19.

## Iteration 24 (2026-10-31)

**Verified first:** iteration-23 fixes, by independent review 19 (snapshot `snap_r19`): bz16 contest item, fidelity pass ("study designs, populations and nulls are described accurately"), allocate evidence bars, sibling hold, CSV, Streamlit.

**Independent score:** 87/100 (review 19, `qa/reviews/review19.md`). 0 Blocking, 1 Major.

**Fixes:**
- **M1.** biz04 uses the full-sample comparison (93.3% vs 76.5%) in quote, explanation and figure, rechecked against the journal HTML.
- **Minors.** "Choice architecture" principle says menu effects are contested in real plans; axb08 drops the human-human baseline as an option (it is the comparison point, stated in the scene); bz02 asks "more than how many points"; the server accepts estimates only on the slider's grid (no exception for the target, so validation is not an oracle); projector labels per format ("Most points on the best option", "Routed every task as the evidence suggests", "Exact order"); tutor routes for stakes and population.

**Gates:** build check, 234 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 1 Major found and addressed. Next: independent review 20.

## Iteration 25 (2026-10-31)

**Verified first:** iteration-24 fixes, by independent review 20 (snapshot `snap_r20`): biz04 full-sample pairing, principle wording, axb08 options, estimate grid validation, projector labels, tutor stakes and population routes. Also in that snapshot: 64 Dimant quotes verified against published texts or preprints (`docs/audit/dimant_verification_2026_10_31.json`).

**Independent score:** 87/100 (review 20, `qa/reviews/review20.md`). 0 Blocking, 0 Major, 11 Minor.

**Fixes (all 11 minors):**
- Estimate skill baseline is the best fixed slider position across the bank (`GUESS_FRAC = 0.30`), with a gate that keeps it current.
- axf06 tolerance 1 (control 74 lies outside 76 ± 1); axb03 and axb14 axes 0 to 40 with tolerance 3, all estimate gates holding.
- Allocate counts as a call only with the top weight on a best option and at least half the points there (JS and Python).
- Tutor: after the routes, a distinctive word the question shares with one follow-up question, or found only in a follow-up answer, picks that follow-up; words common to three or more decisions' follow-ups do not count (`tutorRoutes.common`); "does the X work" goes to the summary; believing or trusting a lab study goes to transfer, not ethics. Server and page agree (test).
- Streamlit tutor holds same-paper siblings of an open decision (test).
- bates17 quote stored (verified against the published article PDF); biz04 explanation drops N = 204; opposing-views-bot implication stays with what was tested; bz11 claim at the level of the finding.
- Projector delegate shows the evidence route under each task; the stat row is a fixed four-column grid.
- "Start playing" opens the featured path; rank hint says where first place goes; a rank card that starts on the answer is reshuffled; the sparkline label sits away from the data; the All-decisions list shows forecast claims; a phone refreshes the room count right after its answer lands.

**Gates:** build check, 240 tests, audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 0 Major. Next: independent review 21.

## Iteration 26 (2026-10-31)

**Verified first:** iteration-25 fixes, by independent review 21 (snapshot `snap_r21`): estimate baseline (fixed position 0.319 against GUESS_FRAC), axes, allocate verdict, tutor distinctive words, Streamlit sibling hold, projector delegate, rank start order (no leak on the served page).

**Independent score:** 87/100 (review 21, `qa/reviews/review21.md`). 0 Blocking, 0 Major, 14 Minor.

**Owner's instruction this iteration:** remove every AI design marker from every page, gather 25 rules for interfaces that do not read as AI-made, add the chart guidance he sent (headline titles, annotate in place, source inside the figure), ask on every page "what would Tufte do?", and put all of it into the loop.
- `qa/DESIGN_RULES.md`: 30 rules (25 on AI giveaways and usability from five published catalogues, 5 on figures). `tools/design_lint.js` and `tools/design_lint.py` detect 27 of them in a real browser on every page state at 1440 and 390 px, including the console, projector and a phone; `tests/test_design.py` fails on any hit, and a live-fire test injects one tell per detector. Baseline: 50 distinct hits across 15 rules; now 0.
- Fixes, all pages: no blur, no glow or coloured shadows, no side stripes or hatching, no decorative dots, labels folded into headings ("Best call: …", the hero's demo without "Try one now"), the verdict as a sentence under the headline instead of a pill above it, tracking no tighter than −0.03 em, balanced headings and orphan-free paragraphs, a three-line hero headline, a radius scale of 4, 10 and 14 px, paths as an index instead of a grid of identical cards, flattened option recaps and projector lists, 12 px minimum text, 40 em measure.
- `qa/TUFTE_PASS.md`: the page-by-page answers. Path drawings replaced by a word-sized strip (one tick per decision, filled once played); the reveal's theme drawing removed; legends replaced by labels on the marks; each chart titled by its measure with its source inside the figure; one amber bar per chart; calibration plot without box and grid, its diagonal and dots labelled in place; the record's number carries its unit.
- `qa/REVIEW_PROMPT.md` asks every reviewer to run the lint, read the rules by eye and ask the Tufte question on every page.

**Review-21 fixes (all 14):** rank header contrast on the dark plate, plus axe on every format's reveal at both widths; tutor routes for skill level, countries, foresight and a delegate task's reason, and an honest "the lab's summary does not cover that detail" fallback (server and page agree); the polarized-norms item keyed on the printed variance (2.68 against 1.26), with the abstract's "most" attributed to the authors, after reading the published text (the 46% share concerns contributing more than two); subtract21 status "checked against the publisher's abstract and figure legends"; ai01's follow-up replaced by one the stored quotes answer (and not ai02's key number); delegate baseline is the best constant routing; allocate calibration scores "top-weighted option is a best one"; the reveal says how sure you were and whether you were right, calibration lives in the record; bz02 is a forecast (its answer is a threshold), axb04 0 to 60, axe04 0 to 60, GUESS_FRAC 0.36; instructor controls have their own bucket (test); Streamlit pauses solo play while any class holds an unrevealed decision and the no-passcode warning says what it exposes; record number with unit; phone readout on its own row; titles "Four honesty messages" and "Tight, loose or split".

**Own audit:** no number in an estimate's scene inside its band (gate; judg05 tolerance 5).

**Gates:** build check, 251 tests (including `tests/test_design.py`: 0 design-lint hits on every page state, detectors live-fired), audit doc, counts and screenshots regenerated.

**Count:** 0 Blocking + 0 Major. Next: independent review 22, which now runs the design lint and the Tufte question on every page.

## Iteration 27 (2026-10-31)

**Verified first:** iteration-26 fixes, by independent review 22 (snapshot `snap_r22`), the first review to run the design lint and ask the Tufte question on every page.

**Independent score:** 86/100 (review 22, `qa/reviews/review22.md`). 0 Blocking, 2 Major, 15 Minor.

**Fixes:**
- **M1.** The path styles were twelve layers of overrides; they are now one block (featured path as the dark surface, the rest an index; one column below 640 px). The start flag moved into the count line ("Start here. 11 decisions, with a multi-step case"). The phone home screenshot is now full page. New detectors: squeezed text (a long string in a column under 150 px), patterned backgrounds, and labels above any headline-styled title, not only h1 to h3; all three live-fired.
- **M2.** axf06 is a forecast ("Physicians with GPT-4 scored significantly higher than physicians without it", false), with a chart of 74, 76 and GPT-4 alone at 92, its note stating P = .60. New gate: no estimate's finding may be a non-significant contrast. bz07 tolerance 6 keeps the constant-guess cap.
- **Minors.** Plain surface behind causal diagrams; the Library is an index with rules between principles, no drawings, progress as the same word-sized strip; rank reveal with column heads "Study" and "You" over the numbers and rows as rules; currency before the number; biz05 in kWh per day; the enforcers chart outlines the marginal equity contrast and says P = 0.074; outlined bars for non-significant values in any chart; in-bar labels keep a backing so they stay legible; format and area moved into the study line on predict, and the console states its phase as a sentence; page titles without middle dots; dimant-hate-choice reads "Expectations, more than unwillingness, drove the gap"; tutor routes for bot (AI), auditing your own model (pilot), definitions, contests (both sides), and why-questions, with one-word follow-ups no longer matched on a single shared word (server and page agree, tests); the scoring explainer says confidence does not change a score; eight claims reworded so claim length no longer predicts truth (39% vs 56% true), with a gate; the notalie scene states the manipulation and the projection rival replaces the strawman; the allocate reveal follows the order played; a negative record reads "below guessing"; judg09 scope states only what the study covers.
- **Optional taken.** The projector's revealed view leads with the finding.

**Gates:** build check, 258 tests (design lint 0 hits on every page state including console, projector and phone; new detectors live-fired), audit doc, counts and screenshots (phone home now full page) regenerated.

**Count:** 2 Major found and fixed. Next: independent review 23.

## Iteration 28 (2026-10-31)

**Verified first:** iteration-27 fixes, by independent review 23 (snapshot `snap_r23`).

**Independent score:** 84/100 (review 23, `qa/reviews/review23.md`). 0 Blocking, 2 Major, 17 Minor.

**Owner's instruction:** stop introducing new Majors while fixing old ones. Diagnosis: three of the four Majors in reviews 22 and 23 were regressions of earlier fixes (stacked CSS overrides, a tolerance narrowed without checking what it scored, a baseline changed on one reviewer's advice that the next reviewer's finding contradicted). Response: `qa/INVARIANTS.md`, a regression register (10 invariants, each with its test), a settled-decisions list, and a change protocol. Every fix names the invariants it touches; the complete gates run (the design lint now covers every decision); a fresh agent audits the diff since the last reviewed snapshot against the register before any external review; every new Major becomes an invariant with a test. A CSS ratchet stops override blocks from growing.

**Fixes (invariants touched in brackets):**
- **M1** [I5]. Estimate skill baseline is one format constant (0.35), the best bank-wide average of any blind strategy (constant value 0.348, fixed position 0.302, random 0.176), so every correct estimate earns full credit and no blind strategy earns skill; gates for baseline currency and for no item baseline at 0.9 or above.
- **M2** [I2]. Evidence figures added from numbers the explanations already quote: ai07, social07, social15, social16, opposing-views-bot, dimant-observability-choice; forecast reveals show the paper's figure under the claim.
- **Minors** [I2, I6, I7, I8, I9]. Projector delegate route in ink at body size; design lint over every decision; allocate figure titled by its measure, effects on their own axis with a zero line; calibration label placed away from the dots; SVG text 12 px or more (and a detector for SVG text at its rendered size); blue end dot for the player, ink verdict; rank badges without the unexplained ring; axb05 chart titled by its measure, the simulation labelled as one; console lessons flattened; tutor routes for why-not, significance, a team's next step, the task, a term's meaning, and detection (bot); a contest item that held up (Many Labs 1, anchoring, from the published article) and neutral contest titles; keyed options balanced across stored positions; scoring explainer and CSV note on allocate's range; dimant-proximity baseline wording; axe13 "not significant"; a social15 follow-up on which games these were; headline-style titles for social15, social07, social01; "up to five" in ai07; one forecast prompt; true minus signs; Library filter pills removed; notalie node inside the frame; Streamlit claim without a side stripe; a class-ended dialog; the study line under the question.

**Gates:** build check, 267 tests (design lint over every decision at 1440, one per format at 390, console, projector and phone: 0 hits), audit doc and counts regenerated.

**Regression audit 28 (protocol step 3):** a fresh agent attacked the diff against the register. It found 1 Blocking (dimant-notalie-causal showed a duplicate option and lost its confounder distractor: an index-based edit in the content script ran after the option order was balanced) and 1 Major (the observability chart drew a +9.3% gain as a short bar in the same direction as the losses), plus 8 Minor. Fixed: options restored, the script edits by text, positions balanced within each option count, every item's keyed text and option set pinned (I11); plain charts draw signed values on an axis with a zero line, true minus signs and printed decimals, with detectors (I12); calibration labels kept inside the plot and off neighbouring dots; social15 highlights the bar that proves its title, social16's half-story chart removed; tutor routes for significance, task and meaning ordered after subgroup, population, duration and stakes, the task route narrowed, the why-not fallback only when that follow-up states a negative; minus signs on the record; dead Library CSS removed. 268 tests pass. Re-audit follows before the external review.

**Re-audit 28b:** no Blocking; one borderline Major (calibration labels collided with the diagonal label and with axis labels in some sessions) and five Minor. Fixed by class: reference-line explanations moved out of every plot into captions (calibration, sparkline), an inner margin keeps dots off axis labels, and a new detector (rule 31, R31) fails on any figure label that overlaps another label or a data mark, live-fired. Also: the task route answers before "who"; a single why-follow-up that explains a miss still answers; values never wrap; negative bars grow from zero. Stored local records keep option indices from before the balancing; they are scores, never re-rendered as options, so nothing shows a moved option. 270 tests pass. The protocol's audit is clean of Blocking and Major; the external review follows.

## Iteration 29 (2026-10-31)

**Independent score:** 81/100 (review 24, `qa/reviews/review24.md`). 1 Blocking, 0 Major, 12 Minor.

**What the protocol caught and missed.** Audits 28 and 28b stopped a Blocking (duplicate option) and two Majors before the external review. They missed B1 because neither reloaded the hosted page after play. The audit prompt (`qa/AUDIT_PROMPT.md`) now requires it, and I13 enforces it in the suite.

**Fixes (invariants touched):**
- **B1** [I13]. The allocate calibration outcome is stored on the record when it is made (`topBest`); the scorer guards the missing values and falls back for older records. New test plays every format on the hosted page, adds a pre-`topBest` record, reloads every view and requires no page errors and non-empty content; it fails on the old code and passes on the fix.
- **Minors** [I2, I9, I11, I14]. Delegate reveal shows each task's evidence under its row; tutor: recommendation questions about one's own organisation go to the manager's action, a question about one task gets that task's evidence, "by itself" means alone, "real money" goes to the incentive follow-up, a term's meaning matches by prefix (ECU, ECUs), follow-up ties go to the one sharing more words, and the follow-up's own question weighs double in the last fallback (server and page agree; REVIEW24 tests); axb15 uses 2,190 from the abstract as corrected by the erratum, with the erratum recorded on the source; bz06 follow-ups attribute the 1990 reading; social01 and biz05 distractors are rivals a manager could believe, ai11 has a third option and a neutral scene; six keyed or distractor options rewritten so option form is no clue (gate I14); true minus signs and en-dash ranges in reader-facing text (the number gate now checks negative values by magnitude, which exposed axb01's g = −0.54 stored only in a location note; the published sentence is now quoted from the Europe PMC full text); the allocate effect is a point on its own axis, not a bar on the points scale; Library actions sit under each principle, the record's sections are rules instead of three cards, the featured path takes one cell so eight cells fill two columns; ai09, ai11 and biz02 headlines state findings; projector lists without bullets.
- **Own slips caught before any review:** an inline comment swallowed the rest of a one-line statement (18 browser tests failed; a new `node --check` test now fails in a second on any script syntax error), and the Library's new two-column placement left an implicit column on phones (the design lint's squeezed-text check caught it; fixed in the phone rule). 278 tests pass.

**Regression audit 29:** no Blocking; 3 introduced Majors stopped before the external review. Two new distractors stated the papers' own findings (social01, social14), so a right answer would have scored wrong; a single-word "what is X" tutor clause redirected "What is the design?" and "What is the sample?" on 14 decisions. Fixed: distractors the evidence contradicts (I15: every new option is read against the item's quotes, explanation and follow-ups, and the audit repeats the check); the define clause moved to a narrow late route that answers from the study's own text; a golden battery of 15 everyday questions over every decision now fails on any silent redirect (I16). Minors: the recommendation rule leaves ethics and staffing questions to the ethics route; in-bar labels removed from the allocate figure (the title names both measures and every value is labelled), after the label was found covering an effect point at phone width in an order-dependent case; grey rings on non-best non-significant effects; axb02's keyed option reworded so form is no clue; one rule on the record. The lint now checks every allocate, delegate and rank item at phone width and in-bar labels against data points. 279 tests pass.

**Re-audit 29b:** no Blocking; 1 introduced Major (the ethics-and-staffing exclusion used bare words such as "right", "wrong", "hire" and "fewer", so everyday hiring and roll-out questions got the ethics non-answer). Fixed with narrow phrasings for ethics ("is it fair", "ethical", "legal") and staffing ("fire", "lay off", "fewer workers"); the golden battery gains three "should" and ethics questions so this class is caught (I16); AUDIT29 tests. Minors: axb02's keyed option reads with its question and matches its chart, whose amber bar is now the keyed group; social14 regains a two-part distractor the evidence contradicts; "what is X" uses a follow-up whose question names X first; dead in-bar label CSS and its lint block removed. 285 tests pass.

**Re-audit 29c:** no Blocking; 1 Major and 1 borderline (the define tweak returned unrelated Yes/No follow-ups to "what is X"; the narrowed ethics exclusion let "is this fair?" and "are we allowed?" reach the recommendation). Both fixed with the auditor's own patterns, which it had validated on about 7,000 question pairs; the implementation reproduces its validated outputs with zero differences on all three batteries. Because three audits in a row found a new tutor Major in each hand-tuned fix, the router is now frozen behind those batteries (tests/tutor_golden_wide.json): any routing change produces an explicit diff to read before it can ship (I16). AUDIT29 tests now assert the action itself, so they fail on the old code. 286 tests pass. The audited change set is clean of Blocking and Major; review 25 follows.

## Iteration 30 (2026-11-01)

**Independent score:** 84/100 (review 25). 0 Blocking, 2 Major (both latent from earlier iterations, none introduced by iteration 29), 10 Minor.

**Fixes (invariants touched):**
- **M1** [I13, I5]. Every record stores its own skill baseline when the call is made; the record never recomputes it from a bank that may lack answers. I13 is generalised: records made on the hosted page must read exactly as the offline file (which has every answer) reads the same records, for one decision of every format and for blind constant routing on every delegate item (test fails on the old code, passes on the fix).
- **M2** [I9, I16]. English-word surnames name a study only when capitalised (shared list in the routing table); ethics questions get the ethics answer before any follow-up match; a question that is not yes/no never gets a follow-up answer opening with Yes or No (class test over every decision). The router change produced 12 golden-battery diffs, each read and accepted (all were Yes/No non-answers replaced by an honest "not covered" with the finding); golden files regenerated deliberately; REVIEW25 tests.
- **Minors** [I2, I15]. Follow-ups no longer name another live item's authors or state its answer (ai09, dimant-contagion-multi, genai3), with a gate; axb01's paraphrase replaced by the two published sentences (Europe PMC full text); social15 shows the painting out-group (11.99%, completed from the author's public working-paper version because the published-version quote truncates the sentence) beside taking from opponents (22.9%), in text and chart; source lines inside estimate, forecast and rank plates; the allocate projector shows no confidence stat; record bars are signed around a zero line and the short-record copy reads "Score shows after 3 calls".
- **Deferred to the next iteration:** the estimate band labelled on its axis, a rank dot plot, the empty right column on wide reveals, Library repetition.

**Gates:** 292 tests pass, including the design lint over every decision and the tutor golden batteries.

**Regression audit 30:** no Blocking; 2 introduced tutor Majors that the frozen batteries did not cover. The yes/no guard dropped every Yes/No follow-up when a question opened with a filler word ("So did the effect fade?": 0 of 330 answered); "know" in the detection route sent "did participants know…" questions to unrelated follow-ups. Fixed with the auditor's patterns: Yes/No follow-ups are dropped only for clearly open questions after any filler; detection uses a narrow know-about-AI pattern and whole detection words in the follow-up's own question; an item's own ethics follow-up answers ethics questions about it; a sentence-initial capital no longer counts as a surname. 326 of 332 prefixed phrasings now get their follow-up. Coverage now grows with every audit: the auditor's probes (76 pairs), 21 questions asked of every decision, and every Yes/No follow-up asked after four filler words joined the golden batteries (I16). Minors: source line once per figure (with a detector), chart titles state the measure without citations (8 rewritten, with a detector), an "hit band" label on the estimate axis replaces the caption, projector stat row fits its items, true minus on the projector's average score. The social15 working-paper value stays (it verifies the published sentence the stored quote truncates), with its provenance in the evidence record only; the gate against working-paper material in player-facing text held. 294 tests pass.

### Audit 30b (2026-11-01)
Regression audit found 2 tutor Majors (lead-in questions answered Yes/No; "know … AI" detect route hijacking) and 8 Minors. Applied the auditor's tested router exactly; probe outputs identical, ~10k golden entries unchanged. Added the probes and lead-ins to the wide golden battery and a page-vs-server tutor parity test. Minors fixed (rank source line, hit-band label margin/size/minus/aria, bz07 note, phone class-panel minus). Phone-width lint extended to every estimate item: by rule {}. Suite: 295 passed.

### Iteration 31 (2026-11-01): review 26 fixes
- **M1 tutor (both tutors, one routing table).** New routes: `compare` ("better than", "or not": the finding plus a follow-up stating a comparison on the question's words; skipped when the study does not make that comparison), `whatif` (the version the study tested), `control` (the control-group follow-up, Yes/No kept only for "was there a control group?"). A why question never takes a quantity follow-up and otherwise gets the explanation. A near-match follow-up keeps its Yes/No only when the question adds no word of its own beyond filler. British spellings and doctor/physician meet. Golden diff read line by line: 13 changes, all better or equal (judg09 "was real money at stake?" loses its "No." prefix; the rest of the answer stands). Page/server parity now compares full text on every probe and every decision × 21 everyday questions.
- **Minors.** True minus on every plate number and a measure title (`estimate.label`); notalie distractor replaced by one the 38.1% → 62.7% shift refutes; social15 re-quoted from the published PDF (p. 10), working-paper entry removed; biz07 scene neutral; false-news-spread keys the mechanism; axe10 headline; projector estimate is a dot strip with the study value and hit band on the same axis; percentage rank values plotted as dots on a 0–100 track; Library leads opened principles with the player's own skill and collapses unopened ones to one line; record headline signed with the duplicate stat removed; delegate tasks separated by rules; console delegate list unordered; "Call it" renamed "Pick one".
- **Detectors (closing the classes).** R13 reads SVG and display numbers; R21 counts borderless filled rounded boxes as tiles; R31 now checks HTML text overlapping text (it caught a phone-grid regression in the new Library during this iteration); the lint plays the Library after principles open. Each live-fired in `tests/test_design.py`.

### Audit 31 (2026-11-01) and fixes
Regression audit of iteration 31 found 4 introduced Majors and 7 Minors; all fixed the same day.
- **M1** compare answers appended a follow-up's own "Yes."/"No." → `strip_yn` everywhere a follow-up is borrowed for a different question (compare, control, whatif, and the word-overlap fallbacks), keeping "Yes, partly" whole.
- **M2** compare guard let "experts more accurate than laypeople" through on half the words → every distinctive word (or its synonym) must be in the study, except for "… or not?" questions.
- **M3** whatif claimed "the study tested one version" → it first borrows a follow-up that shares a distinctive word (never a quantity follow-up), else states the design neutrally; "what would happen in/for X" goes to transfer.
- **M4** projector dot strip clipped at class size and binned values → the server sends every answer's value; dots fit the height and become bars with a count when a room is too large; labels sized for the projector.
- **Minors** Library "Play the other N" plays the unplayed; Library scores wait for 3 calls; rank values readable by screen readers and the track shows both ends; Streamlit says "Pick one" (new test: format names agree on page, console and Streamlit); aria hit band clamped.
- **Pre-existing, fixed too**: social12 white/Black callbacks now answers with the finding; "as good as" and "more X than" are comparisons.
- **Detectors**: R31 flags marks drawn outside their SVG; the lint now runs the projector with 80 answers. It caught two collisions in the new strip before commit.

### Audit 31b (2026-11-01) and fixes
1 introduced Major, 3 Minors.
- **M1** what-if borrowed follow-ups on one stray shared word ("used", "lower", "observed"), some opening with a bare verdict. Two narrower borrowing rules were tried against a 15 × 112 what-if battery and both still produced non-sequiturs, so what-if now never borrows: it states the design, the scope and the finding. Deliberate trade, read in the golden diff: six what-ifs that a follow-up used to answer well (wallet key, loss framing, stronger résumé, health label, bots removed, visible productivity) now get the neutral design-plus-finding answer, which is true but less specific.
- **m1** a rejected comparison now says the summary does not cover that comparison instead of falling through to a stray follow-up; the comparison's own words ("outperform", "better") no longer count as missing.
- **m2** the projector strip's count label anchors left at the right edge; R31 now flags SVG text running past the right of its drawing area.
- **m3** rank values sit above their dots, clear of the leader and both end ticks.
- Python `strip_yn` and the page's `stripYN` now agree on a digit after "Yes.".

### Audit 31c (2026-11-01) and fixes
1 introduced Major, 4 Minors.
- **M1** the compare guard (every distinctive word must appear in the study's text) asserted "does not cover that comparison" for comparisons the study makes (paraphrase words such as "without", "applicant", "empty"). A word-presence test cannot prove absence, so the reply never claims it: "Here is the comparison this study made: …" (golden diff: only that sentence changed, on the experts-vs-laypeople probe and three others).
- **m1** "what would happen with X" goes back to the subgroup and other routes; "what would happen to X" stays a what-if. **m2** the projector count label sits above its own bar, with headroom under the study label. **m3/m4** test docstrings fixed.

### Audit 31d (2026-11-01) and fixes
1 introduced Major, 2 Minors, all fixed with the auditor's tested patterns.
- **M1** excluding every "what would happen with …" from the what-if route sent counterfactuals ("with no fine", "with no treatment") to "does not cover" or to a stray number. The exclusion now applies only when a subgroup term follows "with". Eight counterfactual phrasings on every decision are now a test; six new questions joined the every-decision golden battery (672 new frozen answers).
- **m1** the subgroup route reads plurals ("novices", "newcomers"). **m2** an unmatched comparison now says so about the matcher, not the study: "I could not match that exact comparison to this study's summary. Here is what the study found: …".
- Golden diff: 113 wording changes on that sentence only; nothing else moved.

### Iteration 32 (2026-11-01): review 27 fixes
- **M1 tutor.** "should we/I/my/our <any verb>" is a recommendation unless it is about ethics, staffing or belief ("should we believe this?"); the action route reads "what does this mean for my team", "for our company", "learn from this"; "what did the study find" is a summary; "were these students?" is a who-question. Golden diff: one changed answer (an improvement); 16 new everyday questions frozen on every decision.
- **Minors.** Causal node labels wrap to two balanced lines or shrink to fit their pill; calibration labels take the first side clear of every dot and label; the phone's locked screen has no badge, names the decision as a fact and offers "Leave the live class"; no middle-dot strings anywhere (new test); the room's bars in slate on console, projector and phone, blue only for the player; axb02 copy; axf05 "Baseline, 73.0%"; curly quotes in all player text (new test; evidence quotes verbatim); "Room 1.67"; axb01 scene says the tasks are the authors' worked examples; Library uses the record's small-sample note instead of hiding the score; dead theme-art code and an unreachable caption removed; featured path ticks in white, not amber.
- **Detectors.** R31 flags a label wider than its pill and SVG text past either edge; the phone lint covers every causal item.
- **Open (not fixed this iteration):** bz12's "Find the cause" framing; one more contest item that held up; the header-less join bucket (API clients only).

### Iteration 33 (2026-11-01): the key-less tutor stops guessing
Eight reviews in a row found a new key-less tutor misroute; each fix was tested, but the space of phrasings is open. The class is closed at its source: the word-overlap fallbacks (one shared word in a follow-up's question, a word in a follow-up's answer, generic overlap) no longer answer. A follow-up is borrowed only when its own question shares two distinctive words with the question, or two thirds of them (synonyms count, filler words do not); an unanswered "what is X" never borrows on X. Anything weaker gets: "I could not match that question to this study’s summary. Here is what the study found: …", with the decision's own follow-up questions as buttons under the answer; each button answers exactly. "Okay, was it expensive?" matches the follow-up "Was it expensive?" exactly.
Golden diff read by class: 7,076 wording changes on the not-covered line; 158 weak matches now offer the summary's questions (sampled 30: almost all were non-sequiturs, e.g. "which conspiracy theories were included?" answered with an unrelated follow-up; a few good answers are now one click away); 11 other changes, all improvements (filler-prefixed follow-ups now answered exactly, "which group did best?" gets the finding). New test: every decision's weak-match reply carries its three questions and each answers exactly.

### Iteration 34 (2026-11-01, in progress): the two visual items reviewers kept naming
- **The wide reveal's empty right column** now holds a second comparison at one scale (TUFTE open question since review 25): under the study card, this call against the player's other first calls on the same principle, as skill points versus guessing (−100 to 100, 0 = guessing marked), with "this call" labelled on its mark. Shown from 1200 px; needs two other calls on the principle. Coincident calls stack. Linted as a new state.
- **Streamlit shell**: the class pages use the game's typeface (Streamlit 1.66 theme font faces from `static/`, pinned to the game's file by a test), navy pill buttons and the game's background; the Play page keeps one header (the game's), with a slim strip for the page menu.
- **Not done, deliberately**: one large signature drawing per theme. The owner's Tufte instruction removed decoration that encodes nothing; a drawing per theme would encode nothing, so it stays out.

### Audit 33 (2026-11-01) and fixes
2 introduced Majors, 6 Minors.
- **M1** with an AI key, a suggestion button (a decision's own follow-up question) called the model and spent budget → such questions are answered from the summaries before cache and budget, on the server and in the rate limiter (`is_follow`); test with a stubbed transport.
- **M2** a missing bracket let the server give "why" questions a quantity follow-up (page and server split, I9) → bracketed; parity probes added.
- **Minors** suggestions ordered by closeness to the question; the font-load redraw happens only when the real font measures differently and keeps focus on the heading; two-line node labels centred in their pills; the Library waits for 3 calls like the record's areas; the rank average and the projector's answer count no longer use the player's blue; the locked screen keeps a question title a question.

### Audit 34 (2026-11-01): no introduced Major or Blocking; 6 Minors fixed
Locked-screen titles keep their own punctuation only; the theme strip stacks ties under "this call" in 5-point columns with a "+n" count past three, and its type is sized for 1200 px (lint now checks the strip at 1200); the Streamlit primary button keeps white on blue when hovered; the AI-key test stubs the bound transport (it could not fail before) and checks a free question does reach the model; suggestion order is pinned by a test and by page/server parity.

### Iteration 35 (2026-11-01): review 28 fixes
- **Verdict**: "Close." only above what a blind call earns; partial credit reads "partly right, not exact", not "missed".
- **All decisions** is a ruled index (title, question, format and area as a phrase, source; best score in ink); the lint state for it used a dead hash ('#atlas') and silently linted the home page; it now uses '#studies' and a test checks every lint hash is a real route.
- **Record**: "Calibration: 44 points more confident than accurate." as one sentence.
- **Figures**: the allocate effect track prints its scale at both ends and at zero; the theme strip explains its marks in words and states how this call compares with the player's average.
- **Tutor**: "can we trust X from our vendor/tool/model" is a recommendation; "how many / what share / what percent" answers with the explanation when it states numbers. Golden diff: apostrophe-only changes, the retired social20, and the renamed contagion follow-up.
- **Content**: curly apostrophes and single quotes in all player text (test extended; both tutors tokenize curly and straight alike); rollout3's scene neutral; social20 kept in play (it is Dimant 2023, the lab's one decision on how to measure a norm; retiring it would drop the paper) with its strawman distractor replaced by the rival the paper names, the most common answer; the contagion follow-up no longer cites a year from another paper, and the GEB header line is gone from its evidence; genai3's locations say the values come from Table 1; a duplicate social01 quote with a missing space removed.
- **Classroom**: joins use only their own bucket; answer retries honour Retry-After for about 20 s.
- **Kept, with reason**: social01's chart shows the variances the paper reports and calls "much larger"; it stays as the paper states it (RULE 0).

### Audit 35 (2026-11-01) and fixes
1 introduced Major, 4 Minors.
- **M1** the new `numbers` route ran before `duration` and `subgroup`, so "how much more did the weaker writers gain?" lost its subgroup follow-up (123 of 5,424 probes) → moved after `subgroup` (the auditor's tested order); a subgroup question with no subgroup follow-up still gets a share the explanation states. Golden diff: no existing answer changed; 341 new frozen answers from three every-decision questions and five probes.
- **m1** joins bypassed every per-address limit → an address-wide `ip_join` bucket before the per-code one; tests: random codes from one address hit 429; a full class of 120 joins and answers behind one address with no 429.
- **m2** search in All decisions, the console picker and the Streamlit instructor page treats curly and straight apostrophes alike. **m3** answer retries read Retry-After before the body, do not sleep after the last try, and say "busy" when throttled. **m4** record: "Calibration: confidence matches accuracy." and no empty list.

### Iteration 36 (2026-11-01): visual redesign round (owner's choice)
Reviewers have scored visual 12/15 for six reviews and called the look "a well-made product template". One bold element, chosen from the subject: **the measuring scale**, the game's own act of calling a number and seeing the gap.
- **Home**: the headline runs large across the left, the lede and actions sit to its right, and the demo is no longer a dark card but a page-wide scale under a heavy rule: ticks at every point, labels every ten, a giant numeral readout of the call. After the lock the study's value, its hit band and the gap ("12 points") are drawn on the same scale, and the readout turns to the study's number.
- **Options**: a ruled list with hanging numerals in rings, not a stack of boxed buttons; the selected row takes the blue wash and a filled numeral.
- **Estimate plates**: the gap axis carries the same scale (minor and major ticks at round values) on a thin track.
- Tufte check: every new mark encodes a value (ticks are the scale, the bracket is the gap, the band is the hit band); no decoration was added.
- **Owner feedback (2026-11-01): "Still too many AI giveaways… why even mention 'then see the evidence'? Make everything clearer from the get go and focus every screen on what's important."** The home page no longer opens with a slogan: the first decision is the page's heading, with the scale under it and one plain line about what the game is. The "Do X. Then Y." headline is now a detector (R14) with a live-fire test; the meta description lost the same slogan. Verdicts are plain ("Matches the study.", "Partly right.", "Not what the study found."); headline full stops on the record are gone; the reveal drops the format-and-area line and the repeated "your record tracks…" sentence (confidence sits in the verdict line); the predict screen's study line keeps only the case step, design, journal and year. The estimate instrument uses the same measuring scale as the home page, ends always labelled.
- **Owner feedback (2026-11-01): "Fill out the empty spaces better… too often a line break where there shouldn't be one."** Heading width caps (26ch, 24ch, 18ch, 22ch, 30ch, 17em) removed; headings wrap greedily (`text-wrap: wrap`, not `balance`) on the page and the console; rule 11 rewritten; R19 now flags `balance` on headings and the new **R33** flags a heading that wraps while its box stops well short of the space it has (live-fired). The question screen uses two columns at 1200 px and up, like the reveal: question on the left, the answer instrument and confidence on the right; the confidence question sits on its own line with a full-width slider. Forecasts use the measuring scale too. The phone Library rows give the principle's name the full width.

### Regression audit 36 (fresh agent, redesign diff e47c20c..994cea3)
- Gates as audited: 318 passed; lint clean; ruler thumb within 1 px of its tick at 390, 1200 and 1440; no answer before lock; axe clean; classroom clean.
- Introduced, Major: (1) on the locked home try-it, "You" and "Study" labels overlapped whenever the guess was within about 5 points. Fixed: once the study value is shown it takes the axis row in amber (intermediate axis numerals give way, end numerals stay unless it sits on one), the player's label stays above; lint now locks the try-it at 41, 39, 40, 0 and 60. (2, borderline) the home meta line said every decision comes from an "experiment"; at least 20 items are meta-analyses, audits or administrative records. Fixed: "112 decisions on AI, work and behavior, drawn from 109 peer-reviewed studies"; meta description says "a published study".
- Minor, all fixed: the read-out reserved no space and the page jumped on first touch (now a hidden placeholder and a fixed 15rem column; slider top identical before and after touch at 390, 1200 and 1440); the focus ring crossed the scale numerals (ring now on the thumb); a browser test had been loosened (reverted to == 1); the question screen dropped the sample (restored to the study line, sentence style); uneven labels on −50 to 50 (major step now prefers a value both ends sit on: −50, −25, 0, 25, 50) and minor ticks finer than the slider's step (now never finer); "1 points" in two places (fixed; new R14 detector for a plural after 1, live-fired); a double rule between options and the confidence row (one rule).

### Regression audit 37 (fresh agent, diff 994cea3..6ed835a)
- Gates as audited: 319 passed; lint clean. The locked home never overlaps at 0 to 60 on three widths.
- Introduced, Major: the new sample on the study line printed numbers inside two estimates' scoring bands before lock (judg09 "95 respondents", target 92 ± 5; bz04 "33 analyzed", target 29.7 ± 6), against I4. Fixed: `sampleLine()` drops the sample of an estimate when any of its numbers falls in the band, and drops non-samples ("Multiple studies", "Studies 1-4…"). The I4 bank test now reads the study line, and a new browser test reads the rendered line of every estimate (live-fired: it names bz04 and judg09 with the guard off).
- Minor, fixed: end ticks off the minor grid (0 to 95 scales) now always get a tick and a label, and the interior threshold went back to 0.7 of a step (80% returns); rollout4 keeps medium ticks on phones (major/5 when major/2 is off the grid); on phones a numeral closer than one step to an end gives way, and with seven or more numerals every other interior one gives way (bz05 at 390 reads −30, −20, 0, 20, 40; the old −30/−20 collision is gone); the options/confidence rule is folded into the single `.conf-row` rule (`.opts + .conf-row`).
- Minor, kept: the phone home reserves the read-out's height before the first touch (about 70 px above "Slide the scale to answer"); the alternative is a 32 px jump mid-drag, which the earlier audit ranked worse.

## Iteration 38 (review 29: 87/100, 0 Blocking, 0 Major, 14 Minor)
- m1 causal reveal: the stored layout is stretched to a 700-wide canvas (510 on phones) and 1.5 times taller; each link now ends at its pill's edge instead of a fixed pad; all links appear together in 0.3 s, no stagger (rule 25). New test: every link at least 60 units long on the wide canvas (25 on a phone) and clear of every third pill. bz12 is no longer a causal item (m7: its options are subgroup outcomes), so it is a pick-one.
- m2 tutor: a surname that switches study now opens "From <authors> (<year>):"; "Does this mean … should …" goes to the manager's action; writing tasks (cover letter, résumé, email, speech, posts) are declined; ai01 gains "Did quality improve too?" (18%, quoted) in place of a follow-up that restated the scene (o2); rollout3 gains "What is the jagged frontier?". A one-word follow-up match was tried and dropped: the golden diff showed it borrowing "cost" and "card" answers for significance questions (the iteration-30 class). Golden diff otherwise: only the four "From …" prefixes. Reviewer phrasings added to the probes.
- m3 dimant-polarizednorms: full text read (Management Science 71(3), coauthor-hosted version of record). The explanation now states the body's result: reactions concentrated at the extremes, and with most others at zero and the rest at four, 46% contributed more than the risk-free two. Three quotes added.
- m4 biz05: the third option no longer contradicts the first ("Above-average homes did not change their usage", false). m5 judg02: already quarantined (its source is unverified) and never served; it stays as the quarantine test's case and returns only as a contest item. m6 social13 asks for the estimate and how firm it is. o3 genai3 "find", not "predict".
- m8, m9 projector: tied rank rows share a place ("1="); only the top place is amber; the join code is ink; "Exit projector view" is invisible until hover or focus; "3 answers" sits on one line.
- m10 Library: the three-call rule is stated once at the top; "Play the other N" moves into the principle's status line. m12 record: no empty meter under three calls. m11: axe12 note names the direction of its scale; social15 labels given and taken; bz08 names its one center; rank figure title names its measure.
- m13 classroom: tried releasing an open decision after 20 minutes of console silence; reverted, because two settled tests require an open question to stay held while an instructor talks (tests/test_http.py). m14: the tutor returns 400 for a non-string id (test); the CSV writes the page's default unit (%).
- Kept: m13 (settled; the hold ends when the instructor ends or reveals); phones log the session-end 404s (the page handles them with the "class ended" dialog); the client bucket keyed on X-Client-Id (the IP bucket still caps paid calls); axe12's scale range is not stated because no stored quote gives it.

### Regression audit 38 (fresh agent, diff 6ed835a..7dc3a0c)
- Gates as audited: 321 passed; lint clean. Every changed number in a stored quote (46%, four, two; 50% and 30%; 4.3 points and 20%; 7.25, 15.25, six centers); bz12 reads well as a pick-one; no sibling leak.
- Introduced, Major (process): the writing-task decline was only in the route script, never in the bank (a later `git checkout src/bank.json` dropped the routes write), and the golden locked the old answer. Fixed in iteration 39: the route is in the bank, limited to requests ("write me", "can you write", "help me draft"…) so "Did they write an email to customers?" and "Did the résumés include a cover letter?" are answered; a test checks both directions.
- Minor, fixed in iteration 39: "does this mean … should" now needs a person as subject and skips "should hold / generalize / apply / work / be trusted"; staffing nouns gain writers, agents, analysts, reps; biz05's distractor is false in both periods ("raised their usage"); one amber badge on a shared top place; social13 no longer restates its scene; phone causal links (vertical layout, below).

## Iteration 39 (review 30: 88/100, 0 Blocking, 0 Major, 16 Minor; audit 38)
- Tutor: three-letter surnames (Noy) switch study when capitalised; the topic word picks among one author's papers using the item's title and scene as well; sales pitches, ad copy and scripts are declined as requests. Golden diff read by class: content-driven implication and scope changes, the writing declines, and "Should we use AI to replace our writers?" now taking the staffing answer (the settled class).
- Colour grammar: the projector join code is white, the answer meter slate, "For a manager:" ink, the Streamlit join code ink; the console delegate reveal draws the room's counts in slate.
- Phones: causal diagrams run top to bottom (each stored column becomes a row; meta-perception-causal carries its own phone positions); every link is at least 50 units at both widths and clear of every third pill (test). Node labels use one size on both widths.
- Forecast and estimate question screens: the floating "Slide the scale" prompt is gone (the read-out keeps its space hidden); the action bar carries the one instruction.
- Content: social15's chart shows the money comparison its headline makes (allies 14.97% against a painting group-mate 13.54%); dimant-hate-choice says what set the divide apart (expectations, in the paper's terms); axb10's key names the family of forcing designs; two implications gain their honesty condition (dimant-enforcers-rank, axe01); bz13's scope line states coverage; pick-two length cue closed (facebook-deactivation, social16, genai1) with a gate: at most one pick-two solved by the two shortest or two longest options.
- Projector and phone: "Back to waiting screen" hidden on the projected screen; "Discussion prompt" renamed "For a manager"; rank rows read "Room’s average rank 2.0"; allocate results in pts on phone and projector; "The room, 1 answer".
- Server: a cut-off or slow body returns 400 (test); the public bank drops an estimate's sample when it prints a number inside the band (judg09, bz04; test).
- Kept: the empty right column on a wide first-play reveal (no second comparison stored for most items; filling it would be decoration); four follow-ups on five items (the guide's floor is three); confidence enters calibration, not pick-one scores (settled scoring design).

### Regression audit 39 (fresh agent, diff 7dc3a0c..ec59b24)
- Gates as audited: 325 passed; lint clean; server and page tutors agree on 714 pairs except one; public bank differs only by the intended edits.
- Introduced, Minor, all fixed in iteration 40: "Write me a résumé" declined on the server but not on the page (JavaScript's \b at "é"; the page now also tests routes on the accent-stripped question); a three-letter surname as a question's first word ("Van drivers…") switched study (now the same first-word rule as longer surnames); "Does this mean that we should replace our writers?" fell through while "Should we…" took the staffing answer (both now take it); axb10's key became the longest option ("Engaging users before the AI answers"); social15 said allies got "no more" at 14.97% against 13.54% (now "about as much"). Kept: one amber badge on a shared top place (rule 29; audit 38 asked for it, audit 39 for the opposite).

## Iteration 40 (review 31: 87/100, 0 Blocking, 1 Major, 16 Minor)
- M1 genai2: the claim keys what the design supports, edited prompts alone matched the originals (46.4% against 47.4%, not significant). The 52.7% is stated as the authors' after-the-fact upper bound, the chart shows the edited-prompt bar with the 52.7% in its note, the follow-up says the pick used the measured agreement, and the manager action says to test drafts on a small sample. The unedited 43.5% stays out of this item (it is axe04's answer; the sibling test caught a first draft).
- m1 number gate: a percentage in player text must now match a quoted number that is not a count or a duration (new test, live-fired on biz01's old "3%"); biz01's follow-up drops the unquoted 3%. m2: the Dimant (2019) header is gone from dimant-proximity-estimate's quotes. m11: z and P values leave two explanations (plain words; the statistics stay in the Source tab). m12: axe01 asks which source customers will prefer; the reveal's study card uses the same sample filter as the question screen.
- m3, m5: non-significant allocate labels are grey; zero is labelled whenever the effect track crosses it (an end label it would crowd gives way). m8, m9: projector controls are invisible until hovered or tabbed to; after a reveal the unranked option list leaves the projector for rank and allocate.
- m13 tutor: "legal team / department / counsel" no longer reads as an ethics question; golden diff confined to the edited items.
- Kept, with reasons: decoding sentences on the allocate and record figures (m6) and the calibration label near the diagonal (m7) — the labels sit on the marks where the figure allows and the sentences are one line; phone reveal order (m10) — moving the study card into a tab changes every reveal and needs its own audit; phone causal predict (m14) — the masked layout is the settled pre-reveal view; hosted practice lock after an abandoned console (m16, settled).

### Regression audit 40 (fresh agent, diff ec59b24..10cfb2c) and iteration 41
- Gates as audited: 326 passed; lint clean; page and server tutors agree on 38 of 38, including accented questions and "legal team" against real legality questions.
- Introduced, Major: grey non-significant allocate labels lost their grid class and fell onto their own rows at full size (axb08, both widths). Fixed: the label keeps `ev` and adds `ns`; a browser test checks every allocate label keeps one size and its class.
- Minor, fixed: the reveal's study card now uses `sampleLine()` (axe01 no longer shows "Studies 1-4…"); the unused `studyLine()` is deleted; genai2's chart drops the unedited 43.5 bar (axe04's answer) and the sibling test now reads chart values; biz01's default follow-up asks what the paper reports (86% after 3 to 15 months against 37%); the percent gate skips sample sizes, test statistics and years and also reads scenes, implications, chart notes and delegate reasons (live-fired on "8,221%"); the classroom shows a dash, not "null pts", before any answer.
- Kept: the rank and allocate option list also leaves the plain console after a reveal (the reveal lists every option).

## Iteration 42 (visual round on the reviewers' standing asks; owner, 2026-11-03: "Keep going… screenshots along the way… publish and deploy")
- Wide reveal: the questions and the tutor now span the full width below the two columns (questions left, tutor right), so the right column no longer ends in a dead quadrant beside them; the figure no longer sticks.
- Phone reveal: the finding and the manager's action follow the verdict directly, then the figure, then the tabs; the study card moves into the Source tab on phones.
- Labels on the mark: "as sure as right" is written along the calibration diagonal and the diagonal is an obstacle for the dot labels; "guessing" sits at the end of the dashed zero line in the record's trend; the decoding sentences ("Hollow points…", "Dashed line…", "(the dashed line in the trend)") are gone. The record's big score number gets line-height 1 (a two-digit negative score touched the line under it).
- Projector after the reveal: the join banner shrinks to one slim line, the lessons move under the question, the redundant task list and answer count leave, the delegate stat reads "Every task routed right". Revealed rank, allocate and estimate fit 1440×900; a delegate case step with three long tasks runs 56 px over.
- Deployed: the offline build is published as a private claude.ai page (owner's approval, 2026-11-03), republished after each round. GitHub needs an empty repository created by the owner (no repository-creation rights from this session).
- Exports: on the claude.ai page, Export CSV and Export JSON go through the page's downloads capability (the viewer confirms a save); elsewhere they stay plain browser downloads.

## Iteration 43 (review 32: 87/100, 0 Blocking, 0 Major, 17 Minor)
- Wide reveal (m9): the study card and the principle strip move out of the evidence card into the left column under the manager line, so causal, allocate and delegate reveals no longer stack a 1,100 px right card beside an empty left one. On phones the study card stays in the Source tab and the strip follows the figure.
- Question screen (m10): the answer column centres against the question at 1200 px and up.
- Content (m1 to m5, m11, m12; script `tools/content_review32_2026_11_03.py`): bz16's false claim is about size ("rose roughly in step"); statistical notation leaves 8 explanations, 2 answer titles and 9 follow-ups (plain words; statistics stay in the Source tab), with a new gate on explanations, titles, scenes, implications, questions and follow-ups; the INFORMS running header leaves two items' quotes, with a gate against headers and copyright lines; rollout3 prints 60% as quoted; civic-wallet-rank's scope line drops the unsourced critique; axe12's chart note states the measure (the citation stays in the source line) and keeps 2.50; judg05's amber bar is the headline's 78% (share choosing the gamble, 28% against 78%).
- Labels on the mark (m13, m15, m16): the allocate effect track keeps its negative end label unless zero sits within 9% of it; the room's rank view puts "avg rank" on the first value, the delegate view "routed as the evidence suggests" on the first count, and the decoding sentences go; the record's calibration finding is the plot's title ("You were 48 points more confident than accurate"), not a line 600 px away.
- Projector (m7): the revealed causal diagram is drawn under the question, the scene and the factor line leave after the reveal, the option list leaves for every format once the bars show it, and the explanation has room above it. Causal, rank and allocate reveals fit 1440×900 (a delegate case step runs 29 px over).
- Server (m17): the instructor console's reads have their own per-address bucket (test: the shared bucket empty, a phone gets 429, the console 200).
- Tutor (m6): "can we cut headcount / reduce staff" takes the staffing answer (scope and the manager's action). Golden diff: content-driven text changes in the edited items, plus biz01 "What was the default?" now answered with the suggestions (the routing vocabulary shifted with the rewritten follow-ups).
- Not done this round: m8 (projector allocate open view at 1440×900), m14 (delegate reveal numeral), the remaining tutor misses in m6, o1 to o5.

### Regression audit 42 (fresh agent, diff 1143057..84f8492), fixed in iteration 43
- Introduced, Major: projector stat labels set to nowrap ran into each other at 1280×720 ("Matched the evidenceAverage score"). Fixed: nowrap only from 1400 px.
- Minor, fixed: "as sure as right" sat under high-confidence dots (now low on the diagonal, where calls rarely sit, with a halo); the case line jumped above the title on phones (same order as the verdict); full-width Scope, Source and Note text ran about 130 characters per line (68ch measure); the phone Source tab said "Checked against…" twice (the phone copy of the study card drops its Checked row); a live-class panel pushed the finding below the figure at 1440 (pre-existing; `grid-auto-flow: row dense`).
- m14: the delegate reveal drops the big score numeral; one line says the evidence routing and how many the player matched.
- Audit 42 follow-up: on phones the zero label of the allocate effect track gives way to the end label when zero sits within a quarter of the track (axb08 at 390); two tests updated to the plain-words text and a clean limiter.

### Regression audit 43 (fresh agent, diff 8255388..deef225), fixed in iteration 44
- Introduced, Major: "avg rank 1.0" and the long delegate count, put inside the room panel's values, ran past the panel at 390 (sideways scroll) and squeezed task labels to one word per line. Fixed: the measure moves into a caption over each room chart ("The room’s average rank, 1 is the top"; "Classmates who routed each task as the evidence suggests"); values stay bare; the projector's delegate counts lose " right".
- Minor, fixed: a forged X-Instructor-Key reached the console's read bucket (the key now must open the room in the path, or the request uses the shared buckets; test extended); the bare "headcount" route sent factual questions to the staffing answer (dropped; the "we can cut … headcount" form stays); dimant-masks-forecast's follow-up turned a negative correlation into "opposite directions" (now "messages forecasters expected to work best tended to do worst", with its significance); social16 said "large" where the quote reports only significance; rollout3's task note still printed 60.0%; short evidence figures (estimate, forecast, delegate) keep the principle strip beside them so the right column does not end early; the projector's causal reveal is drawn tighter (dimant-notalie-causal's card now ends inside 900 px).

## Iteration 45 (review 33: 86/100, 0 Blocking, 0 Major, 13 Minor; m1 and m3 were already fixed in iteration 44)
- Plain words (m2, RULE G): sample sizes in five explanations ("with 4,559 participants"), "(not significant)" in allocate value labels, the rank values of forecast-teams-rank ("More accurate than independents"), two chart notes with P values, facebook-deactivation's unit; the notation gate now also covers N and n, "n.s.", t values, chart units and notes, rank values and allocate labels.
- Charts (m7, m8, m11): only the study's top place is amber in the rank comparison (the rest outlined); forecast-teams-rank's title no longer promises Brier values it does not draw; facebook-deactivation keeps one amber bar (rule 29 holds over the reviewer's ask; the lint caught the second); chart notes state the measure, citations stay in the source line (genai1, genai3).
- Verdict (m5): on pick-two and delegate, some right and not all reads "Partly right"; the record states that a confident miss can fall far below 0 (m4).
- Wide reveal (m9): when the figure ends well above the left column's text, the study card and principle strip move under the figure (measured after render, at 1200 px and up).
- Projector open view (m10): the heading also scales with the screen's height. Allocate headings no longer carry the instruction (m13); the question screen says "Spread 100 points…" under the heading. social13's key is no longer the only hedged option (m12).
- Not done: tutor phrasings in m6, rank track ticks (m7), o1 to o4.

### Regression audit 45 (fresh agent, diff deef225..6932bf7), fixed in iteration 46
- Introduced, Major: the outlined rank badges used the dark evidence ink on the dark plate (2.37:1; axe files them as incomplete). Fixed: plate amber outline and numeral; a browser test checks the colour.
- Minor, fixed: the wide-reveal balance moved the study card in the DOM (wrong screen-reader order, no resize handling, a live-class panel ignored); it is now a class (`meta-right`) that places the block in the right column by CSS, recomputed on resize and skipped when a room panel is present (test: 1440 to 390 hides the card again). "Partly right" on pick-two and delegate now also needs the score at or above guessing (judg02 and 1-of-3 routings no longer read "Partly right"). The projector's open allocate view shows the "Spread 100 points…" line. "Can we cut headcount with AI?" takes the staffing answer. dimant-enforcers-rank's chart note says the equalizing difference was not statistically significant at the 5% level (similar in size, not weaker).
- Not fixed: the projector's open view for allocate and delegate still clips at 1280×720.

## Iteration 47 (review 34: 86/100, 0 Blocking, 0 Major, 13 Minor)
- Introduced in 45 and caught by review 34 (m1): the "(not significant)" allocate labels clipped at every width. Fixed: the label wraps; a new lint check (R31, clipped text in an overflow-hidden box) is live-fired.
- Projector open view (m2): slimmer banner while a question is open, smaller scene (the QR renders at 120 px, another rule sets it), heading by screen height, tighter option rows; the open views of delegate, rank, choice, causal and allocate now run 0 to 35 px past 900 (from 75 to 205). The revealed rank view with five rows and a tie note still runs over.
- Tutor (m3): a straight apostrophe in a surname ("Dell'Acqua") now splits the same way on server and page (parity).
- Verdict and bar (m4): the action bar counts "matched the study", so "Partly right" no longer contradicts it. Ties (m5): the player's rank reveal uses the projector's notation ("1=") and the whole top group carries the evidence colour, on both screens; the per-row "not separated" notes give way to one caption. axf06's non-significant contrast carries no amber (m6). axf05's values read "points" (m7). The record's per-decision caption says what the big number subtracts; its "guessing" label drops below the line when the last call sits near 0 (m11); the Library says "decisions", not "findings" (m13); the wide-reveal balance triggers earlier (m9).
- Kept: confidence feeds calibration, not per-decision scores (m8, settled scoring design); social07's figure (m10) needs per-party counts the stored quotes do not give; the minus glyph (m12).

### Regression audit 47 (fresh agent, diff 6932bf7..dffb2e8), fixed in iteration 48
- Introduced, Major: the `meta-right` class placed the study card in a grid row below the left column, so on 42 wide reveals it moved sideways only and lengthened the page. Fixed: after the class is set, the card is pulled up to sit 24 px under the figure (a measured negative margin, reset on every balance); a browser test checks every reveal that triggers it (card within 40 px of the figure).
- Minor, fixed: a left single quote in a surname (Dell‘Acqua) now splits the same way on server and page; the player's room panel colours the whole top tie group, as the reveal and projector do; the QR note in the ledger corrected (it renders at 120 px); the lint comment says what R31's clipped-text check covers.

## Iteration 49 (2026-11-03): review 35 fixes

- **M1, fixed.** A live-class answer that failed for the whole retry window now keeps its data on the device, is sent again on the next good poll while the decision is open, and offers "Send my answer again". The headline reads "Not sent yet." with the reason below. Browser test `test_stranded_room_answer_can_be_sent_again` cuts `/responses`, restores it and checks the instructor count.
- **m10.** The phone question screen's header says "reconnecting…" while polls fail.
- **Content (tools/content_review35_2026_11_03.py).** dimant-enforcers-rank equity gap stated as similar and not statistically significant; manylabs-anchoring measure in plain words; axb08 title no longer breaks at "human-human"; forecast-training scope; axe05 raters on the author team; rollout2 scope cut to the setting.
- **Gates.** 335 tests (2 tutor goldens regenerated after reading the diff: only the four edited scope lines changed); design lint by rule {}; build current.
- **Open from review 35.** m1 verdict at skill 0, m6, m7, m9, m11, m12, m13, m14, m15, m16; m3 stays open until the full text settles it.

## Regression audit 49 (fresh agent, diff since iteration 47): 3 introduced Majors, fixed in iteration 50

- **M1.** A stranded answer could be filed under the next decision (cid read when the retry gave up; the POST named no decision). Fix: the POST carries `challenge`, `Store.submit` returns 409 for an earlier decision, the phone drops a stranded answer when the class moves on, and the retry loop stops when the decision changes. Test `test_stranded_answer_never_lands_on_the_next_decision` (live-fired: the old code filed ai09's answer under ai11) and `test_an_answer_for_an_earlier_decision_is_refused`.
- **M2.** Auto-resend never fired on an unchanged room (`same` polls carry no phase). Fix: the check reads the stored state after every good poll; one quiet POST per try, backoff 5–60 s, 10 tries, then the button alone. Test `test_stranded_room_answer_goes_out_on_its_own` (live-fired: fails on the old code).
- **M3.** The reconnecting notice overflowed at 390 px. Fix: the header shows "Reconnecting…" alone and `.count` may shrink.
- **Minors.** Focus stays in the card after a resend (asserted in the test); the notice is announced once; "Not counted." after answers close; dimant-enforcers-rank implication matches the explanation; forecast-training scope from the stored quote; axb08 compounds kept whole by the page, not by U+2011; the review 35 content script no longer pins keyed options.
- **Gates.** 338 passed; design lint by rule {}; build current.

## Iteration 51 (2026-11-03): review 36 fixes

- **M1, fixed.** Console, projector and phone panels mark the keyed option in words ("the study's answer" / "in the study") and with an amber outline at any count. Test `test_reveal_marks_the_study_answer_nobody_picked`.
- **m1.** axb08 title flows as one line (`.plate-h:has(.nw){display:block}`).
- **m2.** A 2xx without a boolean `accepted` is not a receipt; the answer strands and resends. Test `test_a_page_that_is_not_the_class_server_is_not_a_receipt`.
- **m7.** "Partly right" needs a score above the baseline.
- **m3.** axb08 asks which opponent clearly beat human-human debates (tools/content_review36_2026_11_03.py).
- **m12.** The Library states each principle's count once.
- **Open.** m4 dimant-hate-choice figure, m5 rank amber and scale, m6 repeated numbers, m8 decoding sentences, m9 tutor, m10 projector rank height, m11 dead space, m13 hero prompt, m14 axe12 scale (not in the stored quotes); review 35 m6 amber non-significant labels.
- **Gates.** 340 passed; design lint by rule {}; build current.

## Regression audit 51: no introduced Major or Blocking (4 Minors, fixed in iteration 53)

## Iteration 52 (2026-11-03): open review 35/36 minors

- **Review 35 m6.** Non-significant allocate labels were amber: `evNs` matched only "n.s." after review 33 renamed the labels "(not significant)". It now matches both. Test `test_non_significant_allocate_values_are_not_amber`.
- **Review 36 m5.** Rank charts: amber only on the top place's dot and value; the last track labels its ends 0% and 100%.
- **Review 36 o1.** The projector's repeated "Where would this fail in your organization?" is gone.
- **Gates.** 341 passed; design lint by rule {}; build current.

## Iteration 53 (2026-11-03): audit 51 minors

- **m1.** Rank and allocate class bars name the keyed row ("the study's top place", "worked best") on the phone and console.
- **m2.** The phone's class bars are text, not `role="img"`, so the evidence words reach screen readers.
- **m3.** A half-right pick-two or delegate answer reads "Some right, no better than guessing."; test `test_half_right_pick_two_is_not_called_wrong`.
- **m4.** `.plate-h` is a block in its own rule; the appended override is gone.
- **Gates.** 343 passed; design lint by rule {}; build current.

## Iteration 54 (2026-11-03): review 37 quick minors

- **m2 (I12).** axf02 prints 0.60 (decimals 2); dimant-hate-choice prints 59.0% (decimals 1).
- **m10.** `Store.control` refuses a non-string decision id with 400; test `test_malformed_open_is_a_400`.
- **m11.** `roomLine()` reads "Reconnecting…" while polls fail, so the lobby shows it too and keeps it across re-renders.
- **m12.** axe05 headline "of evaluations"; biz05 note unit once; bz04 no longer sets a share against a duration (tools/content_review37_2026_11_03.py).
- **o2.** `div.tutor` has `role="region"`.
- **Open from review 37.** m1 projector rank height, m3 dimant-hate-choice figure, m4 band label vs axis end, m5 repeated numbers, m6 decoding sentences, m7 tutor, m8 dead space and hero prompt, m9 phone causal pills, m13 brief wording; o1, o3, o4.
- **Loop status.** Reviews 36 and 37: 1 and 0 Majors; review 37 has none. The score holds at 85–88; the open items are design decisions for the owner.
- **Gates.** 344 passed; design lint by rule {}; build current.

## Iteration 55 (2026-11-10): review 37 design items

- **m1.** Projector reveals fit 1440x900: the explanation sits in the left column, rank rows carry the measured value, "Room's average rank" is one header, the key is one line. axf05 1,176 px to 900; forecast reveals about 1,100 to 900. Test `test_projector_rank_reveal_fits_one_screen`.
- **m4, m5.** Plate axis marks are named only ("You", "Study"); the band label reads "hit band ±N".
- **m6.** The forecast scoring sentence left the figure (it is in the record's "How scoring works").
- **m8.** The hero prompt sits on the slider handle; question screens are centred on tall wide viewports.
- **m3.** dimant-hate-choice chart colours neither drop.
- **Rules 7 and 21.** The projector's forecast claim is a plain quotation (it had an accent stripe and a box in a card, in a state the lint did not visit).
- **Open.** m7 tutor, m9 phone causal pills, dead space right of short figures, o1, o3, o4.
- **Gates.** 345 passed; design lint by rule {}; build current.

## Iteration 56 (2026-11-10): tutor phrasings, phone causal diagram

- **Review 36 m9 / review 37 m7.** New routes (funding, raters, scope, prereg), wider authors and off-topic patterns, a duration fallback to the item's own "Did it last?" answer, and a nearest-sentence fallback that needs two shared distinctive words and two thirds of the question's own. Same code in `server/tutor.py` and `src/app.js`; no regex lookbehind. 13 of about 22,000 stored answers changed, each read. Tests `test_offline_tutor_review37` (12 phrasings) and `test_nearest_line_needs_two_distinctive_words`.
- **Review 37 m9.** Before the call the phone causal diagram is 212 px tall (was 318); no pill overlaps on the four causal items.
- **Regression audit 55.** Started, stopped by a usage limit before it reported. To rerun with review 38.
- **Open.** Three tutor phrasings (company fix, better or faster, worst interface), the Dietvorst 2015/2018 pick, dead space right of short figures, record dot overlap.
- **Gates.** 358 passed; design lint by rule {}; build current.

## Iteration 57 (2026-11-11): review 38, introduced items

- **I-1.** "Slide to answer" is removed on the first move; test `test_home_prompt_leaves_with_the_first_move`.
- **I-2.** On phones the empty read-out slot shows a grey "?%" placeholder; nothing shifts under the thumb.
- **I-8.** Raters and duration routes say when the lab's summary has no such line (379 stored answers changed, all the duration prefix); the scope route matches "scope" alone.
- **m11, m15.** axf06 "model-adjusted difference"; "Your best: N" in the list.
- **Open from review 38.** Projector at 1280x720 and open views; allocate plate; phone class panels; projector histogram unit and delegate caption; console poll notice; Thaler routing and tutor misses; ai10 units; biz05 baselines; weak items (social01, social13, bz11); repeated numbers; phone slider label.
- **Gates.** 359 passed; design lint by rule {}; build current.

## Iteration 58 (2026-11-11): review 38 visual round

- **m3.** Allocate plate is one dot plot of the study's result per option; the player's points are numbers under a "Your points" header; amber only on the option that worked best; no scoring sentence (I-6 residue). Test `test_allocate_plate_is_one_dot_plot`.
- **I-3.** `fitProjector()` scales the projected page to its screen (never the console view). Open and revealed views end inside 1280x720. Test `test_projector_fits_a_720p_screen`.
- **I-4.** No hairline above the projector's right column; stat labels wrap evenly.
- **m4 to m6.** Phone class panels: allocate on a 0 to 100 scale with whole points, rank as dots on a 1-to-N axis, histogram with counts, units and the study's value named.
- **m7, m8.** Projector histogram bins carry the unit and the evidence row is named; delegate bars state their measure.
- **m9.** The console shows a reconnecting note after two failed polls.
- **Gates.** 361 passed; design lint by rule {}; build current.

## Iteration 59 (2026-11-11): review 38 m1, m2, m13

- **m13.** social01 (checked against CESifo WP 10233): scene no longer states the set-up as the answer; the two keys are distinct results (tight: clustered near the average; polarized: most chose extreme contributions); explanation adds the polarized result. social13: options differ in the finding. bz11: the claim is the false statement "a preregistered direct replication again found fewer dishonest reports". Keyed options pinned by hand in `tools/content_review38b_2026_11_11.py`.
- **m1.** A surname goes to the decision whose main paper carries it, and the answer names that paper (Thaler to Thaler & Benartzi 2004).
- **m2.** Routes `peer` and `causal`; sample-size questions for more roles. Test `test_offline_tutor_review38`.
- **Open.** Dietvorst 2015/2018 pick; "how much money was at stake"; definition questions; ai10 units; biz05 baselines; repeated numbers; phone slider label.
- **Gates.** 366 passed; design lint by rule {}; build current.

## Iteration 60 (2026-11-11): review 39

- **Major I-1, fixed.** social01 no longer states the polarized result (the key of the next path decision). Keys: tight norms cluster choices near the average; a higher group average raised contributions (Result 4, read in the published article, p. 2255; quote stored).
- **I-2.** Allocate plate: the study's value is printed on its dot; the scale spans the full track.
- **I-3.** `fitProjector()` measures the content's own bottom edge.
- **I-4, I-6.** Phone estimate histogram unit; the reconnect note is hidden in projector view.
- **I-8.** The duration decline is dropped when the summary states a duration.
- **I-9.** social13 asks about "certain preliminary rounds"; distractors are false for those rounds.
- **Other.** A 50% forecast reads "You sat on the fence."; the AI preset chip only on AI-track items; ai10 units; biz05 first-week households.
- **Sweep.** 112 decisions x 7 viewports: no content under the action bar, no text overlap in figures, no overflow.
- **Open.** Empty right column on wide reveals; charts with no stated scale (axe12, social01); repeated headline number on estimate reveals; social20, dimant-conspiracy-choice distractors, axe10 claim; Dimant surname routing with a topic word; projector histogram empty bins.
- **Gates.** 366 passed after merging duplicate CSS rules (lint, bank and browser suites rerun after the merge: 215 passed); design lint by rule {}; build current.

## Iteration 61 (2026-11-11): wide-reveal balance, stated scales, routing

- **Empty space on wide reveals (honest metric, 1440x900, 112 reveals).** Median 163 to 103 px; reveals over 150 px 59 to 33; worst 559 to 258. `balanceReveal()` picks among four placements: a full-width study band (`meta-wide`), under the figure (`meta-right`), under the text (`meta-left`), or a tall-figure layout (`fig-tall`) where card, tabs, questions and tutor run down the text column. The principle strip leaves figures that already carry a chart or task list. A first metric counted the band as both columns and overstated the gain; `scratchpad/gaps.py` measures to the band's top.
- **Scales.** Every bar chart ends on a round number with both ends labelled; `chart.axis` draws dots on a stated axis (axe12).
- **Tutor.** A topic word (authors' names excluded) outranks the author count: Dimant + masks, Dimant + hate, Dietvorst + adjust (2018), Thaler.
- **Items.** axe10 claim; dimant-conspiracy-choice distractors.
- **Projector.** Histogram shows the span of bins in use.
- **Gate.** `test_reveal_layout_sweep` (22 decisions x 5 screen sizes: nothing under the action bar, no text overlap in figures, nothing outside its figure, no sideways scroll).
- **Open.** 33 reveals still leave more than 150 px empty (widen `fig-tall`); repeated headline number on estimate reveals; social20; format mix; phone and projector estimate charts differ.
- **Gates.** 367 passed; design lint by rule {}; build current.

## Iteration 62 (2026-11-11): review 40

- **Major I-1, fixed.** The principle strip is capped at 560 px in the full-width band. Test `test_principle_strip_keeps_its_size_with_a_record` plays five decisions per principle first; earlier tests started from an empty record and never drew the strip.
- **I-2.** `fig-tall` is kept only when the text column then ends within 260 px of the figure.
- **I-3, I-6.** Signed charts end on a round negative number; axis ends print without the values' decimals.
- **I-4, I-5.** axe12 has no invented axis; social01 and dimant-polarizednorms-choice share a 0 to 3 scale (`chart.max`).
- **Classroom.** A phone that has not answered gets a notice when answers close.
- **Items.** dimant-conspiracy-choice distractor answers the question; dimant-deviant-choice manager line follows the finding.
- **Lesson.** Reviews 36 to 40: 86, 86, 85, 85, 84. Three of the last four rounds introduced a defect the next review caught. Measure layout with a record present; next round is an audit pass on review 40's remaining Minors, no new layout.
- **Open (review 40).** Allocate scale ends and zero label at 390; projector text at 720p and open-view layout; histogram bin labels; surname + topic when the author is on screen; tutor misses; dimant-hate-choice figure; ai02 follow-up and index charts; bz02 and rollout4 scenes; wording cues on choice items; Library rows.
- **Gates.** 368 passed; design lint by rule {}; build current.

## Iterations 63 to 65 (2026-11-11 and 2026-11-12)

- **Iteration 63.** Audit round on review 40's Minors: tutor glossary, replication route, same-author routing; round allocate ends; separate histogram bins; social12 measured callback rates (read in the published article); bz02 and rollout4 scenes; comparative-word gate.
- **Iteration 64.** Owner: the landing page did not say what the game is. Rebuilt: headline, two-sentence description, how a round works, the sample under "Try one now", then the paths. Credit with name, website and email on the landing page, footer and research standard.
- **Review 41 (snap63, finished on snap64): 84/100.** 0 Blocking, 1 Major (the closed-answers notice called `toast()`, an element, since iteration 62), 25 Minor. Full report: `qa/reviews/review41.md`.
- **Iteration 65.** Fixes: notice() with a detector test; near matches drop the stored Yes or No; glossary phrasings; raters from the scene; social12 follow-up, amber bar and full-text status; rollout4 scene states the design; bz02 scene without the mechanism; dimant-hate-choice figure line restored; biz02 distractor; landing label smaller than its question and the sample above the fold; strip "+N" inside the strip; zero label on phones.
- **Lesson.** Reviews 36 to 41: 86, 86, 85, 85, 84, 84. Iteration 63's content edits introduced five Minors: a rewritten scene needs the same check as an explanation (design stated correctly, no mechanism before the call).
- **Open (review 41).** Projector text at 720p; three-step block reads as a template; biz01 numbers via a secondary source; record headline minus sign; tutor misses ("Was it a field experiment?"); two-part option cue on choice items; four fact-checks the reviewer could not complete.
- **Gates.** 385 passed; design lint by rule {}; build current.
- **Published.** GitHub `eugendimant/the-human-variable` (public, MIT), `gh-pages` branch holds the built game.

## Iteration 66 (2026-11-12)

- **Owner feedback.** Question screen scales up on large screens (`fitQuestion`, CSS zoom) and breaks lines without stranded words; claims answered True or False plus how sure (stored answer stays the probability); up to seven tutor suggestions, each checked against the offline tutor; "Research by Eugen Dimant" lists every paper under its published title with a DOI link; source line, study card and tutor citations link to the DOI.
- **DOI check.** `tools/verify_dois.py`: 114 of 114 sources resolve and match their Crossref title (`qa/DOI_CHECK.md`).
- **New decisions from the owner's papers,** each read in full: repro-msci-estimate (Fišar et al. 2024), dimant-competition-choice (Huber et al. 2023), dimant-megastudy-estimate (Duckworth et al. 2025), dimant-deterrence-choice (Buckenmaier, Dimant, Posten & Schmidt 2021). 116 decisions, 113 sources.
- **Lint.** R21 measures boxes at design size (the question card is zoomed); headings use `text-wrap: pretty`.
- **Gates.** 394 passed; design lint by rule {}; build current. Not yet reviewed.
- **Handover.** `docs/HANDOVER_PROMPT.md` holds the prompt for a new project, with next steps and the evaluation method.

## Iteration 67 (2026-11-12): owner feedback on the landing page and review 42

- **Review 42 (iteration 66): 83/100.** 0 Blocking, 3 Major, 19 Minor, 3 Optional. Reviewer: a fresh Sonnet 5.5 agent (a Fable 5.2 run hit a usage limit). Full report: `qa/reviews/review42.md`. Categories: Science 13, Learning 12, Visual 12, Gameplay 13, AI and business 9, Content 8, Technical 8, Classroom 4, Accessibility 4.
- **Owner feedback.** "Orphans are a no-no"; the credit moves to the top; declutter the front page; show different studies at random. Done: credit line above the headline (not in the hero); two sentences instead of three; the steps are one line each; the decision count sits beside "Choose a path"; the sample under "Try one now" is one of seven short percent-scale estimates, random on each visit and never the one shown last (`heroPick`, `?hero=<id>` fixes it for tests); the paper list in the Dimant band shows five rows and the rest under "Show all 18 papers".
- **Orphans (rule 32, detector R34).** `src/tie.js` (shared by the game and the classroom pages) keeps the last two words of each text block together in a nowrap span. R34 flags a single word alone on the last line; tests `test_orphan_is_caught` (injected case) and `test_pages_tie_the_last_two_words`.
- **M-1, fixed.** The server strips source titles, so the served band showed 18 empty rows. The public bank now carries `bandTitles` for the owner's papers only; `test_served_landing_page_names_the_owners_papers` reads the served page. The served-page leak test exempts these titles on purpose.
- **M-2, fixed.** The venue line of each paper was `nowrap` and made the landing page 475 px wide at 390. `test_landing_page_has_no_sideways_scroll` checks ten widths.
- **M-3, fixed.** dimant-hate-choice figure note: "Share of conditional cooperators, who cooperate if the partner does."
- **Minors fixed.** m-1 and m-2 (deterrence: four parallel options, the delay lasted two rounds, experimental currency; quotes added); m-3 (competition: a distractor that tests the heterogeneity half, the authors' "suggestive evidence"); m-4 (exploratory analyses named); m-5 (at least largely reproduced); m-6 (two quotes verbatim); I-2 and I-4 (the invented plan sentence and "blind" leave); m-8 (True/False digits hidden from screen readers, `aria-valuetext` on the sureness slider); m-10 (scene wraps `pretty`); m-13 (DESIGN_RULES rule 1). Script: `tools/review42_fixes_2026_11_12.py`.
- **Open from review 42.** m-7 forecast results in a live class (two bars, True and False); m-9 and I-13 small link boxes; m-11 four-line questions; m-14 projector text 11.7 to 13.2 px at 1280x720; m-15 and m-16 tutor misses and chip fit; m-17 reveal width at 1920; m-18 content cues; m-19 two classes block each other's practice mode. Not run by the reviewer: Streamlit, most body-text fact checks, a real screen reader.
- **Lesson.** Iteration 66's DOI links and paper list were checked on the offline file only. A change that touches the public bank is read on the served page too.
- **Gates.** 399 passed; design lint by rule {}; DOI check 114 of 114 (title match); build current. Not yet reviewed (review 43).

## Iteration 68 (2026-11-12): owner's follow-up on the landing page
- **Request.** The credit line goes above the "Continue" banner, and the banner can be closed. The numbered "How a round works" box "sounds like AI speak": removed. The intro sentence already says it.
- **Done.** Credit line first; the banner has a close button (the choice is kept per path in localStorage, and a different path brings it back); the three-step box and its CSS are gone. Test: `test_resume_banner_sits_below_credit_and_can_be_closed`.
- **Note.** Review 43 was started on the iteration 67 snapshot before this change. Its landing-page findings about the step box no longer apply.
- **Gates.** See the line added after the run.
- **Front page redo (same iteration, after the owner said the page is "hella busy" and the intro reads as AI speak).** Hero now has two columns: headline, one sentence ("Every round is a real situation from a published study. Make your call, then see what the researchers found.") and Start on the left, the sample in a card on the right. Removed: the "How a round works" box, "Join a live class" in the hero, the "N decisions from N studies" note, the strips and the dark first path, the repeated sentence in the research band, the duplicate credit in the footer. The research band shows 3 papers, then "Show all". The sample's reference sits under its question and links to the paper once the player has locked the call (a link before the call would lead to the answer). The result line no longer repeats the study's number. The credit line cannot strand a word. A fresh reader (Sonnet 5.5, screenshots only) listed 12 findings; fixed: repeated result, hero jump, credit wrap, repeated band sentence, path text wrap. Not done, by choice: rewording the path blurbs (the owner's own words), "Play this path" as a link, the Continue banner wording.

## Review 43 (Sonnet 5.5 agent, on iteration 67): 81/100, 0 Blocking, 1 Major, 13 Minor
- **M-1 (introduced by iteration 67), fixed in 68.** `tieEnds` listed `summary`. Each accordion "Questions" row is a flex row, so the tied last two words sat 17 to 320 px from the rest on every reveal. `summary` is out of the list. Test: `test_tie_leaves_flex_rows_and_path_lines_alone`.
- **m-1, fixed.** The tied pair in a path's count line took the blurb's serif (`.path span` matched it). The rule is now `.path>span`; the test checks one typeface.
- **m-8, fixed.** The forecast slider says "not chosen yet" until touched. **m-11, fixed.** Every tutor chip is checked against the offline tutor, not only the last four. **m-12, fixed.** Credit links have a 32 px hit area.
- **Lesson.** The R34 detector reads the same selector list as `tieEnds`, so it cannot see damage `tieEnds` does. A selector added to the tie list needs a layout probe on the real element (flex rows especially).
- **Open from review 43.** m-2 other orphans (All decisions list, Library, rank/delegate/causal labels, phone footers, projector); m-4 projector text 10.7 px at 1280x720; m-5 live forecast bars; m-6 wide reveal hole under one column; m-7 tutor 53% useful; m-9 option cues (deterrence answer is now the shortest option, conspiracy, polarized norms, false-news, axb02, social20); m-10 closed-phase notice over live controls on phones; m-13 random sample can open on the racial-callback item. The three biggest Visual changes: scale the wide reveal like the question screen, and the landing first screen (done in 68).
- **Gates (iteration 68).** 401 passed; design lint by rule {}; build current; tutor golden unchanged. The lint caught the second half of M-1 at once: with `summary` out of the tie list, two accordion questions at 390 px ended on one word. The question text now sits in a span that is tied. DOI check not rerun (no bank or source change since 114 of 114). Not yet reviewed (review 44).

## Iteration 69 (2026-11-12): owner's note on the front-page sample
- **Request.** "Try again" on the front-page sample only gave the same question again, with the answer known. Removed; "Play five more" stays. Test: `test_front_page_sample_has_no_try_again`.
- **Owner's wording (iteration 69).** Headline "How well can you predict people’s actions?" and intro "Each round presents a real-life situation, from a published research study, that you are asked to predict. Once you have made your prediction, you will then be shown what the researchers actually found." Both are the owner's text, kept word for word.
- **Gates (iteration 69).** 402 passed; design lint by rule {}; build current; tutor golden unchanged. Not yet reviewed (review 44).

## Review 44 (Sonnet 5.5 agent, on iteration 69): 81/100, 0 Blocking, 0 Major, 12 Minor
- **Verified fixed:** M-1 accordion, m-1 typeface, m-8 slider text, m-12 link size; landing page has no sideways scroll and no stranded word at six widths; the Continue banner closes.
- **Open, in the reviewer's order:** m-I1 the headline wraps with "predict" alone on a line (the owner's words; layout only); m-I2 the locked sample card runs below the fold at 1440x900; m-1 stranded last words everywhere except the landing page (All decisions list, Scope tab, reveals, projector, phones: 54 of 416 plays hit one; no gate sees them); m-2 projector text 10.7 px; m-3 live forecast histogram; m-4 closed-phase toast over the options; m-5 wide reveal gap on 13 of 26; m-6 tutor 49% useful; m-7 served tutor drops paragraph breaks; m-8 tutor chips give the wrong fact on some decisions; m-9 option cues; m-10 sample pool includes the racial-callback and Saudi-men items; m-11 record page columns; m-12 three decisions scroll at 1280x720.
- **Score trend:** 84, 84, 83, 81, 81. The Visual score (11 of 15) and Learning (12) hold the total down. The next iteration goes after the global orphan class (m-1) with a detector that reads the real layout of every page, not a selector list.

## Iteration 70 (2026-11-12): orphans everywhere (review 44, m-1)
- **Cause.** `tieEnds` worked from a list of selectors, and the R34 detector used the same list, so neither saw the other pages (All decisions list, Scope tab, projector, phones: 54 of 416 plays).
- **Fix.** `tieEnds` now walks every text block of the page (blocks of three words or more; flex and grid boxes, buttons, code and inputs are skipped; a pair over 26 characters is left alone). R34 now reads the real layout of every element, with no selector list. A first lint run with the new detector found one stranded word (`p.gh-gap`, a three-word block the old length test skipped); the test is now "three words or more".
- **Gates.** See the line below.
- **Gates (iteration 70).** 402 passed; design lint by rule {} with the all-element R34; build current; tutor golden unchanged. Not yet reviewed (review 45).

## Iteration 71 (2026-11-12): small fixes from review 44
- **m-4 fixed.** Notices (the closed-phase message on a phone) appear at the top, under the bar. At the bottom they sat on the options and the action bar.
- **Decided, not changed.** m-10 (the sample can open on the racial-callback or the Saudi-men item): the owner saw both in his own screenshots and raised no objection, and they are two of five items in the sample pool, so they stay. m-I2 (locked card below the fold): the card ends at 760 px of 900 for the shorter items; no change.
- **Still open from review 44:** m-2 projector text (`fitProjector` zooms the page down to 0.6 when the content is taller than the screen; the fix is a more compact projector layout, not a bigger zoom floor), m-3 forecast bars, m-5 wide reveal gap, m-6 to m-8 tutor, m-9 option cues, m-11 record columns, m-12 three decisions scroll at 1280x720.
- **Gates (iteration 71).** 402 passed; design lint by rule {}; build current; tutor golden unchanged. Not yet reviewed (review 45).

## Iteration 72 (2026-11-13): graded credit for estimates (owner's question)
- **Question.** "Does being inside the band somehow give you more points?" Before: any call inside the shaded band scored 100, so 15 and 13 against a study value of 13 (band ±3) scored the same; outside the band credit fell from 100 to 0 over one more band width. Closeness inside the band did not count.
- **Change.** An estimate now scores 1 at the study value, 0.5 at the edge of the band, and 0 at twice the band, falling evenly (half a slider step is free, so the nearest slider position to the study value scores 1). The band still decides "Matches the study" and feeds the calibration plot (`correct` is unchanged). Done in `src/scoring.js` and `server/scoring.py` (Streamlit uses the server's function), the "How scoring works" text, the "Partly right" threshold for estimates (0.2), and the estimate baseline `EST_BASE` (0.35 to 0.245: the best blind strategy now averages 0.242, constant guess). Test: `test_estimate_credit_is_graded_by_distance` (page and server agree; every point closer earns more, inside the band too).
- **Effect on stored records.** Scores already saved in a browser keep their old value; new calls use the new rule. Skill above guessing is rescaled by each record's own baseline.

## Iteration 72, part 2: projector (review 44, m-2), partial
- **Measured** at 1280x720 on three decisions (probe in the scratchpad): the page was zoomed to 0.77 on the open view of the deterrence item with 120 px of empty screen below; the smallest texts were 10.7 px (join line, buttons) on open and 11.2 px (the "study's answer" tag) on reveal.
- **Changed.** `fitProjector` refines the zoom until the content ends just inside the screen (0.77 to 0.80 with larger type; it was 0.77 with small type); the open view gives the question 1.9 of 2.9 columns; scene 19 to 26 px, options 21 to 30 px, chrome and labels 17 px. Smallest text on screen now: 13.7 px open, 12.4 px reveal (was 10.7 and 11.2). Body paragraphs of the reveal are still 13 to 15 px on screen. A projector layout built for 720p (the reveal as one column of short blocks) is not done.
- **Gates (iteration 72).** 403 passed; design lint by rule {}; build current; tutor golden unchanged. Not yet reviewed (review 45).

## Review 45 (Sonnet 5.5 agent, on iteration 72): 79/100, 0 Blocking, 0 Major, 11 Minor
- **Held up:** estimate scoring (page and server agree on 200 cases; baseline right; text matches the code); True/False scoring and storage in 12 cells; 500 plays with 0 sideways overflow, 0 clipped text, 0 page errors; stranded-word plays fell from 13% to 10%; live class with no leak, 120 joins accepted, closed phase disables Lock; all 26 stored quotes of the iteration-66 decisions verbatim.
- **Introduced by 70 to 72:** m-I1 the all-block tie leaves "least" alone mid-heading (repro-msci-estimate); m-I2 the meta-perception-causal reveal title breaks one word per line; m-I3 wide-reveal column gap median about 205 px (21 of 25 items at 100 px or more); m-I4 the landing h1 breaks "predict" alone (owner's wording; layout only); m-I5 live forecast result still a ten-bar histogram, "Class median 100%" under a false claim; m-I6 projector at 1280x720 still has text down to 11.6 px and dead space.
- **Not introduced:** tutor 24% fully answered and 44% partly (75 questions of the reviewer's own); served tutor drops paragraph breaks (25 of 75); lies-in-disguise study line is the placeholder "see the paper"; dimant-competition-choice explain states the effect as established where the paper says "suggestive"; option cues on deterrence; sample pool can open on the racial-callback or Saudi-men item.
- **Score trend:** 84, 84, 83, 81, 81, 79. Reviews 43 to 45 were by different agents, and the spread between agents (2 to 3 points) is as large as the movement. No review since 36 has found a Major in a core flow, but the Visual (10 to 11 of 15) and Learning (11 to 12 of 15) scores have not moved. The three changes the reviewer names for Visual: align the wide-reveal columns, one line-breaking rule for headings, a projector layout built for 720p.

## Iteration 73 (from review 45: m-I1, m-I2, m-I4, m-I5)
- **Headings.** The tied pair is kept in headings, but a heading with a one-word line is set smaller (5% steps, up to 34%) until no line holds one word (`fitHeadings` in `src/tie.js`; runs after the tie, after the fonts load and after a resize). A tied pair wider than its box is put back. This fixes the lone "least" (repro-msci-estimate), the one-word-per-line title (meta-perception-causal) and the stranded "sign." / "originals." in the forecast claims. The reveal is now balanced after the tie and the heading fit, because the caption wrapped and the study card overlapped the facts row (found by lint R31 on reveal-dimant-requiem-forecast).
- **Landing headline.** Three nowrap phrases: "How well can / you predict / people's actions?" (m-I4).
- **Live forecast result (m-I5).** Two bars, "Said true (above 50)" and "Said false (below 50)" (plus "Said 50, unsure" when used), the side the study found marked, a count on each. The median of probabilities is gone. Test `test_live_forecast_result_is_two_bars`.
- **Gates (iteration 73).** 404 passed; design lint by rule {}; build current; tutor golden unchanged. Not yet reviewed (review 46).

## Review 46 (Sonnet 5.5 agent, on iteration 73): 79/100, 0 Blocking, 0 Major, 16 Minor, 4 Optional
- **Held up:** headings (500 plays, 5 widths: no one-word line in any h1 to h3, no overflow, no clipped text); estimate scoring (250 of 250 cases, page equals server); live class with no leak; axe 0 violations on 54 scans; 404 tests; all 18 Dimant DOIs resolve; the four iteration-66 decisions match their papers.
- **Introduced by 73:** m-I1 phones still show the forecast histogram and "Class median"; m-I2 the "The claim is" label wraps to "The / claim is"; m-I3 one-word lines outside headings (bz04 gap "20.3", civic-wallet "46%").
- **Open:** tutor 37% direct; served tutor drops paragraph breaks (30 of 66); chip "How long did the effect last?" wrong on about 14 of 19 decisions; placeholder "see the paper"; dimant-competition-choice wording; option cues; wide reveal gap (22 to 26 of 100 plays at 100 px or more); reveal narrower than the question screen; record page columns; projector at 1280x720; dimant-motivated broken sentence; rule 33 does not match the page.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79.

## Iteration 74 (from review 46)
- **Phones (m-I1).** The live forecast result on a phone is the same two bars as on the instructor page and projector ("Said true", "Said false", the study's side marked, no median). Test extended.
- **Labels (m-I2, m-I3).** "The claim is" and the other label cells stay on one line; the gap text ("20.3 days off") is one unbreakable phrase.
- **Tutor (m-2, m-3).** A served answer starts a new paragraph at each labelled part ("Design:", "What the study covers:", "In practice:", and others), as the offline answers do. The chip "How long did the effect last?" shows only where the decision has a follow-up about duration (it was wrong on about 14 of 19 decisions).
- **Content (m-11).** dimant-motivated-estimate: "a self-serving tilt in the sources they consulted" (`tools/review46_fixes_2026_11_13.py`). Not changed: dimant-competition-choice (RULE 0 caution; its follow-up already quotes the authors' "suggestive evidence"), lies-in-disguise placeholder (needs a verified source quote).
- **Rules (m-12).** DESIGN_RULES 33 now matches the page (the owner's lede, no numbered steps).
- **Tried and reverted (m-8).** Zooming the reveal like the question screen: CSS zoom broke the vw-sized verdict numbers (label overlap, 30 lint hits), the plate's "You were 100% sure" and three tests. The reveal keeps its own column. `balanceReveal` now divides its margin by the zoom so a future zoom is safe.
- **Gates (iteration 74).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 47).

## Review 47 (Sonnet 5.5 agent, on iteration 74): 80/100, 0 Blocking, 0 Major, 17 Minor, 4 Optional
- **Held up:** 405 tests, lint clean, axe 0 violations on 42 scans; four iteration-66 decisions match their papers (26 of 26 quotes verbatim); True/False scoring; no leak by any route in a live class; 120 joins accepted; no one-word line in any heading, label or gap text.
- **Introduced by 74:** served tutor paragraphs differ from the offline tutor on 22 of 66 answers (same words); duration chip wrong on ai10; "46%" alone in a civic-wallet list item.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80.

## Iteration 75 (from review 47)
- **Duration chip.** Shown only where a follow-up asks outright "Did the effect last/fade/persist?" or "How long did the effect last?" (ai10's "When did the preference fade?" no longer counts).
- **Record page.** After the page is built, "By area" moves under "This round" when the left column is taller (`balanceRecord`).
- **Not changed:** the reveal's width (zoom tried and reverted in iteration 74), wide-reveal gaps on meta-left items, projector at 1280x720, option cues, tutor coverage (41% direct; needs new checked follow-ups with source quotes), hedged-forecast wording (Brier rule: a 60% wrong call scores 0.28 by design).
- **Gates (iteration 75).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 48).

## Iteration 76 (owner, 2026-11-13: "improve the upper part of the landing page so that it's all in one line and not crowded"; review 47, m-1)
- **Header.** The credit line sits in the header bar between the logo and the menu, on one row, at 1260 px and wider (sentence and website; the email stays in the page footer). Measured at 1260, 1300, 1440 and 1920 with "Join a class" showing: the credit ends at least 28 px before the menu starts and the menu stays on one line. Below 1260 px the page carries the credit as before.
- **Tutor routes (m-1).** `tools/tutor_routes_review47_2026_11_13.py` widens five routes (who took part / subjects; "was it a field/lab/online study"; "where can I read the paper"; "one-line takeaway"; "how reliable / how sure can I be"). Page and server read the same table. Golden regenerated: 29 answers changed, all of them "Is this a lab study?" (now the design and sample line, was the scope line).
- **Gates (iteration 76).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 48).

## Review 48 (Sonnet 5.5 agent, on iteration 76): 81/100, 0 Blocking, 0 Major, 14 Minor, 4 Optional
- **Held up:** header bar at nine widths (no overlap, no wrap, with and without "Join a class"); duration chip right on both decisions that show it; 26 of 26 quotes for the iteration-66 decisions; all 114 DOIs resolve; True/False scoring 12 of 12; no leak; 120 joins and answers; 240 plays with 0 stranded words.
- **Introduced by 76:** the bare word "subjects" stole questions; "how reliable" matched other subjects ("How reliable is ChatGPT at writing?"); "original paper" missed.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80, 81.

## Iteration 77 (from review 48)
- **Tutor routes.** "subjects" alone is gone (only "who were the subjects"); "how reliable" needs "this / it / the study / the finding / the result / the evidence / the paper / the effect"; "original, full, actual, published paper" accepted. Same script, idempotent; golden unchanged.
- **Paragraphs (m-2, again).** Both tutors now give the same words; the page makes paragraphs from labels at render time for both, so the offline and the served answer look the same. (Old unlabelled breaks in the offline answers are gone.)
- **Not changed:** meta-left hole beside the figure, reveal width, projector 1280x720 type, option cues, biz02 and bz14, landing lede rag, a phone that has not answered keeps live controls after answers close (server rejects it).
- **Gates (iteration 77).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 49).

## Iteration 78 (review 48, m-4)
- **Reveal width.** The reveal column is as wide as the window allows up to 1480 px (at least the old 1240 px), instead of a fixed 1128 px; at 1920 px it is 1368 px wide against the question screen's 1808. The principle strip is capped at 640 px (was 560; the test bound moved with it). Text lines keep their 38 em measure.
- **Gates (iteration 78).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 49).

## Review 49 (Sonnet 5.5 agent, on iteration 78): 80/100, 0 Blocking, 0 Major, 13 Minor, 3 Optional
- **Held up:** 260 plays over 26 decisions, 0 errors, 0 overflow, 0 stranded words, 0 clipping; axe 0 violations on 52 scans; header credit clean from 1260 to 1380; all 26 quotes for the iteration-66 decisions verbatim; no leak; 120 joins; True/False 12 of 12.
- **Open:** the reveal is wider only from 1440 px up and the hole beside the figure grew to 291 px at 1600 and 1920 on axb05; projector 11.6 px; record page blank space; tutor 28% direct (own wording); one wrong tutor answer ("Was cheating real?"); option cues and strawmen; repro-msci question hid the counting rule; false-news-spread key named novelty but the explain did not.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80, 81, 80.

## Iteration 79 (from review 49)
- **Content.** repro-msci-estimate question now states the counting rule ("counting inaccessible data as not reproduced", 21 words, inside the 22-word cap); false-news-spread explain names the novelty finding ("false news was also more novel than true news"; the quote is already in evidence.json). Script: `tools/review46_fixes_2026_11_13.py` (idempotent).
- **Tried and not done:** moving the Questions block into the hole beside the figure (needs the tabs and the Ask card split across two columns; high risk for a Minor).
- **Gates (iteration 79).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 50).

## Review 50 (Sonnet 5.5 agent, on iteration 79): 82/100, 0 Blocking, 0 Major, 14 Minor, 4 Optional
- **Held up:** 390 plays, 0 errors, 0 overflow, 0 stranded words; axe 0 violations on 44 scans; 80 of 81 quotes verbatim (one footnote number in the PDF text); page and server tutor identical on 80 questions and 716 chips; no leak; 120 joins; both iteration-79 content changes right against the paper.
- **Introduced by 79:** I-1 the repro-msci question became a 6-line heading at 1280x720; I-2 false-news-spread follow-up repeated the explain and the key stated a mechanism the paper only suggests.
- **Open:** tutor 22% direct (3 wrong), causal reveal hole 290 px at 1920, projector 11.6 px, five predict screens scroll at 1280x720, phone that has not answered keeps live buttons, landing lede rag, option and frame cues, a wrong forecast can show a small positive score by design, 11 px SVG text on a phone reveal.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80, 81, 80, 82.

## Iteration 80 (owner, 2026-11-13: "make my name clickable and have the email address underlying it"; review 50)
- **Credit.** "Dr. Eugen Dimant" is the mailto link (underlined, title "Email Eugen Dimant") in the header bar, the page credit and the footer; the separate email text is gone from those three places (the research-standard paragraph still lists it). The footer's website link is tied to "Pennsylvania." so it never stands alone on a line at 390 px.
- **I-1.** The counting rule moved from the question to the scene of repro-msci-estimate; the question is back to its original 15 words.
- **I-2.** The explain of false-news-spread is back to its earlier wording; the key now reads "False stories were more novel, and humans spread them" (what the paper measured); the pin file is updated. Script `tools/review46_fixes_2026_11_13.py`, idempotent.
- **Gates (iteration 80).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 51).

## Iteration 81 (review 50, m-3 and m-6)
- **Landing lede.** The owner's text is unchanged. It is cut into six phrases that wrap as wholes where the column is wide enough (1100 px and wider, and 600 to 900 px). Between 900 and 1100 px and below 600 px it wraps freely (the spans are `display:contents` there). Six short lines at 1440 px; no line starts with "from a" and none ends with "that you are".
- **Projector.** Labels, units and tags are 17 px before the zoom. Smallest text at 1280x720 on the open view of the allocate item is 13.9 px (was 11.6); on the reveal 13.3 to 15 px.
- **Gates (iteration 81).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 51).

## Review 51 (on iteration 81): 82/100, 0 Blocking, 0 Major, 13 Minor, 4 Optional
- **Held up:** 400 plays, 0 errors; axe 0 violations on 61 scans; page and server tutor identical on 106 questions; all 26 stored quotes verbatim; no answer leak by any route.
- **Introduced by 81:** the projector text is 12.9 to 17 px, not a 17 px floor (body text about 13 px). The earlier ledger line "17 px" applies to labels, units and tags only. Optional: the false-news-spread key is now the longest option.
- **Tutor (m-1):** 46% direct, 27 partial, 26 miss, 4 wrong.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80, 81, 80, 82, 82.

## Iteration 82 (review 51, m-1)
- **Four wrong tutor answers fixed** by `tools/tutor_review51_2026_11_14.py` (data only): ai10 experts question now gets the experts follow-up (`subgroupFollow` gains `^did (experts?|...)`); social04 follow-up reworded "Did beliefs change later in the semester?" so duration questions find it; facebook-deactivation gains "How long did people stay off Facebook?"; axb01 gains "When does a human reviewer help?" (answer from the stored explain). Golden files regenerated.
- **Gates (iteration 82).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 52).

## Review 52 (on iteration 82): 81/100, 0 Blocking, 0 Major, 12 Minor, 5 Optional
- **Held up:** 580 plays, 0 errors; axe 0 violations on 50 scans; page and server tutor identical on 126 questions and 716 chips; no answer leak; Crossref has all 114 DOIs; the four iteration 82 tutor fixes hold for the wordings tried (axb01 misses two other wordings).
- **Open:** tutor about 22% direct with 4 wrong (genai2, axf06, rollout1, axb15); record page column holes at 1 to 7 calls; causal reveal hole 290 px at 1920; projector body text about 13 px; closed phone keeps live controls; five predict screens scroll at 1280x720; axb12 scene names the mechanism; biz08 'who took part' answer is 'see the paper'.
- **Score trend:** 84, 84, 83, 81, 81, 79, 79, 80, 81, 80, 82, 82, 81.

## Iteration 83 (review 52, m-5 and m-8)
- **Record page.** With fewer than eight calls the record is one centred column (`rec-stack`), so neither side leaves a hole.
- **axb12.** The scene no longer says the platform delivers the ad "cost-effectively" (`tools/review52_fixes_2026_11_14.py`).
- **Gates (iteration 83).** 405 passed; design lint by rule {}; build current. Not yet reviewed (review 53).
