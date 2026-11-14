# Independent review 52 (snap, iteration 82)

**Score: 81/100.** 0 Blocking, 0 Major, 12 Minor (1 introduced by iteration 82), 5 Optional (1 introduced).

Reviewer: fresh agent, own copy (`r52/work`), `/home/user/the-human-variable` not read or changed, nothing published. Scripts `r52/*.py`, shots `r52/shots/`.

## Score

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All 26 stored quotes of the four iteration-66 items verbatim in the PDFs; scene and answer numbers match; 114 cited DOIs have a matching Crossref record (3 title forms differ only by subtitle or the "RETRACTED:" prefix the bank states); one soft scene wording (45 of 50 drawn designs ran). |
| Learning | 15 | 10 | True/False scoring right in 14 of 14 cells (False 70 stores 30, True 100 on a false claim scores -100); but of 112 own tutor questions about 22% direct, 43% partial, 31% miss, 4 wrong, and 3 of 6 chips repeat the screen. |
| Visual | 15 | 11 | Calm, no overflow, strand or clipping in 580 plays; but causal reveal hole about 290 px at 1920, record page holes 375 px (1 call) and 335 px (7 calls), projector body text 12.9 to 13.8 px at 1280x720. |
| Gameplay | 15 | 13 | 580 plays, 29 decisions, 8 formats, 5 viewports, file and served, fresh and with record: 0 errors, Lock always enabled; predict screen scrolls at 1280x720 on 5 decisions. |
| AI and business relevance | 10 | 9 | Items are management decisions; implication lines are formulaic ("Benchmark... skip that layer"). |
| Content | 10 | 8 | 60 decisions read, no invented firm, no null result scored; axb12 scene states the mechanism, two two-part keys, replication frame cue. |
| Technical | 10 | 9 | 405 passed (1245 s), lint `{}`, build current, axe 0 on 50 scans, page and server tutor identical on 126 questions and 716 chips, validation holds, 120 joins in 0.34 s. |
| Classroom | 5 | 4 | 3 phones, 8 decisions, offline phone recovered, 0 leaks by any route; closed phone keeps live controls and a toast ellipse over the scene; projector text small. |
| Accessibility | 5 | 4 | axe 0 on 50 scans (with best-practice rules), focus ring 2.4 to 3 px at every zoom, no hit target under 24 px; no screen-reader run. |
| **Total** | **100** | **81** | One below review 51 (82): nothing new is broken, but my stricter tutor grading and the unchanged visual holes keep it there. |

## Introduced by iteration 82

No regression found. The four wrong tutor answers of review 51: ai10 and social04 and facebook-deactivation are fixed for the wordings tried; the axb01 fix is incomplete.
- **I-1 (Minor). axb01 "when does a human reviewer help" fix reaches only its own wording.** "When does having a human check the work help?" and "in which cases does a human in the loop help" both return "I could not match that question... Here is what the study found: Combine only where humans beat the AI..." (useful text, wrong frame). The same for facebook "what was the duration of the break". Fix: add "when|in which cases|under what conditions" to the follow-up matcher or list two more phrasings.
- **I-2 (Optional). The new subgroupFollow alternative is narrow.** It matches ai10 only (one follow-up in the bank starts "Did experts"); "Did seasoned forecasters follow the algorithm?" still misses. No other decision changes; golden tests pass (405).

## Findings (not introduced)

