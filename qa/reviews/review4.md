# Independent review 4 (2026-10-31)

Fresh agent, snapshot `snap_r4` after iteration 8. 190 tests passed; 64 browser rounds (16 decisions, all 8 formats, two widths, offline and served) with 0 errors and 0 overflow; keyboard-only path with reduced motion; axe on 21 states, 0 violations; live class with 3 phones over 6 formats; 50-student load test (p95 12.8 ms, 0 errors); server validation probes; Streamlit run; 10 fact-checks (8 correct or consistent, 1 wrong number from a working paper, working-paper follow-ups on two Dimant items).

## Score: 76 / 100

Science 11/15, learning 11/15, visual 11/15, gameplay 11/15, AI/business 8/10, content 7/10, technical 8/10, classroom 4/5, accessibility 5/5.

## Findings
- **Blocking:** none.
- **Major.**
  - M1: answers leak between items inside curated paths.
  - M2: one working-paper number (social13) and working-paper follow-ups (social15, social16).
  - M3: allocate is a disguised single choice; axe04 chart mixes units.
  - M4: any session, including abandoned ones, blocks solo play on the hosted server for up to 3 hours.
  - M5: contested, exploratory or inferred results scored as truth (bz06, social13, axf06, axe02, axe03).
  - M6: phone rank chart in a live class shows inverted numbers.
  - M7: 45 explanations lack the key number; several read as generic.
- **Minor (17).** Alternating picks beat axf04; 3-option pick-two items collapse to a coin flip; axb05 diagram narrows options; record mixes directions and leaves empty space; jargon in confidence wording; grey "?" placeholders; confidence thumb anchors at 50; projector not scaled for a room; rank by arrow taps only; re-opening a revealed decision keeps it released; the offline file carries answers (GitHub Pages); Streamlit tutor page and forecast default; two framings advise questionable practice; small number and wording drift; doc drift; CSV guard and HEAD; unverified Gemini model ids.

Disposition: `qa/LOOP_LEDGER.md`, iteration 9.
