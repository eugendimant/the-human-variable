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
