# Content guide

Read this before you add or change a decision.

## Evidence

- Use only peer-reviewed journal articles or scholarly books. No working papers or preprints, unless the journal version of record is cited.
- Check each source's metadata against `https://api.crossref.org/works/<DOI>`. Use the year of the version of record.
- Every number in a decision must appear in text you read. In `src/evidence.json`, store the quote and its location (page, table, figure). In the source's `verification` block, record whether you read the full text or the abstract.
- Contested findings appear only as items about the contest. Expressions of concern, retractions and failed replications go in the source record.
- Scenes describe the real design: population, task and setting. A scene can frame the study for a manager, but it never invents a firm or a rollout that did not happen.

## Writing

- Scene: at most 40 words. Question: at most 16 words. Options: at most 9 words each, plausible to a smart manager.
- `answerTitle`: the result, in at most 9 words.
- `explain`: one or two sentences with the key number.
- `implication`: one concrete managerial action.
- `boundary`: what the evidence covers (population, task, setting), stated positively.
- Three follow-ups, each answering something the screen does not already show. The gate `test_followups_add_information` fails on repeats.
- No generated filler. `tests/test_bank.py` holds the banned-phrase gate; add new offenders to it.

## Formats

Use `docs/audit/SCHEMA.md` for the fields. Use the format the evidence supports:
- Forecast for a yes/no finding.
- Estimate for one headline number.
- Rank only when every value is reported.
- Allocate only when each option has a comparable reported effect.
- Delegate for task routing grounded in measured performance.
- Causal when the lesson is about identification.

## Making a change

Write a script in `tools/` that edits `src/bank.json`, run it, then run `python src/build.py`, `python tools/make_audit_doc.py` and `python -m pytest -q`.
