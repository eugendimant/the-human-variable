# Independent review 41 (snap63 for iterations 62 and 63, finished on snap64 with the rebuilt landing page)

**Score: 84/100.** 0 Blocking, 1 Major (introduced in iteration 62), 25 Minor, 4 Optional.

Work was done in copies (`scratchpad/r41/work` = snap63, `scratchpad/r41/work64` = snap64). snap64 differs from snap63 only in `src/app.js` (home, heroTry, methods line), `src/app.css` (end of file), `src/shell.html` (footer) and the two built pages, so everything checked on snap63 outside the landing page carries over; the Major below was re-confirmed in snap64 (`grep` finds the same call in `src/app.js` and `index.html`).

## Score table

| Category | Max | Score | Evidence in one line |
|---|---|---|---|
| Science | 15 | 13 | 10 fact-checks, no number mismatch; one rewritten scene misstates who used GPT-4; one headline number rests on a secondary source |
| Learning | 15 | 13 | Proper rules, no blind strategy earns skill on estimates or forecasts; reveal teaches; two wording cues remain |
| Visual | 15 | 11 | Reveal plates are strong; landing reads clearly but has a template "1-2-3" block, an inverted label/question hierarchy, an empty band at 820 px, clipped strip labels |
| Gameplay | 15 | 13 | 20 decisions x 2 widths x 2 hosts and a 112 x 4 sweep with a record: no overflow, no console error, keyboard round of 11 completes |
| AI and business | 10 | 9 | Strong orientation; manager lines concrete |
| Content | 10 | 8 | 39 decisions read; clean overall; a few leaks of direction, near-true distractor, copy slips |
| Technical | 10 | 8 | 379 tests pass, lint 0, load fine; but a call to an undefined function shipped in the class poll loop with no test |
| Classroom | 5 | 4 | No leak on any route; close notice broken; projector text small at 720p |
| Accessibility | 5 | 5 | axe clean on 89 states (WCAG 2.0 to 2.2 AA plus best practice), keyboard round, reduced motion |

## Tests and tools

- `python -m pytest -q`: **379 passed** on snap63 (18 min 56 s) and **379 passed** on snap64 (18 min 38 s).
- `python3 tools/design_lint.py`: `by rule: {}` on both snapshots.
- `python src/build.py --check` on snap64: built pages current.
- axe: 89 states clean (home fresh and with record at five widths, play and reveal for 10 decisions at 1440 and 390, tabs, record, Library, All decisions, round complete, Research standard panel, console create/lobby/open/revealed, projector open/revealed, phone lobby/question/sent/revealed for five formats).
- Keyboard only: Tab to Start playing, 11 decisions of "Leading with AI" answered and locked with keys only (choice, forecast, delegate, estimate, multi, allocate), focus lands on `#r-h` after every reveal, round-complete page reached.
- Reduced motion: 0 running animations, max transition 0 s.
- Load: 120 students from one IP, 1,200 requests in 2.7 s, all 120 joins and 120 answers recorded, p50 1 ms, p95 67 ms, max 140 ms. 201 polls got 429 because my simulated phones polled every 0.3 s (real phones poll every 2 s); no join or answer was refused.
- Streamlit 1.66.1, headless, with and without `THV_INSTRUCTOR_PASSCODE`: all four pages load, 0 exceptions, 0 page errors. With a passcode the Play page shows the "This deployment runs live classes" notice and Run a class shows the passcode field. The wrong-passcode path was not exercised (unverified).

## Introduced (iterations 62, 63 and the snap64 landing page)

### Major

**I-1. The "answers closed" phone notice calls a function that does not exist (iteration 62).**
- Where: `src/app.js` line 688: `toast('Answers are closed for this decision. …')`. The page's notice function is `notice()` (line 756). `toast` resolves to the `#toast` element, so the call throws a TypeError inside `roomPoll()`'s `try`.
- Observed (two separate runs, served page, 390 px, phone that had not answered when the instructor pressed Close): no notice ever appears; the header changes from "Live class L8WQM" to **"Reconnecting…"** for about 4 seconds although every poll returned 200; `render()` is skipped; the question and its controls stay on screen as if answers were still open. In the page, `typeof toast` is `"object"`.
- Why it matters: the ledger records this as done ("a phone toast when answers close"); the feature never worked, every unanswered phone gets a false connection warning at each close, and the next poll is delayed from 2 s to 4 s. No test covers the closed phase on a phone.
- Fix: call `notice(...)`; add a browser test that closes a decision with one unanswered phone and asserts the notice text, `#room-conn` still reading "Live class", and no caught exception. Keep a persistent line on the card ("Answers are closed") because a 3.2 s notice is easy to miss.
- Screenshots: `r41/shots/phone_closed_noanswer.png`, `r41/shots/phone_closed3.png`.

