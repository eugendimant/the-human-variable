# Independent review 52 (snap, iteration 88)

**Score: 82/100.** 0 Blocking, 0 Major, 14 Minor (13 listed in section 8, 1 introduced by iteration 88 in section 9), 8 Optional (7 + 1 introduced).

Reviewer note: the supplied prompt names this "review 52"; the ledger calls it review 56. The diff file named in the prompt (changes_since_review50_snapshot.diff) was not in the folder, so I audited the code and content directly. Work was done in a copy (`r56/work`); `/home/user/the-human-variable` was not read or changed; nothing was published. Scripts are in `r56/tools/`, data in `r56/*.json`, screenshots in `r56/shots/`.

## Score table

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All 26 stored quotes of the four iteration-66 items verbatim in the PDFs and every number and design matches; 5 more Dimant items (deviant, masks, hate, social15, social16) and 2 Mellers items checked; 100+ items and all DOIs not checkable here. |
| Learning | 15 | 11 | Predict, commit, reveal and calibration work and True/False scoring is exact in 12 of 12 cells; but the tutor answers 43% of 108 own-wording questions directly (71% direct or partial), 1 wrong, and one confident forecast miss reads "-300". |
| Visual | 15 | 12 | Calm, consistent, no overflow, no stranded word in 500 plays; reveals now balanced (holes of 60 to 100 px) except causal (285 px at 1920); projector text 12.9 to 15 px at 1280x720; unset sliders show a stray "?". |
| Gameplay | 15 | 13 | 500 scripted plays (25 decisions, 8 formats, 5 viewports, file and served, fresh and with a record): 0 errors, Lock enabled after every legal call; 6 predict screens scroll at 1280x720 and one puts the required slider fully under the bar. |
| AI and business relevance | 10 | 9 | Every item ends in a manager action; AI track strong; the four new items are business-facing (reproducibility, competition, nudges, compliance timing). |
| Content | 10 | 8 | Designs described correctly, null results handled; no number error in the 70+ items read; option cues remain in 5 items (meta-perception-causal, biz07, axb12, bz06, bz15) and a title cue in dimant-contagion-multi. |
| Technical | 10 | 8 | 415 passed, lint `{}`, build current, axe 0 on 42 scans, page and server tutor identical on 108 questions and 601 chips; served page still ships the 21 Dimant paper titles mapped to their decisions; heavy runtime layout JS. |
| Classroom | 5 | 4 | 3 phones, 8 decisions in 8 formats, offline-then-online phone recovered, closed phone shows no live control, 0 leaks by any route; 120 joins in 0.2 s (121st refused); projector text small. |
| Accessibility | 5 | 4 | axe 0 on 42 scans; 3 px focus rings on options and sliders; slider aria-valuetext "75 percent sure"; one invisible focus stop (`.in-play`); no screen reader run. |
| **Total** | 100 | **82** | |

Calibration (after forming my own view): review 55 gave 80 and review 51 82. Nothing Major or Blocking turned up and the iteration 86 to 88 fixes hold, so I land at 82; the tutor and the causal-reveal hole are unchanged and keep Learning and Visual where they were.

## 1. Gates I ran

- `python -m pytest -q -x`: **415 passed in 1247.60 s**, run to completion in my copy (nothing browser-heavy beside it for the first 20 minutes except `design_lint`, which is part of the gates).
- `python3 tools/design_lint.py`: `by rule: {}`. `python3 src/build.py --check`: "built pages are current".
- axe 4.x (tests/vendor/axe.min.js; wcag2a, 2aa, 21a, 21aa, 22aa, best-practice): **42 scans, 0 violations.** 40 on file and served pages at 1440 and 390 (home; predict of repro-msci-estimate; reveal of repro-msci-estimate, axb05, axb07, axb01, forecast-teams-rank; record after plays; Library "almanac" and "atlas"), 1 on the console setup page, 1 on the projector view at 1280x720 (open and revealed states were scrolled through, one scan at the end).
- DOIs: `tools/verify_dois.py` not run (blocked). The 18 Dimant DOI links on the landing page exist as anchors with `https://doi.org/...` hrefs; resolution is unverified.

