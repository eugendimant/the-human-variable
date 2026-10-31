# Claude implementation handover

## Start here
1. Run `python -m unittest discover -s tests -v`. Open `index.html` in a real browser and inspect desktop/mobile.
2. `src/bank.json` is the editable content. `python src/build.py` embeds it in `index.html`. Avoid editing embedded JSON by hand.
3. Preserve all existing gameplay, scoring, field notes, curated questions, atlas, and local cohort export.
4. Do not claim that the tutor is connected to Gemini. It is not. Do not claim that classroom sessions are real-time. They are not.

## Top priorities
P0: Independently check every DOI and each claim against the actual published paper. Flag any abstract-only verification. Record precise study conditions, samples, effect sizes, and uncertainties.
P0: Run browser automation and inspect actual screenshots at 375, 768, 1440 widths, including numeric, multi-select, result and modal states.
P0: Audit keyboard navigation, focus trapping in modal, screen readers, contrast, reduced motion, data retention, and scoring.
P1: Extract JS and CSS from single HTML into maintainable components with a repeatable build. Add real browser integration tests.
P1: Build differentiated simulations, sequential decisions, and prediction revision without inventing empirical outcomes.
P1: Add a properly secured server-side Gemini proxy with quota control, caching, rate limits, retrieval grounding and offline fallback. Never expose a key to browser code.
P1: Build real instructor session persistence, aggregation and anonymized results if live multiuser classroom use is desired. Local JSON aggregation is not real-time.
P2: Human-test with 5+ MBA students and 2 instructors. Collect task completion, comprehension, willingness to continue, and qualitative critiques.

## Quality gate
Use the 100-point rubric supplied in the user's master prompt. No 95/100 claim without concrete evidence. Simulated reviewers are not independent humans. Log each substantive change with before/after evidence and test result. Do not inflate iteration counts.

## Visual direction
Premium editorial, not generic cards. Distinctive typographic hierarchy, restrained palette, clear chart semantics, progressive disclosure. Remove unnecessary text and decorative UI. Respect mobile and reduced motion.

## Delivery
Produce an audited source repository, working static build, Streamlit option, browser tests, source-by-source audit, screenshots, documented limitations, and a verified ZIP. Include exact GitHub Pages and Streamlit Cloud steps.
