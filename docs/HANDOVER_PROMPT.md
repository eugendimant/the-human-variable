# Handover prompt: The Human Variable

Paste everything below into the new project. It is written for a Claude session that has not seen the earlier work.

## 1. What this is

"The Human Variable" is a predict-then-reveal decision game on behavioral science, AI and business. The players are MBA students, graduate students and executives. Original concept: Dr. Eugen Dimant, University of Pennsylvania (eugendimant.github.io, edimant@sas.upenn.edu).

A round works in three steps. The player reads a situation from a published study. The player commits to an answer and says how sure they are. The reveal shows the published result, the distance to it, and one action for a manager.

State on 2026-11-12: 116 decisions from 113 peer-reviewed sources, 8 paths, 21 decisions on 18 papers with Eugen Dimant as an author. Check `README.md` in the repo for the current counts.

## 2. Where everything is

| What | Where |
|---|---|
| Source code (public, MIT) | https://github.com/eugendimant/the-human-variable, branch `master` |
| Built game for GitHub Pages | same repo, branch `gh-pages` (only `index.html`, `LICENSE`, `.nojekyll`) |
| Pages address | https://eugendimant.github.io/the-human-variable/ (works only after Pages is switched on, see section 8) |
| Playable artifact on claude.ai | https://claude.ai/artifact/XihgedtB22cjua4AaqgaXs (private until Eugen shares it) |
| Copy on Eugen's laptop | `Z:\Dropbox\Privat\Unterlagen\Universität\Promotion\Forschung\Claude Cowork\5 Tools\The Human Variable` (`source\`, a git bundle, the latest zip, `README.md`, `!DELETE ME\`) |
| Eugen's own published papers (PDF) | `Z:\Dropbox\Privat\Unterlagen\Universität\Promotion\Forschung\#Own Paper\Published` (48 files) |

Start by cloning the repo. Then read, in this order: `docs/HANDOVER_FOR_CLAUDE.md`, `docs/LEARNINGS.md`, `qa/LOOP_LEDGER.md` (last three entries), `qa/reviews/review41.md`, `qa/DESIGN_RULES.md`.

## 3. How the code is organised

- `src/bank.json`: decisions, sources, paths, themes, tutor routes. `src/evidence.json`: the verbatim quotes behind every number.
- `src/app.js`, `src/app.css`, `src/shell.html`: the game. `src/classroom.js`, `src/classroom.css`: the instructor and projector pages.
- `src/build.py` builds `index.html` and `classroom.html`. Run it after every change. `python3 src/build.py --check` proves the built pages are current.
- `server/`: classroom server (`app.py`, `classroom.py`) and the tutor (`tutor.py`). The offline tutor exists twice, in `server/tutor.py` and in `src/app.js`. Both must give the same answer. Do not use regex lookbehind in the page code.
- `tools/`: one idempotent script per content change. `tests/`: about 390 tests. `qa/`: reviews, ledger, design rules, DOI check.

## 4. Rules that must hold

