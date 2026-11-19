# The Human Variable rubric v1 (frozen 2026-11-17)

This sheet is frozen. Reviewers score against it as written. A change to any line needs Eugen's OK and a new version number. Scores from different versions are never compared. It replaces the open category maxima in `qa/REVIEW_PROMPT.md` (science 15, learning 15 and so on) for every review from round 1 of this protocol on.

## What the game is for

**Audience:** MBA students, graduate students and executives. They play alone or in a live class run from the instructor console and a projector.

**Purpose:** a player commits to a call about a published study, says how sure they are, then sees the evidence on the same axis as their call. They should leave able to say what a manager does with the finding, and with a record of how well their confidence matched their hits.

## Hard gates

A build that fails any of these is not scored.

| # | Gate | How it is checked |
|---|---|---|
| G1 | `tools/gates.sh NN` passes: the build check, design lint by rule and the full pytest suite, Playwright and axe included | its log files |
| G2 | `python src/build.py --check` reports the built pages are current | output |
| G3 | The served page and every API give no answer, no paper title joined to its decision, and no DOI before the reveal, while a class is open or closed | the existing leak tests plus a probe of the seeded holdout decisions |
| G4 | Offline `index.html` plays every format with 0 console errors | browser drive |
| G5 | Scoring parity, JS against Python, on all decisions | pytest |
| G6 | No secrets in the repo or the served page. The server's hardening (CSP, rate limits, body cap) is unchanged or stronger. | grep plus the server tests |
| G7 | The owner decisions in `qa/REVIEW_PROMPT.md` ("OWNER DECISIONS YOU MUST NOT FLAG") and in OWNER_DECISIONS.md are respected | reviewer read |

## Scored criteria (100 points)

There are 20 criteria at 5 points each, each one PASS or FAIL with evidence: a screenshot id, a test name, a decision id or a measured number.

**Defect rule:** any Major against a criterion fails it, and so do three or more Minors. A Minor that names no criterion is logged and costs nothing.

**Severity:**
- **Major:** a player would learn something false, get stuck, lose their record, or see the answer before the call.
- **Minor:** a player would hesitate or notice a flaw but carry on.

### A. Learning (the purpose)

| # | Criterion | Pass when |
|---|---|---|
| A1 | Commit before the evidence | Nothing on a predict screen, in the page source or in an API response lets a player infer the answer. This includes option cues (see B2). |
| A2 | The reveal teaches | Every reveal puts the player's call and the evidence on one axis, states the finding in one sentence, and gives a "For a manager" action that follows from the finding. Checked on all formats in the board plus the holdout. |
| A3 | Honest calibration | The record headline is skill above guessing. Confidence and hits are shown so a player can tell over-confidence from under-confidence. Numbers on the record match the calls listed. |
| A4 | The tutor answers the question asked | On the fixed regression set in OWNER_DECISIONS.md, the tutor without a key answers directly, or says plainly that the stored text does not say, at the rate set there. It gives 0 wrong answers. Restating the finding in place of an answer counts as not direct. |

### B. Science and content

| # | Criterion | Pass when |
|---|---|---|
| B1 | Verbatim and exact | On 8 decisions (4 fixed, 4 from the holdout), every quote matches the source and every number matches the paper. The PDF is read where the repo holds it. |
| B2 | No option cues | On 20 decisions drawn by seed, a reviewer who reads only the options, without the scene, picks the right one no more often than chance plus 2. |
| B3 | Claims stay inside the source | No explanation says more than its stored quotes (the review 57 m-9 class of defect). No non-significant contrast is treated as a finding. |
| B4 | Every decision reads cleanly | Each scene, question and option on the sample reads once without re-reading: one point per sentence, plain words, no stranded words. |

### C. Gameplay and logic

| # | Criterion | Pass when |
|---|---|---|
| C1 | Every format plays | All 8 formats complete at 1440x900, 1920x1080, 1280x720, 1366x768 and 390x844 with 0 errors. |
| C2 | Scoring is right and visible | Proper scoring rules, parity holds, and the score shown on a reveal matches the rule for that format, ties and caps included. |
| C3 | First contact is clear | On the outsider procedure, a first-time player knows what to do on each format's predict screen within 10 seconds, without help. |
| C4 | No contradictions | No screen says something another screen contradicts, such as "Unsure" at 50 per cent (see OWNER_DECISIONS.md). |

### D. Visual craft and premium feel

| # | Criterion | Pass when |
|---|---|---|
| D1 | Balanced reveals | On causal and pick-two reveals at 1440 and 1920, both columns end within 40 px of each other. No empty block over 120 px sits inside the content area (review 57 m-1). |
| D2 | Predict screens fill the space | At 1920x1080 and 1280x720 the question block is anchored to the top third, with no more than 120 px empty above it (review 57, change 3). |
| D3 | Finish | Design lint clean, 0 stranded words with the R34 detector extended to the reviewers' cases, and type and spacing on the published scale. |
| D4 | It looks like one product | Across the 8 formats in the board, a reviewer finds no screen that looks like a different app: same type, colours, spacing and chart grammar. |

### E. Classroom and access

| # | Criterion | Pass when |
|---|---|---|
| E1 | The live class holds | 120 simulated joins, a dropped link, the closed phase and an instructor lock all behave, with no leak. |
| E2 | A projector built for a room | At 1920x1080 the body text is at least 24 px and the card fills the width with no dark band over 15 per cent. At 1280x720 every text is at least 16 px. |
| E3 | Accessible | axe shows 0 violations on every board scan. A full play works by keyboard alone. The smallest text is at least 13 px. |
| E4 | Technical health | pytest passes, the build is current, there are 0 console errors over 110 file plays and 110 served plays, and the server tests pass. |

## Pass bar

The Human Variable counts as 95+ only when all of these hold:
1. Both blind reviewers score 95 or more on this version: at most one FAIL each, and never in section A.
2. No Major is open.
3. Eugen passes the owner board (REVIEW_PROTOCOL.md, step 9).
