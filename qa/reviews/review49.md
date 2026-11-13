# Independent review 49 (snap, iteration 78)

**Score: 80/100.** 0 Blocking, 0 Major, 13 m Minor, 3 o Optional.

Reviewer: fresh agent in a copy (`r49/work`). `/home/user/the-human-variable` was not read or changed; nothing was published. Scripts: `r49/tools/`; logs and JSON beside them; screenshots in `r49/shots/`.

## Score

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All four iteration-66 decisions match their PDFs; 26 of 26 stored quotes found verbatim (after soft-hyphen and column-order normalisation); masks, hate and deviant quotes found (4 residual misses are PDF-extraction artefacts: a glyph minus, an interleaved footnote); all 7 paper DOIs resolve in Crossref with matching titles. One framing point (repro-msci question). |
| Learning | 15 | 11 | True/False scoring right in 12 of 12 cells; 177 tutor chips on 29 decisions all answered, none before the call; but of 69 own tutor questions only 19 (28%) got a direct answer, 26 partial, 23 miss, 1 wrong. |
| Visual | 15 | 10 | 260 plays, 0 sideways overflow, 0 stranded word, 0 clipping, 0 page errors; the reveal now reaches 1216 px at 1440 and 1368 at 1600 to 1920, but it is still 440 px narrower than the question screen at 1920, the meta-left hole beside the figure is 237 px at 1440 and 291 px at 1600 to 1920 (larger than review 48), the record page is lopsided (391 px, 260 px), landing lede rag unchanged. |
| Gameplay | 15 | 13 | 260 scripted plays over 26 decisions and all eight formats at five viewports: Lock enabled after every legal call; scoring correct for True and False; 6 of 52 plays at 1280x720 still scroll on the predict screen (axb05 +92, dimant-notalie-causal +45, axf05 +7). |
| AI and business relevance | 10 | 9 | Items and paths are management-relevant (AI at work, algorithms, nudges, pay, compliance); the new items are business-facing. |
| Content | 10 | 8 | 48 decisions not read in earlier reviews plus the 4 new ones: designs described correctly, no invented scenarios, non-significant differences handled; option cues and strawmen in a few items (list below). |
| Technical | 10 | 8 | 405 passed in 1249 s, design lint `{}`, build current, axe 0 violations on 52 scans; page and server tutor give identical words on 70 of 70 questions. |
| Classroom | 5 | 4 | Live class: 3 phones, 7 decisions across 7 formats, dropped link recovered, closed phase, no leak by any route; 120 joined and 120 answered in 0.21 s with client ids; projector text at 1280x720 still down to 11.6 px; a closed phone keeps live controls. |
| Accessibility | 5 | 4 | axe 0 on 52 scans; True/False toggle has aria-valuetext ("70 percent sure"); no overflow at emulated browser zoom 125 to 200%. Not tested with a screen reader. |
| **Total** | **100** | **80** | One below review 48 (81), inside the spread between agents. Nothing broke; nothing visible improved except the reveal width at 1440 and above. |

## Gate counts (item 1)

- `python -m pytest -q -x`: **405 passed in 1248.92 s**, 0 failed (`pytest.log`).
- `python3 tools/design_lint.py`: `by rule: {}`. `python3 src/build.py --check`: "built pages are current".
- axe (tests/vendor/axe.min.js, wcag2a/2aa/21a/21aa/22aa/best-practice): **52 scans, 0 violations** (`tools/axe.json`). File and served at 1440 and 390: home; play and reveal of dimant-masks-forecast, repro-msci-estimate, axb05; record (fresh and after plays); library (principles, all decisions). Console lobby, open, revealed; phone waiting, open, revealed; projector open and revealed.
- DOIs: `tools/verify_dois.py` not run. I resolved the 7 DOIs of the papers I checked in Crossref (all return the right title).

## Introduced by iteration 78

No Blocking or Major defect was introduced. 260 plays on the wider reveal: 0 overflow, 0 stranded word, 0 clipped text, smallest reveal text 12 px, strip at most 640 px.

