# Independent review 52 (snap, iteration 88)
**Score: 81/100.** 0 Blocking, 0 Major, 8 Minor, 3 Optional.

(Snapshot is iteration 88 plus the iteration 89 addendum as shipped in snap/. Report written from my own copy in work/.)

## Score table
| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All 26 quotes of the four new decisions verbatim in the PDFs; numbers match; wording slightly beyond quote in dimant-masks-forecast. |
| Learning | 15 | 12 | Reveal, "for a manager" and own-call-vs-evidence plate are strong; key-less tutor menu restates the finding in 280 of 601 generic answers. |
| Visual | 15 | 12 | 110 file plays and 110 served plays look consistent and premium; causal/pick-two reveal leaves 304 to 426 px empty under the figure; projector is small. |
| Gameplay | 15 | 12 | 8 formats play on 5 sizes, 0 errors; True/False plus how-sure scores right; 50% "Unsure" contradiction. |
| AI and business relevance | 10 | 9 | Manager action on every reveal, AI tracks, rollout cases. |
| Content | 10 | 8 | Read 117 decisions; few cues (deviant, deterrence, competition, bz12). |
| Technical | 10 | 9 | pytest 419 passed, lint clean, build current, 0 console errors, hardened server. |
| Classroom | 5 | 4 | 120 joins, 8 formats, dropped link, closed phase, no leak; projector text 14.9 to 15.2 px at 720p. |
| Accessibility | 5 | 4 | axe 0 violations (wcag2a/aa/21aa plus best-practice) on 12 scans; min text 12.5 px. |
| **Total** | 100 | **83 raw, scored 81** | I took 2 off for the unmet iteration 89 claims (projector 16 px, causal balance). |

Calibration against review 51 (82): about level; no regression found, no gain.

## Gates (run to completion myself)
- `python -m pytest -q`: 419 passed in 1238.61 s.
- `python3 tools/design_lint.py`: "by rule: {}".
- `python3 src/build.py --check`: built pages are current.
- axe (tests/vendor/axe.min.js): home 1440 and 390, record both, principles both, library both, play both, reveal both, console lobby: 0 violations on every scan. Projector and phone pages were not scanned with axe.

## Findings

### Introduced (iteration 88/89)
**m-1 (Minor, iteration 89): causal and pick-two reveals now end with a hole under the figure.** The fig-tall threshold went from 260 to 420. Right column bottom vs left column bottom (px, measured with leaf elements): ai07 (pick two) 1440: 742 vs 1116 (gap 374); 1280: 729 vs 1132 (403); 1920: 722 vs 1116 (394). axb05 (causal) 1280: 798 vs 1225 (426); 1440: 358; 1920: 304. dimant-notalie-causal 1920: 352. With the old 260 value (my work2 copy) the same pages gave gaps of 10 to 51 px but a ~190 px hole mid left column (shots/thr260_1440_ai07.png). So the hole moved, it was not removed. Other formats are unchanged (forecast, estimate, rank, choice gaps 10 to 63 px; ai09 and dimant-contagion-multi 116 to 157, same as before). Screens: shots/file_1440x900_fresh_ai07_reveal.png, file_1920x1080_fresh_axb05_reveal.png. Fix: when fig-tall, move the "Questions about this study" chip panel under the figure (right column) so both columns end together.

**m-2 (Minor, iteration 89): projector text at 720p is below the stated 16 px.** After Reveal at 1280x720 the smallest text is 16 (estimate, rank), 15.2 (forecast, allocate, causal, pick-two), 15 (delegate), 14.9 (choice); no scroll (scrollHeight 720). At 1920x1080 smallest is 17 px, and the card is 1388 px wide with a ~280 px empty dark band below (shots/projector_revealed_axb06_1920.png). Fix: let the projector card use the full 1920 width and scale type to about 24 px; at 720p drop the "Where the evidence comes from" block instead of shrinking.

### Other
**m-3 (Minor) "Unsure" contradicts the player's pick.** bz08: I pressed True and left the slider at 50. The plate reads "You said Unsure ... You sat at 50%"; record stores 50, correct False, score 0.5. Fix: if True/False was chosen, label it "True, 50% sure" and score by the stored probability only.

