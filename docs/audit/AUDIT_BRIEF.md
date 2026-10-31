# Source-and-claim audit brief (The Human Variable, a behavioral-science teaching game for MBA/executive students)

Your batch file lists source records and every game challenge that cites them. For EACH source:

1. Verify bibliographic metadata against the DOI registry: fetch https://api.crossref.org/works/<DOI> (WebFetch) and compare authors (full list, order), year of the version of record, title, journal, volume, pages. If Crossref fails, use the publisher page or PubMed. Record any mismatch exactly.
2. Find the primary finding text: abstract at minimum (publisher, PubMed, Crossref abstract, PMC full text, author PDF on a university site). Prefer full text when the challenge cites a specific number. State for every check which text you actually read: "full text", "abstract only", or "secondary source" (secondary sources cannot verify a number).
3. For EVERY challenge citing that source, check each factual statement in scene/question/options/answer/answerTitle/explain/boundary/follow answers/estimate target/chart values: sample size, population, conditions, effect size, direction, percentages. Classify each challenge:
   - SUPPORTED: every number and claim matches the paper (quote the supporting sentence).
   - CORRECTABLE: wrong or overstated detail; give the exact corrected value with a quote and location.
   - UNSUPPORTED: the paper does not show it; say what it does show.
   - UNVERIFIABLE: you could not access text that settles it.
   Also flag a correct answer key that is debatable (another option also defensible), and scenes that misdescribe the design.
4. Output: write a JSON file to the path given in your task with this shape:
{"sources":{"<id>":{"metadata_ok":bool,"metadata_corrections":{...},"text_read":"full text|abstract only|...","text_url":"...","key_findings":["exact quote with numbers", ...],"status":"verified|verified_with_corrections|abstract_only|failed"}},
 "challenges":{"<challenge id>":{"verdict":"SUPPORTED|CORRECTABLE|UNSUPPORTED|UNVERIFIABLE","issues":["..."],"corrections":{"field":"corrected text"},"evidence":"quote + where"}}}
Then reply with a short summary (counts per verdict, the most serious problems). Do not invent quotes. If you could not read something, say so. Be precise and terse. Do not edit any project files.
