# Independent review 52 (snap, iteration 86)

**Score: 80/100.** 0 Blocking, 1 Major, 9 Minor, 4 Optional.

Reviewer note: the supplied prompt names this "review 52" and the ledger calls it review 55; I kept the heading the prompt asked for. The diff file named in the prompt was not in the folder, so I audited the code and content directly.

## Score table

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | 26 of 26 stored quotes for the four iteration-66 items verbatim in the PDFs; all numbers and designs match; 5 further Dimant items checked; 100+ other items could not be checked against papers; DOIs unverified. |
| Learning | 15 | 11 | Predict, commit, sure-ness, reveal and calibration work; but the tutor answers 33% of 115 natural questions directly (75% direct plus partial), gives 3 wrong answers, and the record headline loses its minus sign (M-1). |
| Visual | 15 | 11 | Restrained and consistent at 1440, 1920 and 390; but 291 px hole beside the causal reveal at 1920, 192-225 px beside ai07 and facebook-deactivation, a toast covering the class notice, 10.3 px causal labels on the projector, and the 14 px minus beside a 128 px number. |
| Gameplay | 15 | 13 | 112 scripted plays on file and served, 8 formats, 5 viewports: 0 errors, 0 overflow; True/False plus sure-ness clear and keyboard operable; six predict screens scroll at 1280x720, one puts the required slider 36 px under the bar. |
| AI and business relevance | 10 | 9 | Every item carries a manager action; AI track strong; a few items (replication, deterrence) are generic. |
| Content | 10 | 8 | Careful distractors, 36 choice items with the answer longest in 7 (chance about 9); odd-one-out cues remain (axb05, axb02); no number or design error found in the 40+ items read. |
| Technical | 10 | 7 | Build current, lint 0, axe 0, limits and leak probes hold, 120 joins in 0.16 s; served page still ships the Dimant paper titles next to the decision-to-source map; pytest result below. |
| Classroom | 5 | 4 | Closed phone, dropped link, late arrival and 120 joins behave; late offline answer ends on a mixed message; causal projector reveal text 10.3 px. |
| Accessibility | 5 | 4 | axe 0 violations on 49 scans; 2.4 to 3 px focus rings everywhere; slider has aria-valuetext; confidence slider 36 px high; no screen reader run. |
| **Total** | 100 | **80** | |

Calibration against review 51 (82) and 54 (80): the product is at the same level. I found no Blocking defect and the iteration 86 fixes hold, but I found one real regression in the headline score, and the tutor is still a third direct in natural wording.

## 1. Gates I ran

- `python3 src/build.py --check`: "built pages are current".
- `python3 tools/design_lint.py`: ran to completion, output `by rule: {}` (0 violations).
- `python -m pytest -q`: **413 passed in 20:00** (run to completion in my copy, `-x`, no failure).
- axe 4.x (tests/vendor/axe.min.js, wcag2a, 2aa, 21a, 21aa, best-practice): 49 scans, 0 violations. Home, play (estimate, causal), reveal for estimate, forecast, rank, causal, allocate and delegate at 1440 and 390, record, library on file and served; instructor console (lobby, open, revealed), projector (open, reveal).
- Streamlit headless: starts (health 200). Without THV_INSTRUCTOR_PASSCODE the Play page is on and the page itself warns that it carries the answers; with the passcode set, Play is replaced by "Self-study play is available in the offline game your instructor shares." I did not drive Streamlit's native live class or tutor.

## 2. Play sweep (file:// and served)

112 plays: 5 viewports (390x844, 820x1100, 1280x720, 1440x900, 1920x1080), 8 formats (24 decisions at 1440), first plays on a fresh profile, later plays with a growing record, on file:// and on the served page. 0 page errors, 0 horizontal overflow, 0 clipped boxes, no disabled lock button. Smallest rendered text on any play or reveal screen: 12 px (390 phone reveal chips), 12.5 px study line. Screenshots: shots/sw_*. Extra: browser zoom 125, 150, 200, 300 percent (viewports 1152x720 down to 640x360 at device scale): 0 overflow, 0 clipping, focus ring 2.5 to 3 px solid blue on every focus, pages scroll as expected, the action bar stays.

