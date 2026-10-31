# The study tutor

Students can open three predefined follow-up questions on every decision (curated, no AI), and they can ask their own questions. The tutor is built so that it never breaks the game and never makes up facts.

## Answer order, cheapest first

1. **Presets:** the three suggested questions ("How big is this effect in practice?" and the others) are answered from curated text and never call the model.
2. **Cache:** the question is normalised (lowercase, stop words removed, tokens sorted), keyed with the decision id, and stored in SQLite. Repeated questions in a class cost nothing.
3. **Gemini:** used only when a key is configured, every budget allows the call, and a concurrency slot frees up within `GEMINI_QUEUE_WAIT` seconds.
4. **Curated fallback:** BM25 retrieval over the checked bank. The fallback is labelled with a short note such as "The AI tutor is busy" or "You have used today's AI questions", so students know where the answer came from.

## Grounding and safety

- The model sees only the six highest-ranked records from the lab's verified bank. The decision on screen and its source always come first.
- The system instruction treats records and the question as data. The question is wrapped in delimiters and labelled untrusted.
- The model must return JSON with `answer` and `cited_ids`. An answer that cites nothing, or cites anything outside the retrieved records, is discarded and the curated answer is shown instead. Citations shown to students are built from the lab's source records, never from model text.
- Safety thresholds are set explicitly to block medium-and-above harassment, hate, sexual and dangerous content. Since Gemini 2.5 the API default is off.
- Output is capped at 1,500 characters and escaped before display. Answers are limited to about 110 words.

## Budgets for 30 to 50 students on a free key

| Control | Default | Variable |
|---|---|---|
| Global requests per minute | 12 | `GEMINI_RPM` |
| Global requests per day | 900 | `GEMINI_RPD` |
| AI questions per student per day | 15 | `TUTOR_PER_CLIENT_DAY` |
| Concurrent model calls | 4 | `GEMINI_CONCURRENCY` |
| Wait for a free slot | 6 s | `GEMINI_QUEUE_WAIT` |
| Model timeout | 12 s | `GEMINI_TIMEOUT` |
| Models tried in order | `gemini-3.1-flash-lite,gemini-3.5-flash-lite` | `GEMINI_MODELS` |

Google no longer publishes per-model free-tier numbers. Check your project's limits in AI Studio and set `GEMINI_RPM` and `GEMINI_RPD` slightly below them.

In a class of 30 where each student asks three questions over ten minutes, the load is about 9 requests per minute before caching, which fits a 12-RPM budget. During bursts the extra questions get curated answers immediately; the test `test_global_rpm_cap_thirty_students` shows 10 model answers and 20 labelled curated answers, with no failures.

Error handling follows Google's guidance:
- A 429 rate limit triggers a 30-second cooldown.
- A 429 daily quota closes the tutor for an hour; the quota itself resets at midnight Pacific.
- A 500, 503 or timeout moves to the next model.
- A 400, 401, 403 or 404 means the configuration is wrong; the tutor stops calling rather than hammering the API.

## Privacy

- The tutor sends only the question text and the retrieved lab records. It sends no names, codes or tokens.
- Under Google's terms, content sent to the **unpaid** Gemini API may be used to improve Google products and may be read by human reviewers. Google asks that no personal or confidential information be submitted.
- Unpaid services may not be used to serve users in the EEA, Switzerland or the UK. For those classes, use a billing-enabled (paid) project.
- Users must be 18 or older.

Sources: Google AI for Developers, Gemini API docs (generate-content, rate limits, api-errors, safety settings, terms), retrieved 31 October 2026.

## Not tested here

This environment has no Gemini key, so no live call was made. The request and response shapes follow the published `generateContent` reference. They are tested with a simulated transport for success, ungrounded output, rate limits, daily quota, configuration errors and concurrency. Google now recommends its Interactions API for new projects; `generateContent` remains supported.