### Minor

- **I-2. rollout4 scene (iteration 63) misstates the design.** "nearly 1,000 high school students practiced math with unrestricted GPT-4" — the nearly 1,000 students were split across a control arm, GPT Base and GPT Tutor (abstract: students given "one of two" tutors, compared with students who never had access). The scene also adds "Your plan gives new hires the same unrestricted access", an invented plan. Fix: "nearly 1,000 students were randomly assigned to practice with unrestricted GPT-4, a tutor version with safeguards, or no AI".
- **I-3. bz02 scene (iteration 63) hands over the mechanism.** "A customer's weekly sales swing far more than an ad can move them", under the title "The noisy ROI test", before the claim "…confidence interval was under 50 percentage points wide". The scene argues for "false". Fix: move the sentence to the explanation; retitle neutrally ("How precise is one ad test?").
- **I-4. ai02 scene and manager line now say graders were blind; the tutor denies knowing it.** Scene: "Independent professionals graded the finished work blind." Tutor on ai02, "were the graders blind?": "The lab's summary does not record who rated the outcome". No stored quote supports "blind" (evidence is the abstract only). Fix: store the methods quote and let the raters route read the scene, or drop "blind".
- **I-5. social12 chart numbers are invisible to the tutor.** "What were the actual callback rates?" returns "I could not match that question…" while the plate shows 6.45% and 9.65%. The numbers themselves are correct (see fact-checks). Also the study card says "Checked against the published abstract" beside two numbers that are not in the abstract, and the evidence location for 6.45 reads "(9.65 minus 3.20)", which looks derived although the paper prints the sentence. Fix: let the tutor read `chart.labels/values`; store the verbatim 6.45 sentence; show "abstract and full text" on the card.
- **I-6. dimant-hate-choice figure line (iteration 63).** "The drop is as large for painting taste, so expectations set politics apart": the drops are 13.8 and 10.8 points (statistically indistinguishable, not "as large"), and the chart shows no expectation data, so the "so…" clause is a conclusion the figure does not carry. The title runs two lines. Not a weakening of the science, but the figure overstates. Fix: title "Share who cooperate if the partner does"; caption "The two drops are statistically indistinguishable".
- **I-7. Principle strip: the "+N" overflow label is clipped at the right end** (introduced with the 560 px cap). Sweep of 112 reveals with a full record: text outside the strip's SVG on 37 reveals at 1440, 32 at 1280x720, 28 at 1920; none at 390. Visible in `r41/shots/rec_1920_dimant-hate-choice.png` (a cut "+" at the 100 end). Fix: reserve 24 px at the right or anchor the label to the left of the stack at the upper end.
- **I-8. Allocate track at 390 has no zero label** (ends read "−20%" and "100%", the tick is unlabeled; `r41/shots/file_390_axb08_r.png`). At 1440 the "0" is there. Fix: print "0" under the tick at every width.
- **I-9. Landing, 820 px: an empty band of about 120 px between the sample question and its slider** (space held for the read-out that only appears after the first move; `r41/shots/land_file_820_fresh_fold.png`). Fix: do not reserve the read-out's height before the first move between 600 and 900 px.
- **I-10. Landing: the label is bigger than the thing it labels.** "Try one now" is set at about 44 px, the sample question under it at about 34 px, and "How a round works" (also an h2) at 14 px. `qa/DESIGN_RULES.md` rule 1 and `qa/TUFTE_PASS.md` still say the "Try one now" label was dropped and "the question is the heading"; the detector misses it because the question is now a `<p>`. The owner asked for the section, so the finding is the hierarchy and the stale documents. Fix: make "Try one now" a small run-in or a 14 px section label matching "How a round works", let the question keep the weight, and update both documents.
- **I-11. Landing: the sample is below the fold on laptops.** Fresh, the "Try one now" section starts at y=720 on 1280x720 (exactly off screen) and y=794 on 1440x900; with a resume banner it moves to 802 and 876. The first screen is headline, paragraph and three text steps. A first-time visitor does understand what this is (the headline and two sentences work, and at 390 the first screen is clean), but the reason to play is the slider, and nothing on the first screen hints that it is one scroll away. Fix: tighten the hero (h1 two lines at 1280: it now breaks to three with "do?" alone on the last line when the resume banner is present), or put the slider in the right column and the three steps beneath.
- **I-12. Landing: the numbered three-step block is the stock "how it works" device** (blue numerals, bold title, grey sentence, hairlines). It is honest sequence, so rule 5 allows it, but it is the one part of the page a creative director would call templated. Fix: show the three steps as one annotated miniature of a real round (situation, slider, result plate) instead of a list.
- **I-13. Credit links are 18 px tall** on the landing page and footer; "Research standard" is 21 px. Inline links are exempt from WCAG 2.2 target size, and axe passes, but on a phone the two links sit 16 px apart on one line. Fix: stack them or give them 24 px line boxes.

