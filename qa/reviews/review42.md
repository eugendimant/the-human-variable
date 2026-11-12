# Independent review 42 (snap66, iteration 66)

**Score: 83/100.** 0 Blocking, 3 Major, 19 Minor, 3 Optional.

Reviewer: a fresh Sonnet 5.5 agent on a `git archive` snapshot of commit 4bf1ab4 (a Fable 5.2 run hit a usage limit before it wrote a report).

Reviewer note: two earlier runs of this review were cut off; this report reuses their raw logs (pytest.log, lint.log, sweep_*.json, tf.log, zoom.log, class_log.txt, tutor_out.json, chips_out.json) and adds my own reruns and checks, listed in `notes.md` in the same folder. Every number below was observed in those logs, in my reruns or in a screenshot I opened.

## Score

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All 20 stored quotes of the four new decisions are verbatim in the supplied PDFs and every number checks; two older Dimant quotes are not verbatim, and the iteration 65 caption on dimant-hate-choice names the wrong quantity. |
| Learning | 15 | 12 | Predict, commit, reveal, calibrate works and True/False plus "how sure" scores correctly in all 16 combinations; the new deterrence item has a form cue and leaves out that "delay" means two rounds. |
| Visual | 15 | 12 | Reveal and question screens are calm and measured clean (0 overflow, 0 clipped text in 240 sweep runs); the served landing page has empty paper titles in the research band and scrolls sideways on every phone width. |
| Gameplay | 15 | 13 | 116 decisions, 8 formats, working scaled question screen; 4-line questions leave a stranded last word at 1280 to 1920, and the landing hero strands "do?". |
| AI and business relevance | 10 | 9 | Strong AI and management coverage; the four new items are business-relevant, though two answers (reproducibility, deterrence) are framed more broadly than the lab or journal scope. |
| Content | 10 | 8 | 48 decisions read; mostly sound and honest about non-significance; a few overstated or loosely scoped lines (listed). |
| Technical | 10 | 8 | 394 tests pass, lint 0, build current, server limits sound at 120 students; the test suite did not catch the blank served band or the 85 px sideways scroll. |
| Classroom | 5 | 4 | Live class (3 phones, closed phase, dropped link, 120 joins) held with no leak on any route; projector text is 11.7 to 13.2 px at 1280x720; forecast results are shown as a probability histogram. |
| Accessibility | 5 | 4 | axe 0 violations on every screen scanned; slider lacks aria-valuetext and True/False buttons are named "1True" and "2False". |
| **Total** | **100** | **83** | Review 41 was 84. Two functional landing defects introduced in iteration 66 cost more than the fixes from iteration 65 gained. |

## Gate counts (item 1)

- `python -m pytest -q`: 394 passed (1201.86 s), pytest.log.
- `python3 tools/design_lint.py`: "by rule: {}" (lint.log, plus my rerun in work/ printed no violation).
- `python3 src/build.py --check`: "built pages are current" (my rerun).
- axe 4.x (tests/vendor/axe.min.js, wcag2a/2aa/21a/21aa/22aa and best-practice): 0 violations on home 1440 and 390, play and reveal for 12 decisions at 1440 and 390 (tf.log "AXE TOTAL VIOLATIONS 0"), the three reveal tabs, record, library, studies, console setup, lobby and reveal, projector open and reveal, phone lobby, question, sent and reveal (class_log.txt, 14 scans, all 0).
- `tools/verify_dois.py` (run in the work copy, network reachable): "114 sources; 0 to check". This is a title match against Crossref, not proof that each DOI is the paper behind the decision.

## Introduced (iterations 65 and 66)

### Major

**M-1. The served landing page shows the 18 "Research by Eugen Dimant" paper rows with empty titles.**
- Where: `server/app.py:25` (`SOURCE_PRIVATE = ('takeaway', 'flags', 'title')`) and `:36-37`, used by `public_source()`; band built in `src/app.js:207`.
- Observed: `scripts/band.py` on file:// returns 18 rows with titles ("Competition and moral behavior: A meta-analysis of forty-five crowd-sourced experimental designs", ...), row height 66 to 87 px. On the served page the same 18 rows have `strong.textContent === ''`, only "Dimant (2024), Management Science" remains, rows are 45.75 px tall. Screenshot `shots/band_served_1440.png` (a column of grey lines, no titles) against `shots/band_file_1440.png`.
- Why it matters: the owner decided the band shows the real titles with DOI links. On the page students actually use, it shows 18 unlabelled links. The offline file is fine, so the 394 tests never saw it.
- Fix: serve a separate public list for the band (id, title, authors, year, venue, DOI) for the 18 Dimant sources. The owner already accepted that these titles are visible. Keep hiding titles for sources whose decision is unplayed elsewhere. Add a served-page test that asserts every band row has a non-empty title.