**m-4 (Minor) projector wording.** Forecast rows read "Said true (above 50)" / "Said false (below 50)" (shots/projector_revealed_axb06_1920.png): internal jargon, and a 50% answer fits neither. Say "Said true" / "Said false" / "Unsure".

**m-5 (Minor) key-less tutor menu is safe but thin.** All 957 menu and own-follow-up questions over 116 decisions: page answer equals server answer on all 957 (0 differences), 0 fallback or empty answers. But 280 of 601 generic answers just restate the finding the student has on screen; "Would this hold with AI tools today?" answers with the scope sentence, not the question; the chip "Who took part in the study?" duplicates the decision's own "Who took part?" row (shots/file_1440x900_fresh_ai09_reveal.png). Extra check: 62 free-text questions of my own through server curated(): about 25 direct, 25 partial (fallback text that contains the answer), 12 miss or off-target ("how many weeks did the emails run" returns the best-email text; "is 5 percent big?" and "which nudge won" restate). The page offers no text box now, so these cannot reach a student; if a model is added the router needs the fixes. No model was configured, so I did not grade 100 model answers.

**m-6 (Minor) served page still joins decision to paper.** GET / has no answerTitle/explain/implication strings (0 of 116), but carries "sources":["hate23"] on each decision and a source record (authors "Dimant", 2024, Management Science 70(1), 1-31) while the band lists title, year and DOI link without id. A reader of view-source can match them by venue and volume. Fix: ship source records with the evidence, as the owner's iteration 89 note intends for links.

**m-7 (Minor) option cues.** dimant-deviant-choice: two options are not combinations, so "Which combination" leaves two; the correct one is the only one saying "cheap". dimant-deterrence-choice: options 0 and 1 are exact opposites, the answer is the hedged "or" option. dimant-competition-choice: the answer shares a clause with every distractor (small adverse effect + disagreed). bz12: correct option is two-part and longest. Over all 32 choice items the answer is the longest option in 8 (25%), so no length cue overall.

**m-8 (Minor) stranded last words.** With text-wrap: pretty, single-word last lines occur: source line "Maréchal, Tannenbaum & | Zünd" (civic-wallet-rank, 4 widths), "from | 17.7%" (axb05 at 390), headings ending "could be at | least" (repro-msci-estimate), "...among | Democrats" (dimant-masks-forecast), "Which interface kept people | most honest?" variants. Fix: non-breaking space before the last word of source lines and the last two words of headings.

**m-9 (Minor, content) dimant-masks-forecast explanation.** Says "none of the 7 nudges raised mask-wearing intentions or pledges" and forecasters overestimated "most of all for Democrats". Stored quotes support "no evidence", z = 4.40 pooled and 4.84 for Democrats; "pledges" and "most of all" are not in a quote I could check. Reword to the quoted text.

**o-1 (Optional)** Session cap is 120 (130 joins gave 120 ok and 10 "This session is full"); executive classes of 150 need THV_MAX_PARTICIPANTS.
**o-2 (Optional)** Landing has no separate "how a round works" heading; the hero paragraph carries it (owner decision lists it, so confirm).
**o-3 (Optional)** Predict screen at 1920x1080 leaves large empty bands above and below the card (shots/file_1920x1080_fresh_ai09_predict.png); the scale cap of 1.6 could rise.