Empty space in wide reveals (measured, figure bottom against left-column bottom): axb05 291 px at 1920 (237 at 1440, 169 at 1280); ai07 192 to 221 px at 1280 to 1920; facebook-deactivation 225 px at 1440; bz02 75, axb14 50. On the other side, short figures leave the right column empty beside the text: axb01 and dimant-competition-choice at 1440 end the figure 150 and 130 px above the text.

## 3. Live class (server on localhost, instructor 1280x720, three phones 390x844)

Rounds: rank, allocate, delegate, causal, estimate, forecast, multi. One phone never answered, one dropped its connection (offline) in the causal and estimate rounds.
- A phone that had not answered shows "Answers are closed." with 0 live controls in every round (after the 1 to 2 s poll; at 1 s the controls are still there, 0 at 2 s), and on reveal "You did not answer this one."
- The offline phone, back online after the stop, ends on "Responses are closed for this decision" (not counted, correct, but see m-4).
- Leak probes while a decision was open: /api/reveal for the open item 409; /api/library 200 with 0 decisions; /api/challenges has no answer, explain, answerTitle, multiAnswers or rankAnswer for the open item; tutor says "opens after your instructor reveals it"; reveal while closed 409. All held in all 7 rounds. Served index.html has 0 `"answer":` keys, no `"truth"` in the data, and no answer titles.
- 130 joins from one IP in 0.14 to 0.16 s: 120 accepted, 10 "This session is full" (cap by design). 120 concurrent answers in 0.15 s, all recorded; 240 concurrent polls p50 15 ms, p95 24 ms, max 29 ms.
- Validation: confidence "abc" 400 "Confidence must be 0 to 100"; 2 MB body 400; bad JSON 400; control without key 403; student token as key 403; with passcode set, room creation without or with a wrong passcode 403; path traversal and /src, /server, /tests paths 404; CSP, nosniff, no-referrer headers present.
- Projector at 1280x720: no overflow; smallest text 13.9 to 14.6 px open, 15 px on rank and allocate reveals, 10.3 px on the causal reveal (m-2).
- An abandoned room with an open decision (my own test left ai01 open) shows every solo player of that decision a banner and "Results open after the class reveal"; the banner is covered by a toast (m-3). By design for two hours.

## A. Fact-check (papers/ PDFs, pdftotext raw text)

- The four iteration-66 decisions, every stored quote in src/evidence.json normalised and searched in the paper text: repro-msci-estimate 6/6, dimant-competition-choice 6/6, dimant-megastudy-estimate 7/7, dimant-deterrence-choice 7/7 verbatim. Numbers and designs agree with the papers (700 reviewers, ~500 articles, >95% / 29% / 68% / 12% / 55%; 95 designs, 45 drawn, 18,123 participants, d = -0.085 CI -0.147 to -0.022; 140,461 teachers, 2,992,027 students, 5.06% / 3.30% / 1.89% / 2.26%; 296 subjects, non-monotonic delay result).
- Also checked: social15, social16, dimant-hate-choice (Hate Trumps Love), dimant-masks-forecast (Politicizing mask-wearing), dimant-deviant-choice (Deviant or wrong): all quotes found after ignoring typography, one exception (418-participants sentence in deviant21) is split by a footnote in the PDF text; the number 418 is in the paper.
- Web: Cohn et al. (wallets): 40 countries, 38 of 40 more likely to report with cash, USD 13.45 and 94.15 in Poland/UK/US, 279 economists and 299 laypeople: matches. Dell'Acqua et al.: 12.2% more tasks, 25.1% faster confirmed; the per-arm quality numbers (29.9%, 33.9%) and 84.5/70.6/60% I could not confirm from the page (the page gives "40% higher" and a 60-70% range), so unverified.
- DOI resolution: not run (proxy), unverified.

