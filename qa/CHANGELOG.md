# Change log

## October 2026 rebuild

### Science

- **Source audit.** Every source carried over from the handover (28) was checked against its Crossref record and its published text. Corrections were logged in `docs/audit/corrections_2026-10-31.json`. One contested finding (Walasek & Stewart 2015) was quarantined. Two Dimant years were corrected: Hate Trumps Love is 2024, and the Management Science norms paper is 2025.
- **New sources.** About 70 peer-reviewed sources were added, each checked against Crossref and against the text the checking agent read. Every number has a stored quote (`src/evidence.json`). The full or abstract status is recorded and shown to players.
- **Dimant research.** 14 of Eugen Dimant's published papers are represented. Working papers are excluded by rule.
- **Replication status.** Retractions, active expressions of concern and failed replications are recorded on the source. Contested findings appear only as items about the contest: choice overload, signing first, and the Kristal correction notice. Costello et al. (2024) is included.
- **Retired items.** 29 low-value items were retired, mostly "name the concept" questions. Each has a stated reason.
- **Rewritten classics.** Framing, defaults, anchoring, prospect theory and algorithm appreciation were rewritten as predictions of measured numbers, verified on the page.
- **Follow-ups.** Templated follow-ups were replaced with three grounded, specific questions per decision. A gate test blocks repeats.

### Gameplay and learning

- **Eight formats:** choice, causal (with a diagram), pick two, estimate, forecast (Brier skill), rank (with ties), allocate (payoff under reported effects) and delegate.
- **Multi-step cases:** "Rolling out an AI assistant" (4 steps) and "Generative AI in your content team" (3 steps).
- **Structure:** eight curated paths, a Library of ten principles with their evidence, and a "continue where you left off" prompt.
- **Feedback:** confidence is required before locking, a calibration plot and Brier score sit on the record, and the round summary shows the best call and the biggest surprise.
- **Anti-gaming:** a midpoint estimate or a 50% forecast now scores near zero, and rank and allocate must be touched before they can be locked.

### Design

- **Visual system:** blue for the player's call, amber for the evidence. Faces are Schibsted Grotesk and Newsreader, embedded and licensed OFL, so the game works offline. There are no all-caps eyebrows.
- **Focus mode:** one decision per screen with a fixed action bar. The reveal shows the verdict, a gap figure, the finding and one manager action; deeper material sits in tabs.
- **Home page:** a live first prediction and paths, with custom rounds behind a link.
- **Motion:** the evidence marker glides from the player's position to the result. Motion is disabled under reduced-motion settings.

### Classroom

- **Server:** a new standard-library server with SQLite in WAL mode and versioned in-memory state.
- **Instructor console:** QR code, decision picker, live count, close and reveal, per-format class charts, CSV export, and end-and-delete.
- **Phones:** a room mode that uses the same option order as the projector, with the evidence held until reveal.
- **Answer protection:** served pages carry no answers.
- **Security:** hashed tokens, rate limits that work behind campus NAT, a join-flood limit, a passcode required on public hosts, the right-most `X-Forwarded-For`, CSP, and 48-hour retention with a background purge.

### Tutor

- **Answer order:** three curated follow-ups per decision; presets that never call the model; then cache, Gemini, and finally a curated fallback.
- **Grounding:** retrieval over the checked bank, and an enforced citation check.
- **Budgets:** global per-minute and per-day caps, a per-student daily cap, a concurrency cap, cooldowns on 429, and shutdown on daily quota.
- **Privacy:** documented, including Gemini free-tier terms.

### Deployment

- **Streamlit:** a multipage app with the embedded game, a native live class and a native tutor.
- **Container:** a Dockerfile plus Render and Fly configurations.
- **Static:** GitHub Pages works for the offline game.

### Engineering and tests

- **Source split:** `src/` holds the CSS, JS, scoring, shell and content; `src/build.py` builds the page and checks freshness with `--check`.
- **171 automated checks:**
  - Content gates, including banned phrases, word limits and follow-up repeats.
  - JS/Python scoring parity.
  - Classroom store.
  - Tutor budgets and grounding.
  - HTTP integration and a 50-client load test.
  - Answer-leak tests.
  - Playwright tests at 1440 and 390 px covering every format, keyboard play, axe (no serious violations), reduced motion and a three-phone live class.
