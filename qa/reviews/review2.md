# Independent review 2 (2026-10-31)

A fresh agent reviewed a snapshot copy after iteration 6. It played in Chromium at two widths, ran the served (public) page, a live class, axe and server probes, and read the content through the ten lenses. This file reproduces its findings from the returned text.

## Score: 59 / 100

## Findings

- **Blocking.**
  - B1: on the served page, pick-two and rank crashed because the readiness check read answer fields that the public bank strips. (Already caught by the new served-page browser test and fixed before triage.)
  - B2: during a live class, a student could still get answers from `/api/reveal`, `/api/library` and the tutor for decisions the class had not reached.
- **Major.**
  - M1: the clamped forecast score was not a proper scoring rule.
  - M2: one confidence question across formats, although "right" means different things per format.
  - M3–M7: content precision (fact-check findings on rollout1, genai1, axe05, dimant-enforcers-rank, dimant-polarizednorms, bz06; author lists).
  - M4: bz07 scored a subgroup ranking the study did not separate statistically.
  - M5: rollout3 offered routes the study never compared; axe01 task text hinted at the answer.
  - M6: the expression of concern on Costello et al. was not visible to players.
  - M8: titles shown before play stated the finding.
  - M9: absolute-word strawman distractors; the correct option was often the longest.
  - M10: Dimant et al. (2025) was described three different ways.
  - M11: Streamlit solo play and tutor stayed open during a native live class; phone option order differed from the projector.
  - M12: the console rank chart drew a lower average rank as a shorter bar.
  - M13: the confidence row overflowed at 390 px; the lock hint was hidden on phones.
  - M14: Enter on an option button locked the answer instead of selecting.
  - M15: the fixed action bar covered focused elements.

Disposition: `qa/LOOP_LEDGER.md`, iteration 7.
