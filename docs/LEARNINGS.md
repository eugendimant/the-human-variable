# Learnings from the build sessions (October 31 to November 2, 2026)

Read this after `docs/HANDOVER_FOR_CLAUDE.md`. It records what forty iterations, thirty-one independent reviews and about twenty regression audits taught, so the next worker (Claude or another model) does not pay for the same lessons again. Each item is a rule, the incident that produced it, and where it is enforced.

## 1. What Eugen asked for, beyond the handover's section 1

- "Still too many AI giveaways… why even mentioning 'then see the evidence'?… just focus every screen on what's important." The home page now opens on one decision answered on a scale; no slogan, no lede. Two-beat headings ("Do X. Then Y.") are lint rule R14.
- "Fill out the empty spaces better. Too often do you do a text line break where there shouldn't be one." Headings wrap greedily (`text-wrap: wrap`, never `balance`, no `max-width` in ch or em on headings); the question screen runs in two columns from 1200 px. Lint R19 flags `balance` on headings; R33 flags a heading that wraps while its box stops well short of the space available.
- "Give me visual previews." Send screenshots after every visual round, at 1440 and 390, of the screens that changed.
- "Do not publish the repository or deploy publicly without my approval." Still binding. Nothing has been published.
- RULE 0: never a sentence that downplays Dimant's contribution; scope lines state what a study covers. RULE G: a fix applies to every place the same defect class occurs, with a detector.
- Do not retire or weaken a Dimant item to fix a review point. When social20 was flagged, the strawman distractor was replaced instead (iteration 35).

## 2. Process rules that prevented regressions

1. **Fix, gates, regression audit, review, in that order.** Every iteration since 36 found at least one introduced defect in the audit that the 300-plus tests missed. Never send a snapshot to a reviewer before an audit by a fresh agent reports no introduced Major (`qa/AUDIT_PROMPT.md`).
2. **A detector for every new defect class**, live-fired: inject the defect in a copy, see the test or lint rule fail, remove it, see it pass. Examples: plural after 1 (R14), heading squeezed (R33), sample number inside an estimate band (browser test), causal links too short or crossing a pill (bank test), pick-two solved by option length (bank test), percent not quoted as a percent (bank test), allocate labels leaving their grid (browser test).
3. **The bank is written by scripts, never by hand.** `src/bank.json` is changed only by `tools/*.py` scripts, each idempotent and editing by text. After any `git checkout src/bank.json`, rerun `tools/tutor_routes_2026_10_31.py` and every content script newer than the commit you restored. Iteration 38 lost the tutor's writing-request route this way and the ledger claimed it shipped.
4. **The tutor is frozen by golden batteries** (`tests/tutor_golden.json`, `tests/tutor_golden_wide.json`, about 24,000 pairs). Before regenerating with `tools/tutor_golden.py`, diff old against new and read the changes by class. A class you did not intend means the change is wrong. Iteration 38 tried matching a one-word follow-up and the diff showed significance questions borrowing "cost" and "card" answers; it was dropped.
5. **Server and page tutors must agree word for word.** `server/tutor.py curated()` and `src/app.js curated()` implement the same router. JavaScript's `\b` treats "é" as a boundary and Python's does not; the page tests routes on the accent-stripped question as well (audit 39).
6. **Sibling decisions share papers.** A follow-up, explanation or chart in one decision must not print another decision's answer (ai01 and ai02; genai2 and axe04). `tests/test_bank.py::test_siblings_do_not_leak_each_other` now reads chart values too.
7. **Settled decisions are tests.** Before changing behaviour, search the tests: iteration 38 released an abandoned console's open decision after 20 minutes and broke two tests that require an open question to stay held while an instructor talks. It was reverted.
8. **Quarantined items are never served** and one must exist for the quarantine test (judg02). Do not retire it to fix a review point about its content.
9. **Two auditors can disagree** (one amber badge on a shared top place). Pick the rule in `qa/DESIGN_RULES.md`, record the choice in the ledger, and stop flip-flopping.
10. **A long test run is about 12 minutes.** Start it in the background and keep working; never kill processes by pattern (`pkill -f` once killed the agent's own shell).

## 3. Content rules learned the hard way

- A number in player text must be in a stored quote, with its unit: "3%" once passed on "3–15 months" (review 31).
- A sample line on the question screen can leak an estimate's answer ("95 respondents" on a target of 92 ± 5). `sampleLine()` drops the sample of an estimate when any of its numbers lies inside the band, on the screen and in the public bank.
- An after-the-fact "best of three" is an upper bound, not a lever (genai2, review 31 Major). Key what the design supports.
- A distractor must be false in every period the item talks about (biz05: "did not change" was true longer term).
- Pick-two keys must not be the two shortest or two longest options; pick-one keys should not be the longest option either.
- Statistics (z, P values) stay in the Source tab; explanations say "a reliable difference".
- Contested findings enter only as contest items; non-significant differences are never scored or coloured as evidence (grey, "n.s.").

## 4. Design rules learned

- Two colours carry meaning: blue is the player's call, amber is the evidence. Nothing else uses them (join codes, meters, "For a manager:" are ink or slate).
- One amber mark per chart; tied places share a number ("1=").
- Every visual change is linted at 1440 and 390, including states reached only by interaction (locked home try-it at several values, revealed reveals, record after several rounds, projector).
- Labels on the mark; no colour keys; a figure's title or note names its measure.
- Read-outs reserve their space before the first touch (a hidden placeholder), so nothing jumps mid-drag.
- Causal diagrams: stretched to the canvas on wide screens, top to bottom on phones, each link at least 50 units between pills and crossing no third pill.

## 5. Where the score stands and why

Independent scores: 86 to 88 for the last fifteen reviews (review 31: 87). Science, learning, gameplay, content and technical sit one or two points short; visual has sat at 12 of 15 for nine reviews. The reviewers' recurring asks are in `docs/HANDOVER_FOR_CLAUDE.md`, "Where it stands". The cheapest points are probably: a composed wide reveal (one page, not stacked panels), the phone reveal order, labels on marks in the allocate and calibration figures, a projector reveal that fits one screen, and more key-less tutor coverage for natural phrasings.

## 2026-11-10: never rerun every content script

- After `tools/tutor_routes_2026_10_31.py`, nothing else needs to run: it writes only `tutorRoutes`. The rule "rerun newer content scripts" applies only after `git checkout src/bank.json`.
- The early scripts (`content_review1` to `content_review13`) are not safe to rerun on the current bank: they fail midway or rewrite retired items. A loop over `tools/content_review*.py` changed 249 lines of `bank.json` and `evidence.json`; `git checkout` of both files restored them.
- The tutor's sentence splitter uses no regex lookbehind: older Safari cannot parse one, and a parse error stops the whole page script.

## 2026-11-11: test layouts with a record present

- The principle strip is drawn only after earlier calls on the same principle. Every layout test that starts from an empty record misses it. A layout change is checked with `test_principle_strip_keeps_its_size_with_a_record` and by measuring with a record.
- A gap metric must not count a full-width element as part of both columns. Measure each column to its own last element.
- Do not invent a chart axis. If the instrument's scale is not in the stored quotes, draw from zero on a round scale.
