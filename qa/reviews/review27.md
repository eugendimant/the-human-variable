# Independent review 27 (snapshot after iteration 31 and regression audits 31, 31b, 31c, 31d)

**Score: 86/100.** 0 Blocking, 1 Major, 13 Minor, 4 Optional. Tests: 305 passed; design lint 0 hits; axe 0 violations on 46 states.

| Science 13 | Learning 12 | Visual 12 | Gameplay 13 | AI/business 9 | Content 8 | Technical 9 | Classroom 5 | Accessibility 5 |
|---|---|---|---|---|---|---|---|---|

- **M1.** Offline tutor: "should we <verb>?" reached the manager action only for 13 listed verbs; every other "should we …" (publish salaries, set a default, offer remote work) got the ethics non-answer; "what does this mean for my team?" got "not covered".
- **Minor (13).** bz12 causal labels overflow at 390 px; a calibration label over a dot; a badge above the locked-screen headline; middle-dot strings in a page title and Streamlit captions; the room drawn in blue; axb02 rank-format leftover; bz12 asks an outcome question under "Find the cause"; axf05 mixes a level with differences; straight quotes, "Room #1.67", statistics jargon; axb01 tasks are worked examples; contest items lean "the famous finding failed"; record headline after one call; dead code and the header-less join bucket.
- **Fact-checks (8 plus 2 publication checks).** All correct, including two Dimant items.
- **Not found:** no answer leak; 120 students; no regression from the audit-31 fixes.