## 2. Play, measurement and screenshots (items 2, 8a, 8b)

- 500 plays: 25 decisions (all 8 formats; the 4 new items; 3 causal, rank, 2 allocate, 4 delegate, 2 multi) x 5 viewports (390x844, 820x1100, 1280x720, 1440x900, 1920x1080) x fresh profile and a profile with 4 rounds already in the record, 250 on `file://index.html` and 250 on the served page (own server, port 18732). 0 page errors, 0 console errors, 0 horizontal overflow, Lock enabled after every legal answer, 0 stranded last words (word rectangles, headings, paragraphs and list items). Screenshots read: `shots/file_fresh_*_{390,1280,1440,1920}_{pred,rev}.png`, `shots/home_*.png`, `shots/record_neg_*.png`, `shots/proj_1280_*`, `shots/cls_*`, `shots/rv2_*`.
- Smallest rendered text (zoom-corrected): predict 12.4 px at 390 to 1280; reveal 11.9 px (delegate chip "You: Human and AI together"); projector at 1280x720 12.9 to 16.8 px (13.4 on repro-msci-estimate, 12.9 on axb05 "Where the evidence comes from").
- Predict screens at 1280x720 on all 116 decisions: 6 scroll (axb05 777 px, meta-perception-causal 813, dimant-notalie-causal 730, dimant-enforcers-rank 770, axf05 727, manylabs-anchoring 737). On meta-perception-causal the required confidence slider has top 637 = top of the fixed action bar, so it is fully hidden (`shots/pred_meta_1280.png`); on axb05 it starts at 601 and is half under. 1440x900 and 1920x1080: 0 scroll, 0 under the bar. 1536x864 at 125% zoom: 0 scroll. 1024x768: 38 scroll. 960x540 (200% on a 1920 screen): all 116 scroll and the first option or the slider sits under the bar on most. Hit targets under 24 px: none. Horizontal clipping: none at any size. Text at the scaled sizes (CSS zoom 1.4 to 1.6) is crisp in the 1920 screenshots.
- Focus: options, sliders, skip link and close button show a 2.5 to 3 px solid ring (rgb 47,84,235) at 390, 1440 and 1920. Tab order reaches `.in-play` (a 1920x1042 container) with `outline: none` between the slider and the skip link: an invisible focus stop.
- True/False plus "how sure" (item 8a): truth True and truth False, answered True and False at 50, 75 and 100: scores 0.5 / 0.875 / 1 when right and 0.5 / -0.125 / -1 when wrong, symmetric in all 12 cells. Slider min 50, max 100, aria-valuetext "75 percent sure"; arrow key moves 5; Lock stays disabled until the slider is touched; buttons expose aria-pressed. The record headline is skill = (score - 0.5) / 0.5, so one 100% miss reads "-300" while the call list beside it reads "-100" (explained in one sentence under the list).
- Record page (iteration 87 and 88): with a negative total the minus is 128 px like the digits at 1440 and 1920 and 72 px like the digits at 390 (computed style), same colour. "Practise AI x Business, your weakest area" shows only with 2 or more areas at 2 or more calls; it started a 10-decision round, all in that area, unplayed decisions first; a fresh browser shows no button and the text "Nothing here yet".
- Reveal (iteration 88: two tabs, "Covers" row): reviewed at 390, 1280, 1440, 1920 on 8 decisions. Nothing is lost (Published stays in the card as a link, Covers carries the old Scope line). The full-width Covers row ends the study card cleanly. Wide balance is good on choice, forecast, estimate and multi (holes 60 to 100 px). Unchanged on causal: axb05 left column ends at y=665, the tab row starts at 950 at 1920 (285 px empty); about 237 px at 1440, 165 px at 1280.

## 3. Live class (item 3)

