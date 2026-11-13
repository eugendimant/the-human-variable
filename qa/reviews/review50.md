# Independent review 50 (snap, iteration 79)

**Score: 82/100.** 0 Blocking, 0 Major, 14 Minor (12 not introduced, 2 introduced), 4 Optional.

Reviewer: fresh agent in a copy (`r50/work`). `/home/user/the-human-variable` was not read or changed; nothing was published. Scripts: `r50/tools/`; data: `play.json`, `tutor_res.json`, `cls_log*.json`, `axe.json`, `pytest.log`; screenshots: `r50/shots/`.

## Score

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | 80 of 81 stored quotes for the 4 iteration-66 items, masks, deviant, hate, and social16 found in the PDFs after layout normalisation (the one miss is a footnote number interleaved in the text, "418 participants (in 34 sessions"); numbers and designs of all four new items match; biz07 21% to 48% confirmed in the paper; two soft points (Introduced m-1, m-2). |
| Learning | 15 | 11 | True/False scoring right in 12 of 12 cells and the stored probability is right; but of 80 own tutor questions only 18 (22%) got a direct answer, 28 partial, 31 miss, 3 wrong. |
| Visual | 15 | 11 | Calm, low clutter, no overflow, strands or clipping in 390 plays; but the wide-reveal hole on causal items is unchanged (290 px at 1920), projector text is 11.6 to 13 px at 1280x720, and the new repro question makes a 6-line heading at 1280x720. |
| Gameplay | 15 | 13 | 390 scripted plays (26 decisions, 8 formats, 5 viewports, file and served, fresh and with a record): 0 errors, Lock enabled after every legal call; predict screen scrolls on 5 of 26 at 1280x720. |
| AI and business relevance | 10 | 9 | Items and paths read as management decisions (AI at work, algorithms, pay, defaults, compliance); the four new items are business-facing. |
| Content | 10 | 8 | 60+ decisions read; designs described correctly, non-significant results handled; option cues in 4 items and a "famous study then a re-test" frame that predicts False (5 of 7). |
| Technical | 10 | 9 | 405 passed in 1243.66 s, design lint `{}`, build current, axe 0 violations on 44 scans, 716 tutor chips identical on page and server, server validation holds. |
| Classroom | 5 | 4 | 3 phones, 7 decisions across 7 formats, dropped link recovered, closed phase, 0 leaks by any route; 120 joined and 120 answered in 0.2 s. Closed phone keeps live controls; projector text small. |
| Accessibility | 5 | 4 | axe 0 on 44 scans (file, served, console, projector, phone); True/False buttons expose aria-pressed and the slider has aria-valuetext ("70 percent sure"). Not tested with a screen reader. |
| **Total** | **100** | **82** | Two above review 49 (80), inside the spread between agents. The two iteration-79 content fixes are correct; no visible change otherwise. |

## Gate counts (item 1)

- `python -m pytest -q`: **405 passed in 1243.66 s**, 0 failed (`pytest.log`).
- `python3 tools/design_lint.py`: `by rule: {}`. `python3 src/build.py --check`: "built pages are current".
- axe (tests/vendor/axe.min.js; wcag2a, 2aa, 21a, 21aa, 22aa, best-practice): **44 scans, 0 violations.** 36 in `axe.json`: file and served, 1440 and 390; home; play and reveal of axb05, dimant-masks-forecast, axb08; record (with plays); library. 8 more on a live class: console lobby, open, revealed; projector open and revealed; phone waiting, open, revealed.
- DOIs: Crossref was not queried by me beyond the papers' own pages; `tools/verify_dois.py` was not run. See Could not verify.

## Introduced by iteration 79

No Blocking or Major defect. Both content changes are correct against the paper and the evidence file; the side effects are Minor.

