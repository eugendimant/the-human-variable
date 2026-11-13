# Independent review 48 (snap, iteration 76)

**Score: 81/100.** 0 B Blocking, 0 M Major, 14 m Minor, 4 o Optional.

Reviewer: fresh agent in a copy of the snapshot (`r48/work`). `/home/user/the-human-variable` was not read or changed; nothing was published. Scripts in `r48/tools/`, logs and JSON beside this file, screenshots in `r48/shots/`. I followed the iteration 76 addendum.

## Score

| Category | Max | Score | Evidence line |
|---|---|---|---|
| Science | 15 | 13 | All four iteration-66 decisions match their PDFs (26 of 26 stored quotes found verbatim after normalising soft hyphens); masks, hate and deviant numbers match their papers; all 114 source DOIs resolve in Crossref with matching titles. One wording point (competition explain). |
| Learning | 15 | 11 | True/False scoring and stored probability correct in 12 of 12 cases; but of 75 own tutor questions only 27 (36%) got a direct answer, 26 partial, 22 miss; the widened routes fixed 5 phrasings and added a steal (bare "subjects"). |
| Visual | 15 | 10 | 240 plays, 0 sideways overflow, 0 stranded word in a heading, paragraph or list; header credit clean. But a 230 to 270 px hole beside the figure on meta-left reveals, the reveal is 1128 px against a 1328 to 1808 px question screen, the record page is lopsided by 322 to 391 px at 1 and 7 calls, the projector finding is the smallest heading, and the landing lede rag is unchanged. |
| Gameplay | 15 | 13 | 240 scripted plays plus 116 chip plays: 0 page errors, Lock enabled after every legal call; fitQuestion holds at 1280, 1440, 1920; 3 decisions still scroll at 1280x720 (axb05 +92, meta-perception-causal +128, axf05 +7). |
| AI and business relevance | 10 | 9 | Paths and items are management-relevant and the new items are business-facing. |
| Content | 10 | 8 | About 60 decisions read; designs described correctly, no invented scenarios; option cues in a few items (deviant cost cue, social20, ai12), strawman distractors in biz02, bz14 has two options. |
| Technical | 10 | 8 | 405 passed in 1249 s, design lint `{}`, build current, axe 0 violations on 42 scans; page and server tutor give the same words on 75 of 75 questions but different paragraph breaks on 38 of 75. |
| Classroom | 5 | 4 | Live class with 3 phones, 7 formats, dropped link, closed phase: no leak by any route probed; 120 joined, 120 answered in 0.17 s when each phone sends its client id; projector text at 1280x720 still goes down to 11.6 px; a closed phone keeps live controls. |
| Accessibility | 5 | 4 | axe 0 on 42 scans; True/False is a labelled group of toggle buttons, slider has aria-valuetext ("100 percent sure"); keyboard order in header correct at every width. Not tested with a screen reader. |
| **Total** | **100** | **81** | One above review 47 (80). Gains: duration chip gate right, header credit on one row, tutor routes for who/where/how-reliable. Still open: tutor coverage, reveal and record column balance, projector at 720p. |

## Gate counts (item 1)