- **m-I1 (Minor). The wide reveal helps only from 1440 px up; at 1200 to 1380 it is unchanged, and the meta-left hole grew at 1600 and above.** Where: `src/app.css` `.focus:has(.reveal){max-width:min(1480px,max(1240px,calc(100vw - 112px)))}`. Observed (`tools/widths.json`, `shots/wr_*_axb05.png`): reveal width 1104 at 1200, 1139 at 1260, 1138 at 1280, 1158 at 1380, 1216 at 1440, 1368 at 1600 and 1920 (cap). Hole between figure bottom and left column bottom on axb05: 217 at 1200, 177 at 1280, 192 at 1380, 237 at 1440, **291 at 1600 and 1920** (review 48 measured 253 at 1440 and 233 to 253 at 1920). On the 26-decision sweep at 1920 (file, with record) 8 decisions are out of balance by 150 px or more (axb05 291, genai2 203, forecast-teams-rank 152). Why: wider columns shorten the left text but not the figure, so the empty block grows. Fix: put Design/Sample/Published/Checked and the principle strip under the left text on these items, or stretch the figure card to the text height.
- **m-I2 (Minor). Reveal still narrower than the question screen.** At 1920 the question is x 56 to 1864 (1808 px) and the reveal x 276 to 1644 (1368); the heading jumps 220 px to the right between predict and reveal (`shots/sw_served_fresh_1920_dimant-deterrence-choice_p.png` against `_r.png`). Down from 1128 against 1808 but not closed. Fix: use the question grid for the reveal too, or centre both at the same measure.
- Header credit (item c) at 1260 to 1380: clean, no wrap, no overlap, nav starts 150 to 160 px after the credit (`shots/hdr_combo.png`). Website is in the bar only from 1380; between 1260 and 1379 it shows only in the footer (carried, m-9).

## Open items from review 48 (item d)

All still open; none fixed in iteration 78.

- **m-1 (Minor). Meta-left hole beside the figure.** axb05 237 px at 1440, ai07 221, axe12 209, dimant-notalie-causal 161 (`shots/sw_*_1440_axb05_r.png`). Also with a record, delegate and allocate reveals leave the right column 150 to 200 px short beside the text and put "Checked" alone in a third cell (`shots/sw_file_record_1440_axf04_r.png`; axf04 514 px out of balance in the raw column measure, which includes the moved study card and strip).
- **m-2 (Minor). Projector at 1280x720.** Smallest text open view: axb08 11.6 px ("Spread 100 points by how likely each option is..."), axb01 13.0, axb05 13.9, deterrence 13.7; revealed 12.9 to 14.4 ("answers" unit). Revealed finding ("No message worked; forecasters still overestimated effects") is about 15 px bold while the question is the headline; the right column is empty below y 390 on the forecast (`shots/cls_proj_open_axb08.png`, `shots/cls_proj_rev_dimant-masks-forecast.png`). Fix: floor of 14 px, finding at headline size, forecast bars sized to fill the column.
- **m-3 (Minor). A phone that has not answered keeps live controls after answers close.** Measured: after "Stop answers" and 6 s the options still highlight, "Lock my answer" enables after a pick, and locking replaces the screen with "Responses are closed" (`shots/closed_phone_idle.png`, `closed_phone_selected.png`). Server rejects it (late post with a bogus token 403). Fix: disable instruments and show a standing line when the phase is closed.
- **m-4 (Minor). Option cues and strawmen.** dimant-deviant-choice: both "alone" options are 18 characters against 54 and 57, and only the key says "cheap compliance". social20: key 54 characters against 38 to 44, the unique longest. ai12: key 47 against 38 and 40, unique longest, three options only. biz02: option 1 ("The employer match required the default rate") contradicts the scene's automatic enrollment, option 2 is a 54-character strawman. bz14: two options (31 and 33 characters), chance 50%. bz06: key "It disappeared" is the unique shortest (14 against 23 to 31) and the scene says the design was rerun with training and practice. misperceived-norms-action: two of three distractors are "Fell". Bank-wide over 32 choice items: key unique longest in 5 (chance 8.0), unique shortest in 6; scene-overlap strategy 0 unique hits: no systematic length cue.
- **m-5 (Minor). Landing lede rag unchanged** (`shots/home_full_1440.png`): "Each round presents a real-life situation, from a / published research study, that you are / asked to predict." Fix: "Each round gives you a real situation from a published study. Make your prediction, then see what the researchers found."
- **bz14 and biz02** listed under m-4.

