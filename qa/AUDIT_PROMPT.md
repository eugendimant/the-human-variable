# Regression audit prompt (protocol step 3 in qa/INVARIANTS.md)

Fill in DIFF and SNAPSHOT and give this to a fresh agent that did not make the changes.

```
You are a regression auditor for "The Human Variable" (static page index.html built from src/, a Python server in server/, classroom.html console and projector, a Streamlit app in thv_streamlit/). You did not write these changes. Find defects INTRODUCED by them, above all anything an external reviewer would call Blocking or Major: a core flow that breaks, a right answer scored wrong, an answer shown before a class reveals it, a paper's number misstated, a duplicated or lost option, layout breakage at 390 or 1440 px, an accessibility failure.

Inputs: the diff at DIFF; a full copy of the project at SNAPSHOT (work only there or in a copy; publish nothing; free ports; kill only your own processes by PID); the regression register qa/INVARIANTS.md and qa/DESIGN_RULES.md in that copy.

Do all of these:
1. Read the diff. For each change, ask what it could break elsewhere and check it against every invariant in the register.
2. Content: for every changed item, every number matches its stored quotes; options are unique; keyed texts match tests/keyed_options.json; nothing refers to options by position.
3. Both pages: play every changed item plus at least six others at 390 and 1440 on the offline file AND on the hosted page (start the server). On the hosted page, after playing one decision of every format, RELOAD and open every view (home, record, Library, All decisions) and check for page errors and empty views.
4. Classroom: console, projector (open and revealed) and a phone for every changed format.
5. Tutor: 40+ natural questions across 15 decisions through server/tutor.py curated(), compared with the previous version where useful.
6. Run `python -m pytest -q` and report the count.

Return introduced defects triaged Blocking / Major / Minor with where, evidence and a concrete fix, and say explicitly "no introduced Major or Blocking found" if that is the case.
```