- **I-1 (Minor). repro-msci-estimate question is now a 6-line heading at 1280x720** (`shots/pred_repro-msci-estimate_1280.png`). "Of all articles under the new policy, what share could be at least largely reproduced, counting inaccessible data as not reproduced?" is 21 words; the heading wraps to 6 lines of about 48 px in a 520 px column, the largest block on the screen, with the slider centred in the empty right half. The rule is correct (paper: 68% across all articles; 95% only where data were accessible; 29% inaccessible; quotes verbatim in `evidence.json`), and it also tells the player the answer is below the 95% headline. Fix: put the rule in the scene ("Articles whose data the reviewers could not access count as not reproduced.") and keep the question to "...what share could be at least largely reproduced?".
- **I-2 (Minor). false-news-spread: follow-up 2 now repeats the explain, and the key states a mechanism as a result** (`src/bank.json`, id false-news-spread). The explain gained "false news was also more novel than true news" (quote "false news was more novel than true news" is in `evidence.json`, Abstract). Follow-up "Why might people share falsehoods more?" already said exactly that, so the screen shows it twice. The key "Novel false stories drew more human shares" claims novelty caused the shares; the paper measures that false news was more novel and offers novelty as a possible reason. Fix: reword the key to "False stories were more novel, and humans spread them", and give follow-up 2 new content (for example how novelty was measured).
- Item (a) check: both edits match the paper and evidence. I checked every decision's stored quotes for a changed quote or number against the diff: the diff touches only these two strings in `bank.json`; `evidence.json` is unchanged.

## Findings (not introduced)