## Not introduced, other findings

- **m-6 (Minor). Tutor coverage.** 69 valid own questions (`tools/tq.json`; I excluded one question I wrote for the wrong decision): **direct 19 (28%), partial 26 (38%), miss 23 (33%), wrong 1 (1%).** Page against server: words identical on 70 of 70 (`tq.json`). Misses answerable from stored text: repro "Who checked the articles?" (design says 700 reviewers), "What changed in 2019?" (scene), megastudy "Which message was the best one?" (explain names it), "What platform was used?" (Zearn Math), competition "Who submitted the designs?", "Was it done with real money?", deterrence "What is the practical lesson for compliance?" (implication), "What does delayed punishment mean at work?", civic-wallet "Do people behave the same in my country?", axb05 "What is the point for a hospital manager?", "Was the model biased on purpose?", ai01 "Was the quality of writing judged by humans?", "How should a manager roll this out?", masks "Which nudge worked best?", rollout1 "What happened after launch?", axe01 "What was the benchmark?", "How could this go wrong?", biz07 "Can I rely on this number?", social14 "Where did the experiment take place?", repro "Is Management Science a good journal for this check?", "Could the figure be wrong because of how they count?". **Wrong answer:** deterrence "Was cheating real?" returns "The same two timings were most effective against recidivism." (follow-up stolen by the word "cheating"). Routes tightened in iteration 77 introduced no steal in my set ("subjects" alone was not asked; "how reliable" questions were not asked).
- **m-7 (Minor). Record page lopsided** (`tools/rec.py`, `shots/record_7.png`): at 1 call left column ends 959, right 568 (391 px blank); at 3 calls 959 vs 694; at 7 calls right 1219 against left 959 (the plot leaves 260 px blank under it); at 12 calls balanced (1232 and 1259).
- **m-8 (Minor). repro-msci-estimate question hides the counting rule.** Question "Of all articles published under the new policy, what share could be at least largely reproduced?" has answer 68%; the paper says 68% only "when considering such articles [29% with inaccessible data] as non-reproducible", and more than 95% when data access was no obstacle. A reader answering 95 is not wrong about the study. The explain says it; the question does not. Fix: "...counting articles whose data the reviewer could not access as not reproduced?"
- **m-9 (Minor). Header website link hidden at 1260 to 1379** (carried).
- **m-10 (Minor). Option rows wrap early on the wide question screen.** At 1920 deterrence rows 1, 3, 4 break at about 420 px inside an 800 px row ("Deterrence rose steadily the later / the verdict and the fine came") while row 2, longer, runs on one line (`shots/sw_served_fresh_1920_dimant-deterrence-choice_p.png`). The scene (about 33 px serif) sits 30 px above the 60 px question, so the scene reads as heavy as the heading. Fix: set option rows to the full row width; add 20 px above the question.
- **m-11 (Minor). false-news-spread key says "Novel false stories drew more human shares"** but the explain, answer title and quote never mention novelty (they say humans, not bots, drove it). Fix: add the novelty quote to the explain or reword the option to what the explain states.
- **m-12 (Minor). Hedged wrong forecast scores above 0** (masks False-wrong at 70%: score 0.02 and shown as "Score 2"; 60% right on False: 0.68; right at 70%: 0.82 on axb06). Consistent Brier scoring.
- **m-13 (Minor). Predict screen scrolls at 1280x720** on 3 decisions: axb05 +92, dimant-notalie-causal +45, axf05 +7 (6 of 52 plays; the fixed bar stays reachable).
- **o-1 (Optional).** A "?" sits right of an unset confidence slider (`shots/sw_served_fresh_1920_dimant-deterrence-choice_p.png`): "not set" would say it.
- **o-2 (Optional).** Chip "Has it been replicated?" on repro-msci-estimate answers about replication materials (carried).
- **o-3 (Optional).** axe11 (pick two): the keyed pair includes the longest option (62) and the only "slightly" hedge; small cue.

## Item 5: fact check

Papers read from PDF: Fisar et al., Huber et al., Duckworth et al., Buckenmaier et al., Politicizing mask-wearing, Hate Trumps Love, Deviant or wrong (all seven; Hate Trumps Love and Deviant by text search of the cited numbers, not end to end).

