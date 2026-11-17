# The Human Variable review protocol v1 (blind, two reviewers)

Fifty-seven reviews rose to 88 (review 30), then settled at 79 to 83. The product kept improving. The scoring did not hold still, for these reasons:
- There were open category maxima with no anchors.
- Reviewers read earlier reviews and the score table ("Calibration against review 51").
- The reviewer changed from Fable 5.2 to Sonnet 5.5 at review 42.
- The prompt was rebuilt each round.
- Five caps waited on owner choices.

This protocol fixes each of those. It replaces `qa/REVIEW_PROMPT.md` for scoring. Keep that file's "OWNER DECISIONS YOU MUST NOT FLAG" paragraph and give it to reviewers as data.

## Steps

1. **Freeze.** Record the commit, the iteration, the rubric (v1) and the owner decisions in `qa/path-to-95/rounds/ROUND_n.md`.
2. **Shoot the fixed board** with `tools/screenshots.py` (extend it as needed). Capture these states at 1440x900, 1920x1080, 1280x720 and 390x844:
   - home
   - library
   - one predict screen and one reveal for each of the 8 formats, using decisions fixed in round 0
   - record with 12 calls
   - record empty
   - live class: instructor console, a phone joined, projector open, projector reveal
3. **Seeded holdout.** Draw 8 more decisions by a seed chosen at review time and written in the round file. Shoot their predict and reveal at 1440x900 and 1280x720. Use 4 of them for B1 and all 8 for G3. Draw the 20 B2 decisions with the same seed.
4. **Machine evidence.** Collect:
   - `tools/gates.sh` logs
   - build check
   - axe output
   - the 110 file plays and 110 served plays, with console errors
   - the 120-join class run
   - the leak probes
   - the tutor regression results
   - the stranded-word and column-balance measurements
5. **Calibrate once per reviewer setup.** Plant 6 defects in a copy, one each against A1, A2, B3, C2, D1 and E2. A reviewer who finds fewer than five is replaced.
6. **Score blind.** Two reviewers work independently, each with only:
   - RUBRIC_v1.md and OWNER_DECISIONS.md
   - the REVIEW_PROMPT owner-decisions paragraph
   - the built pages and the server
   - the board and the holdout
   - the machine evidence

   They never see earlier reviews, scores, the ledger, the changelog or builder claims. Use procedures, not personas: each reviewer does the outsider first-contact pass, the keyboard play, the projector check and the fact-check of B1. Pin and record each reviewer's model and effort, and keep them the same every round. Use two model families if the setup allows. If not, use two different pinned Claude models.
7. **Reconcile.** Each criterion gets PASS or FAIL, with evidence and severity. When the two disagree, a third reviewer scores that criterion only. Majority wins, and scores are never averaged.
8. **Fix only what failed.** The builder gets the failed criteria and their evidence, never the score. The full board and evidence rerun after each fix round. Content changes go through a dated script in `tools/`, as before.
9. **Owner board.** When both reviewers reach 95, Eugen looks at home, one predict screen, the estimate reveal and the causal reveal at 1440, the record, and the projector reveal at 1920. He answers one question per screen: "Would I put this in front of an executive class without apologising?" A no fails a D criterion, with his words as the evidence.
10. **Report and stop.** Nothing merges to `master`, nothing goes to `gh-pages`, and `tools/deliver.sh` is not run until Eugen has seen the round file and the owner board and said yes.
