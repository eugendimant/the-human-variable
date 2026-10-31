# Independent review 7 (2026-10-31)

Fresh agent, snapshot `snap_r7` after iteration 11. 200 tests passed; 72 decisions played (offline and served, two widths) with 0 errors and 0 overflow; live class with 3 phones (rank, allocate, delegate, choice) and leak probes on every route; lock test; 50-student load (p95 12 ms); tutor probes; Streamlit with and without passcode; axe on 34 states, 0 violations; 11 fact-checks (no wrong number confirmed; several unverified).

## Score: 79 / 100
Science 12/15, learning 11/15, visual 11/15, gameplay 12/15, AI/business 9/10, content 7/10, technical 8/10, classroom 4/5, accessibility 5/5.

## Findings
- **Blocking:** none.
- **Major.** M1 axe04's `best` and `valueName` reach the served page, `/api/challenges` and room state; M2 both allocate items test common sense, not prediction; M3 34 decisions rest on paraphrased or summarized evidence entries rather than verbatim quotes; M4 the "Measure before you scale" path is solvable with a "debunk" heuristic; M5 scenes, titles and strawman options still give answers away (social20, biz07, bz06, ai11, misperceived-norms-action, biz02, social07, social13).
- **Minor (13).** axb01 count; internal notes in study lines; cross-item leaks in theme decks and custom rounds; ungrounded forecasting principle; scope lines phrased as gaps (gate too weak); tutor declines on-topic free questions; confidence has no stake; allocate reveal colours; chart legend on counterfactual bars; titles before play; Streamlit double navigation, open class creation without passcode, non-constant-time compare; "Try again" during a lock; enforcers cell contrast unverified.
- **Optional (premium look).** Signature reveal moment, two-line answer titles, theme illustrations at scale, one dark and one warm band, research band with figure thumbnails, dark mode, record narrative, compact phone path list.

Disposition: `qa/LOOP_LEDGER.md`, iteration 12.