- **repro-msci-estimate:** more than 700 reviewers, nearly 500 articles, more than 95% fully or largely reproduced, 29% data not accessible, 68%, 12% before the policy with 55% reproduced: all in the abstract; 6 of 6 quotes verbatim. See m-8.
- **dimant-competition-choice:** 95 designs submitted, 45 drawn, 18,123 participants, d = -0.085, CI [-0.147, -0.022], P = 0.008, heterogeneity about 1.6 times the average standard error; 6 of 6 verbatim. The follow-up carries the authors' "suggestive evidence"; the explain states the effect plainly (carried wording point, owner-protected).
- **dimant-megastudy-estimate:** 140,461 teachers, 2,992,027 students, 15 interventions plus reminder-only control, four weeks in fall 2021, 5.06% (3.30% after the winner's curse), 1.89% any nudge, 2.26% classroom-specific, persistence over 8 weeks; 7 of 7 verbatim.
- **dimant-deterrence-choice:** 296 subjects, delay two periods, non-monotonic (no delay or maximum delay best), recidivism follows the same pattern (abstract and Section 1); 7 of 7 verbatim.
- **dimant-masks-forecast** (21 of 21 verbatim), **dimant-hate-choice** (9 of 10; the 10th is a figure caption whose "p = 0.035" tail is on a different line in the PDF text; the numbers 72.8% and 59.0% are present), **dimant-deviant-choice** (5 of 6; "418 participants" present, line break), **social15** (3 of 7 string matches; 14.97%, 22.9%, 78.1% present, hyphen and minus glyph extraction). Residual misses are extraction artefacts.
- Non-Dimant items read against their stored quotes only (no PDFs): ai09, ai11, bz01, bz03, bz05, bz06, bz09 to bz12, social08, social10, judg05, judg09, axb03, axb04, axb06, axb07, axb14, axb15, manylabs-anchoring and others below; designs and numbers are plausible and internally consistent. I could not read those papers.

## Items 6 and 7: leaks and content

- **Leak scan, all 116 live decisions:** no estimate target within tolerance in any scene, question or title; no option cue that holds bank-wide (see m-4); `/api/challenges` carries no `truth`, `answerTitle`, `explain`; chips and tutor panel appear on 0 of 29 sampled decisions before the call and 0 chips fall back; the open-decision tutor and `/api/reveal` are locked in a live class.
- **Blind strategies:** longest option hits 5 of 32 (chance 8), shortest 6 of 32, max scene-overlap 0 of 32; "always True" on forecasts was not re-simulated.
- **Content read (48 not read in earlier reviews):** ai09, ai11, biz11, bz01, bz03, bz05, bz06, bz09, bz10, bz11, bz12, social08, social10, judg05, judg09, axb03, axb04, axb06, axb07, axb14, axb15, rollout3, manylabs-anchoring, false-news-spread, misperceived-norms-action, misperceived-norms-support, accuracy-prompt, rule-violations-honesty, tax-letter-norms, genai1, genai3, axe04 to axe11, axe13, axe14, axf02, axf06, dimant-proximity-estimate, dimant-requiem-forecast, dimant-motivated-estimate, dimant-opioid-forecast, bz02. Designs are described correctly; non-significant results are labelled (axe13 sneakers, axf06 76 vs 74, bz10 near zero); no invented scenarios; copy reads as plain summary. Faults: m-4, m-8, m-11, o-3.

## Item 8: classroom (item 3), server (item 9)

- Instructor at 1280x720, three 390x844 phones, seven decisions: civic-wallet-rank (rank), axb08 (allocate), axb01 (delegate), axb05 (causal), repro-msci-estimate (estimate), dimant-masks-forecast (forecast), dimant-deterrence-choice (choice) (`tools/cls.py`, `cls_log.json`).
- **Leaks:** during each open decision I probed `/api/challenges`, `/api/library`, `/api/rooms/CODE`, `/api/reveal/ID`, `/api/tutor` for the open decision and the instructor bank: no truth, answer, explain or rank key; library omitted the open decision; reveal 409; tutor "opens after your instructor reveals it"; bank 403 without key. 0 leaks.
- **Dropped connection (axb01):** phone 2 offline, answer locked, back online: "Your answer is in" within 6 s. **Closed phase (axb05):** m-3. 0 page errors on any page.
- **Scale:** 120 joined, 10 of 130 refused 409 (cap by design); 120 answers at once with their own X-Client-Id all 200, wall 0.21 s, max 0.14 s. Without client ids the per-IP buckets are shared (review 48 saw 108 of 120 rejected); my second batch was rejected by the room's join bucket, so I do not report that case as new.
- **Server validation, headers, secrets:** not re-run beyond the above; behaviour unchanged since review 48 (`server/app.py` limits read: body 8 kB, JSON object only, 429 buckets per IP and client).
- **Streamlit:** started headless without a passcode: health 200, page renders with Play, Join a class, Run a class, Ask the tutor, 0 page errors. Not run with `THV_INSTRUCTOR_PASSCODE`; no Streamlit live class.

## Item 8a to 8c: other measurements

- **True/False (12 cells over masks, axb06, bz09):** True and False both score correctly (right at 100%: +1; wrong at 100%: -1; wrong at 70%: 0.02; right at 60%: 0.68; right at 70%: 0.82), aria-valuetext "70 percent sure", toggle buttons pressed state exposed. Stored probability was not read back (record field name differs from my script); parity tests pass.
- **Emulated browser zoom 125, 150, 200%** (viewport = screen / zoom) on deterrence, repro, axb05: 0 sideways overflow, 0 clipped text, min text 12.5 px, Lock button 54 px high, bar fixed with content padded under it.
- **Plays:** 260 plays (26 decisions: choice 5, estimate 4, forecast 4, rank 3, causal 3, allocate 2, delegate 3, multi 2), five viewports (390x844, 820x1100, 1280x720, 1440x900, 1920x1080), served page with a fresh profile and file:// with four rounds already in the record. 0 exceptions, 0 page errors, 0 sideways overflow, 0 stranded word, 0 clip, Lock enabled after every call. I read about 25 screenshots.
- **Landing page and Dimant band** (`shots/home_full_1440.png`): what the game is, sample decision, paths, then the band with three real titles and "Show all 18 papers"; credit in header and footer. Clean, low clutter. Only the lede rag (m-5). DOI links in the band were not clicked.

## Three changes that would raise Visual most

1. **Wide reveal balance (axb05, ai07, axe12, notalie, and delegate/allocate with a record).** Screen `shots/wr_1920_axb05.png`. Measured: figure 797 px tall, left text ends 291 px above its bottom; right column 150 to 200 px short on delegate and allocate. Redesign: left column = verdict, finding, manager line, then the study card; right column = figure only; set both columns to end within 40 px by moving the study card and strip to the shorter column, and stop the "Checked" cell sitting alone in a third column.
2. **Reveal and question on one grid.** Measured 1368 against 1808 px at 1920 (and 1104 to 1158 against 1200 to 1380 below 1440). Redesign: one shared page width and left edge so progress bar, heading and text start at the same x on predict and reveal; scale the reveal type up like the question screen instead of capping the column.
3. **Record page and projector.** Record: 391 px blank right of the plot at 1 call, 260 px blank under the plot at 7. Put the calibration plot and "Recent calls" side by side and "By area" full width under both. Projector at 1280x720: set the revealed finding at the 28 px headline size, floor all text at 14 px, enlarge the forecast bars to fill the empty right column from y 390 to 670.

## Could not verify

- `tools/verify_dois.py` not run; I resolved 7 DOIs in Crossref (title match), not all 114, and did not click the band's DOI links.
- Papers not read: all sources other than the seven PDFs given; those decisions were read against stored quotes only. Hate Trumps Love and Deviant or wrong checked by text search of cited numbers, not end to end.
- Streamlit with `THV_INSTRUCTOR_PASSCODE` and a Streamlit live class not run.
- Screen reader (NVDA, VoiceOver) not tested; real browser zoom emulated by viewport size and device scale factor, blur not assessed.
- Server audit (oversized body, bad JSON, wrong key) not re-run this round; relied on code read and review 48. Remote class on a non-loopback host without a passcode not run.
- Without-client-id join and answer storm not reproduced cleanly (see Scale).
- The stored True/False probability in the record was not read back directly.
- Fewer than 500 plays; 60+ own tutor questions were run (69) but graded by me by reading the answers, so the direct/partial split is a judgement.