- `python -m pytest -q`: **405 passed in 1248.96 s**, 0 failed (full run in the copy, `-x`).
- `python3 tools/design_lint.py`: "by rule: {}" (0 hits). `python3 src/build.py --check`: "built pages are current".
- axe (tests/vendor/axe.min.js; wcag2a, 2aa, 21a, 21aa, 22aa, best-practice): **42 scans, 0 violations** (`axe.json`). File and served, at 1440 and 390: home; play and reveal of dimant-masks-forecast, repro-msci-estimate, axb05; record; library. Console create, lobby, open, revealed; projector open and revealed at 1280x720.
- DOIs: `tools/verify_dois.py` not run. I resolved all 114 source DOIs in Crossref myself (`doi_res2.json`): 114 return a record whose title matches the stored title (fisar24's Crossref title carries italic markup only). This checks that the DOI exists and names the right title, not the page text.

## Introduced by iteration 76

No Blocking or Major defect was introduced.

- **m-I1 (Minor). Credit disappears from the bar at 1260 to 1379 px and the website is missing there.** Where: `src/app.css` `.bar-credit` media rules. Observed (served and file, `header.json`, `shots/hdr_served_1259.png`, `hdr_served_1440.png`): at 1259 and below the credit is a second row under the bar (name, website, email, one line, no overlap). At 1260 to 1379 the bar shows only the sentence (308 to 701 px, 17 px high), and the website link is hidden; the page credit is also hidden, so the website and email appear only in the footer at the bottom. At 1380 and wider the website sits in the bar (772 to 905 at 1380), 28 px before the first menu item; the email is footer only. No wrap at any tested width (1024, 1200, 1259, 1260, 1280, 1379, 1380, 1440, 1920), no sideways overflow, with and without "Join a class" (file hides it; gap credit to menu 273 px there, 157 to 175 with it). Why it matters: 1280 and 1366 are common laptop widths and the owner wants name, website and email on the landing page; there the first screen carries the name only. Fix: show the website link from 1260 (the 157 px gap has room) or keep the page credit row until 1380.
- **Header order is correct.** DOM and Tab order: skip link, brand, credit link (at 1380 and wider), Play, Library, Your record, Join a class; hidden credit links are skipped at 1260 to 1379 and below 1260 the page credit row comes after the nav.
- **m-I2 (Minor). Tutor routes steal questions with the bare word "subjects".** Where: `bank.json` tutorRoutes `who` (`\bsubjects\b`). Observed: "Which school subjects were measured?" (megastudy), "Which subjects did they write about?" (ai01) and "What subjects did the students study?" (social04) return "Who was studied: ..." instead of the topic. Fix: require "the subjects" with a participant cue (`\b(who were|how many) (the )?subjects\b`).
- **m-I3 (Minor). The widened `catch` route answers reliability questions about something else.** "How reliable is ChatGPT at writing?" (ai01), "How reliable is the model in this study?" (ai09), "How sure are workers about what colleagues earn?" (bz13) all return "What the study covers: ...". Acceptable for "how reliable is this", off for the others. Fix: anchor to `this (finding|result|number|study|figure)|the (finding|result|number|figure)`.
- **m-I4 (Minor). The "where can I read the paper" route is too literal.** "Where can I read the original paper?" (civic-wallet-rank) and "Where can I read the full paper?" (bz07) miss; the exact "the/this/it/that paper" works (checked on civic, megastudy, masks, deterrence). Fix: allow one optional adjective, or `\bwhere\b.*\b(read|find|get)\b.*\b(paper|study|article)\b`.
- **Fixed from review 47:** duration chip (m-I2) is right on all 2 decisions that show it (axb15, megastudy; bz13 and forecast-training no longer show it because their follow-ups are about run length and training length); who/subjects, field/lab, where to read, one-line takeaway, how reliable now answer on the questions I tried.
- **Not fixed (carried):** page and server paragraph breaks differ (review 47 m-I1, below as m-4).

## Tutor battery (item 8b)

75 questions in my own wording on 14 decisions (`tools/tq.py`, `tq_both.json`), plus 29 rerun probes.

- **Page against server:** words identical on 75 of 75 (after collapsing whitespace); raw text identical on only 37 of 75. Through the real UI (`tools/tutui.py`, served against file) the displayed answers differ in paragraph breaks on 4 of 8 questions (for example served "Sample: ... Reporting rose" in one paragraph, file with a break). Same words, different layout; unfixed since review 47.
- **Directness:** 27 direct (36%), 26 partial (35%), 22 miss (29%). Review 47 was 41/32/27 on a different set, so the route work has not moved coverage.
- **Misses (generic "I could not match that question" or an unrelated explain):** repro "Who were the reviewers that reran the articles?"; megastudy "Was it a lab or a field study?", "What did the winning email say?", "What was the control condition?", "Which email won?", "Who sent the emails?"; competition "Was it online or in a lab?"; deterrence "How big was the fine?", "What is non-monotonic?", "What does non-monotonic mean?"; repro "What counts as reproduced?"; civic-wallet "Where were the wallets dropped?", "Is this a survey or a real experiment?", "Where can I read the original paper?"; bz04 "Who were the students?", "What is the planning fallacy?"; ai01 "Did quality suffer?"; social04 "Who were the students surveyed?", "What is pluralistic ignorance?"; axb05 "What is a confounder?"; masks "What are the seven messages?"; biz04 "Which hotels were tested?", "Were these guests in a lab?"; ai10 "What is algorithm aversion?"; conspiracy "Was this run online?"; bz02 "What does ROI mean here?".
- **Honest non-answer:** "Was it preregistered?" on competition says the summary does not record it (counted as miss).
- **Several misses are answerable from stored text:** megastudy explain names the winning email; civic-wallet design says "Field experiment"; masks scene lists the message types; bz04 sample says "37 honors students". Fix: route "which/who sent/what did X say/was it online or lab/where was/who were the students" to explain, scene, design and sample lines before the fallback, and add concept lines (planning fallacy, pluralistic ignorance, confounder, ROI, algorithm aversion, non-monotonic) to follow-ups with quotes. Golden files regenerate (I16).
- **Steals found:** m-I2, m-I3 above. No route took a question from a better one on the 29 rerun probes beyond those.
- **Chips (item 8c of old list, kept):** 116 decisions played; 716 chips (96 decisions with 6, 20 with 7); 0 chips or tutor panel before the answer; 0 fallback answers; page and server give the same words on all 716. "Has it been replicated?" on repro-msci-estimate answers about replication materials (a reproduction item), mildly misleading (o-1).

## Record page columns (item 8c)

Measured on the file page after 1, 3, 7 and 12 calls at 1280, 1440, 1920, 820, 390 (`tools/record.py`, `shots/record_7_1440.png`).

- 3 calls: left 408 to 959, right 408 to 905 (balanced). 12 calls: left 1295, right 1259 (balanced).
- **1 call:** right column ends at 568, left at 959: 391 px blank (no "By area" exists yet).
- **7 calls:** "By area" moves to the right although the left is already shorter after the move: left ends 959, right 1281, so the right is now 322 px longer (review 47 had the opposite 725 px). `balanceRecord` moves on a half-height test but never checks the result. Fix: move only if it reduces the absolute difference, else leave it.
- At 820 and 390 the columns stack, 0 overflow.

## Duration chip gate (item 8d)

`durationOk` matches follow-ups beginning "Did the effect last/fade/persist" or "How long did the effect last". Shown on 2 of 116 decisions (axb15, megastudy), correct answers ("persisted at the two-month follow-up"; "persisted in the 8-week period"). ai10's "When did the preference fade?" no longer triggers it. Fixed.

## Open items from review 47 (item 8e)

- **Wide reveal gap on meta-left items: still open, smaller than reported.** Empty block under the left column down to where the tabs start: axb05 677 to 930 = 253 px at 1440 (figure ends 864); ai07 616 to 888 = 272 px; at 1920 233 px for ai07. Bottom-to-bottom differences at 1280 to 1920: axb05 168 to 196, ai07 167 to 206, axe12 147 to 182, biz05 129 to 155, ai10 206 to 209 (file run), biz04 164 to 166 (meta-wide), axb01 154. Nothing else exceeds 119.
- **Reveal narrower than the question: open.** Reveal 1128 px (x 156 at 1440, x 396 at 1920) against a question screen at x 56 to 1384 (1440) and 56 to 1864 (1920).
- **Projector at 1280x720: open.** See Classroom.
- **Option cues: partly open.** See Content.
- **biz02 and bz14: unchanged.** biz02 options 1 and 2 are strawmen ("The employer match required the default rate" contradicts the scene's automatic enrollment); keyed option is the shortest (39 against 44 and 54). bz14 has two options (31 and 33 characters), so a coin flip is 50%.

## Findings not introduced by 76

- **m-1 (Minor). Tutor coverage.** 36% direct on my wording; list under Tutor battery.
- **m-2 (Minor). Wide reveal hole on meta-left items** (253 to 272 px; above). Fix: move Questions and the tutor under the left column on those items, or move Design/Sample into the figure column.
- **m-3 (Minor). Reveal 1128 px against 1328 to 1808 px question screen.** Heading and progress bar jump about 340 px at 1920.
- **m-4 (Minor). Paragraph breaks differ between page and server tutor** (38 of 75 raw, 4 of 8 in the UI). Put the paragraph rule in `server/tutor.py` and `curated()` once; delete the regex in `tutorParas`.
- **m-5 (Minor). Record page balance** (391 px at 1 call, 322 px at 7). Above.
- **m-6 (Minor). Projector at 1280x720** (`class_log.json`, `shots/cls_proj_*`). Smallest text open view: axb08 11.6 px ("Spread 100 points by how likely each option..."), axb01 13.0, axb05 13.9, deterrence 13.7, civic 15.6, estimate and forecast 17; revealed view 12.4 to 14.4 ("answers" unit). The revealed finding ("No message worked; forecasters still overestimated effects", "More money, more wallets returned") is about 15 px bold while the question above it is the 28 px headline, so the result is the smallest heading on the screen. Forecast reveal: right column empty from y 390 to 670. "Average confidence" wraps to two lines and its value sits 5 px lower than its neighbours. Fix: raise the floor to 14 px, set the finding at headline size, put the two forecast bars at that size.
- **m-7 (Minor). A phone that did not answer keeps live controls after the instructor stops answers.** `tools/close.py`: about 2 s after "Stop answers" the phone shows a transient toast ("Answers are closed for this decision...") that overlaps the scene text (`shots/cls_phone_closed_bz04.png`), but the estimate or choice stays editable and "Lock my answer" enables; locking then replaces the page with "Responses are closed". Server rejects correctly (409, nothing stored). Fix: disable the instruments and show a standing line when the phase is closed.
- **m-8 (Minor). Option cues.** dimant-deviant-choice: the keyed option is the only one that says "cheap compliance" while the distractors say "costly" or omit cost, and the "alone" distractors are strawmen (follow-up says neither works alone). social20: keyed option is the unique longest (54 against 38 to 44). ai12: keyed longest (47 against 38 and 40). dimant-competition-choice: keyed option differs by one dimension from two others (hub of the set); its explain says "competition lowered moral behavior" as fact where the paper's own wording is "suggestive evidence" (P = 0.008); the follow-up does say so. biz05: both keyed options mention "efficient" households as the scene does, both distractors say "above-average". Bank-wide over 36 choice and causal items: key is the unique longest in 5 of 33 (chance 9.4), unique shortest in 8 of 32 (chance 9.2): no systematic length cue. Forecasts: 16 true, 19 false; "more/higher/raised" in 56% of true and 42% of false claims; claim length 96 against 89.
- **m-9 (Minor). Landing lede rag unchanged** (`shots/land_1440.png`): "Each round presents a real-life situation, from a / published research study, that you are / asked to predict. Once you have made your". The line ends on "from a", the comma sits before "that you are", and "you will then be shown" runs on. Fix: "Each round gives you a real situation from a published study. Make your prediction, then see what the researchers found."
- **m-10 (Minor). Phone reveal order.** At 390 the evidence plate starts at y about 567 for the masks forecast and below the fold for repro-msci (headline plus a long paragraph first). Fix: plate directly under the verdict line on phones.
- **m-11 (Minor). Manager paragraph on the wide reveal has a narrower measure and smaller type than the body above it** (repro at 1920: lines 410 to 440 px against about 515 px), so the block reads as a different text. Fix: same measure and size, or set it as a margin note.
- **m-12 (Minor). Placeholder "see the paper"** remains in lies-in-disguise `study.n` (open since review 45; not re-checked in the UI this round).
- **m-13 (Minor). Hedged wrong forecast scores above 0** ("Not what the study found. Score 2" at 70% wrong; 82 for 70% right; fence 50). Consistent Brier scoring; wording invites the question.
- **m-14 (Minor). Concept questions cannot be answered by the tutor** (planning fallacy, pluralistic ignorance, confounder, ROI). Subsumed in m-1; listed because MBA users will ask these first.
- **o-1 (Optional).** Chip "Has it been replicated?" on repro-msci-estimate answers about replication materials, not about reproducing.
- **o-2 (Optional).** Three decisions scroll at 1280x720 on the predict screen: axb05 +92, meta-perception-causal +128, axf05 +7 (axb06 +25 on the served page).
- **o-3 (Optional).** A "?" glyph sits right of an unset confidence slider (`shots/srv_fresh_1920_p_dimant-competition-choice.png`); "not set" would say it.
- **o-4 (Optional).** Option rows on the wide predict screen wrap at about 410 px inside a 650 px row (deterrence at 1440: "Deterrence was best with no / delay or with the longest delay"), leaving 160 px empty and a break after "no" (`shots/srv_fresh_1440_p_dimant-deterrence-choice.png`).

## Item 5: fact check

- **repro-msci-estimate:** 700 reviewers, nearly 500 articles, 2019 policy, more than 95% fully or largely reproduced, 29% data not accessible, 68% overall, 12% before with 55% reproduced: all in the abstract and introduction. 6 of 6 quotes verbatim. Design and boundary correct ("reproduced" is not "replicated" is in the follow-up).
- **dimant-competition-choice:** 95 designs submitted (102 teams invited), 45 drawn, 18,123 participants, d = -0.085, CI [-0.147, -0.022], P = 0.008 (approach A), -0.086 (B), heterogeneity about 1.6 times the average standard error. 6 of 6 verbatim. Wording point in m-8.
- **dimant-megastudy-estimate:** 140,461 teachers, 2,992,027 students, 15 interventions plus reminder-only control, 4 weeks in fall 2021, 5.06% (3.30% after winner's curse), 1.89% any nudge, 2.26% personalised, persistence over 8 weeks. 7 of 7 verbatim.
- **dimant-deterrence-choice:** 296 subjects, four treatments IR-ND 66, IR-D 85, DR-ND 69, DR-D 76, punishment delayed two rounds, non-monotonic: no delay (IR-ND) and maximum delay (DR-D) deter best, IR-D (immediate verdict, delayed fine) is the reference and lowest, so the implication "quick verdict with a slow penalty gave away deterrence" is supported. Scene "card game" and fine "with a given probability" match Section 1. 7 of 7 verbatim. Note: DR-ND against DR-D is only marginal (p = 0.071) and IR-ND against DR-D is not different (p = 0.823); the explain does not overclaim.
- **dimant-masks-forecast:** N = 4,931 nudge study, 1,034 forecasters, seven messages, no evidence that any nudge worked, forecasters overestimated (pooled z = 4.40, Democrats z = 4.84; Republicans not significant, p = 0.09). The explain "reliably overestimated ... most of all for Democrats" is fair.
- **dimant-hate-choice and social15:** 78.1% closeness, 14.97% against 13.54%, 11.99%, taking 22.9%, cooperators 72.8% to 59.0% and 73.2% to 62.4%, over 8,600 participants all appear in the paper. "25 to 35%" and "20% to essentially 0%" appear in the nudge section.
- **dimant-deviant-choice:** 418 participants, 42.7% against 28.7% (low stakes), 22.2% against 36.5% (high stakes): verified. Weak penalty alone not significant (28.7 against 23.7, p = 0.17), consistent with the follow-up.
- Not read against a paper here: the other decisions (no PDFs); I read them against their stored quotes and the bank's gates.

## Items 6 and 7: leaks and content

- **Leak scan.** Public `/api/challenges` for all 116 decisions carries no `truth`, `answer`, `answerTitle`, `explain`, `target`, `rankAnswer`, `multiAnswers`, `best`, `why`, `valueLabels`; the only forbidden-key matches are `study` (design line, shown on the decision screen by design) and `mask: true` on the masked causal node, whose label is "?" and whose edges are empty. No estimate target appears in its own scene or question; no scene number sits inside an estimate's midpoint tolerance. Tutor chips and panel: 0 of 116 before the answer.
- **Blind strategies.** Longest, shortest, scene-overlap and two-part strategies hit at or below chance on 36 choice and causal items; the overlap strategy hit 5 of 11 against 2.9 expected (small n, dominated by social13 and bz12). "Always true" on forecasts earns 16 of 35. I did not re-simulate scoring-level skill; tests cover it.
- **Content read (about 60 decisions).** Read in full: the four new ones, masks, deviant, hate-choice, social15, social16, social01, social07, social20, contagion, notalie, enforcers, observability, conspiracy, opioid, polarizednorms, ai01, ai02, ai07, ai10, ai12, axb01, axb02, axb05, axb08, axb09, axb10, axb11, axb12, axb13, biz01, biz02, biz04, biz05, biz07, biz08, bz02, bz04, bz07, bz08, bz13, bz14, bz15, bz16, rollout1, rollout2, rollout4, civic-wallet-experts, truth-telling-gains, lies-in-disguise, opposing-views-bot, facebook-deactivation, forecast-teams-rank, forecast-training, overconfidence-hard-task, social04, social08, social10, social12, social13, social14. Designs are described correctly; non-significant differences are not treated as real (axb08 labels them "not significant" and counts them zero); no invented scenarios; copy reads as plain research summary. Faults: m-8, biz02 and bz14 above; ai10's scene gives the 30% baseline, which the claim then tests (stated before, not a leak of direction).

## Classroom (item 3)

Instructor 1280x720, three 390x844 phones (`tools/cls.py`, `class_log.json`), seven decisions: civic-wallet-rank, axb08 (allocate), axb01 (delegate), axb05 (causal), repro-msci-estimate (estimate), dimant-masks-forecast, dimant-deterrence-choice.

- **Leaks:** during each open decision I probed `/api/challenges`, `/api/rooms/CODE`, `/api/library`, `/api/tutor` for the open decision and its same-paper siblings (three questions each), `/api/reveal/ID`, the instructor bank and the CSV export. Library omitted the open decision; the tutor answered "opens after your instructor reveals it" for the decision and siblings; `/api/reveal` 409; bank and CSV 403 without the key. Phone pages contained no answer title. No leak.
- **Dropped connection (axb01):** phone 2 offline, then back: its answer was recorded and the phone showed "Your answer is in".
- **Closed phase (axb05):** phone 1 never answered; "Stop answers"; the phone got a toast but kept live controls (m-7); a late API post with a bogus token returned 403; after reveal all phones got the reveal.
- **Forecast result:** two bars (Said true / Said false), counts, the study's side marked, no median, on projector and phone (`shots/cls_proj_rev_dimant-masks-forecast.png`).
- **Scale:** 120 joined, 5 refused with 409 "This session is full" (cap by design). With each student sending its own X-Client-Id (as the page does): 120 concurrent answers all 200, wall 0.17 s, max latency 0.14 s; 120 concurrent polls all 200, max 0.01 s. Without client ids the 120 requests from one IP share a bucket and 108 get 429; browsers always send an id, but a scripted client or a proxy that strips the header would see this.
- **Phone updates:** about 2.3 s from "open" on the console to the question on the phone.
- Errors: 0 page errors on any page.

## Server audit (item 9)

- Validation: 20 kB body 400, bad JSON 400, array body 400, wrong content type 400, string and 10^30 answers 400, bad confidence 400, bad token 403, answer for an earlier decision 409, duplicate answer 200 with `accepted: false`, wrong or missing key 403, unknown room 404.
- Headers: CSP, nosniff, no-referrer, COOP, Permissions-Policy present.
- Secrets: grep of source for key patterns, API keys, passcodes found none; passcode and key are read from the environment; `.gitignore` covers sqlite files and `server/data/`.
- Instructor creation without a passcode on a loopback host works (as designed); on a non-loopback host the code returns 403 (read at `server/app.py:211`, not run).
- **Streamlit not run** (skipped; limited time). No Streamlit live class.

## Item 2: plays

240 scripted plays across 24 decisions (choice: deterrence, competition, ai09, social04; estimate: repro, megastudy, ai01, bz04; forecast: masks, axb06, biz04, ai10; rank: civic-wallet, forecast-teams, axf05; causal: axb05, meta-perception, axe12; allocate: axb08, axf01; delegate: axb01, rollout3; multi: ai07, biz05), five viewports (390x844, 820x1100, 1280x720, 1440x900, 1920x1080), on the served page with a fresh profile per play and on file:// with four rounds already in the record (`sweep_srv_fresh.jsonl`, `sweep_file_rec.jsonl`). Results: 0 page errors, 0 sideways overflow, Lock enabled after every legal call, 0 clipped text outside screen-reader-only spans, smallest text 12 px on every reveal and 12.5 px on predict screens (study line), fitQuestion keeps the predict screen inside the viewport at 1440 and 1920; I measured by script and read about 40 screenshots (landing at 1440, deterrence and competition predict, axb05, repro and masks reveals, record, header, projector and phone shots). The record-present run and the served run agree. My own stranded-word detector found 0 in headings, paragraphs and list items; the design lint (R34) also reports 0. Browser zoom was not tested by real browser zoom.

## Three changes that would raise Visual most

1. **Wide reveal on meta-left items (axb05, ai07, axe12, biz05, ai10).** Screen `shots/srv_fresh_1440_r_axb05.png`. Measured: left text column ends at y 677 while the figure ends at 864 and the tabs start at 930, a 253 px hole (272 px on ai07). Redesign: for these items put "Design / Sample / Published / Checked" under the figure and let the manager line and Questions tab take the left column, so both columns end within 40 px.
2. **Reveal width against the question screen.** Measured: 1128 px reveal against a 1328 px (1440) to 1808 px (1920) question; progress bar and heading jump 340 px at 1920. Redesign: give the reveal the question's grid (text left, plate right) and step the type scale up instead of leaving a centred narrow column; leave the vw-sized verdict numerals alone.
3. **Record page and projector reveal.** Record: 391 px blank right of the plot at 1 call, 322 px blank under the plot at 7 calls. Redesign: put the calibration plot and "Recent calls" side by side and run "By area" full width beneath both, no DOM move. Projector at 1280x720: finding set at the 28 px headline size, floor 14 px, forecast bars sized to fill the empty right column (y 390 to 670).

## Could not verify

- `tools/verify_dois.py` not run; I checked DOI existence and title through Crossref, not the landing pages or the "Research by Eugen Dimant" band's links in a browser (I read the band: three real titles and a "Show all 18 papers" control).
- Papers read: the four iteration-66 PDFs in full for numbers and quotes (26 of 26 quotes verbatim); masks, hate (all the numbers I listed) and deviant (all numbers I listed) by text search; Politicizing masks quotes for 7 numbers; Hate Trumps Love and Deviant not read end to end. No other decision had a source text available.
- Streamlit (with and without `THV_INSTRUCTOR_PASSCODE`) not run.
- Screen-reader use (NVDA, VoiceOver) not tested; keyboard operation and ARIA attributes were.
- Real browser zoom not tested; viewport sizes only. Blur not assessed.
- Blind-strategy skill simulation not re-run beyond the cue counts above.
- The console's "room full" message to the instructor was not seen in the UI (API returns 409 "This session is full").
- Remote class on a non-loopback host without a passcode not run.
- 500-play sweep: I ran 240 plays plus 116 chip plays.