**M-2. The landing page scrolls sideways at every phone width and clips the research band.**
- Where: `src/app.css` `.dimant` grid (the band's column is 459 px wide).
- Observed (`scripts/ov390.py`, `zoom.log` LAND rows): at a viewport of 390, `scrollWidth` is 475 (overX 85); at 360 it is 475 (115 over); at 430 it is 476. Same on file and served. 77 elements extend past the viewport (band div, h2, p, ul, li, a, strong). Screenshot `shots/band_file_390_view.png`: titles are cut at the right edge ("Promoting Safe Opioid Disposal: Experimental Evi", "Strategic Behavior with Tight, Loose, and Polarize").
- Why it matters: the first page a phone visitor sees can be dragged sideways and the paper titles cannot be read. The 240-run sweep did not open the landing page, so it was missed.
- Fix: `.dimant>div{min-width:0}` and `grid-template-columns:minmax(0,1fr)` below 900 px, and let `.paper-list a` wrap (`overflow-wrap:anywhere`). Add `docEl.scrollWidth <= innerWidth` for the landing page at 360, 390 and 430 to tests/test_browser.py.

**M-3. dimant-hate-choice: the figure note now misnames the measured quantity (iteration 65, I-6 fix).**
- Where: item `dimant-hate-choice`, `chart.note`: "Share who cooperate when they expect the partner to. The drop is about as large for a painting-taste outgroup as for a political one." Reveal screenshot `shots/sweep/file_1920_rec_dimant-hate-choice_r.png`.
- Observed: the paper (Dimant 2024, pp. 16-17) plots the fraction of conditional cooperators: 72.8% to 59.0% for Trump views, 73.2% to 62.4% for painting taste (p = 0.035, differences "indistinguishable"). That is a preference measure ("cooperate if the partner does"). Review 41 proposed "Share who cooperate if the partner does"; the fix instead describes the expectation mechanism the item says is not measured here.
- Why it matters: the item teaches "expectations, not preferences, drove the gap". A caption that calls the preference variable "cooperate when they expect" blurs that exact distinction.
- Fix: "Share of conditional cooperators (cooperate if the partner does)". Keep the second sentence, which is accurate.

### Minor

- **m-1. dimant-deterrence-choice: the correct option has a form cue.** Options (shuffled in play): "The faster the verdict and the fine, the stronger the deterrence", "The longer ... delayed, the stronger the deterrence", "An immediate verdict with a delayed fine", and the answer "Verdict and fine both immediate, or both delayed as far as possible". Two options mirror each other; the answer is the only two-part, "or" option. A test-wise player eliminates the mirror pair and takes the odd one. The ledger already lists "two-part option cue on choice items" as open, and this adds a fresh instance. Fix: write all four as parallel single clauses, for example "Deterrence was strongest at no delay and at the longest delay", "... at the shortest delay only", "... at the longest delay only", "... at a medium delay".
- **m-2. deterrence: scope and wording.** `scripts` check against Buckenmaier et al. Table 1: the four cells are IR-ND, IR-D, DR-ND, DR-D with a delay of two rounds inside one 28-round card game, and fines are experimental currency. The scene says "how soon" and the boundary "monetary fines"; nothing says the delay is two rounds. The implication ("compliance process") reaches further than the lab. The paper itself lists real-money delay as a limitation, and its conclusion says the timing of the verdict alone had no effect. Fix: scene "waited two rounds", boundary "Delays of two rounds within one lab session; fines in experimental currency." The option wording "the longer ... the stronger" reads as a dose-response, but there are only two levels per dimension.
- **m-3. competition: omitted caution and a centroid answer.** Paper: approach A is "suggestive evidence" (P = 0.008 against a stricter threshold), approach B "statistically significant"; the follow-up "excludes zero" and the answer state it flatly. Option 3 (answer) shares a feature with each of the other three (small, adverse, disagreed widely), the classic test-wise pick. Fix: add "the authors call approach A suggestive" to the follow-up; make one distractor "A small adverse effect, and the designs agreed closely".
- **m-4. megastudy: exploratory results stated as findings.** The 1.89%, 2.26% and 8-week persistence are "exploratory analyses" in the abstract; the explain and follow-ups drop the word. Fix: add "in exploratory analyses".
- **m-5. repro-msci: question says "reproduced", the paper says "fully or largely reproduced".** The 68% is for all assessed articles under the 2019 policy (text: "about 68% could be at least largely reproduced"); the stored abstract quote says "all articles in our sample". Fix: "what share could be fully or largely reproduced".
- **m-6. Two evidence quotes are not verbatim** (the content rule says verbatim): `dimant-hate-choice` "ingroup-love occurs in the perceptional domain whereas outgroup-hate occurs in the behavioral domain (how one helps/harms/cooperates with others)" drops "(how close one feels toward others)," without an ellipsis; `dimant-masks-forecast` "(r(28) = -0.63, p = 0.0003)" drops ", t(26) = −4.12," (and uses a hyphen for the minus). Fix: restore the text or add an ellipsis.
- **m-7. Forecast results in a live class show a probability histogram, not True/False.** `shots/class/console_rev_bz02.png`: bins "0 to 9% ... 60 to 69%", "the claim is false" tag on the first bin, "Class median 35%" with no unit; the phone panel says "1 | 1 | 0% | 100% | The claim is false | Class median 35%". Students said True or False; the instructor wants "x said True, y said False, median confidence". Fix: two bars (True, False) with the correct side marked, plus "median sureness".
- **m-8. True/False controls and screen readers.** `tf.log`: slider has `aria-label` "How sure are you?" but no `aria-valuetext` (reads "60", not "60 percent", with range 50 to 100); the buttons' accessible names are "1True" and "2False" (hotkey digit fused with the word). Fix: `aria-valuetext="60 percent sure"`, hide the digit from the accessible name (`aria-hidden` on the digit span, `aria-keyshortcuts="1"`).
- **m-9. The new DOI links in source lines are 15 px tall at 390** (`sweep_file.json` smallTargets: 194 entries, e.g. "Dimant et al. (2022), Sc..." 15 px). Inline links are exempt from WCAG 2.2 target size, but on a phone they sit in a dense line. Fix: 24 px line boxes for `.study-line a`.
- **m-10. Question scene is `text-wrap: balance` (iteration 66)** and leaves visible gaps: `shots/sweep/file_1280_fresh_repro-msci-estimate_p.png` shows the first two lines of the scene about 90 px short of the column edge. This is a paragraph, not a heading, but DESIGN_RULES rule 11 says balance leaves "lines short and space empty". Fix: `text-wrap: pretty` for the scene.
- **m-11. Stranded last words persist on the question screen.** The sweep's own detector flags "reproduced?" alone on line 4 at 1280, 1440 and 1920 (repro-msci), "debates at shifting agreement?" (4 lines), "people lie and misreporting?" and others: 19 distinct question or title strandings across the widths, plus reveal titles ("…68% could be reproduced [2 lines]", "…unwillingness, drove the gap [3 lines]"). Owner decision is `pretty`, not `balance`; `pretty` does not prevent a one-word last line in Chromium when the line is short. Fix: shorten the four-line questions (repro: "What share of articles under the policy could be reproduced?") rather than relying on wrapping.
- **m-12. Landing hero strands "do?" on its own line at 1440 and 1920** (h1 60 px, 3 lines; `shots/land_file_1440_fold.png`) and the right column (three steps) ends at y = 485 while the left runs to y = 680, leaving about 195 px empty. Fix: cap the h1 at two lines ("How well do you predict / what people do?" at 52 px).
- **m-13. Stale design documents.** `qa/DESIGN_RULES.md` rule 1 still names "Try one now" as a forbidden label above a heading, while the page keeps it as a 14 px section label (I-10 asked for both documents to be updated; TUFTE_PASS was, DESIGN_RULES was not).

### Verification of iteration 65 fixes (review 41, I-1 to I-13, m1)

| Item | Result | Evidence |
|---|---|---|
| I-1 closed-answers notice | Fixed | class_log: phone 3 shows "Answers are closed for this decision. The evidence appears when your instructor reveals it."; a late submit shows "Responses are closed for this decision"; no page error on any phone. |
| I-2 rollout4 scene | Mostly fixed | Scene now reads "some practiced math with unrestricted GPT-4, and everyone then took exams without it". The invented "Your plan gives new hires the same unrestricted access" remains. |
| I-3 bz02 scene | Fixed in the scene | "Each one estimated its campaign's return on investment." The title "The noisy ROI test" still hints at the answer; it is not on the question screen, but it is in the Library and record. |
| I-4 ai02 "blind" | Not fixed at the source | The tutor now answers "From the study's setup: Independent professionals graded the finished work blind." (agrees with the scene) but evidence.json has three ai02 quotes, none about blind grading. Store the methods quote or drop "blind" from scene and implication. |
| I-5 social12 | Fixed | Tutor "What were the actual callback rates?" returns "9.65% ... 6.45% ... 3.20 percentage points"; source status now `verified_full_text`; the 6.45 entry is still stored as "printed ... (9.65 minus 3.20)", a derivation. |
| I-6 hate-choice figure | Not fixed correctly | See M-3; title unchanged and still 3 lines at 390. |
| I-7 "+N" overflow label | No defect seen | 0 clipped texts outside screen-reader spans in 480 reveals (sweep_*.json `clipped`), with a record present at all five widths. |
| I-8 zero label at 390 | Fixed | `shots/sweep/file_390_rec_axb08_r.png` shows "-20%   0   100%". |
| I-9 820 px gap | Fixed | `shots/land_file_820_full.png`: no band between question and slider. |
| I-10 label larger than its question | Fixed on the page, not in DESIGN_RULES | h2 14 px, question 23 to 34 px; see m-13. |
| I-11 sample above the fold | Partly | "Try one now" top is 601 px at 1280x720 (was 720) and 723 at 1440x900 (was 794), but the slider is at 818 and 950, both below the fold; the h1 is 3 lines at 1440. |
| I-12 stock three-step block | Not addressed | Unchanged (ledger lists it as open). |
| I-13 credit links 18 px | Not fixed | `zoom.log` LAND: links 18 px high at all widths. |
| m1 "Did the effect last?" | Fixed | Tutor on axb15 returns "The reduction in belief persisted at the two-month follow-up." with no leading "No."; the megastudy's stored "Did the effect last?" keeps its "Yes." |

## Findings that are not introduced

### Minor

- **m-14. Projector text is below 14 px at 1280x720** (class_log "PROJ"): smallest rendered text 11.7 px (allocate, open), 12 px (rank, open), 12.8 px (reveals); "Students join at / with code" is 12 to 13.6 px; 14 px only at 1920x1080. 13 to 15 of 18 text nodes are under 18 px in the open phase. Projectors are read from the back of a room. Fix: projector CSS minimum 20 px for everything in the open phase, and a 28 px join line.
- **m-15. Tutor misses on my own wording (75 questions, page and server identical in 75 of 75).** Fully useful 56/75 (75%); an honest fallback that still shows the finding adds 13 (92% useful or honestly deferred); six misses the stored data could answer: "what happened with repeat offenders" (deterrence follow-up exists, answer returned the headline instead), "what's the difference between reproducing and replicating" (repro-msci has the follow-up "Is reproduced the same as replicated?", the tutor returned scope text), "who checked the papers" (700 reviewers is in the design line), "what is a norm" and "What is variance?" (social01: returned the scene text), "what is p-hacking" (bz11, fallback). Correct fallbacks: cheating rate per group, how to measure ROI, who is Eugen Dimant, joke, weather.
- **m-16. Suggestion chips (116 decisions, 6 or 7 each, 0 miss answers) include a few poor fits.** repro-msci "Has it been replicated?" answers "Only 12% of articles voluntarily provided replication materials" (a non sequitur); "How would I test this in my company?" returns the generic "Run a small randomized pilot" for a reproducibility audit and a deterrence experiment; "Who took part in the study?" for articles as units. Chips appear only after the reveal (`src/app.js:424`), so none leaks before the call.
- **m-17. Reveal is capped at about 1130 px at 1920** (`shots/sweep/file_1920_rec_dimant-hate-choice_r.png`: content spans x = 396 to 1524, 41% of the width as margins) while the question screen scales; measured holes at 1440: 118 px under the options card (competition, x 727 to 1284, y 447 to 565) and about 160 px to the next band; at 1920 about 110 px under the chart.
- **m-18. Content lines.** rollout4 keeps an invented plan sentence; axb02 correct option is the only one without "adjust"; social01 distractors ("After a loose norm, choices clustered more closely than after a tight one") are logically absurd strawmen; dimant-conspiracy-choice, dimant-polarizednorms-choice and false-news-spread have the answer as the only comparative or two-part option (flagged by `scripts/leak.py`); social20's answer is the longest and most elaborate option and restates the paper's method; bz07 title "Who stays with hybrid?" does not match its question (overall quit-rate cut); claims with a number in them are false in 4 of 5 forecast items (small n, but a learnable cue).
- **m-19. Two concurrent classes block each other's practice mode.** `server/classroom.py:241-245`: a decision is released only when every running class has revealed it; after one instructor revealed bz02 `/api/reveal/bz02` still returned 409 because my second test room was open. Documented behaviour, but a shared server with two teachers will confuse their students' Library.

### Optional

- o-1. Landing paths list is a ragged two-column list with one dark feature card ("Leading with AI"); a single column ranked by length of path or a quiet table would read more like an index.
- o-2. Console picker shows full titles for all 116 decisions (instructor-only, fine) but has no format filter beside track and idea.
- o-3. Record headline "−42" in a very large weight dwarfs the explanation line; a smaller headline with the calibration diagram beside it would carry the same information.

## Required parts: what I did

1. Gates: above.
2. Play (items 2 and 8b): sweeps of 24 decisions per cell, 5 viewports (390x844, 820x1100, 1280x720, 1440x900, 1920x1080), fresh and record present (12 seed rounds), file:// and served: 480 reveals, 480 answered question states, 0 page errors, 0 sideways overflow in play or reveal, 0 clipped text, minimum rendered text 12 px (reveal) and 12.5 px (question), 14 px at 1920. I opened 14 screenshots including landing at 390, 820, 1440, band at 390 and 1440 (file and served), question screens at 1280, 1536 and 1920, reveals at 390, 1440 and 1920 and the record. Scaled question screen: zoom.log at 125% and 150% browser zoom and short windows (1280x600, 1100x560, 999 and 1000 px wide): no sideways overflow, nothing hidden under the fixed bar, smallest target 36 px, focus ring 2.5 px solid with 1.875 px offset inside the card at 1920.
3. Live class: instructor, projector, three phones, nine decisions (rank, allocate, delegate, causal, estimate, two forecasts, choice, pick-two), closed phase with a phone that had not answered, dropped connection (my own rerun: "Sending your answer…" then "Your answer is in." within 5 s of reconnect; the earlier "NOT RECOVERED" line was a harness artifact), 125 joins from one IP (120 accepted, 8 refused "This session is full" in 0.17 s), leak probes on 14 routes per decision plus sibling decisions: 0 hits.
4. Tutor: 75 own questions, page against server identical; 116 decisions x 6 to 7 chips all answered (m-15, m-16).
5. Fact checks against papers (item 5): repro-msci-estimate, dimant-competition-choice, dimant-megastudy-estimate, dimant-deterrence-choice (all four new: every number, design and the 20 quotes verbatim; see m-2 to m-5), social15, social16, dimant-hate-choice, dimant-masks-forecast, dimant-deviant-choice (quotes and numbers, m-6, M-3), ai02 (three abstract quotes verbatim in Crossref). That is 10 decisions with a Dimant paper behind 9 of them.
6. Leak check of every live decision: `scripts/leak.py` over all 116 (wording cues, numbers repeated from answer titles, blind-strategy statistics), plus a served-page scan: none of the 116 decisions' answer titles, explanations, implications, follow-up answers or source takeaways and titles appear in `/` or `/api/challenges`. The only cue findings are in m-1, m-3 and m-18. Blind strategies: always-False earns 54% hits on 35 claims (16 true) but the forecast score pays confidence, so a constant 55% earns about 0; estimate targets sit at a median of 0.41 of the range with tolerance about 5% of range, and the constant-guess cap holds (owner decision).
7. 48 decisions read in full (the 39 listed in notes.md plus the four new and five Dimant items).
8. Introduced audit: (a) True/False: scoring correct in all 16 matrix cells for both True and False, stored probability 55 to 100 (truth True, said True) and 45 to 0 (said False), calibration points match, keyboard (1, 2, arrows, Home, End, Enter) and ARIA (m-8), classroom and projector (m-7); (b) scaled question screen: above; (c) tutor chips: no leak, all answer; (d) four new decisions: above; (e) landing and band: M-1, M-2, m-12, DOI links resolve (114 of 114 titles match Crossref); (f) iteration 65 table above.
9. Server audit: bodies over 8 KB 400; bad JSON, array, wrong content type and negative length 400; no or wrong instructor key 403; forged key for another room 404; no secret, aggregate or evidence in a student's state before reveal; submit rejects bool, string, negative, list, NaN, 1e308, null and object with 400 and keeps the first answer; room-code guessing from one client got 40 of 60 reads 429; path traversal and `/src`, `/server` 404; security headers present; title truncated to 80; 120 parallel joins, 120 parallel submits in 0.22 s (p50 118 ms), 1,200 student polls plus 40 instructor polls all 200 (p50 1 ms); the 121st join 409. Phones poll every 2 s (60 requests per second for 120 phones against the 150 per second per-IP bucket).

## The three changes that would raise the Visual score most

1. **Landing research band (1440 and 390).** At 1440 the left column of the dark band is 263 px of content next to a 1,425 px list, leaving about 1,160 px of empty navy; at 390 it overflows by 85 px; on the served page the titles are blank. Redesign: put the heading and the stat line above a two-column list (year, authors, title, venue) at 1440 so the band is about 600 px tall, a single wrapped column at 390, and serve the titles (M-1, M-2). Expected gain: about 1.5 points.
2. **Wide reveal.** At 1920 the reveal fills 59% of the width (x 396 to 1524) and leaves 110 to 160 px holes under the options card and chart, while the question screen scales to fill. Redesign: apply the same `fitQuestion` zoom to the reveal (about 1.25 at 1920), let the options card and the "For a manager" block share one row, and stop the principle strip at the column edge. Expected gain: about 1 point.
3. **Landing hero.** At 1440 and 1920 the h1 breaks as "How well do you / predict what people / do?" (3 lines, 60 px, a stranded word) and the right column ends 195 px above the left; the sample's slider starts at y = 950 on a 900 px screen. Redesign: two-line headline at 52 px, the sample question and slider in the right column beneath the three steps so the slider is on the first screen at 1280x720 and 1440x900. Expected gain: about 1 point.

## Could not verify

- **Streamlit headless, with and without `THV_INSTRUCTOR_PASSCODE`:** not run; only the passcode code path in `server/app.py` was read (no passcode on a non-loopback host returns 403 on room creation).
- **Papers I could not read:** only seven PDFs were available (the four new items' papers, Hate Trumps Love, Politicizing mask-wearing, Deviant or wrong). For the rest of the bank I checked ai02's abstract quotes through Crossref (3 of 3 verbatim); Crossref abstracts are truncated and rate-limited (429 after about ten calls), so the body-text quotes of Bloom, Obermeyer, Centola, Goh, Allcott, Kahneman and Tversky and others were not checked. I did not use WebFetch or WebSearch. `verify_dois.py` confirms titles only.
- **Screenshots looked at:** I opened about 14 of the 960 sweep images and relied on the measured metrics (overflow, clipping, stranded words, font sizes) for the rest; I did not inspect the record-present reveal of every one of the 24 decisions by eye.
- **Screen reader behaviour:** judged from the accessibility tree (names, roles, aria attributes) and axe; no real NVDA, VoiceOver or JAWS run.
- **Browser zoom at 200% and 300%, and a hardware projector:** only 125% and 150% (zoom.log) and Chromium at 1280x720 and 1920x1080 were measured.
- **Live class with more than 3 real browser pages:** the 120-student load was done with HTTP clients (joins, submits, polls), not 120 browser pages, so rendering of a full room on a phone was not measured. The projector was checked with 3 participants.
- **Gemini tutor path:** the key-less curated router only; no `GOOGLE_API_KEY` was available, so the Gemini fallback and its budget limits were read but not exercised.
- **Evidence quotes of the 112 other decisions against paper text** (verbatim rule): only the four new ones and the five Dimant items were checked.
