# Independent review 3 (2026-10-31)

Fresh agent, snapshot copy after iteration 7 (`snap_r3`). 178 tests passed; 56 browser rounds (14 decisions × 2 widths × offline and served) with 0 errors; live class with 3 phones; axe on 19 states (1 moderate); load test with 50 students (p95 14.5 ms, 0 errors); Streamlit run; 9 fact-checks (all correct or consistent; one Dimant item's percentages could not be fetched).

## Score: 70 / 100

| Category | Score |
|---|---|
| Science | 11/15 |
| Learning | 10/15 |
| Visual | 10/15 |
| Gameplay | 11/15 |
| AI/business | 8/10 |
| Content | 7/10 |
| Technical | 6/10 |
| Classroom | 3/5 |
| Accessibility | 4/5 |

## Findings

- **Blocking.** B1: served page carries answers through `sources[*].takeaway` (14 of 27 estimate targets verbatim).
- **Major.**
  - M1: causal diagram alt text and masked node label reach the page before lock.
  - M2: projector lists rank options in answer order; answer indices skewed to 0/1 in bank order.
  - M3: Streamlit tutor crashes during a class lock (`exclude` passed as a set).
  - M4: with a Gemini key, source records and the cache bypass the class lock.
  - M5: a midpoint guess scores 100 on 6 of 27 estimates.
  - M6: allocate payoff is linear, so the format teaches "go all in"; axe04 wording invites a proportional split; axb08 is a disguised single choice.
  - M7: rank reveal draws ties as a strict order; some titles overclaim.
- **Minor.** 12 px overflow at 390 px before confidence is touched; unit wording in captions; chart colours vs legend; 16 negative boundaries; record mixes measures; forecast reveal omits the claim; orphan path card and empty Record space; remaining weak distractors; title hints and cross-item leaks; content details (enforcers implication, axe06 tolerance, genai2, axe04 test); tutor label without a key; tutor IP limit throttles free presets; class lock edge cases; Streamlit double nav and offline answer file; doc drift; Library filter labels and heading order.
- **Optional.** Constant-time passcode comparison; a signature visual per theme; dark mode.

Disposition: `qa/LOOP_LEDGER.md`, iteration 8.
