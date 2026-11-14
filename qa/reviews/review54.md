# Independent review 52 (snap, iteration 85)

**Score: 80/100.** 0 Blocking, 0 Major, 9 Minor, 4 Optional.


## A. Fact-check of the four iteration-66 decisions against the papers (PDFs in papers/)

Method: `pdftotext` raw text of each PDF; every stored quote in `src/evidence.json` for the four items normalised (case, dashes, quotes, whitespace) and searched in the paper.

| Item | Quotes | Verbatim in paper | Design and numbers |
|---|---|---|---|
| repro-msci-estimate (Fišar et al. 2024, Management Science) | 6 | 6 of 6 | Abstract: "more than 700 reviewers", "nearly 500 articles", 2019 policy, "more than 95%" reproduced when data and hardware were no obstacle, 29% data not accessible, "Considering all articles in our sample reduces the share of reproduced articles to 68%", 12% voluntary / 55% reproduced before. Conclusion: 68% "when considering such articles as non-reproducible". Scene (inaccessible counts as not reproduced) and key (68, band 62 to 74) match. |
| dimant-competition-choice (Huber et al. 2023, PNAS) | 6 | 6 of 6 | 18,123 participants, 45 of 95 designs, d = -0.085 (CI -0.147 to -0.022), heterogeneity "about 1.6 times as large as the average standard error". Options are a clean 2x2 plus a large-effect decoy; the answer is the paper's "small adverse effect" plus "substantial design heterogeneity". Explain says "competition lowered moral behavior"; the paper itself calls the main-text evidence "suggestive" (Fig. 2 caption). See m-4. |
| dimant-megastudy-estimate (Duckworth et al. 2025, PNAS) | 7 | 7 of 7 | 140,461 teachers, 2,992,027 students, 15 nudges plus reminder-only control, 4 weeks fall 2021, best nudge 5.06% (3.30% after winner's curse), any nudge 1.89%, personalised data +2.26%. The band (5, tolerance 2 = 3 to 7) holds both the raw and the curse-adjusted value, a fair design. |
| dimant-deterrence-choice (Buckenmaier, Dimant, Posten & Schmidt 2021, J Risk Uncertain) | 7 | 7 of 7 | 296 subjects, card-guessing game (32 cards, 10 ECU vs 4 ECU), cheaters detected and fined with a given probability, resolution immediate or +2 rounds, punishment immediate or +2 after that; abstract: "non-monotonic ... either no delay ... or maximum delay ... most effective". Correct answer and the three distractors (monotonic up, monotonic down, mixed) are faithful. |

All 26 quotes for the four items are verbatim; no misquote, no wrong number found. DOI resolution: not run (proxy blocks Crossref/doi.org), **unverified**.

## B. Gates (what I ran)

- `python3 src/build.py --check`: "built pages are current".
- `python -m pytest -q` (started first, background): **did not finish**. After about 50 minutes the log stood at 52% with no failure printed (two pytest processes were running on the machine). Result unknown.
- `tools/design_lint.py`: started in the background, **no output after several minutes; not completed**.
- axe (tests/vendor/axe.min.js, wcag2a/2aa/21a/21aa plus best-practice): **25 scans, 0 violations** (home, play and reveal for estimate, forecast and rank at 1440 and 390, record, library, studies at both widths, instructor console lobby/open/revealed, projector open and reveal).
- 135 scripted plays on file:// (27 per viewport at 390x844, 820x1100, 1280x720, 1440x900, 1920x1080; all eight formats, three of each where available; the first three of each viewport on a fresh profile, the rest with a growing record): 0 page errors, 0 horizontal overflow, 0 clipped boxes.
- All 116 predict screens at 1280x720, 1366x768, 1024x768, 1440x900 (see m-2, m-3).
- Scoring of True/False claims: bz11 (false) False@100 gives score 100 stored 0; True@100 gives -100 stored 100; biz08 (true) True@90 gives 98 stored 90; False@90 gives -62 stored 10. Scoring and stored probability are correct both ways.
- Not done: the same play sweep on the served page (I used the served page for the class, leak and axe-console tests only), Streamlit (skipped), browser zoom, screen-reader testing, DOI resolution.

## C. Live class (server on localhost, instructor 1280x720, four phones 390x844)

- 130 joins from one IP in 0.1 s: 120 accepted, 10 refused "session full" (cap THV_MAX_PARTICIPANTS = 120, by design).
- Rounds run: allocate, rank, delegate, causal (one phone offline), estimate, forecast, multi. A phone that had not answered when answers stopped showed "Answers are closed." with 0 live controls in every round (checked in the DOM and screenshot). A phone that joined after the stop saw the same text; after reveal it saw "You did not answer this one." A reloaded phone returned to the open decision. A phone that locked its answer in the same moment the instructor stopped got "Your answer is in." (server accepted it first). An offline phone's answer, when the connection returned after the stop, ended on "Responses are closed for this decision" (correct, not counted).
- Leak probes during an open decision, all held: /api/reveal for the open item, a same-paper sibling and an unrelated item: 409; /api/library: 0 decisions; /api/challenges has no answer, explain, key or title field; instructor bank, export and control without the key: 403; a student token used as the key: 403; student state has no evidence or aggregate; the tutor returns "opens after your instructor reveals it" for the open item, a sibling and a question that names the study from another item; no tutor card or chips on an open phone; closed-phase aggregate hidden from students.
- Validation: duplicate answer reported not recorded; answer index 9 and a non-numeric confidence refused with 400; late submit 409.
- Projector at 1280x720: no overflow; smallest text 13.9 px (open) and 15 px (reveal).

## D. Tutor (offline, own wording)

165 questions of my own wording on 100 decisions (the list is in tools/tq.py; none copied from earlier reviews that I could see). Two further questions went to judg02, which is quarantined (see o-1) and are excluded.

- **Page versus server: identical text and chips on all 165.**
- Graded by me: direct answer 57 (34.5%), partial (relevant but not the thing asked) 44 (26.7%), miss 59 (35.8%), wrong 5 (3.0%). Useful (direct plus partial) 61%.
- Wrong answers: ai11 "What does subjective task mean?" returns an unrelated finding sentence; biz02 "Why do people stick with defaults?" answers "The lab's summary does not record how long the effect lasted" (a duration route fires on "stick"); social01 "What is a tight norm?" returns the glossary sense (a rule strongly enforced) whereas in this study a tight norm is a narrow spread of others' observed choices, so the definition overrides the item's own meaning; rollout4 "What country were the students in?" says the summary does not name the setting while the stored boundary says Turkey; overconfidence-hard-task "What is overprecision?" defines overconfidence (the boundary says overprecision is a separate bias).
- Setting route misses where the answer is in the stored text: biz04 "Where were the hotels?" (scene: German), social12 "Which cities?" (Boston and Chicago), bz09 "Where was the lender based?" (South Africa), tax-letter-norms "Which government?" (UK). Where the scene holds the answer it works (bz05, bz08, bz12).
- Other misses: follow-up exists but not matched: biz11 "Do experts get fooled by anchors?" (follow-up "Are experts immune?"), facebook-deactivation "How much money did people need to quit?" (follow-up "What did people need to be paid?"), axb10 "Did users like the better designs?" (answer title says they disliked them), ai01 "Who got the least out of ChatGPT?", ai01 "What is the take-home for a manager?" (implication exists), ai02 "better or only faster?", axb13, axb12, axb09, axb07, axb03, axb04, axe01, axe08, genai1, axf01, axf04, axf05, ai10, ai11, ai09, biz01, biz07, social07, social13, bz15, truth-telling-gains, dimant-masks-forecast (ITT), dimant-enforcers-rank, dimant-contagion-multi, judgement of "what is X" for algorithm appreciation, opt-out default, loss aversion, proxy variable, attrition, crowding out, celerity, Zearn, MTurk, many-labs.
- Chips: on all 116 decisions every chip shown returns a non-miss answer (by construction); "How would I test this in my company?" returns the same paragraph on all 116 decisions; "Is this cause or correlation?" and "Who funded the study?" never qualify. No chip or tutor card exists before the call.

## E. Content and leak read (all 116 decisions read; 52 not named in the supplied ledger entries)

- Option cues: answer is the longest option in 8 of 36 choice/causal items (chance about 10); the answer is two-part in 15 of 36 while 1.36 options per item are two-part (about 40%); strict scene-and-question word overlap favours the answer in 3 items. No blind strategy stands out. Forecasts: 16 true, 19 false, mean claim length 96 vs 89 characters.
- Remaining cues I would still change: social20 (the answer is the longest and the only "ask each person" option), misperceived-norms-action (two options carry numbers and "within noise"), axb08 (the scene names demographic details, which only the answer uses), false-news-spread (answer shares three content words with the scene).
- No scene, question, option, sample line or title states its answer. Titles worth a look: axb03 "Same jail rate, less crime" gives the direction (the question also says "fall"); lies-in-disguise "Honest, liar, or in between".
- Facts checked against the seven PDFs: the four iteration-66 items (section A), plus Hate Trumps Love (social15 78.1, 14.97, 13.54, 11.99, -22.9; social16 20% to about 0 and 10 to 15% to 25 to 35%; dimant-hate-choice 72.8 to 59.0 and 73.2 to 62.4, 8,600 participants), Politicizing mask-wearing (N = 4931, 1034 forecasters, no nudge effect, overestimation for Democrats), Deviant or wrong (418, 42.7 vs 28.7, 22.2 vs 36.5). All correct. Papers I could not read: all others (no web tool used); their numbers I only read for internal consistency.
- No overclaim or non-significant difference treated as real found in the items read; the enforcers item correctly outlines the non-significant gap.

## F. Visual (looked at 40+ screenshots; see shots/)

Home, predict and reveal at 1920, 1440, 1280x720 and 390 are restrained and consistent: one serif and one grotesk, navy ink, one amber mark, no cards inside cards, no gradients. The landing page order (headline, six-line lede, sample, paths, dark Dimant band with DOI-linked titles, credit) matches the owner's spec. The projector is clean. The weak spots are measured below.

## G. Findings

### Introduced by iteration 85

- **m-1 (Minor) Causal graph labels shrink to 8.7 to 10.3 px at 1280x720.** Where: `src/app.js` causal graph sizing; axb05 and meta-perception-causal at 1280x720 (shots/axb05_1280x720.png). Observed: node label font 10.3 px (axb05) and 8.7 px (meta-perception-causal), graph height 140 px; at 1366x768 and 1440x900 it is 13.3 px, at 1024x768 17.6 px. Why: below the 12 px floor (rule 9) and the shrink is the iteration-85 "tighter causal graph"; the lint runs only at 1440 and 390, so it cannot see it. Fix: keep node text at 13 px or more and give the graph its height back by moving the hint line under the options, or scale only the node boxes; add 1280x720 to the lint.
- **m-2 (Minor) "On all 116 decisions nothing sits under the action bar" holds at 1280x720 but not at the neighbouring sizes.** Where: fit sweep (tools/fit.py). Observed: 1280x720, no element under the bar but 6 pages scroll by 7 to 50 px (axb05, meta-perception-causal, dimant-notalie-causal, dimant-enforcers-rank, axf05, manylabs-anchoring); 1366x768, 4 scroll and the confidence slider of meta-perception-causal is 22 px under the bar (shots/meta_1366x768.png); 1024x768, 38 of 116 scroll, and on axb05 two options and the slider are 53 to 217 px under the bar (shots/axb05_1024x768.png). 1440x900: all fit. Why: 1366x768 is the commonest laptop size and the confidence slider is a required step. Fix: reserve the bar height in the causal layout and lower the DAG at heights under 800 px.
- **o-2 (Optional) Ledger line "five predict screens" earlier versus six now**: the claim of a fit is about overlap, not scroll; word it that way.

### Open from earlier reviews or new in my reading

- **m-3 (Minor) Tutor coverage in natural wording is low.** 35% direct, 27% partial, 36% miss, 3% wrong on 165 questions (section D). The 40 definitions help where a term is in the list; "what is X" for terms not in it (loss aversion, proxy variable, attrition, crowding out, celerity, Zearn, ITT, algorithm appreciation, opt-out default) misses. Fix: add the missing concept entries; let "What did X find about whom" reach `implication` and the follow-up Jaccard match accept "experts immune" and "need to be paid".
- **m-4 (Minor) Wrong tutor answers (5)**: see section D. Highest value fixes: do not let a duration route fire on "stick" (biz02); when a definition's term appears in the item's scene with a different sense (social01 tight norm), prefer the item's wording; the setting route must read `boundary` (Turkey, Boston and Chicago, South Africa, UK) before saying the setting is not named.
- **m-5 (Minor) Causal reveal hole at 1920x1080 is about 285 px** (axb05: figure ends at y 885, text column at about 600; shots/axb05_1920_reveal.png). Meta-perception-causal 205 px. Unchanged from earlier reviews.
- **m-6 (Minor) Projector body text 13.9 to 15 px at 1280x720** (labels such as "Students", "Allocate, AI x Business"). Known and left by the owner's note; from the back of a room it is small. Fix: raise only the kicker and label lines to 18 px and drop the redundant "Allocate, AI x Business" kicker.
- **m-7 (Minor) The phone's offline outcome mixes messages.** An answer sent offline and arriving after the stop ends on the server string "Responses are closed for this decision" with the sub-line "The evidence appears for everyone when your instructor reveals it." and no "not counted". Fix: use the existing "Not counted." state for a 409 on a pending answer.
- **m-8 (Minor) The Dimant paper titles ship in the served page next to a decision-to-source map.** `bandTitles` plus each decision's `sources` let a student read, before answering, the title of the paper behind a Dimant decision. For social15 and dimant-hate-choice the title "Hate Trumps Love: ..." tilts the answer. The band is an owner decision; the map is not. Fix: serve bandTitles without the sources array on the decision objects, or key the band by an opaque order.
- **m-9 (Minor) Heading breaks on the estimate predict screen.** ai01 at 1280x720 breaks "How much less time did / the ChatGPT / group take?" (middle line short, shots/ai01_predict_1280.png) because the tied last two words cannot join "the ChatGPT". Fix: tie only the last word when the heading is three lines or fewer.
- **o-1 (Optional) judg02 is quarantined in the bank but present in the offline index.html's data lookup** (`THV.BY_ID`); `THV.ALL` and the served page exclude it, and the page and server tutors disagree on it (page answers, server says outside scope). Not reachable by a player.
- **o-3 (Optional) The "How would I test this in my company?" chip returns one paragraph on all 116 decisions.** Make it item-specific from `implication` or drop it.
- **o-4 (Optional) Stranded-word metric**: my own detector was invalid (it ignored the tied spans) so I report no count; the design lint (R34) stands as the check, and I did not see a stranded word in 40+ screenshots except m-9's short line.

## H. Category scores

| Category | Max | Score | Evidence |
|---|---|---|---|
| Science | 15 | 13 | All 26 quotes for the four new items verbatim; numbers and designs match the four papers and three further Dimant papers; no overclaim found; DOIs unverified. |
| Learning | 15 | 11 | Predict-then-reveal with calibration and scoring correct both ways; tutor answers usefully only about 61% of natural questions and gives 5 wrong ones. |
| Visual | 15 | 12 | Restrained, consistent, polished at 1920/1440/390; 285 px causal reveal hole, 8.7 px graph labels at 1280x720, short heading line. |
| Gameplay | 15 | 12 | 135 plays with 0 errors across eight formats; True/False plus sureness clear; screens scroll at 1366x768 and 1024x768 for a few items. |
| AI and business relevance | 10 | 9 | Every item has a manager action; AI track strong; four items weakly tied to action (e.g. abstract replication items). |
| Content | 10 | 8 | Careful distractors, few cues; remaining cues in social20, misperceived-norms-action, axb08. |
| Technical | 10 | 7 | Builds current; axe 0; leak probes and limits hold; but the full pytest run and design lint did not finish for me, and the m-8 map. |
| Classroom | 5 | 4 | Closed phone, late join, reload, dropped link and 120 joins all behave; projector text small. |
| Accessibility | 5 | 4 | axe 0 on 25 scans; keyboard 1/2 keys work for True/False; no screen reader run; sub-12 px graph labels. |
| **Total** | 100 | **80** | |

Calibration against review 51 (82): I see no Blocking or Major defect, but the tutor in my own wording is not better than 35% direct, iteration 85's glossary adds wrong or overriding answers in a few places, and the 1280x720 fix cost the causal graph its legibility. 80 is honest.

## I. Three changes that would raise Visual most

1. **Causal reveal, 1920x1080 and 1440x900**: the text column ends 285 to 390 px above the figure's bottom (axb05, shots/axb05_1920_reveal.png). Move the Questions and Ask block into the left column under the study card for causal items (the figure is the only tall element), so both columns end together.
2. **Causal predict at 1280x720 and 1366x768**: graph labels 8.7 to 10.3 px, slider under the bar (m-1, m-2). Put the DAG above the question on the left (which has 280 px free, shots/axb05_1280x720.png) and keep the options and slider alone on the right at full size.
3. **Projector at 1280x720**: body labels 13.9 px with 400 px of empty card below the options (shots/live_proj_axb08_open_1280.png). Scale the option list and kicker to 20 px, drop the "Answers are open. Allocate, AI x Business." line and use the freed height for the options.

## J. Could not verify

- Full pytest result (did not finish); design lint result (did not finish); DOI resolution (proxy; not run).
- Play sweep on the served page; browser zoom; screen-reader testing; Streamlit with and without THV_INSTRUCTOR_PASSCODE (skipped); 30 to 120 concurrent students beyond the 130 joins (no concurrent answer load, polling load or latency measured).
- Fact checks beyond the seven supplied papers (no web fetch used).
- Whether the two-hour release of an abandoned class works (code read only: OPEN_HOLD_HOURS = 2, not waited out).
- Tutor grading is my judgement on 165 questions; not double-marked.
