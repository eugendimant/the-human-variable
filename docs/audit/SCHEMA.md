# Drafting brief: new decision items for "The Human Variable"

Audience: MBA students, graduate students and executives. Orientation: AI and business first, merged with psychology and behavioral science. Original concept by Eugen Dimant.

## Hard evidence rules
- Only peer-reviewed journal articles or scholarly books. No working papers, NBER/SSRN/arXiv, unless you cite the journal version of record.
- For each source: fetch https://api.crossref.org/works/<DOI> with WebFetch to confirm authors, year (version of record), title, journal, volume(issue), pages. Then read the abstract at least; full text when an item uses a number not in the abstract (PubMed Central, author PDFs on university sites, publisher open access).
- Every number in an item must appear in text you read. Record the quote. If a number is only in a source you could not read, do not use it; write a qualitative item instead.
- Flag retractions, expressions of concern, failed replications or prominent reanalyses (search "<title> replication" / "retraction"). Contested findings may be used only as an item ABOUT the contest (e.g., "did it replicate?"), citing the replication paper too.
- Do not invent study outcomes. Scenes describe the real design accurately (population, task, setting), in manager-relevant language.

## Writing rules
- Short. Scene: 1-2 sentences, max 40 words. Question: max 16 words. Options: max 9 words each. Explain: 1-2 sentences with the key number. Implication: one concrete managerial action, max 25 words. Boundary: where the finding stops holding, max 25 words, a fact about the study's scope, stated plainly.
- No AI phrasing: no "delve", "crucial", "landscape", "it's important to note", "game-changer", "in today's world", no rhetorical questions in explanations, no em dashes.
- Follow-ups: exactly 3 predefined questions a curious MBA would click, each with a 1-3 sentence answer grounded in the paper. Make them specific (e.g., "Who gained the most?", "Was quality measured?", "How large was the sample?", "What did firms do next?").

## Formats (pick the one that best fits the evidence; vary them)
Common fields for all: id, track ("AI × Business" | "Business" | "Culture & Society" | "Judgment"), concept (2-3 words), title (max 6 words, a hook), scene, question, answerTitle (the result in max 9 words), explain, implication, boundary, sources [source ids], follow [{q,a}x3], study {design, n} (design e.g. "Field experiment", n e.g. "758 BCG consultants"), evidence [{source, quote, location}] (quotes that support EVERY number and the answer key).
- "choice": options [3-4], answer (index). Distractors must be plausible to a smart manager.
- "multi": options [4-5], multiAnswers [two indices].
- "estimate": estimate {target, min, max, tolerance, label, unit ("%" or "" or " days" etc.)}. Use when the study reports one headline number.
- "forecast": forecast {claim, truth (bool)}. A crisp yes/no proposition about what the study found; the player gives a probability. Make about half false (a plausible claim the study contradicts).
- "rank": options [3-5 items], rankAnswer [indices from highest to lowest], rankLabel ("Highest share choosing the model first"), rankValues [reported value per option, same order as options, strings]. Only when the paper reports all values.
- "allocate": options [3-4], allocate {total:100, step:10, label:"Pilot budget", prefix:"", suffix:"%", values:[reported effect per option], valueLabels:["+34%",...], valueName:"reported effect on X", pass:0.8}. Only when the paper reports a comparable effect for each option.
- "delegate": delegate {choices:["AI drafts, human checks","Human alone","AI alone"], tasks:[{text, answer (index), why (one sentence grounded in the paper)}x3-4]}.
- "causal": like choice, plus dag {alt, height:200, nodes:[{id,label (max 14 chars),x (60-460),y (30-170),hidden?:true}], edges:[[from,to,"q" for a questioned or hidden link]]}. Use for confounding, selection, reverse causality, measurement (e.g., ad lift observational vs RCT).
- Optional "chart" for choice/multi/causal items when the paper reports comparable values: chart {labels:[...], values:[numbers], unit:"%", highlight: index, note:"Values reported in <paper>, Table/Fig X."}.

## Output
Write a JSON object {"sources": {<id>: {id, authors ("Surname, Surname & Surname" or "Surname et al."), authors_full, year, title, venue, volume, pages, doi, url:"https://doi.org/<doi>", kind:"peer-reviewed", takeaway (one sentence), verification:{status:"verified_full_text"|"verified_abstract", checked:"2026-10-31", metadata:"matched Crossref record", text_read, text_url}, flags?}}, "challenges": [ ... ]} to the file named in your task. Source ids: short lowercase like "kleinberg18". Reply with a terse summary listing items by format and anything you dropped and why.