Own server; instructor page, one projector (the console's projector mode at 1280x720 and 1920x1080), three 390x844 phones, 8 decisions: forecast (axb07), rank (forecast-teams-rank), allocate (axf01), delegate (axb01), causal (axb05), estimate (repro-msci-estimate), choice (dimant-deterrence-choice), multi (axb11).
- Phone 1 answered; phone 2 went offline before answering, answered ("Sending your answer... Reconnecting..."), came back online and its answer was confirmed ("Your answer is in") in 8 of 8 decisions; phone 3 never answered and, when the instructor stopped answers, showed "Answers are closed." with no option, slider or lock control in 8 of 8 (`shots/cls_phone_closed_axb01.png`). Evidence appeared on all phones after Reveal.
- Leaks: no answerTitle or explain text on a phone or projector while open (checked by text); HTTP probe of the open and closed states: no `answer`, `truth`, `rankAnswer`, `multiAnswers`, `answerTitle`, `explain`, `implication` or `target` in the student state; `/api/reveal/<id>`, `/api/library` (empty), `/api/challenges`, tutor ("opens after your instructor reveals it"), `/api/instructor/bank` and the CSV were refused or empty; sibling decisions on the same paper: none for this item, the code holds them. Phone-side queued answers survive a dropped link.
- 120 joins from one IP in 0.2 s; joins 121 to 130 got 409 "This session is full" (MAX_PARTICIPANTS 120). 118 concurrent answers: all 200 in 0.17 s. Wrong challenge id 409, invalid answer 400, unknown token 403, late answer after Stop 409, title of 5,000 characters truncated to 80, forged instructor key 403, open with a path-like id 400.
- Projector at 1280x720: nothing scrolls, no overflow, axe 0; question 30 px but the finding ("Cost was a biased proxy for need") is a 16 px bold line (`shots/proj_1280_rev_axb05.png`). At 1920x1080 smallest text 14.9 to 16.8 px.

## 4. Tutor (item 4)

- 108 questions in my own wording, 27 decisions (incl. the four new ones), none taken from reviews 51 to 55 (`tools/qs.py`; answers `tutor_server.json`; grades `tutor_grades.json`). Page `curated()` in the browser and `server/tutor.py curated()`: **identical on 108 of 108**. Graded by me: **46 direct (43%), 30 partial (28%), 31 miss (29%), 1 wrong (1%)**; useful (direct or partial) 70%.
- Wrong (1): dimant-megastudy-estimate, "how long did the emails run" -> "The effects persisted in the 8-week period after the intervention." (the emails ran 4 weeks; the answer is the follow-up for "Did the effect last?", picked by the words "how long").
- Misses (31), by question: dimant-deterrence-choice "is this the first study of fine timing" (the follow-up "What was new in this study?" exists) and "why do both extremes work"; repro-msci-estimate "how many reviewers" (700 sits in the scene only; answer prints the 95% sentence) and "what does it mean to reproduce a paper"; dimant-competition-choice "real workers or students"; dimant-megastudy-estimate "what was the control condition" (a reminder; in the scene), "how many teachers" (140,461 in the scene); axb07 "what should HR do about AI-written applications", "what cues did people lean on" (fallback prints them but says "could not match"); rollout1 "who benefited least"; judg05 "what does this mean for how I present investment options"; axe06 "what tasks counted as completed", "which companies took part"; axe05 "were the doctors real", "does that mean chatbots are better doctors" (gets the 45.1% empathy line instead of the scope); social08 "what was the health behavior"; accuracy-prompt "what exactly did the message say", "how many Twitter users"; truth-telling-gains "what is the die roll task", "how many studies were combined", "do managers need to worry about expense fraud then"; misperceived-norms-support "how many men took part" (gets 87%/63%); dimant-opioid-forecast "what was on the reminder cards", "how much cash did veterans get"; forecast-teams-rank "can I run this inside my company"; axe14 "what did the bot sell", "what should a company do with this result"; biz11 "was the wheel rigged", "how do I avoid being anchored in a negotiation", "did paying for accuracy help" (the scope line says it did not), "who were the participants" ("Who was studied: see the paper"); axb04 "do experts ever win", "what should a hospital do with this".
- Suggestion chips (item 8c): every one of the 116 decisions, at the reveal, offers up to 7 chips (601 in all); all 601 answered identically on page and server, none fell to "could not match", none appears before the call (0 `data-ask` buttons on any predict screen). But 464 of the 601 are the same four generic chips on every decision (How would I test this in my company? / Who took part in the study? / Who wrote the paper? / What should a manager do with this?) and 70 are "What does the study cover?"; only 67 are decision-specific.

## 5. Fact checks (item 5)

Checked against the PDFs in `papers/` (pdftotext, whitespace, hyphenation and dash normalised) or the paper online:
- **repro-msci-estimate** (Fisar et al.): >700 reviewers, nearly 500 articles, policy 2019, >95% reproduced when data accessible, 29% data not accessible, 68% across all, 12% voluntary before and 55% of those; reason list; all 6 quotes verbatim. Design and question wording ("at least largely") match the abstract.
- **dimant-competition-choice** (Huber et al.): 18,123 participants, 45 of 95 designs, d = -0.085 (CI -0.147 to -0.022), heterogeneity about 1.6 times the average standard error, "suggestive evidence"; 6 of 6 quotes verbatim.
- **dimant-megastudy-estimate** (Duckworth et al.): 140,461 teachers, 2,992,027 students, 15 nudges plus reminder-only control, 4 weeks fall 2021, 5.06% (3.30% after the winner's curse), 1.89% any nudge, 2.26% personalised data, effects persisted 8 weeks; 7 of 7 quotes verbatim.
- **dimant-deterrence-choice** (Buckenmaier et al.): 296 subjects, card-guessing game (the scene says "card game"), resolution immediate or delayed 2 periods, punishment t+1 or t+3 (IR-D) and t+5 (DR-D), non-monotonic relation, IR-ND and DR-D best; 7 of 7 quotes verbatim. The implication names only the quick-verdict-slow-fine arm (IR-D); the paper's lowest are IR-D and DR-ND (Optional below).
- **dimant-deviant-choice** (Bicchieri, Dimant & Xiao): 418 participants, 42.7% vs 28.7% and 22.2% vs 36.5%, low and high stakes; one quote (418 participants) fails only on a footnote number inside the sentence.
- **dimant-masks-forecast** (Dimant et al. 2022): 7 messages, N = 4,931, 1,034 forecasters, no evidence any message worked, forecasters overestimated; quotes found (4 false negatives are duplicates split by line breaks).
- **dimant-hate-choice, social15, social16** (Dimant 2024): 15 experiments, over 8,600 participants, closeness 78.1% vs about 39%, 14.97% vs 13.54%, 11.99%, -22.9%, 72.8% to 59.0% and 73.2% to 62.4% conditional cooperators, default from about 20% to essentially 0% taking: all present in the paper.
- **forecast-teams-rank, forecast-training** (Mellers et al. 2014, escholarship copy): team > crowd-belief > independent (t = 5.52 and 5.92); 2,246 participants in year 1; scenario training also beat no training (t = 3.25) and probability training beat scenario (t = 2.23), so "Neither beat no training" is a false option as intended.
- Not checkable here: biz07 (the page I could open had no numbers: "eight experiments" only), and the other roughly 100 decisions; the Dimant items not in `papers/` were read for internal consistency only.
- Total checked against papers: 13 decisions (4 new + 5 other Dimant incl. 3 of the three given + 2 Mellers + social15/16 counted above).

## 6. Leak and cue audit (item 6)

- Wire audit of all 116 decisions (`public_challenge`): no estimate target or number inside its band appears in the public scene, question, study line or title; no answer-bearing key in the payload. Title overlaps with the answer title exist for 6 items; only dimant-contagion-multi ("Which behavior spreads faster?" tells that the behaviours differ, which is option 2's content) and biz08 ("Under pressure" for a claim about pressure) lean on it.
- Option form: of 32 choice items the keyed option is the longest in 8 (chance about 9.2); it is the only two-part option in 2; answer positions 0 to 3 are 11, 8, 8, 5 (a mild lean to the first). Forecast claims: 16 of 35 true; true claims are 7 characters longer on average (95.8 vs 88.8); negation 2 of 16 true vs 5 of 19 false: no usable cue.
- Cues worth fixing: **meta-perception-causal** (a causal question whose only option about random assignment, "Randomly correcting beliefs cut obstructionism ratings", is the keyed one); **biz07** (adding a review step and automating a step are both additions, so "removing" is the odd one out); **axb12** (the only option about cost); **bz06** (the scene says "training, practice rounds and anonymous offers" before asking what happened to the gap, which points at "disappeared"); **bz15** (three options, the answer is the one every student knows).
- Blind strategies: constant guess on estimates is capped by the existing gates (0.35, owner decision); I did not find a new blind strategy that earns skill.
- Served page: `BANK.bandTitles` plus each decision's `sources` ids put the title of the paper behind each of the 21 Dimant decisions in the page source (verified by fetching `/`; e.g. dimant-deterrence-choice -> "Efficient Institutions and Effective Deterrence: On Timing and Uncertainty of Formal Sanctions"). Documented since review 54; reading the source is required.

## 7. Content quality (item 7)

Read in full (scene, question, options or claim, title, explanation, implication, boundary): 60 least-mentioned decisions (biz07, biz08, biz11, social07, social08, social10, social14, judg05, judg09, axb04, axb07, axb09 to axb13, rollout1, rollout2, bz01, bz03, bz05, bz06, bz08, bz10, bz15, bz16, civic-wallet-experts, truth-telling-gains, rule-violations-honesty, tax-letter-norms, opposing-views-bot, accuracy-prompt, misperceived-norms-support and -action, forecast-teams-rank, forecast-training, overconfidence-hard-task, dimant-requiem, -proximity, -contagion, -enforcers, -observability, -motivated, -conspiracy, -opioid, -polarizednorms, axe04 to axe11, axe13, axe14, genai2, genai3, axf02, manylabs-anchoring), plus the 4 new items and 5 further Dimant items: 70 in all. No number or design error found. Points:
- Design descriptions are correct and null results are handled (axe13 sneakers "not significant", genai2 "not statistically significant", dimant-enforcers-rank equity bribe gap "not statistically significant").
- Dimant explanations repeat one sentence frame: "X, Dimant and colleagues show, with N Y, that ..." (dimant-opioid-forecast, -polarizednorms-choice, -contagion-multi, -observability-forecast, -conspiracy-choice): reads as template copy.
- bz16, dimant-requiem-forecast, bz05 and axe06 are handled with care (limits stated in boundary).
- Invented scenarios: genai2 "Your team will publish persuasive AI-written articles" and bz01 "Your agency compares..." are framings, not data; harmless.
- Scoring bands: axe06 (target 26.08, tolerance 10 on 0 to 100) is generous, bz03 and bz05 are fair.

## 8. Findings

### Blocking
None.

### Major
None.

### Minor (13)

1. **Tutor answers 43% of own-wording questions directly (71% direct or partial), 29% miss.** Where: `server/tutor.py curated()` and `src/app.js curated()` (identical); list in section 4. Why: the tutor is the learner's main help after the reveal and the same families fail again and again: counts that sit in the scene ("how many teachers/reviewers/men"), "what should HR/a hospital/a company do" (the stored implication is not routed), what-was-the-control and what-did-it-sell (scene facts), "was it rigged / did paying help" (boundary facts). Fix: route "how many / how much / which companies" to the scene and study numbers; route any "what should [role] do" to the implication; let the scope and scene sentences answer "what was / what did" when they share a rare word; add the 31 misses to `tests/tutor_phrasings.json`. Same arithmetic as reviews 53 to 55 (33 to 35% direct), so no improvement since.
2. **Tutor gives one wrong answer: "how long did the emails run" on dimant-megastudy-estimate returns the 8-week persistence follow-up.** Where: duration route in both tutors; scene says four weeks. Fix: when the question is "how long did X run", answer from the scene's duration ("weekly emails for four weeks"), and keep "did it last" for persistence.
3. **Required confidence slider is hidden under the action bar at 1280x720** on meta-perception-causal (slider top 637 = bar top 637) and half hidden on axb05 (601); 6 predict screens scroll (axb05, meta-perception-causal, dimant-notalie-causal, dimant-enforcers-rank, axf05, manylabs-anchoring). `shots/pred_meta_1280.png`. Why: a student sees "How sure are you" and no control and a disabled Lock. Fix: scale the causal diagram by 0.85 below 760 px height, or put the confidence row inside the action bar for these formats.
4. **Causal reveal still leaves a hole under the left text column**: axb05 at 1920 the left column ends at y=665 and the tab row starts at 950 (285 px); about 237 px at 1440. Fix: in `fig-tall` mode let the Questions list sit under Covers in the left column and the tutor box under the figure, as two independent columns, instead of one full-width tab band.
5. **Projector text at 1280x720 is 12.9 to 15 px, and the finding is a 16 px line.** Where: `shots/proj_1280_rev_axb05.png`, `src/classroom.css` lines 83 to 94. The room cannot read "Where the evidence comes from" (12.9 px) or "For a manager" body (13.4 px on repro-msci-estimate); the question stays 30 px but the answer title is smaller. Fix: after reveal make the answer title the largest line, remove the join banner instead of shrinking it, and cut the manager and scope text to one line of 20 px or more.
6. **Unset sliders show a thumb and a lone "?".** Where: every predict screen (`shots/file_fresh_axb07_1440_pred.png`, `..._repro-msci-estimate_1280_pred.png`). On the forecast slider (50 to 100) the thumb sits at the midpoint, which reads as 75% already chosen, and the first arrow key jumps to 80. Fix: no thumb until touched, and "50%: a coin flip" / "100%: certain" labels under the confidence slider of choice items (they exist only on forecast).
7. **One confident miss reads "-300" on a scale described as 0 to 100.** Where: record headline (`shots/record_neg_1440.png`); the call list under it shows "-100" per call while the headline is -300 (skill = (score - 0.5) / 0.5). Why: a first-time player who sets 100% and misses sees a number far outside the scale and two different scales on one page. Fix: show the headline on the same scale as the list, or clamp the first five calls and say "-300 means 3 times worse than guessing".
8. **Option cues in five items**: meta-perception-causal, biz07, axb12, bz06, bz15 (section 6). Fix: give meta-perception-causal a second option with random assignment that is not the cause test (for example "A field survey tracked the same bias over time"); make biz07's distractors one subtractive and two additive but different in kind; remove "training, practice rounds and anonymous offers" from the bz06 scene and move it to the explanation.
9. **Title cue in dimant-contagion-multi ("Which behavior spreads faster?")** and, mildly, biz08 ("Under pressure"). Fix: "Peers and behavior" and "A second task".
10. **The served page ships the title of every Dimant paper next to its decision id.** Where: `server/app.py public_bank()` (`bandTitles`, `sources`). Unchanged since review 54; 21 decisions. Fix: send `bandTitles` only to the landing band and fetch the decision's `sources` with the evidence after the lock, as `/api/reveal` already does for takeaways.
11. **Generic tutor chips fill the reveal.** 464 of 601 chips are the same four on every decision and repeat what the study card above them already prints (Sample, Published, Covers). Where: `tutorChips()` in `src/app.js`. Fix: show the decision's own three follow-up questions as chips and drop the generic four (the free-text box stays); that also removes the duplicate list of questions in the tab.
12. **Invisible focus stop.** `.in-play` (1920x1042 container, `outline: none`) is in the tab order between the slider and the skip link. Fix: remove its tabindex, or give it the same ring.
13. **Delegate reveal chip text is 11.9 px** (`You: Human and AI together`, axb01 at every viewport; design rule 9 says 12 px minimum). Fix: set the chip to 12.5 px.

### Optional (7)

1. Landing lede is set in six short lines (about 390 px in a 520 px column, hard breaks), leaving the column half empty; one paragraph at `text-wrap: pretty` would use the width (`shots/home_1440.png`).
2. dimant-deterrence-choice implication names only the quick-verdict-slow-fine arm; the paper's lowest deterrence is in both mixed arms (IR-D and DR-ND). Say "mixing a quick verdict with a slow fine, or the reverse".
3. At 200% browser zoom on a 1920 screen (960x540 CSS pixels) all 116 predict screens scroll and the first option or slider sits under the bar; at 1024x768 38 do. Reachable by scrolling.
4. The room holds 120 students; executive classes above that need a second session. State the cap on the console.
5. While a class is open on a server, `/api/library` returns nothing and `/api/reveal` returns 409 for everyone on that server (documented); a note on the home page would save a support question.
6. biz11 tutor "Who was studied: see the paper" is the only decision with no sample line; add the paper's N or say the study did not report it.
7. Dimant sentence frame ("X, Dimant and colleagues show, with N") repeated in 5 explanations; vary or drop "show".

## 9. Introduced by iteration 87 and 88

No Blocking or Major defect. The minus-sign fix (87) holds at 390, 1440 and 1920. The two-tab reveal, the Covers row, the weakest-area button and the two tutor phrasings (numbers: "what were the callback percentages"; design: "how was the bias measured") all work; the build script and `gates.sh` are not exercised by users.
- **Minor (introduced by 88): the new "Practise <area>, your weakest area" button strands a word at 390.** `shots/record_neg_390.png`: "Practise AI x Business, your weakest" / "area" (the orphan detector R34 covers paragraphs and headings, not buttons). It is a wider button for "Culture & Society" or "Pay, flexibility..." tracks. Fix: shorten to "Practise <area>" with the weakest-area reason as a sentence above, or tie the last two words.
- **Optional: the button names the lowest area even when its skill is positive** (the text "your weakest area" is relative), and with only one area at 2+ calls it does not appear (design intent: at least one other area to compare). Not verified: whether "Play another round" after "Practise" returns to all areas (see Could not verify).
- Not introduced but newly visible: the four-chip generic list is now the only visible suggestion UI because the Source and Scope tabs are gone (Minor 11).

## 10. Server audit (item 9)

- Limits: body capped at 8,192 bytes, JSON object only, content-type checked, 15 s socket timeout, token buckets per client and per IP (join burst 130, answers 12 per client), request_queue_size 128, SQLite WAL, CSP with `connect-src 'self'`, `frame-ancestors 'self'`, nosniff, no-referrer; `THV_TRUST_PROXY` uses the right-most `X-Forwarded-For`.
- Validation: answers validated against the decision's format (`scoring.valid`), confidence 0 to 100, room titles cut to 80 characters, instructor key compared with `hmac.compare_digest`, room creation refused (403) on a non-loopback host with no `THV_INSTRUCTOR_PASSCODE`.
- Secrets: no key in the served page; tutor with no key reports `curated only`; Gemini key read from the environment only.
- Streamlit headless, port 18741 without a passcode and 18742 with `THV_INSTRUCTOR_PASSCODE=sekret`: both start and report `ok` on `/_stcore/health`; the four pages (Play, Join a class, Run a class, Ask the tutor) load without errors. Without a passcode Play embeds the game and "Run a class" shows "No instructor passcode is set, so anyone who opens this page can start a class"; with a passcode Play shows "This deployment runs live classes... Self-study play is available in the offline game" and "Run a class" asks for the passcode. I did not run a full class through Streamlit and did not try a wrong passcode.
- 30 to 120 concurrent students: 120 joins and 118 simultaneous answers on the standard-library server in under 0.3 s each batch, no errors. I did not run a sustained load or the Gemini path (no key).

## 11. What I would cut, and what to generate instead

Cut:
- The four generic tutor chips on all 116 decisions (they restate the study card); show the three follow-up questions as chips and drop the accordion list, or the chips, not both.
- The "Your note" tab on the reveal: a one-field private note on every decision is rarely used and adds a second row of controls under the card; keep it behind the record page.
- Library "almanac" and "atlas" plus custom round plus 8 paths: five ways to pick a decision. Keep paths and one searchable list.
- On the record page: Export CSV, Export JSON and Erase as three link-buttons beside the two primary buttons; move them under "How scoring works".
- The calibration plot with a single dot (under 5 calls) and the guessing sparkline beside the headline number; show them from 5 calls.
- Runtime layout code: `balanceReveal`, `fitQuestion`, `fitHeadings`, `balanceRecord`, `fitProjector` and `tieEnds` measure and move boxes after render; most of the remaining hole and under-the-bar defects come from them. Replace the reveal balance with two CSS grid columns and fixed placement rules.
- About 60 dated one-off content scripts in `tools/` and 55 reviews in `qa/reviews/`; archive them, keep the ledger's last 10 iterations.

Generate from the data instead of keeping by hand:
- The suggestion chips and the tutor's count, sample and "what should X do" answers from `study.n`, `scene`, `follow` and `implication` (they exist as fields).
- The landing page path lines and counts, the README counts (already synced) and `docs/SOURCE_INDEX.md` and `docs/SCIENTIFIC_AUDIT.md` from `bank.json` and `evidence.json` (the audit doc is already generated; the index is not).
- Option cue checks (length, two-part, distinct opening words, random-assignment wording) as a test over `bank.json` so reviewers stop finding them by hand.
- The "Covers" row from `boundary` (already) and the study line from `study`, `venue`, `year` (already); the projector stat strip from the same fields.

## 12. Three changes that would raise Visual most

1. **Causal reveal at 1920 (axb05, meta-perception-causal, dimant-notalie-causal).** Measurement: 285 px empty under the left column at 1920, 237 px at 1440, 165 px at 1280. Redesign: stop using one full-width tab band; make two independent columns. Left: headline, verdict, finding, manager line, study card, Covers, then the follow-up questions. Right: figure with the causal graph and options, then the tutor box. Both columns then end within 60 px of each other, as the choice and forecast reveals already do.
2. **Projector reveal at 1280x720.** Measurement: finding line 16 px bold, body 12.9 to 15 px, join banner still 70 px high, question 30 px. Redesign: after Reveal remove the banner, make the answer title the largest line (36 px), set the explanation at 20 px and show only the figure and the room's count beside it; the manager line and Covers go to the console. Target: no text under 18 px at 720p.
3. **Predict screens at 1280x720 and the unset sliders.** Measurement: 6 screens scroll, 1 puts the required slider fully under the bar (meta-perception-causal at 637 of 720), every slider shows a mid-track thumb and a "?". Redesign: move the confidence row into the action bar (label, slider, Lock on one line) so it can never be covered, draw no thumb until the first touch, and drop the "?" glyph; then predict screens never scroll at 1280x720 and the scale stays clean.

## 13. Could not verify

- DOI resolution (network blocked); `tools/verify_dois.py` not run.
- Facts in about 100 decisions not backed by the seven PDFs; biz07's numbers (the page I could open gave "eight experiments" only); only Mellers et al. was readable online among the other papers.
- Browser behaviour at real browser zoom and on a real phone (I emulated viewports and device scale; no pinch zoom); blur of CSS-zoomed text judged from 1920 screenshots only.
- A screen reader (none available); keyboard use checked by tab order, aria attributes and focus rings.
- Whether "Play another round" after "Practise <area>" returns to all areas (the `st.track` value stays set in the code path I read at `src/app.js` line 883); I did not play a round to the end.
- Streamlit: full class through the native pages, wrong-passcode path.
- A sustained load or the Gemini layer (no key); real students.
- Diff since review 50: the file named in the prompt was absent; I read the iteration 83 to 88 ledger entries and the code instead, so I cannot say a change outside them did not slip in.
- Page and server tutor were compared on my 108 questions and the 601 reveal chips only; the golden batteries were run only through pytest (passed).
