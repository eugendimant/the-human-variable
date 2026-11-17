# Handover prompt: take The Human Variable to 95+

Paste everything below the line into Claude Code (or Cowork) on a machine that can run a browser. It is self-contained.

---

You are taking The Human Variable, Eugen Dimant's decision lab on behavioural science, AI and business for MBA students and executives, from a stalled score of about 81 to 95+. The score is measured on a frozen rubric by blind reviewers.

The diagnosis is already done. The plateau came from how the game was scored, not from the product:
- The rubric had no anchors.
- Reviewers anchored on earlier scores.
- The reviewer model changed at review 42.
- The prompt drifted.
- Five caps waited on owner choices.

Do not add features. Fix what the rubric fails.

## Setup

1. Clone `eugendimant/the-human-variable` and check out `claude/thv-path-to-95`. Make your own working branch from it.
2. Install the dependencies:
   - `pip install -r requirements.txt pytest playwright`
   - `python -m playwright install chromium`

   If you cannot run a browser, stop and say so.
3. Baseline: run `python src/build.py --check` and `tools/gates.sh 91`. It writes its logs to `/tmp/claude-0`, so create that folder first. On Windows without WSL, run its three commands by hand. Record the results.

## Read first, in this order

1. `qa/path-to-95/RUBRIC_v1.md`: 7 hard gates and 20 pass/fail criteria in five sections. It is frozen. Never edit it. If a criterion seems wrong, note why and ask Eugen.
2. `qa/path-to-95/OWNER_DECISIONS.md`: five defaults for the long-standing caps. Work to them unless Eugen overrules one.
3. `qa/path-to-95/REVIEW_PROTOCOL.md`: the board, the holdout, calibration, the blind review and the owner board.
4. The "OWNER DECISIONS YOU MUST NOT FLAG" paragraph in `qa/REVIEW_PROMPT.md`, and `docs/CONTENT_GUIDE.md` for content rules.
5. `qa/reviews/review57.md`, section "What is still missing for 95". Read it as a list of known gaps only. Its score does not count.

## The work

1. **Round 0.**
   - Build the tutor regression set as OWNER_DECISIONS.md, item 1, says, and freeze it.
   - Shoot the board.
   - Score the current build yourself against RUBRIC_v1.
   - Save it as `qa/path-to-95/rounds/ROUND_0.md`.
   - Regenerate `docs/screenshots`, which still show the Scope and Source tabs that iteration 88 removed.
2. **Fix the failed criteria**, starting with section A, then D1, D2, E2, B2 and C4.
   - Write a test for each criterion before you change code: column balance, top-third anchoring, projector sizes, the options-only test, the tutor rate.
   - Make content changes only through a dated script in `tools/`.
   - After each fix round, run the gates and reshoot the board. Look at every screenshot yourself.
3. **Blind review** once your own score is 95, exactly as REVIEW_PROTOCOL.md says:
   - Calibrate first.
   - Use two pinned reviewers who see only the rubric pack and the evidence.
   - Settle each disagreement with a third reviewer on that criterion.
   - Fix only failed criteria and repeat.
4. **Stop at the bar.** The bar is both reviewers at 95 or more, no FAIL in section A and no open Major. Then prepare the owner board.

## Rules that do not bend

- Nothing merges to `master`, nothing is pushed to `gh-pages`, and `tools/deliver.sh` is not run until Eugen says yes. Push to your branch and open a draft pull request. That is where you stop.
- Quotes stay verbatim. Numbers come from the paper. Explanations never say more than the stored quotes. Working papers stay excluded.
- Keep the owner decisions in REVIEW_PROMPT.md: the home page opens on one decision, headings wrap greedily, and the question is on the left with the answer on the right from 1200 px.
- No secrets in the repo. The server's hardening stays as strong or stronger.
- Do not contact anyone and do not post anything publicly.

## What to report to Eugen

Report in at most six lines:
- each reviewer's score and model
- the remaining FAILs
- the draft PR link
- the six owner-board screens
- any owner default he should look at
- one question: "Should I merge and publish this to the live game?"