## D. Tutor (page curated vs server, own wording)

115 questions of my own wording on 113 decisions (list in tools/tq.py in the r55 folder; only one, "What is the endowment effect?", also appears in reviews 51 to 54, so 114 are new; I did not collect the 100-question lists of earlier reviews beyond a text match).
- **Page and server: identical text on 115 of 115** (compared word by word; chips compared on the 400 earlier probes only through the pytest parity test, which passed).
- Graded by me: direct 38 (33%), partial 48 (42%), miss 26 (23%), wrong 3 (3%). Useful (direct plus partial) 75%; partial includes the "could not match, here is what the study found" fallback when that finding itself answers the question, so the figure is generous.
- **Wrong answers (3):** ai09 "Why would people reject a better model?" returns the forecast-error figures, not a reason; axb08 "How long did each debate last?" says "The lab's summary does not record how long the effect lasted" (duration route fires on "how long"; the scene says 10-minute debates); bz07 "Did women quit less?" says the summary "does not break results down that way" while the stored explain says "larger drops for women and non-managers".
- **Misses (26):** ai01 "Which kinds of workers got the biggest boost?" (the follow-up "Who gained the most?" exists), ai02, ai11, biz02 (pension), biz11 (experts), axb03, axb04, axb06, axb07, axb11, axb12, bz02 "What is ROI?", bz03, bz09 "How big was the lender?", bz13 "What is a flat wage?", bz16, lies-in-disguise, false-news-spread (how labelled), dimant-proximity-estimate "What are ECUs?", dimant-enforcers-rank "Who are the enforcers?", dimant-opioid-forecast "What is loss framing?", axe01 "What is a hedonic product?", axe10, axe11, axf01, repro-msci-estimate "What does reproducible mean?".
- Iteration 86 tutor changes, tested: "stick" no longer fires duration (biz02 "Why do people stick with defaults?" now gives the mechanism; "Does the default stick over time?" correctly gives duration); the tight/loose entry is gone (social01 "What is a tight norm?" falls back to the finding, dimant-polarizednorms-choice answers with the study's own definition); "What is overprecision?" no longer defines overconfidence (falls back); the seven new definitions work (proxy, attrition, crowding out, intention to treat, opt-out default, algorithm appreciation, celerity); the setting route for rollout4 now says Turkey and names the scene. Setting questions still miss where the answer is in the boundary or scene: biz04 "Where were the hotels?", social12 "Which cities?", bz09, tax-letter-norms, axb08 "Where did the debates take place?" (each falls back to the finding, which sometimes contains the place).
- **Chips (suggestions) on all 116 decisions** read from the reveal DOM after the call: 5 chips on 93 decisions, 6 on 18, 7 on 1 (the delegate items also show "You: ..." answer pills of a different kind; I excluded them). Every real chip returns a non-miss answer from the server tutor (0 of 616 misses). No tutor element, chip or tutor card exists on any predict screen. The four chips "How would I test this in my company?", "Who took part in the study?", "Who wrote the paper?" and "What should a manager do with this?" appear on all 116 decisions with the same wording (see o-1).

## E. Fact-checks and content

Method as in section A. Plus: every Dimant item shipped has quotes verbatim in the available PDFs (social15, social16, dimant-hate-choice, dimant-masks-forecast, dimant-deviant-choice).
- Verified against the supplied PDFs (9 items): repro-msci-estimate, dimant-competition-choice, dimant-megastudy-estimate, dimant-deterrence-choice, social15 (78.1, 14.97, 13.54, 11.99, -22.9), social16, dimant-hate-choice (72.8 to 59.0; 73.2 to 62.4; 8,600), dimant-masks-forecast (N 4,931; 1,034 forecasters; overestimation), dimant-deviant-choice (418; 42.7 vs 28.7; 22.2 vs 36.5). Described designs and answer keys match; all distractors of the four new items are false by the paper (the 2x2 on competition, the three timing shapes on deterrence).
- Checked on the web (partial): civic-wallet-rank and civic-wallet-experts design (40 countries, 38 of 40, USD 13.45 and 94.15 in Poland, UK, US, 279 and 299 predictors); Dell'Acqua 12.2% more tasks and 25.1% faster.
- Papers I could not read: all others (Noy & Zhang, Dietvorst, Madrian & Shea, Gneezy & Rustichini, etc.). For those I checked internal consistency of scene, key, explain and quotes only.
- **Read for quality (all 116 decisions, dump in dump2.txt; I name 55 here as read closely):** ai01, ai02, ai07, ai09, ai10, ai11, ai12, biz01, biz02, biz04, biz05, biz07, biz08, biz11, social01, social04, social07, social08, social10, social12, social13, social14, social15, social16, social20, axb01 to axb15, rollout1 to rollout4, bz01 to bz16, civic-wallet-rank, truth-telling-gains, tax-letter-norms, facebook-deactivation, forecast-training, genai1 to genai3, axf01, axf05, axf06. No invented scenario, no non-significant difference treated as real (axf05, axf06, social13, enforcers handle it), no overclaim found. Spot items worth a look: axb12 explain still says an algorithm "optimizing cost-effectiveness crowded them out" (the paper's wording, fine); bz13 and civic items I could not confirm.
- Cue analysis over the 36 choice and causal items: answer is the longest option in 7 (expected about 9); 9 of 36 answers contain a comparative or "only/always" word against 18% of distractors; forecasts: 16 true and 19 false, mean claim length 96 (true) vs 89 (false), negation in 1 of 16 true and 2 of 19 false claims. No blind strategy stands out (pytest gaming gates also pass). Odd-one-out cues remain: axb05 (the key is the only option that is not about the model's inputs), axb02 (two options are "adjust by 2 / by 10", the key is the lone "unchanged").
- Reading the screens: no scene, question, option or sample line states its answer. The first-screen citation on every predict screen shows journal and year ("Science 2023"); by owner decision.

## F. Introduced audit (iteration 66 items and 84 to 86)

(a) True/False plus sure-ness: bz11 (false) False@100 gives score 100, stored response 0, "Matches the study"; biz08 (true) False@90 gives -62, True@90 gives 98 (live class, phone 1); record keeps `response:0`, `confidence:null` for forecasts, calibration chart plots them as 100% sure; keyboard 1 and 2 choose, Tab reaches the slider with aria-valuetext "100 percent sure" and "not chosen yet", the buttons are 317x80 px, toggle state in aria-pressed. Classroom: phone reveal "You said True / The claim is True / You were 90% sure"; projector forecast reveal counts "Said true" and "Said false". All correct.
(b) Scaled question screen: 8 decisions at 1280x720, 1440x900, 1920x1080 and 4 browser zoom levels: no overflow, blur or clipping seen in 56 screenshots (shots/zoom_*), focus rings 2.4 to 3 px, option rows 56 to 80 px high; confidence slider is 36 px high (Optional). Fixed bar never covers a required control except meta-perception-causal at 1280x720 and 1366x768 (m-1).
(c) Tutor suggestions: see D.
(d) The four new decisions: A and E.
(e) Landing page: order matches the owner brief (headline, lede, sample, paths, Dimant band with three DOI-linked titles and "Show all 18 papers", credit); 0 overflow at 390, 820, 1280, 1440, 1920. DOI links not resolved (blocked).
(f) Review 41 fixes: I-1 notice (phone "Answers are closed." works), I-2 rollout4 scene now "some practiced ... everyone then took exams without it" (accurate), I-3 bz02 scene has no mechanism, I-4 ai02 no "blind", I-5 social12 tutor returns "9.65% ... 6.45% ... 3.20", I-8 allocate phone zero label present (shots/axb08_390_r.png), I-9 and I-11 the sample sits beside the headline (y 103 to 139 at 820 and 1280; slider y 410 at 1280x720), I-10 "Try one now" is a small label, I-13 credit links unchanged. I did not re-measure I-7 (principle strip +N). m-1 not identified in the supplied files.
Iteration 86 fixes: graph labels 13.3 to 13.4 px at 1280x720 and 1366x768, 17.6 px at 1024x768 (verified on 4 causal items, shots/fit_*). But the "nothing under the action bar at 1280x720" claim fails for meta-perception-causal (slider 36 px under, page scrolls 93 px), and 1024x768 still puts options under the bar on axb05, meta-perception-causal and dimant-notalie-causal (53 to 115 px). Tutor changes verified (D).

### Introduced

- **M-1 (Major) The record headline's minus sign is 14 px beside 128 px digits, so a negative total reads as positive.** Where: src/app.css line 829 (`.score-big .neg`) with a size rule from `.score-row span`; record page at 1440 and 390; shots/record_1440.png, shots/rec_neg_390.png, shots/rec_crop.png. Observed: DOM `<b class="num"><span class="neg">−</span>16</b>`, computed font size 128 px for `.num` (72 px at 390) and 14 px for `.neg`, sitting on the baseline; a 12-call record that sums to -37 shows a lone dash and "37". Why: the first number a player sees on the record, the one the page calls "skill points versus guessing", looks positive; the sparkline below the guessing line and the caption are the only other cues. Introduced by the iteration 84 edit to the minus span. Fix: `.score-big .num .neg{font-size:inherit;vertical-align:baseline}`, keep the 0.07 em gap, and add a test that the span's computed size equals its parent's (the lint missed it because rule R17 only checks the gap).

## G. Findings

- **m-1 (Minor) A required control sits under the action bar at the common laptop sizes.** Where: tools/fit.py logic (my fit.py), meta-perception-causal at 1280x720 (slider 36 px under, scroll 93 px) and 1366x768 (22 px under, scroll 79 px); axb05 at 1024x768 (two options 53 and 115 px under, scroll 274 px). Six predict screens scroll at 1280x720 (axb05 57, meta-perception-causal 93, dimant-notalie-causal 10, dimant-enforcers-rank 50, axf05 7, manylabs-anchoring 17). Why: the confidence step is required, and the ledger says nothing sits under the bar. Fix: for causal items put the graph left under the scene at heights under 760 px and keep options and slider on the right, or shrink the empty space above the graph (the right column starts 108 px down).
- **m-2 (Minor) Causal reveal on the projector uses 10.3 px labels.** Where: classroom projector reveal for axb05 at 1280x720 (shots/cls_proj_axb05_rev.png). Observed: node labels 10.3 px while other projector text is 13.9 to 15 px. Why: below the 12 px floor on the one screen shown to a room. Fix: scale the projector DAG viewBox to the column width (the diagram is about 500 px in a 1180 px card).
- **m-3 (Minor) A toast covers the live-class notice.** Where: solo play of a decision that a class has open (any served page; shots/locked_solo_ai01.png). Observed: the dark toast "A live class is running on this server. Practice mode returns when it ends..." sits over the yellow banner, hiding its text, and repeats it. Fix: drop the toast when the banner is shown.
- **m-4 (Minor) An offline phone's late answer ends on a mixed message.** Where: phone after reconnect in the causal and estimate rounds: "Responses are closed for this decision" with no "Not counted". Open since review 54 m-7. Fix: use the existing not-counted state for a 409 on a pending answer.
- **m-5 (Minor) Tutor: 33% direct, 3 wrong answers (ai09, axb08, bz07), setting questions still miss** (section D). Fix: stop the duration route from firing on "how long did each debate/session last" when the scene states a length; route "did women quit less" to the explain; the follow-up of ai01 "Who gained the most?" should match "Which kinds of workers got the biggest boost?".
- **m-6 (Minor) Reveal holes at wide widths.** Where: axb05 at 1920 (291 px, shots/axb05_served_1920_reveal.png), ai07 192 to 221, facebook-deactivation 225 at 1440; right-column gaps beside short figures (axb01, dimant-competition-choice 130 to 150 px). Fix: see the Visual list below.
- **m-7 (Minor) The served page ships the Dimant paper titles next to the decision-to-source map** (`bandTitles` plus `challenge.sources`, verified in the served HTML; open since review 54 m-8). A student reading the source can name the paper behind social15 ("Hate Trumps Love") before the call. Fix: serve bandTitles without decision ids, or key it by order.
- **m-8 (Minor) Instructor reveal screen puts the answer below the fold at 1280x720.** Where: console after "Reveal to the room" (shots/cls_inst_axb01_rev.png): the card repeats the question, the count and "Back to waiting screen", and the revealed title starts at y 650. Fix: put the revealed result above the repeated scene.
- **m-9 (Minor) Reveal tab row is half hidden under the action bar on first view at 1280x720** (shots/sw_file_1280x720_biz08_r.png: "Questions, Scope, Source" cut at y 622 to 637). Fix: add bottom scroll margin or move the tabs above the study card.
- **o-1 (Optional) Four tutor chips are identical on all 116 decisions** ("How would I test this in my company?", "Who took part", "Who wrote the paper?", "What should a manager do with this?"); only the first is generic text. Make the first item-specific (from `implication`) or drop it.
- **o-2 (Optional) The confidence slider is 36 px high** (target size below 44 px at browser zoom 150 to 300%); WCAG 2.2 AA 24 px is met. Raise the slider's hit area to 44 px.
- **o-3 (Optional) Odd-one-out cues in axb05 and axb02** (section E).
- **o-4 (Optional) Lint blind spots:** the design lint runs at 1440 and 390 only (see M-1 and m-1); add the minus-size check, 1280x720 and 1366x768.

## H. Three changes that would raise Visual most

1. **Reveal columns at 1920x1080 and 1440x900 (axb05: 291 px empty under the left text; ai07 221 px; facebook-deactivation 225 px).** Put the study card (Design, Sample, Published, Checked) in the left column under the manager line for any item whose figure is taller than the text, so both columns end together; where the figure is short (axb01, competition) move the principle-strip into the right column.
2. **Record headline (M-1).** Fix the minus size (14 px against 128 px) and set the number as one tabular figure run; add a thin guessing baseline label to the sparkline. This is the most visible screen after the reveal and the defect is the first thing a creative director would see.
3. **Projector at 1280x720.** Open state: question 22 px, body 14 px, 150 px empty in the card (shots/cls_proj_axf01_open.png); reveal of causal: labels 10.3 px (shots/cls_proj_axb05_rev.png). Scale the option list and the DAG to the column width and use the free height for them.

## I. Could not verify

- DOI resolution (proxy blocks Crossref and doi.org): unverified for all 113 sources.
- Fact-check against papers for every item except the 9 listed in E (all others only for internal consistency; Cohn et al. and Dell'Acqua partly on the web; Dell'Acqua per-arm quality numbers 29.9 and 33.9 unconfirmed).
- Play sweep covers 24 decisions at 1440 and 8 at the other viewports (112 plays), not 20 per viewport and not every decision; every predict screen at 1280x720 was measured for fit (116), the others at 1366x768 and 1024x768 only for 7 causal and tall items.
- Screen-reader use (NVDA, VoiceOver): not done; only ARIA and keyboard checks.
- Streamlit's native live class and tutor: not driven.
- Two-hour release of an abandoned class (code reading plus the observed lock): not waited out.
- Gemini: no key available; not tested.
- Page-versus-server tutor parity for chips was only checked through the pytest parity test, not on my 115 questions' suggestion lists.
- "Stranded word" detector: my own measure was invalid (it ignored tied spans); the lint (R34) passed and I saw no stranded word in the screenshots I read.
- Screenshots viewed: about 20 of the roughly 300 saved in shots/.
