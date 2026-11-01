# Design rules: no AI giveaways

Thirty-one rules that every page of The Human Variable follows (home, play, reveal, record, Library, console, projector, phones). They come from published catalogues of the patterns that make a page read as machine-made, and from established usability guidance. Each rule names its detector. `tools/design_lint.py` runs the detectors in a real browser on every page state at 1440 and 390 px, and `tests/test_design.py` fails on any hit. A rule without a detector is checked by the independent reviewer (see `qa/REVIEW_PROMPT.md`).

Sources:
- [impeccable.style slop catalogue](https://impeccable.style/slop)
- [Krebs, Scoring 500 Show HN pages for AI design patterns](https://adriankrebs.ch/blog/design-slop/)
- [Fountain Institute, 7 tells that a UI is AI-generated](https://pages.thefountaininstitute.com/posts/7-tells-that-a-ui-is-ai-generated)
- [925 Studios, AI slop design tells](https://www.925studios.co/blog/ai-slop-design-tells)
- [IxDF, UI design guidelines (Nielsen's ten heuristics)](https://ixdf.org/literature/article/user-interface-design-guidelines-10-rules-of-thumb)

## Structure

1. **No label above a heading.** A short line sitting on top of a heading ("Try one now", "Your call") either repeats it or belongs in it. Fold the words into the heading or the sentence below, or drop them. Coloured dashes before a label count as the same device. *Detector R01.*
2. **No badge or pill above the main headline.** Status belongs in the sentence under the headline, or beside it. *Detector R02.*
3. **No nested cards.** A boxed element inside another boxed element is flattened: inner groups use space, type and a rule, not a second border or shadow. *Detector R21.*
4. **No grid of identical cards.** Six equal boxes with a picture on top is the template look. Paths are an index that varies with its content. *Detector R22.*
5. **Numbers only for real sequences.** No 01 / 02 / 03 markers on content that is not ordered. *Detector R15.*
6. **The layout follows the content.** Opening columns balance; a heading sits closer to its content than to the section above. *Reviewer.*

## Type

7. **No all-caps text.** Sentence case everywhere, including small labels. *Detector R03.*
8. **No crushed tracking.** Letter spacing no tighter than −0.035 em at any size; small text keeps default spacing (no wide tracking). *Detector R17.*
9. **No text below 12 px; body text 16 px or more.** *Detector R16.*
10. **Lines of about 65 to 75 characters**; no justified text. *Detector R18.*
11. **Headings fill the line.** Headings wrap only when a line is full (`text-wrap: wrap`, never `balance`, which leaves lines short and space empty; owner, 2026-11-01). No width caps on headings narrower than their column (*detector R33*). Long paragraphs use `text-wrap: pretty`. *Detector R19.*
12. **A hero headline of three lines or fewer** at desktop width. *Detector R20.*

## Colour and surface

13. **No gradient text and no decorative gradients.** Gradients only where they draw data (a slider's filled track). *Detector R04.*
14. **No glass or blur.** Surfaces are solid. *Detector R05.*
15. **No glows.** No coloured shadows, and never a border and a wide shadow on the same box. *Detector R06.*
16. **No side stripes.** No thick coloured left border on cards or quotes. *Detector R07.*
17. **No stripe fills.** Hatching or repeating gradients are replaced by an outline or a plain tint. *Detector R08.*
18. **Colour carries meaning, consistently.** Blue is always the player's call, amber always the evidence, navy the ink. No other accent colours. *Detector R24 (palette budget).*
19. **One small radius scale.** At most four corner radii on a page, excluding circles and pills. *Detector R23.*

## Ornament and motion

20. **No decorative dots.** Status dots and bullet dots before titles go; a dot appears only as data (a call or a result on an axis). No looping animation. *Detector R09.*
21. **No emoji as icons.** *Detector R10.*

## Copy

22. **No middle-dot strings.** "A · B · C" metadata is written as a phrase. *Detector R11.*
23. **No arrows in button or link text.** The label says what happens. *Detector R12.*
24. **No em dashes or spaced en dashes in interface copy, and no stock phrasing** ("not just", "unlock", "seamless", "elevate", "dive into", "game-changer", "empower"). *Detectors R13, R14.*

## Usability

25. **Every state reads and works:** contrast meets WCAG AA (axe in `tests/test_browser.py`), status is visible, errors say what happened and how to fix it, and nothing waits invisible for an animation. *Detector R25 (no console errors, no hidden content) plus axe.*

## Figures (after Tufte; Burn-Murdoch's FT chart talks; Knaflic, *Storytelling with Data*; Wong, *The Wall Street Journal Guide to Information Graphics*)

26. **Label marks where they sit; no colour keys.** No legend and no sentence that decodes colours ("Blue: your call"). The words "You" and "Study" sit on the marks. *Detector R26.*
27. **The headline states the finding; the chart's own title states the measure.** The reveal headline is the result; the chart above the bars says what was measured, with units and the study arm, never a generic "What the study measured". *Detector R27.*
28. **The source sits inside the figure**, under the bars, so a screenshot carries it. *Detector R28.*
29. **Colour only the mark that proves the headline.** One amber bar per chart; the rest are grey. *Detector R29.*
30. **Ask on every page: what would Tufte do?** Maximise data ink: remove boxes, rules, labels and decoration that encode nothing; show comparisons at the same scale; annotate the moment that matters in place; prefer a sentence with a number to a widget. The page-by-page answers are in `qa/TUFTE_PASS.md` and every reviewer repeats the question. *Reviewer.*
31. **Labels in a figure never overlap each other or a data mark**, and explanations of a reference line go in the caption, not in the data area. *Detector R31.*
