# Quality assessment

Scores in this file come only from independent reviewers: fresh agents that did not build the product and reviewed a snapshot copy. A score the builders give themselves does not count. Each reviewer played the game in a real browser at 1440 and 390 px, ran a live class with three phones, ran axe, probed the server, read the content through ten lenses and fact-checked items against the papers. Full reports: `qa/reviews/`. What was fixed after each review: `qa/LOOP_LEDGER.md`.

## Independent scores so far

| Review | Snapshot after | Score | Blocking | Major |
|---|---|---|---|---|
| 1 | iteration 5 | 62 | 2 | 15 |
| 2 | iteration 6 | 59 | 2 | 15 |
| 3 | iteration 7 | 70 | 1 | 7 |
| 4 | iteration 8 | 76 | 0 | 7 |
| 5 | iteration 9 | 78 | 0 | 7 |
| 6 | iteration 10 | 79 | 0 | 7 |
| 7 | iteration 11 | 79 | 0 | 5 |
| 8 | iteration 12 | 78 | 0 | 4 |
| 9 | iteration 13 | 79 | 0 | 3 |
| 10 | iteration 14 | 82 | 0 | 2 |
| 11 | iteration 15 | 81 | 0 | 4 |
| 12 | iteration 16 | 84 | 0 | 1 |
| 13 | iteration 17 | 83 | 0 | 3 |
| 14 | iteration 18 | 85 | 0 | 1 |
| 15 | iteration 19 | 86 | 0 | 1 |
| 16 | iteration 20 | 83 | 0 | 1 |
| 17 | iteration 21 | 86 | 0 | 1 |
| 18 | iteration 22 | 86 | 0 | 1 |
| 19 | iteration 23 | 87 | 0 | 1 |
| 20 | iteration 24 | 87 | 0 | 0 |
| 21 | iteration 25 | 87 | 0 | 0 |

The target is 95 from an independent reviewer. It has not been reached yet; the loop continues.

## Latest category scores (review 19)

| Category | Points | Score |
|---|---|---|
| Science | 15 | 13 |
| Learning | 15 | 13 |
| Visual | 15 | 12 |
| Gameplay | 15 | 13 |
| AI and business | 10 | 9 |
| Content | 10 | 8 |
| Technical | 10 | 9 |
| Classroom | 5 | 5 |
| Accessibility | 5 | 5 |

## Evidence the reviewers recorded

- **Tests:** the full suite passed in every review (234 at review 19), including Playwright play of all eight formats at two widths, axe, a three-phone live class and a 50-student load test.
- **Answer integrity:** a byte scan of the served pages found no answer text; the class lock held on every route probed in reviews 4 and 5.
- **Accessibility:** axe reported no serious or critical violations on up to 30 states; keyboard-only play and reduced motion worked.
- **Load:** 50 concurrent students, p95 under 45 ms, no errors.
- **Fact-checks:** 8 to 10 items per review against the papers. Most numbers were correct or consistent; review 6 found one wrong number on a Dimant item and several provenance gaps (fixed in iteration 11). All findings and fixes are in the ledger.

## Not verified

- No live Gemini call has been made from this environment.
- No classroom pilot with real students has been run.
- The Docker image was not built here (no container daemon).
- Fourteen explanations rest on published abstracts because the full texts were not readable; they are listed in `tests/test_bank.py` (`NO_NUMBER`).