Checked and clean among the changes: strip width at most 562 px on all 448 reveals; signed charts and axis ends; axe12 has no invented axis; social01 and dimant-polarizednorms-choice on one 0-to-3 scale; glossary ("what is a p-value?" defines with no citation, "what is the p-value?" stays on the study), replication route, same-author routing; page and server tutor agree on 60 of 60 of my questions; projector forecast bins ("0 to 9%", "10 to 19%"); social12 rates against the paper; comparative-word gate present; axb05, biz02 and social20 distractors are false by the items' evidence; no Dimant item weakened; landing has no overflow, no text under 12 px, h1 at most three lines, no console error at 390, 820, 1280x720, 1440x900, 1920x1080, fresh and with a record, on both hosts; no answer text in the served landing page.

## Other findings

### Minor

- **m1. Tutor says "No." to "Did the effect last?"** on axb15: "No. The reduction in belief persisted at the two-month follow-up." The stored follow-up is "Did the effect fade?"; the router matched it and kept its yes/no word. Fix: strip the leading Yes/No whenever the asked question is not the stored one verbatim.
- **m2. Tutor misses with natural phrasings (9 of 60).** "whats a confidence interval" and "Explain statistical significance to me" get the study instead of the glossary; "Was it a field experiment?" (design field says "Field experiment") and "is this a natural experiment?" (design says "Natural experiment in one firm") get "I could not match"; "What is variance?" and "what is a norm" dump the whole summary; "I dont buy it. why should I trust this" answers with the manager action; "how do I measure ROI then" on bz02 does not return the manager line that answers it.
- **m3. biz01's headline numbers come from a secondary source.** Evidence quotes for 86% and 37% carry `source: cribb20` ("Introduction" of Cribb & Emmerson 2020); the Madrian & Shea record says "participation figures as reported in Cribb & Emmerson". The numbers are right, but the product's rule is the item's own source. Fix: quote Madrian & Shea's table.
- **m4. Wording cues on choice items.** Picking an option that contains a comma, "and" or a semicolon earns +10.5 skill points on average across the 34 choice and causal items (16 have such an option; 200 simulated runs). biz02's key "Inertia, and the default read as advice" is the only two-part option of three. social20's key is the longest option and is repeated word for word as the manager line.
- **m5. biz02 distractor is close to true.** "Changing the rate took more paperwork than most would do" describes a transaction-cost form of inertia; the key is "Inertia, and the default read as advice".
- **m6. Stored key positions are uneven**: 13, 9, 7, 5 for positions 1 to 4 (always-first earns +12.3 skill in stored order). Display order is shuffled, so players cannot use it, but invariant I8 speaks of stored order.
- **m7. Projector at 1280x720**: smallest rendered text 11.2 px on axb05, 12 px on social01, 12.8 px on axb08, ai07 and bz02 ("For a manager" and scope text about 13 px). Unreadable from the back of a room. Open since review 40.
- **m8. Projector at 1920x1080 uses 62 to 78% of the height** (content ends at 651 to 846 px of 1080) in a 1,390 px column; the forecast view's largest heading is the generic "How likely is it that the study found this?" with the claim smaller beneath it (`r41/shots/proj_rev_bz02_1920.png`).
- **m9. Projector copy**: "1 of 1 participants answered".
- **m10. Research standard panel**: "109 sources passed; 1 are held back".
- **m11. Record page**: the minus sign of the headline "−10" renders as a heavy bar fused to the "1"; calibration dots at 0% sit on the x axis line; the sparkline is about 210 px wide beside a 190 px numeral (`r41/shots/file_1440_record.png`).
- **m12. Reveal, case items**: "Rolling out an AI assistant, step 4 of 4" sits as a small label directly above the explanation (label-above-text; no detector).
- **m13. Evidence charts with no amber mark** (social12, dimant-hate-choice): rule 29 says one amber bar proves the headline; here all bars are grey and the amber is only on the title.
- **m14. Wide reveals at 1920** stay in a 1,128 px column with about 400 px empty on each side, against the owner's "fill the width".
- **m15. Library** is nine near-identical rows ending in the same "The decisions behind it" disclosure. Open since review 40.
- **m16. bz08 chart** plots one of the six fined day-care centres ("center 1"); the claim is about all six. Fix: plot the fined-group mean per period, or say why centre 1.

