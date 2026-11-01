# Regression register: invariants that every change must keep

The owner's instruction (2026-10-31): "find a way to not introduce new major problems as you fix them." Three of the four Majors in reviews 22 and 23 were regressions caused by earlier fixes. This register is how that stops.

Every past Major is restated as an invariant with the test that enforces it. A change may not weaken a test to pass. A reviewer suggestion that conflicts with an invariant or a settled decision is not applied as written; the conflict is resolved here first (reviews 20 and 23 gave opposite advice on the estimate baseline, and following the first caused the second's Major).

| Id | Invariant | Enforced by | Origin |
|---|---|---|---|
| I1 | No answer, title or takeaway reaches a student before the class reveals it, by any route, including same-paper siblings | tests/test_http.py (served pages, reveal, library, tutor, siblings) | reviews 8 to 18 |
| I2 | Every number in an explanation, title, follow-up, chart or scene appears in a stored verbatim quote or printed value of the item's own source | tests/test_bank.py number and evidence gates | reviews 10 to 19 |
| I3 | Layout changes edit a component's single rule; no stacked override blocks | test_css_overrides_do_not_grow (ratchet) and the design lint's squeezed-text check at 390 px | review 22, M1 |
| I4 | No estimate scores a non-significant contrast; no scene number sits inside an estimate's band | test_estimates_never_score_a_null_contrast, test_estimate_scene_numbers_sit_outside_the_band | review 20 minor 2, review 22 M2 |
| I5 | No item's skill baseline is 0.9 or more; no blind strategy earns skill on average; the estimate baseline is current | test_no_item_baseline_swallows_correct_answers, test_estimate_baseline_is_current, gaming gates | review 23, M1 |
| I6 | The design rules hold on every decision's predict and reveal screen, every page, console, projector and phone, not on a sample | tests/test_design.py (every decision at 1440, one per format at 390, live pages) | review 23, minor 2 |
| I7 | Every format's reveal passes axe at both widths | test_axe_every_format_reveal | review 21, minor 1 |
| I8 | Claim wording and length do not predict truth; every path mixes true and false forecasts; keyed options carry no positional cue in stored order | wording, length and balance gates; the content script's position balancing | reviews 5, 22, 23 |
| I9 | The offline tutor answers from the decision on screen, never switches study on word overlap, and server and page agree | tests/test_tutor.py, page parity in test_browser.py | reviews 13 to 23 |
| I10 | Reviewer phrasings that once failed keep passing | REVIEW20 to REVIEW23 lists in tests/test_tutor.py | reviews 20 to 23 |
| I11 | Options are unique; a reorder never changes which text is keyed or which options exist; content scripts edit options by text, never by index | test_options_unique_and_keyed_texts_pinned (tests/keyed_options.json) | regression audit 28, B1 |
| I12 | A chart with negative values draws a zero line and losses run left; numbers use a true minus sign; printed decimals are kept | design lint R29 and R13 on every decision; `decimals` in charts | regression audit 28, M1 |
| I13 | On the hosted page (public bank, no answers), every view renders from stored records after a reload, for every format and for records saved by older versions; anything a view needs from the answers is stored on the record when it is made | test_served_views_survive_a_reload_after_every_format (fails on the old code, passes on the fix) | review 24, B1 |
| I14 | Option form carries no clue: picking the only two-part option gains at most 1.5 expected correct answers over chance across the bank | test_option_form_is_not_a_clue | review 24, minor 6 |
| I15 | A distractor is false by the item's own evidence: every new or changed option is read against the item's stored quotes, explanation and follow-ups before it ships, and the audit repeats that check | protocol step 1 (content edits) and the audit prompt's content step | regression audit 29, M1 and M2 |
| I16 | Everyday tutor questions keep their answers on every decision unless a change is reviewed and the golden file regenerated deliberately. The router is frozen: three audits in a row found a new tutor Major in each hand-tuned fix, so routing changes now ship only with the diff these batteries produce, read line by line | test_everyday_questions_keep_their_answers (18 questions × every decision) and test_wide_question_batteries_keep_their_answers (about 7,000 'what is X' and 'should we / is it' pairs from audit 29c) | regression audit 29, M3 |

## History of the protocol

- Audit 28 (the first run): found one Blocking (a duplicated option from an index-based script edit re-run after the stored order was balanced) and one Major (a signed chart drawn unsigned) before any external review; both fixed, both now invariants I11 and I12. The historical content scripts in tools/ are a record of what was done; the bank is the source of truth and the scripts are not re-run in order.

## Settled decisions (not reopened without the owner)

- The estimate skill baseline is one constant for the format: the best bank-wide average of any no-information strategy (review 23). Per-item fixed-position baselines are rejected (they reach 1 on some items).
- Contest items include findings that held up as well as ones that did not (review 23).
- Owner decisions in qa/REVIEW_PROMPT.md stand.

## Change protocol (part of every loop iteration)

1. **Name the invariants a fix touches** before making it, in the ledger entry. A new or changed option is read against the item's quotes, explanation and follow-ups before it ships (I15).
2. **Run the complete gates**, never a sample: the full test suite, which includes the design lint over every decision.
3. **Regression audit before every external review.** A fresh agent that did not make the changes receives the diff since the last reviewed snapshot and this register, and attacks only what changed: each changed rule, item or function is checked against every invariant, at both widths, on both the offline file and the hosted page, including a reload of every view after play (review 24's Blocking slipped past an audit that never reloaded the hosted page). The audit prompt is `qa/AUDIT_PROMPT.md`. Any Major it finds is fixed, a test is added to this register, and the audit repeats until it finds none. Only then does the external review run.
4. **New Majors become invariants.** Whatever a review finds that is Major gets a row here and a test, so the same class cannot return.
