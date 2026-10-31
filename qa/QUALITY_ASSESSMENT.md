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

The target is 95 from an independent reviewer. It has not been reached yet; the loop continues.

## Latest category scores (review 5)

| Category | Points | Score |
|---|---|---|
| Science | 15 | 11 |
| Learning | 15 | 11 |
| Visual | 15 | 11 |
| Gameplay | 15 | 11 |
| AI and business | 10 | 9 |
| Content | 10 | 7 |
| Technical | 10 | 9 |
| Classroom | 5 | 4 |
| Accessibility | 5 | 5 |

## Evidence the reviewers recorded

- **Tests:** the full suite passed in every review (194 at review 5), including Playwright play of all eight formats at two widths, axe, a three-phone live class and a 50-student load test.
- **Answer integrity:** a byte scan of the served pages found no answer text; the class lock held on every route probed in reviews 4 and 5.
- **Accessibility:** axe reported no serious or critical violations on 21 states; keyboard-only play and reduced motion worked.
- **Load:** 50 concurrent students, p95 under 45 ms, no errors.
- **Fact-checks:** 10 items per review against the papers. Numbers were correct or consistent; scoring and framing problems found are listed in the ledger with their fixes.

## Not verified

- No live Gemini call has been made from this environment.
- No classroom pilot with real students has been run.
- The Docker image was not built here (no container daemon).
- Thirteen explanations rest on published abstracts because the full texts were not readable; they are listed in `tests/test_bank.py` (`NO_NUMBER`).