- **m-1 (Minor). Tutor coverage and 3 wrong answers** (`tutor_res.json`, 80 questions in my wording, each asked of the page's `curated` in the browser and of `server/tutor.py`; **80 of 80 identical text**). Direct 18 (22%), partial 28 (35%), miss 31 (39%), wrong 3 (4%). Wrong answers: social08 "how fast did the behavior spread" returns the reach follow-up (53.77% vs 38.26%) although the item has "How much faster?" (more than four times); dimant-notalie-causal "What does belief distortion mean in plain words?" returns the "Which beliefs were distorted?" answer; repro-msci-estimate "Did the authors share their own code?" returns only the citation and "Reproduction attempts by more than 700 reviewers". Misses where the item's own text answers: ai01 "was the writing quality any good or just faster" (follow-up "Did quality improve too?" exists); rollout4 "What did the students with the safeguarded tutor score?" (explain: no measurable exam harm); bz05 "Did people just work longer hours at home?" (explain: 9% from more minutes); rollout2 "Should we take AI away from our best people?" (the recommendation rule excludes "should we take"). Other misses (all fall back with "I could not match"): ai01 smaller company; ai02 replaceable; biz11; social12 identical résumés; axb03 judges; axb05 who built it and "remove race"; axb08; axb09; axb13; axb14 tasks; rollout4 real school; bz02; bz07; bz12 pay; bz13; bz15; truth-telling-gains; lies-in-disguise; tax-letter-norms; forecast-training; overconfidence-hard-task (overprecision); dimant-requiem; dimant-proximity; dimant-deviant "why backfire"; dimant-opioid cards; dimant-megastudy paid teachers; axf01... (full list in `tutor_res.json`). The router is a settled owner decision; the fix is to add the missing follow-ups on the 4 decisions above, not to retune the router (I16).
- **m-2 (Minor). Wide reveal hole on causal items** (`shots/rev_axb05_1920.png`; `tools/hole.py`). Left column ends 594, right column (figure plus option recap) ends 884: **290 px at 1920 and 1600; 236 at 1440; 176 at 1280**. Tabs start at 951. On the other 5 items I measured (megastudy, axb06, civic-wallet-rank, axb08, ai01) the right column is the shorter or equal one at every width (0 to 53 px). Fix: on causal items put the four-option recap in the left column under the manager line and let the figure end the right column.
- **m-3 (Minor). Projector text at 1280x720** (`tools/cls.py`; `shots/cls_open_prj_axb08.png`, `cls_rev_prj_dimant-masks-forecast.png`). Smallest rendered text: **11.6 px** on the allocate open screen ("Spread 100 points by how likely each option is..."), 12.4 px on causal reveal, 12.6 px on estimate reveal, 13.3 px on forecast; "For a manager" and "Where the evidence comes from" bodies are about 12.5 px. Forecast reveal: right column empty from y 390 to 670 (280 px); causal reveal 190 px. Fix: floor all projector text at 16 px, set the manager line at 20 px, and let the room's bars grow to fill the column.
- **m-4 (Minor). Predict screen scrolls at 1280x720 on 5 of 26 decisions** (`play.json`): axb05 +92 px, dimant-notalie-causal +45, manylabs-anchoring +17, repro-msci-estimate +10, axf05 +7 (fixed bar stays reachable). Zero scroll at 820, 1440, 1920.
- **m-5 (Minor). A phone that has not answered when answers close keeps live controls, and the toast covers text** (`shots/cls_phone_closed.png`). After "Stop answers" on axb05 the phone still has 4 enabled option buttons and the confidence slider; Lock is disabled. The toast "Answers are closed for this decision..." is a dark ellipse laid over the scene sentence and the first line of the question. Fix: disable the options when the phase closes and show the sentence as a line in the flow.
- **m-6 (Minor). Landing lede** (`shots/home_file_1440.png`): "Each round presents a real-life situation, from a / published research study, that you are / asked to predict. Once you have made your / prediction, ..." breaks mid-clause and reads as filler. Same text as review 49 (m-5). Suggest: "Each round gives you a real situation from a published study. Make your prediction, then see what the researchers found."
- **m-7 (Minor). Option and frame cues.** axb02: the key ("Could use the model only unchanged") is the one option unlike the two "Could adjust ... up to N" options. dimant-competition-choice: the key shares "small adverse" with option 3 and "disagreed widely" with option 1, so a player who only matches features lands on it. dimant-conspiracy-choice: the key is the longest and the only one built around "feedback", which the wording of option 2 also borrows. Replication frame: forecasts whose scene is "famous or classic study, then a second test or later records" are False in 5 of 7 (biz04, social10, bz10, bz11, bz16 False; bz08, manylabs True). Longest option is the key in 5 of 36 (chance 10.2), shortest 8 of 36; "always False" on the 35 forecasts is right 19 of 35 (54%).
- **m-8 (Minor). Wrong forecast can earn positive score**: True at 70% on dimant-masks-forecast (false) stores 0.02 and shows "Not what the study found. Score 2"; True at 55% stores 0.395 (observed in `THV.records()`). Consistent with Brier, but a "not what the study found" line with a positive number confuses first-time players. Fix: say "Score 2 (hedged, wrong)" or floor wrong calls at 0.
- **m-9 (Minor). civic-wallet-experts**: the claim "Fewer than half of the surveyed economists predicted that return rates would rise" is true with a wide margin (29% did), while the answer title says "Fewer than a third"; the threshold in the claim is looser than the title. Use the title's threshold.
- **m-10 (Minor). Text below 12 px in a figure**: phone reveal of repro-msci-estimate has SVG text at 11 px (`cls_log.json`, ph0_rev_measure).
- **m-11 (Minor). Landing and predict wording for a first-time player** (items d): the confidence prompt "How sure are you that you land within 6 points of the study value?" on estimates is jargon; the "?" beside an unset slider reads as help, "not set" would say it. The chip "Has it been replicated?" on repro-msci-estimate answers about replication materials (carried).
- **m-12 (Minor). Without client ids, 108 of 120 repeat answers are refused 429** (`tools/load.py`): per-IP buckets are shared when X-Client-Id is missing. The phone page sends ids (120 of 120 answers 200 in 0.2 s), so this only matters for scripted clients. Carried from review 48.
- **o-1 (Optional).** judg02 (pick two of three): the one false option is the only one that restates the leader's quote, so two of three is trivial.
- **o-2 (Optional).** dimant-competition-choice scene says researchers "drew 45 of them at random"; the paper draws 50 and 45 delivered software (the abstract itself says 45). Fine as written; "45 that ran" would be exact.
- **o-3 (Optional).** axb08's question says "clearly beat", which the reveal confirms with the 81.2% bar and two "not significant" bars; fine, but the word points at the one significant option.
- **o-4 (Optional).** Scene for dimant-deterrence-choice omits the second consequence (suspension) the paper adds to the fine; the stated design stays true.

## Item 2: play

- 390 plays: 26 decisions (all 8 formats; choice, causal, multi, estimate, forecast, rank, allocate, delegate) at 390x844, 820x1100, 1280x720, 1440x900, 1920x1080; file:// and served; fresh profile (130 each) and with 4 rounds already in the record (65 each). **0 page errors, 0 horizontal overflow, 0 stranded last-line words, 0 clipped text, 0 Lock failures.** Smallest text on predict 12.5 px, on reveal 12 px (delegate chips). Screenshots read: home, predict (repro 1280, axb08 390), reveal (axb05 1920, repro 1280, forecast 390), record (1440), library (1440), projector and phone in class.
- Served page: `/api/challenges` carries no truth, answerTitle, explain, implication, boundary, follow or sources for open decisions; served reveals work after the play.
- **Record page** (`shots/record_file_1440.png`, 16 calls): left column ends 1265, right 1230; balanced. Calibration plot labels each dot with its calls; "as sure as right" labelled in place. No blank-column defect at this state (review 49 m-7 measured at 1, 3, 7 calls; I did not re-measure those).
- **First-time player, phone (item d):** home, one-line credit, lede, sample, paths read in order; the predict screen holds scene, question, source line, controls and a fixed Lock bar with nothing to decode; the only confusion is the confidence phrasing and the "?" (m-11). Reveal opens on the finding, then the score sentence, then the figure; tabs are below the fold.
- **First-time player, 1280x720 laptop:** the sample card is above the fold with the headline; predict is one screen on 21 of 26 decisions; the reveal shows headline and explain, the figure on the right, and the manager line sits under the fixed bar (a second scroll). The heading of repro-msci-estimate (I-1) is the heaviest screen.

## Item 4: tutor and chips

- **Chips:** 716 chips shown on the reveals of 115 decisions (judg02's play was not driven by my script, so not covered); **716 of 716 return the same text on the page and the server and none is a fallback answer**; the tutor panel and chips are absent before the call on 115 of 115.
- Own questions: see m-1 (80 asked, 80 identical between page and server).
- Gemini path not exercised (no key).

## Items 5 to 7: fact check and content

PDFs read (pdftotext): Fišar et al.; Huber et al.; Duckworth et al.; Buckenmaier et al.; Politicizing mask-wearing; Hate Trumps Love; Deviant or wrong.

- **repro-msci-estimate:** 6 of 6 quotes verbatim; "more than 700 reviewers", "nearly 500", 95%, 29% not accessible, 68%, 12% and 55%: all in the abstract; "about 68% could be at least largely reproduced" in the introduction. Scene "Since 2019 the journal requires authors to disclose both" matches the policy year.
- **dimant-competition-choice:** 6 of 6 verbatim; 95 designs submitted, 18,123 participants, d = -0.085 (CI -0.147 to -0.022), heterogeneity about 1.6 times the average standard error. See o-2.
- **dimant-megastudy-estimate:** 7 of 7 verbatim; 140,461 teachers, 2,992,027 students, 15 interventions plus a reminder-only control, 5.06% (3.30% after the winner's curse), 1.89%, 2.26% (classroom-specific), effects lasting 8 weeks; "weekly emails over 4 weeks in fall 2021".
- **dimant-deterrence-choice:** 7 of 7 verbatim; 296 subjects, delays of two periods, non-monotonic (no delay or maximum delay best, for deterrence and repeat cheating). See o-4.
- **Other Dimant items:** dimant-masks-forecast (all quotes found; N = 4931, 1034 forecasters, 7 nudges), dimant-deviant-choice (418 participants, 42.7% vs 28.7%; the one text miss is a footnote number), social15 and dimant-hate-choice and social16 (8,600 participants, 78.1%, 14.97%, five preregistered studies). **80 of 81 stored quotes checked are verbatim** after normalising ligatures, soft hyphens and column order.
- **Non-Dimant, checked outside the bank:** biz07 (Adams et al., full text: mini-golf, no cue 21%, cue 48%); axe08 (Hui, Reshef, Zhou, publisher news release: even top performers not safe); genai1 (Zhou and Lee, secondary page: average content novelty declined; visual novelty not confirmed). Well-known numbers I know independently and found consistent: social12 (50% more callbacks), judg05 (72% and 78%), judg09 (80% and 92%), biz11 (25% and 45%), bz08 (almost twice), bz15 (79% neutral), ai01 (40%, 18%). Other items were checked against their stored quotes only.
- **Content read:** all 116 decisions' scene, question, options, explain, boundary were read (`dump.txt`); I found no invented firm, no non-significant difference scored as real (axb08, axf05, bz15 label them), no AI-sounding filler beyond m-6. Leak scan: no estimate target inside its band in any scene or question; choice keys: longest 5 of 36, shortest 8 of 36, max scene overlap 0 of 36 (chance 10.2).

## Item 3: live class and server (item 9)

- Instructor (1280x720), projector, 3 phones (390x844); 7 decisions: civic-wallet-rank (rank), axb08 (allocate), axb01 (delegate), axb05 (causal), repro-msci-estimate (estimate), dimant-masks-forecast (forecast), dimant-deterrence-choice (choice). 0 page errors on any of the 5 pages in either run.
- **Leaks:** for every open decision: `/api/challenges` no answer keys; `/api/reveal/ID` 409; `/api/library` omits it; room state has no evidence or truth; tutor answers "locked"; instructor bank 403 without key. Re-probed after close on axb05: still clean. 0 leaks.
- **Dropped link (axb01):** phone 2 went offline after locking: "Sending your answer... Reconnecting..."; back online: "Your answer is in. 3 joined. 3 answered so far" within 8 s. **Closed phase (axb05):** phone 3 never answered; see m-5.
- **Scale:** 130 join attempts from one IP: 120 joined, 10 refused 409 (cap by design), 0.2 s. 120 answers with client ids: 120 of 120 200 in 0.2 s. Resubmission without client id: m-12.
- **Validation:** bad JSON 400, 20 kB body 400, JSON list 400, wrong instructor key 403, wrong token 403, forecast answer -1 / "a" / null / true all 400 ("That answer does not fit this decision"); a forecast of 5 is accepted because the scale is 0 to 100 (`server/scoring.py`). Security headers present (CSP, nosniff, no-referrer, COOP, Permissions-Policy). No secret in responses.
- **Streamlit:** started headless with no passcode: health ok, page renders (Play, Join a class, Run a class, Ask the tutor), 0 page errors. Not run with THV_INSTRUCTOR_PASSCODE.

## Item 8: True/False and iteration 66 / 65

- **True/False (dimant-masks-forecast, false claim; axb06, true claim):** True 100, False 100, True 70, False 70, False 60, True 55 all scored as expected (e.g. masks: True@100 -1, False@100 +1, False@70 0.82, False@60 0.68; axb06: True@70 0.82, False@70 0.02). Stored `response` is the probability the claim is true (False@70 stores 30, False@100 stores 0). Record shows the call. Keyboard: keys 1 and 2 choose True and False; toggle buttons expose aria-pressed; slider 50 to 100 has aria-valuetext "N percent sure" and "not chosen yet" until touched. Classroom phone and projector for forecasts show "Said true (above 50)" and "Said false (below 50)" bars with the study's answer outlined (`shots/cls_rev_prj_dimant-masks-forecast.png`).
- **Question screen scaling:** no overflow or clipping at 1280, 1440, 1920 (0 of 390 plays); fixed bar leaves content reachable. I did not test real browser zoom (emulated only by viewport size); see Could not verify.
- **Landing and Dimant band** (`shots/home_file_1440.png`): what the game is, sample, paths, then the band with three real paper titles and "Show all 18 papers"; credit with name, website and email in header and footer. DOI links in the band not clicked.

## Three changes that would raise Visual most

1. **Projector reveal at 1280x720** (`shots/cls_rev_prj_dimant-masks-forecast.png`). Measured: body text 12.4 to 13.3 px, 280 px empty right column from y 390 to 670. Redesign: manager line and evidence line at 20 px, bars and the room's numbers enlarged to fill the right column down to y 650, and a 16 px floor for every string.
2. **Causal reveal hole** (`shots/rev_axb05_1920.png`). Measured: left column ends 594, right 884 (290 px at 1920 and 1600, 236 at 1440). Redesign: move the four-option recap under the explanation in the left column and end the right column with the figure; tabs then start at about 700 instead of 951.
3. **Question screen of long questions** (`shots/pred_repro-msci-estimate_1280.png`). Measured: 6-line, 48 px heading in a 520 px column with 0 content on the right until the slider. Redesign: cap the question at 4 lines (rule in the scene, see I-1), put the sample line directly under the heading, and centre the controls against the heading's first line; rewrite the landing lede (m-6).

## Could not verify

- `tools/verify_dois.py` not run; no DOI was resolved by me; DOI links in the Dimant band not clicked.
- Papers not read in full: all sources other than the seven PDFs. Non-Dimant decisions were checked against their stored quotes, with outside confirmation only for biz07, axe08 and (partly) genai1; the Zhou and Lee abstract page was blocked (reCAPTCHA), so visual novelty is unconfirmed.
- Hate Trumps Love and Deviant or wrong: checked by their stored quotes only, not read end to end.
- Streamlit with THV_INSTRUCTOR_PASSCODE, and a Streamlit live class, not run.
- Screen readers (NVDA, VoiceOver) not tested; browser zoom not tested with the real browser zoom (only viewport sizes); no blur assessment.
- judg02 (pick two of three) was not driven by my play script and its tutor chips were not counted.
- The record page was measured only at 16 calls; review 49's small-record imbalance (1, 3, 7 calls) was not re-measured.
- Fewer than 500 plays (390); 80 own tutor questions graded by reading the answers, so the direct, partial and miss split is a judgement (the page-versus-server identity is exact).
- Gemini mode (key) not exercised.