## Part-by-part results
1. Gates: above.
2. Plays: 220 plays (110 on file://, 110 on the served page) = 8 formats, 11 decisions, 5 sizes (390x844, 820x1100, 1280x720, 1440x900, 1920x1080), each on a fresh profile and after three warm-up rounds. 0 errors, 0 console errors, 0 horizontal overflow, lock button always enabled. Smallest HTML text 12.5 px at every size (14 at 1920 predict); smallest diagram label 12.3 px at 1280, 12 at 390, 13.3 at 1440. About 130 screenshots in shots/; I read about 20. Predict screens at 1280x720 keep the slider above the action bar (axb05, megastudy, rank checked). Hit targets and focus rings not measured.
3. Live class: instructor, projector, 4 phone pages, 8 formats (estimate, forecast, rank, allocate, delegate, causal, pick two, choice), one phone offline during each round (its answer went out on reconnect, count 3 at close), one phone never answering ("Answers are closed." with only a leave button, no live controls), 0 page errors. HTTP probes with 120 students: open decision gave 409 on /api/reveal, absent from /api/library, 403 on instructor bank, tutor "locked", no aggregate in state; late answer 409; reveal then released everything. No leak found. Only one IP, so per-IP limits (write 60/s, burst 200) were tested by accident: 180+ answers in 3 s from one IP hit 429, spaced rounds did not.
4. Tutor: see m-5.
5. Fact-check: read in the PDFs: repro-msci-estimate, dimant-competition-choice, dimant-megastudy-estimate, dimant-deterrence-choice (all quotes verbatim, 26 of 26; numbers 68/95/29/12/55 %, d = -0.085 [-0.147,-0.022], 1.6x, 140,461 / 2,992,027 / 5.06 / 3.30 / 1.89 / 2.26, 296 participants, 28 rounds, delays of 2 rounds, non-monotone result). Also read the Hate Trumps Love and masks PDFs against social15, dimant-hate-choice, dimant-masks-forecast (numbers 78.1, ~39, 14.97, 13.54, 72.8, 59.0, N = 4931, 1034 match). Against stored quotes only (not PDFs): dimant-deviant-choice, dimant-motivated-estimate. Content-read all 117 bank entries (scene, question, options, answer, explanation); no invented scenario or non-significant contrast treated as real found beyond m-7 and m-9.
6. Leak check: served page and API shown clean above; screen-by-screen leak review of every decision was done on text (scene, question, options, study line), not by clicking all 116 screens; estimate study lines drop n when it sits in the band. Blind strategies: forecast 16 true / 19 false, claim length 96 vs 89 characters, no word cue stronger than 5 vs 3 counts.
8. Introduced audit: (a) claims: True/False 80 on a true claim stored 80 score 0.92; False 80 on a false claim stored 20 score 0.92; True 60 on a false claim stored 60 score 0.28; False 100 on false stored 0 score 1; record shows the 5 calls, calibration line and headline 45; keyboard 1/2 selects True/False and the lock stays disabled until the slider moves; slider aria-valuetext "80 percent sure"; classroom projector shows two bars. (b) fitQuestion: zoom works at 1440 and 1920, no overflow, nothing under the bar at 1280x720 on the three screens checked; browser zoom not tested. (c) tutor suggestions: m-5. (d) four new decisions: fact-checked, quotes verbatim, cue note in m-7. (e) landing and band: band lists 18 papers with title, year, journal; I did not click the DOI links. (f) review 41 I-1 to I-13 and m1: not re-verified one by one; the suite's 419 tests cover them.
9. Server: limits, validation and path tests listed in the probes (title cut to 80, 2 MB body 400, object in place of string 400, traversal 404). Streamlit headless started and answered /_stcore/health ok; no passcode run, no page render.

## Could not verify
- DOI resolution (network blocked; verify_dois.py not run).
- Model-backed tutor (no key); 100 own-wording model questions not graded.
- Browser zoom (110, 150, 200 %), focus-ring and hit-target measurements, screen reader.
- Streamlit rendering and the THV_INSTRUCTOR_PASSCODE variants.
- 100+ browser phones (the 120-student test used HTTP clients, plus 4 real pages).
- Projector and phone pages under axe.
- Review 41 items I-1 to I-13 one by one; the 6-flag leak review by eye for all 116 screens; the papers for 18 other Dimant decisions (stored quotes only).
- Papers behind non-Dimant decisions were not read (no network); only their stored quotes.

## What is still missing for 95
Equal column ends on causal and pick-two reveals (m-1); a projector built for a room (type 24 px at 1080p, 16 px or more everywhere at 720p); a tutor that answers the question asked rather than restating the finding; the last option cues; the paper map out of the served page.

## Three changes that would raise Visual most
1. Causal and pick-two reveal at 1440 and 1920 (ai07, axb05): 374 and 304 px empty under the figure. Put the chip panel and the tabs under the figure so both columns end within 40 px.
2. Projector at 1920x1080: card 1388 px wide, 17 px text, 280 px dark band below. Go full width, 24 px body, one column of three big numbers.
3. Predict screens at 1920x1080 and 1280x720: question block floats with 150 to 250 px empty above and below. Anchor the block to the top third and let the question and instrument fill the width (raise the 1.6 zoom cap).