### Optional

- o1. The forecast question "How likely is it that the study found this?" is the heading on 35 decisions; the claim is the content.
- o2. Delegate question screen at 1440 leaves about 150 px empty above and 200 px below the two columns.
- o3. The estimate tolerance travels in the public bank; with min and max it does not reveal the target, noted only for completeness.
- o4. README still says "18 decisions from 15 papers"; 17 live decisions carry "Dimant" in the source authors field (the eighteenth may list him only in `authors_full`; not checked).

## Live class (served, snap63; a11y pass repeated on snap64)

Console, three phones, eight decisions (rank, allocate, delegate, causal, estimate, forecast, multi, multi), answer, close, reveal, projector open and revealed at 1280x720 and 1920x1080, CSV, close joining, 125 joins, end.

- **Leaks: none.** While each decision was open and again while closed: `/api/rooms/CODE` as a student, `/api/reveal/<id>` (409), `/api/library`, `/api/challenges`, `/`, `/classroom`, `/api/instructor/bank` without a key (403), CSV without a key (403), tutor with the id ("opens after your instructor reveals it"), tutor without an id asking by author surname and by title (locked), and every same-paper sibling by reveal and tutor (409 and locked). No answer title, explanation, manager line, follow-up or task reason appeared; the served bank parses to question fields only and holds 0 secret strings.
- **Lock**: with the instructor silent for 21 minutes and students joining and polling, `class_lock` is false and practice evidence is served. Students alone cannot hold it.
- **Joins**: 3 phones plus 125 more from one IP: 117 accepted to reach 120, then "This session is full". Join after "Close joining": 409 with a clear message.
- **Poll errors**: with `/api/rooms/**` aborted, the console shows "Reconnecting to the class server… counts may be behind." and the phone "Reconnecting…"; both recover.
- **CSV**: 200 with key, readable answers per format.
- **End**: phone shows a dialog "This live session has ended".

## Scoring and gaming (server/scoring.py mirror, skill above guessing, bank-wide means)

- Estimates: fixed slider position 0 to 1: best −8.0 (position 0.35); constant value: best −4.2 (25); random slider −26.7.
- Forecasts: always 50% = 0.0; always 40% = −0.6; every other constant negative; alternating 90/10 = −41.1; 45.7% of claims true; every path with two or more forecasts mixes true and false.
- Allocate: uniform −1.0; all-in ranges from −200 to +100 by option.
- Multi: first two −1.5, longest two −10.6. Delegate constant choice: −12.5 to +6.2 (4 items). Rank stored order +16.7 (3 items, shuffled on screen).
- Choice: longest −14.7, shortest −8.3, negation words −5.8, comparatives +3.4, two-part option +10.5 (m4).
- Forecast wording: claims with negative words 38% true against 48% for the rest; short claims 35% true, long 56% (17 and 18 items; weak, worth watching).

## Fact-checks