1. **Content changes only through a new idempotent script in `tools/`.** Never loop over the old `tools/content_review*.py` scripts. The early ones are not safe to rerun. If the tutor routes change, rerun only `tools/tutor_routes_2026_10_31.py`.
2. **Zero fabrication.** Every number in a scene, explanation, answer title or follow-up needs a verbatim quote in `src/evidence.json`, read in the published article. Peer-reviewed sources only. If a paper is paywalled, find the published text another way (Eugen's folder, an author copy of the version of record).
3. **Keyed options are pinned by hand** in `tests/keyed_options.json`. A script that touches options must update that file explicitly.
4. **RULE 0.** Never downplay Eugen Dimant's contribution and never weaken a Dimant item. No sentence says what a design "cannot" show.
5. **RULE G.** A fix is global. Add a detector (a test) that fires on an injected case, so the defect class stays closed.
6. **No leak before the call.** Scene, question and options must not give the answer or the mechanism away. Paper titles stay hidden on decision screens until the player has answered. The "Research by Eugen Dimant" band on the landing page shows the real titles on purpose (owner's decision, 2026-11-12).
7. **Design.** No AI design markers (see `qa/DESIGN_RULES.md` and `tools/design_lint.py`, 30 rules). Ask "what would Tufte do?" on every page. Headings fill their lines (`text-wrap: pretty`, never `balance`, lint R19). The CSS duplicate-selector cap is 40 (`test_css_overrides_do_not_grow`).
8. **Secrets.** The Gemini key stays server-side. Never commit SQLite data or keys.
9. **Never edit files while a gate runs.** I broke this once in the last session and had to rerun.
10. **Writing to Eugen.** Simplified Technical English: active voice, short sentences, one idea per sentence, no em-dashes. Precision over politeness. He wants decisions made, not questions asked.

## 5. The gates (all must pass before delivery)

```
python3 src/build.py && python3 src/build.py --check
python3 tools/sync_doc_counts.py
python3 tools/make_audit_doc.py
python3 tools/tutor_golden.py        # then read the diff of tests/tutor_golden*.json by class
python3 tools/verify_dois.py         # every DOI resolves and its Crossref title matches (114 of 114 on 2026-11-12)
python3 tools/design_lint.py         # must end with: by rule: {}
python -m pytest -q                  # about 19 minutes
```

## 6. The iteration protocol

1. Fix. 2. Run all gates. 3. Commit and push `master`. 4. Send a snapshot (`git archive`) to a fresh, independent reviewer agent that has not seen the work. The prompt template is in `qa/reviews/` history: nine categories, score out of 100, Blocking/Major/Minor counts, plus an "Introduced" section that audits the changes since the last review. 5. Record the review in `qa/reviews/reviewNN.md`, add a row to `qa/QUALITY_ASSESSMENT.md` and an entry to `qa/LOOP_LEDGER.md`. 6. Deliver: push `master`; copy `index.html`, `LICENSE`, `.nojekyll` to `gh-pages` and force-push; republish the artifact to the same URL (pass the URL, or a second artifact appears); write the zip and the bundle to the laptop folder, unzip into `source\`, move the old zip to `!DELETE ME\`, update that folder's `README.md`.

Target: an independent reviewer scores 95 or more. The loop continues while a review finds two or more Blocking or Major issues.

## 7. Where the quality stands

Independent reviews 36 to 41 scored 86, 86, 85, 85, 84, 84. Category scores in review 41: Science 13/15, Learning 13/15, Visual 11/15, Gameplay 13/15, AI/business 9/10, Content 8/10, Technical 8/10, Classroom 4/5, Accessibility 5/5.

What I learned about the plateau:
- Visual has stayed at 11 to 12 of 15. Small fixes did not move it.
- Several fix rounds introduced new defects that the next review found. Rewritten scenes need the same checks as explanations. Layout tests must run with a record present, not only on a fresh profile.
- Eugen's direct feedback moved the product more than reviewer rounds did. Ask him for screenshots of what bothers him.

Iteration 66 (2026-11-12) has not been reviewed yet. It contains:
- A new landing page: what the game is, how a round works, a sample decision, then the paths. Credit with name, website and email on the landing page, the footer and the research standard.
- The question screen scales up on large screens (`fitQuestion()` in `src/app.js`, CSS `zoom`), and scenes and options break without stranded words.
- Claims are answered True or False plus "how sure" from 50% to 100%. The stored answer is still the probability that the claim is true.
- The tutor panel offers up to seven suggested questions, each checked against the offline tutor.
- "Research by Eugen Dimant" lists every paper under its published title, with a DOI link. Every reveal links to the study.
- Four new decisions from Eugen's own folder: `repro-msci-estimate` (Fišar et al. 2024), `dimant-competition-choice` (Huber et al. 2023), `dimant-megastudy-estimate` (Duckworth et al. 2025), `dimant-deterrence-choice` (Buckenmaier, Dimant, Posten & Schmidt 2021).

## 8. Open items

Waiting for Eugen:
- **GitHub Pages is not switched on.** One command: `gh api -X POST repos/eugendimant/the-human-variable/pages -f "source[branch]=gh-pages" -f "source[path]=/"`. Or Settings → Pages → branch `gh-pages`.
- **Live classroom online.** GitHub Pages and Streamlit cannot run it. The repo has `render.yaml` and `fly.toml`; `docs/DEPLOYMENT.md` has the steps. On his laptop: `python start_classroom.py`.
- A duplicate private artifact exists from a publishing mistake (https://claude.ai/artifact/5KzV7wQT75Sazmbfi2fZnd). Delete it if he agrees.

Open from review 41:
- Projector text is 11 to 12 px at 1280x720.
- The three-step block on the landing page reads as a template.
- biz01 quotes its 86% and 37% through a secondary source. Read Madrian & Shea (2001) and quote it directly.
- The minus sign on the record headline touches the digit.
- The tutor misses some everyday questions ("Was it a field experiment?").
- On choice items, the two-part option is keyed too often.
- Four fact-checks the reviewer could not finish because pages were blocked: the dimant-hate-choice percentages, the masks sample size, Centola, Goldstein.

More material in Eugen's folder that is not yet in the game: Gelfand et al. (2022, mask-wearing tournament; overlaps with the existing mask decision), Dimant, Reinhardt & Sambanis (2026, identity and fairness), Buckenmaier, Dimant & Mittone (2018, tax evasion), Romaniuc et al. (2021), Charness, Dimant, Gneezy & Krupka (2025, norm measurement), and the `WP` folder (working papers: not allowed as sources until published).

## 9. Next steps, in order

1. **Confirm the state.** Clone the repo. Run every gate in section 5. If the last commit on `master` says "gates running at commit time", the full run for iteration 66 may not have been recorded: run it and fix what fails before anything else.
2. **Deliver iteration 66** if the laptop folder, the artifact and `gh-pages` are behind `master` (compare the commit in the folder's `README.md` with `git log -1`).
3. **Review 42.** Run the independent review in section 10 on a snapshot of `master`. Iteration 66 changed a lot, so the "Introduced" audit matters most: the True/False input, the scaled question screen at 1280x720, 1440x900 and 1920x1080, the tutor suggestions, the four new decisions, and the landing page.
4. **Fix by rank.** Blocking first, then Major, then the Minors that touch the most screens. Add a detector test for each defect class.
5. **Raise Visual above 12 of 15.** This is the largest gap. Work on one screen at a time, in this order: the reveal page (empty right column on about a third of wide reveals, repeated headline number on estimate reveals), the projector at 1280x720 (text below 13 px), the record page. Show Eugen before and after screenshots and ask what still bothers him. Do not start a second layout change before the first is reviewed.
6. **Close the open content items** in section 8: biz01 direct quote, the four unfinished fact-checks, the two-part option cue on choice items, the tutor misses.
7. **More of Eugen's papers.** Read the remaining candidates in section 8 in full and add a decision only where the paper reports an experiment with a clear, quotable result.
8. **Repeat** steps 3 to 6 until a review scores 95 or more.

## 10. How to evaluate

**Who reviews.** A fresh agent that has not seen the work, on a `git archive` snapshot in a scratch folder. It must not read the working tree. It is adversarial and has no stake in a high score.

**What it does.**
- Runs the test suite, the design lint and an accessibility scan (axe) on the snapshot.
- Plays at least 20 decisions across all eight formats at 390x844, 820x1100, 1280x720, 1440x900 and 1920x1080, fresh and with a record present. It takes screenshots and looks at them.
- Runs one live class with an instructor page, a projector and at least three phones, including a dropped connection and a closed phase.
- Asks the tutor at least 60 natural questions and checks that the page and the server give the same answer.
- Fact-checks at least 10 decisions against the published papers, including 3 Dimant items and all decisions added since the last review.
- Checks every decision for a leak of the answer before the call.

**How it scores.** Nine categories, 100 points: Science 15, Learning 15, Visual 15, Gameplay 15, AI and business relevance 10, Content 10, Technical 10, Classroom 5, Accessibility 5. It lists each finding as Blocking, Major, Minor or Optional, with the evidence it observed (file and line, a measurement, or a screenshot). A separate "Introduced" section lists defects caused by the changes since the last review. It also lists what it could not verify.

**What counts as done.** A score of 95 or more, zero Blocking and zero Major, from a reviewer that did all of the above. A score from a reviewer that skipped a part does not count. Never tell Eugen a score that a reviewer did not give, and always say which iteration the score is for.

**Your own checks before each review.** Measure, do not eyeball: empty space in px on wide reveals, smallest text size on the projector, the share of tutor questions answered. State the numbers in the ledger so the next round can compare.
