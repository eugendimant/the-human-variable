# Content guide

Read this before you add or change a decision.

## Evidence

- Use only peer-reviewed journal articles or scholarly books. No working papers or preprints, unless the journal version of record is cited.
- Check each source's metadata against `https://api.crossref.org/works/<DOI>`. Use the year of the version of record.
- Every number in a decision must appear in text you read. In `src/evidence.json`, store the quote and its location (page, table, figure). In the source's `verification` block, record whether you read the full text or the abstract.
- Contested findings appear only as items about the contest. Expressions of concern, retractions and failed replications go in the source record.
- Scenes describe the real design: population, task and setting. A scene can frame the study for a manager, but it never invents a firm or a rollout that did not happen.

Where a published text is paywalled, a number may be checked in the author's pre-publication version of the same article; the evidence location says so. The source is still the published article, and no number that appears only in a pre-publication version is used.

Prof. Dimant hosts published PDFs of his papers, linked from https://eugendimant.github.io; `docs/audit/dimant_verification_2026_10_31.json` records the check of every number in the 18 Dimant decisions (92 against published texts, 3 cross-checked in a pre-publication version, none mismatched).

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
- Causal when the lesson is about identification. Before the call the diagram shows only the factors in play (the asked-about one masked); the links arrive with the reveal, because links narrow the options.

Decision ids are permanent keys. When an item changes format (for example `dimant-enforcers-rank` became a forecast), the id stays, so players' records, shared `?play=` links and class CSVs keep working.

Two decisions on one paper must not give opposing manager actions. When two papers seem to disagree, each item carries a follow-up that says how the designs differ.

## Making a change

Write a script in `tools/` that edits `src/bank.json`, run it, then run `python src/build.py`, `python tools/make_audit_doc.py` and `python -m pytest -q`.