| Item | Verdict |
|---|---|
| social12 (Bertrand & Mullainathan 2004) | Correct. "9.65 percent", "6.45 percent", "3.20 percentage points, or 50 percent" read in the authors' June 2004 version; abstract wording matches |
| rollout4 (Bastani et al. 2025, PNAS) | Numbers consistent with the abstract as summarised on RePEc; scene misstates who used GPT-4 (I-2) |
| bz02 (Lewis & Rao 2015, QJE) | Correct against the abstract: 25 experiments, $2.8 million, "over 100 percentage points wide", coefficient of variation 10, 10 million person-weeks |
| axf02 (Milkman et al. 2022, PNAS) | Correct against the published PDF: 689,693; 22 texts, all significant; 2.0 points (6.8%); control 29.4%; top 2.9 points (9.9%); shrunk 2.7 (9.3%); r = 0.03 and 0.60; ranks 15th and 16th |
| social15 (Dimant 2024, Management Science) | Correct: 78.1%, 14.97%, 13.54%, 11.99%, −22.9% found in the working-paper version; "about 39%" matches the stored published quote and the working paper's 37.5 to 39.8 |
| dimant-hate-choice (Dimant 2024) | Mechanism correct (beliefs, not preferences; Klee/Kandinsky minimal groups). 72.8/59.0 and 73.2/62.4 are not in the working paper I could read; unverified against the published text |
| dimant-masks-forecast (Dimant et al. 2022, Sci. Rep.) | Abstract level: 1,034 forecasters, seven messages, all groups overestimated, experts more accurate. 4,931 and −0.63 unverified |
| biz01 (Madrian & Shea 2001) | 86% and 37% match my knowledge of the paper; stored via a secondary source (m3); not re-read |
| social08 (Centola 2010) | 53.77%, 38.26%, four times faster match my recollection of the abstract; page did not load, unverified |
| genai2 (Goldstein et al. 2024) | Unverified: both pages blocked |

Blocked URLs (permission request unanswered or browser check; not retried, not fetched by other means): nature.com/articles/s41598-022-10524-1, pubmed.ncbi.nlm.nih.gov/40560616, nber.org w9873.pdf, api.crossref.org/works/10.1093/qje/qjv023, pnas.org/doi/10.1073/pnas.2115126119, pmc.ncbi.nlm.nih.gov/articles/PMC9082983, pmc.ncbi.nlm.nih.gov/articles/PMC10878360, hai-production.s3.amazonaws.com HAI policy brief.

## Content read (39 decisions, ten lenses)

All 17 Dimant-authored decisions' key fields were scanned and 9 read in full, plus 30 drawn at random (seed 41). Manipulation and outcome are described accurately on all but rollout4; no strawman set beyond biz02; no spliced quotes found; non-significant contrasts are outlined and labelled (axb08, genai2, social15); contested findings are taught as contests (bz10, bz11, biz04); manager actions are ethically aware (axf04, axb08). Copy is plain and specific.

## What would make it premium

1. One figure language end to end: the reveal plate is the product's best asset; the landing page and the Library should be built from it, not from lists.
2. A landing page whose first screen is the slider on a real study with the three steps annotated on it.
3. A projector view designed for a room: 24 px minimum text at 720p, the claim as the heading, the full height used.
4. A record page with a typeset headline number and a calibration plot whose points never sit on the axis.

## Key screenshots (all under `scratchpad/r41/shots/`)

`land_file_1440_fresh.png`, `land_served_1280_rec_fold.png`, `land_file_820_fresh_fold.png`, `land_file_390_fresh.png`, `kb_slider_focus.png`, `phone_closed_noanswer.png`, `phone_closed3.png`, `file_1440_social12_r.png`, `file_390_social12_r.png`, `file_1440_dimant-hate-choice_r.png`, `rec_1920_dimant-hate-choice.png`, `file_390_axb08_r.png`, `file_1440_rollout4_r.png`, `file_1440_record.png`, `file_1440_almanac.png`, `proj_rev_axb05_1280.png`, `proj_rev_bz02_1920.png`, `proj64_open_axb08.png`, `phone_ended.png`, `st_nopass_Play.png`. Logs: `r41/pytest.log`, `r41/pytest64.log`, `r41/shots/sweep.json`, `r41/shots/class_log.txt`.