- **m-1 (Minor). Tutor coverage** (`q1out.json`, 112 questions in my wording on 100 decisions, graded by reading; page equals server on 112 of 112): direct about 25 (22%), partial about 48, miss about 35, wrong 4. Wrong: genai2 "how much editing was allowed" (routes to the ethics disclaimer "The study measures what happened, not what is right"), axf06 "did doctors follow the chatbot" (answers only that no prompt training was given), rollout1 "how would I choose which agents get the tool first" (says the summary does not break results down that way, though the study's answer is the whole item), axb15 "how long was the conversation" (answers persistence at two months). Misses are mostly "what is X" definitions (anchoring, endowment effect, planning fallacy, save more tomorrow, loss aversion, REQUIEM) and design details (payment, sample counts, cities). Fix: a glossary line per named concept in bank.json and a "design detail" follow-up per item; remove "allowed" from the ethics route.
- **m-2 (Minor). Chips repeat the screen** (`chips.json`): 716 chips, none shown before the call, parity 716 of 716; "How big is this effect in practice?" returns the explain already printed (116 of 116), "What should a manager do with this?" the manager line (115 of 116), "How would I test this in my company?" the implication (116 of 116). Fix: drop those three or make them add something.
- **m-3 (Minor). Closed phase on the phone** (shots/cls_phone_closed.png): after "Stop answers" a phone that had not answered keeps the allocate sliders enabled (controls al0, al1, al2, x) and a dark toast ellipse sits over the scene sentence. Server refuses the answer. Fix: disable inputs, show the message in the flow.
- **m-4 (Minor). Projector text** (shots/cls_prj_rev_axb05.png, cls_prj_rev_dimant-masks-forecast.png): at 1280x720 smallest text 13.8 to 17 px open and 12.9 to 15 px revealed (axb05 12.9, masks 13.8); "For a manager" and "Where the evidence comes from" about 13 px; right column empty from y 395 to 650 on the forecast reveal. Fix: 20 px body, 16 px floor, scale the bars.
- **m-5 (Minor). Record page** (shots/rec_1_1440.png, rec_7_1440.png): left column ends y 915; right ends 540 at 1 call (375 px empty) and 1250 at 7 calls (335 px empty left). The hero reads "-33" after one call and "-198" after two confident misses. Fix: single column under 8 calls; show the skill number after 3 calls as the area table does.
- **m-6 (Minor). Causal reveal hole** (shots/probe_axb05_1920.png): left column ends about y 595, the right about 884 (290 px) at 1920; ai09 reveal at 1280 leaves 250 px under the left column. Fix: move the "Design / Sample" and the tabs up under the explanation or the option recap into the left column.
- **m-7 (Minor). Predict screen scrolls at 1280x720** on axb05 (+92 px), meta-perception-causal (+128), dimant-notalie-causal (+45), axb06 (+25), axf05 (+7); none at 1440 or 1920. Fix: shrink scene/figure spacing for causal items at 720 px height.
- **m-8 (Minor). axb12 scene gives the mechanism**: "lets the platform's algorithm deliver it cost-effectively" and the key "Showing ads to young women costs more" is the only option about cost. Fix: "delivers it through its default settings".
- **m-9 (Minor). Option cues.** dimant-conspiracy-choice and dimant-polarizednorms-choice: the key is the only two-part option and (conspiracy) the longest; axb02 key is the odd one of three; replication frame (famous study then re-test: biz04, social10, bz10, bz11, bz16 False; manylabs True); forecasts 16 True of 35.
- **m-10 (Minor). biz08 and a few items say "Who was studied: see the paper"** in the tutor ("Who took part in the study?" chip answer), which is a non-answer next to a stored sample. Fix: write the sample line.
- **m-11 (Minor). Served page under load:** with five browsers from one IP, 124 of 290 served plays logged a console 429 (reveal fetch retried and succeeded). A class behind one NAT may see this; raise the read bucket or send client ids on every call.
- **o-1 (Optional).** Server accepts confidence 0 to 100 for choice items (UI minimum 50); harmless.
- **o-2 (Optional).** Value 51 on the True/False slider reads "50 percent sure" and "You sat at 50%"; fine, but the slider step is not announced.
- **o-3 (Optional).** Two servers (or Streamlit) on one machine share server/data/classroom.sqlite3; a class on one pauses Play on the other (documented by design).
- **o-4 (Optional).** Competition scene "Researchers drew 45 of them" follows the abstract; the methods say 50 were drawn, 45 ran.

## Item notes

- **True/False (8a):** axb06 (true claim) and dimant-masks-forecast (false claim), inputs True/False at 50, 70, 100: scores 100, 82, 50, 2, -100 and mirrored; stored response 30 for False 70 (probability the claim is true); record shows it; aria-pressed and "N percent sure" present; classroom projector shows "Said true (above 50)" and "Said false (below 50)" with the study answer outlined.
- **Scaled question screen and zoom (8b):** 9 viewport and zoom combinations (1280x720, 1440x900, 1920x1080, 125, 150, 200 percent on 1280, 1440, 1920) x 7 decisions: no overflow, no hit target under 24 px, focus ring 2.4 to 3 px, vertical scroll only at zoom.
- **Landing page (8e):** what the game is, sample decision, paths, Dimant band with 18 papers and DOI links, credit as mailto name. All 114 source DOIs return Crossref records; doi.org redirects not followed.
- **Leaks (6):** served /api/challenges, room state while open, /api/reveal (409), library, tutor ("locked") carry no answer, explain or title; no tutor chips before the call (0 of 116 predict screens); estimate targets do not appear in scene or question; key is longest in 6 of 36 and shortest in 8 of 36.
- **Server (9):** bad answers (-1, 4, "a", null, true, 1.5, list, object) 400; confidence 101, "x", null, -5 400; wrong challenge 409; bad token 403; wrong instructor key 403; CSV and bank without key 403; 120 joined in 0.34 s from one IP, the 10 above the cap got 409; without client ids joins from one IP 429. Streamlit headless started with and without THV_INSTRUCTOR_PASSCODE and rendered Play, Join a class, Run a class, Ask the tutor in the sidebar (with the passcode: "This deployment runs live classes"); I did not drive Run a class or the tutor page there.
- **Content (7):** read 60 decisions (all forecast claims and the choice/multi items listed above, plus the four new ones and four other Dimant items); no non-significant difference treated as real (axe13 and genai1 say so), no strawman beyond the cues above.

## Three changes that would raise Visual most

1. **Record page at 1 to 7 calls** (shots/rec_1_1440.png): 375 px empty right column at 1 call, 335 px empty left at 7. Redesign: one column until 8 calls, chart then call list; two columns only when both exceed 900 px; hide the hero number until 3 calls.
2. **Projector reveal at 1280x720** (shots/cls_prj_rev_dimant-masks-forecast.png): body 13 px, right column empty 255 px. Redesign: 20 px manager and evidence lines, 16 px floor, bars scaled to fill to y 650.
3. **Causal and wide reveals** (shots/probe_axb05_1920.png, pl_file_1280_ai09_fresh_rev.png): 290 px hole under the explain at 1920, 250 px at 1280. Redesign: put the "Design / Sample / Published / Checked" grid and the tabs in the left column so both columns end together.

## Could not verify

- doi.org redirects not followed (Crossref metadata only); WebFetch and WebSearch not used; non-Dimant facts rest on stored quotes and my knowledge. Papers read: the seven PDFs (quotes for four new items checked in full; deviant, hate, social15 numbers by search; masks 4,931 and 1,034 not found by search because of number formatting, previous review verified them). dimant-notalie-causal paper not in papers/.
- No screen reader run; browser zoom emulated by viewport and device scale factor.
- Gemini mode not exercised. Streamlit live class and Docker image not run; Streamlit navigation beyond the home page not driven.
- Tutor grading is my judgement; page-versus-server identity is exact. Only 60 of 116 decisions read in full (prompt asked 50; the remaining 56 only via claims, tutor and screens).

---
## Appendix: working notes

## Working notes (tutor, 126 own-wording questions: 14 regression probes + 112 fresh)
- Page (THV.curated, file://) versus server (/api/tutor): identical text after whitespace normalisation on 126 of 126.
- Four iteration-82 fixes: ai10 "did professionals trust it less" now gets the experts follow-up (but "Did seasoned forecasters follow the algorithm?" misses: the regex lists "experts, experienced X, professionals", not "seasoned"); social04 "How long did the attitude shift last" gets the semester answer (ok); axb01 "when does having a human check the work help" and "in which cases does a human in the loop help" still return "I could not match that question" (the useful sentence follows, so partial); facebook "How long were they off the platform" direct, "what was the duration of the break" still partial. The new regex alternative matches follow-ups on one decision only (ai10); no regression found on the other 116.
- Own 112 questions, graded by reading: direct about 25 (22%), partial about 48, miss about 35, wrong 4.

## Working notes (play, class, tutor chips, DOIs)
- Plays: 580 completed (29 decisions x 8 formats x 5 viewports x file and served x fresh and with record), 0 exceptions, 0 horizontal overflow, 0 stranded words (measured: last line under 60 px), Lock always enabled. Smallest text: predict 12.5 px, reveal 12.0 px (delegate chip "You: Human and AI together"), phone SVG text 12.0 px. Predict screen scrolls at 1280x720 on axb05 (+92), meta-perception-causal (+128), dimant-notalie-causal (+45), axb06 (+25), axf05 (+7); none at 1440 or 1920.
- Served page: 124 of 290 served plays logged a console 429 when five browsers played at once from one IP; the reveal still appeared (the page retried). Not counted as a defect (my load), but it shows the read bucket is tight for a class behind one NAT.
- Class run (server 18653, 8 decisions: rank, allocate, delegate, causal, estimate, forecast, choice, rank): 0 page errors on instructor and 3 phones; while open the room state, /api/reveal (409), /api/library, tutor ("locked") carry no answer, title or explain; offline phone queued and sent "Your answer is in" after reconnection; closed phase: phone that had not answered keeps live sliders (axb08) and a dark toast ellipse over the scene (shots/cls_phone_closed.png): review 51 m-5 unchanged.
- 120 joined from one IP in 0.34 s; the 10 over the cap got 409; answer validation rejects -1, 4, 'a', null, true, 1.5, list, object (400); confidence 101, 'x', null, -5 (400); 49 accepted for a choice (UI minimum is 50, server allows 0 to 100: cosmetic).
- Both servers on one machine share server/data/classroom.sqlite3; a class on one blocks practice reveals on the other (by design, noted in the ledger).
- Tutor chips: 716 chips on 116 decisions (6 on 96, 7 on 20), none rendered before the call, page equals server on 716 of 716; answer to "How big is this effect in practice?" contains the explain already on screen in 116 of 116, "What should a manager do with this?" repeats the manager line in 115 of 116, "How would I test this in my company?" repeats the implication in 116 of 116 (carried m-2).
- DOIs: Crossref (reachable here) returned a record for all 114 cited sources; 111 titles match, 3 differ only in form (bucinca21 subtitle, manylabs14 subtitle, shu12 "RETRACTED:" prefix, which the bank knows and states in bz11). doi.org redirects themselves were not followed.
- Fact checks (papers/ PDFs via pdftotext): repro-msci-estimate, dimant-competition-choice, dimant-megastudy-estimate, dimant-deterrence-choice: all 26 stored quotes verbatim in the PDFs; scene numbers match (700 reviewers, nearly 500 articles, 2019 policy, 68, 95, 29, 12 and 55 percent; 95 designs, 45 run, 18,123, d -0.085 [-0.147, -0.022], 1.6 times; 140,461 teachers, 2,992,027 students, 15 nudges, 4 weeks, fall 2021, 5.06 and 3.30, 1.89, 2.26, 8 weeks; 296 subjects, 32-card game, delays of two rounds, non-monotonic). Also dimant-deviant-choice (42.7 vs 28.7, 22.2 vs 36.5, 418), dimant-hate-choice and social15 (72.8, 59.0, 78.1, 14.97, 22.9) found in the paper text.
