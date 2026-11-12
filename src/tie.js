// Shared by the game and the classroom pages (build.py puts it in front of app.js and classroom.js).
// Owner, 2026-11-12: no word alone on the last line, anywhere. In every text block the last two words stay together (a nowrap span; the text itself does not change).
// Iteration 70: this walks every text block on the page instead of a list of selectors. Flex and grid boxes are skipped, because their text is an anonymous item and a nowrap span would be pushed away from the rest (review 43, M-1).
const TIE_SKIP = 'svg,script,style,textarea,input,select,option,button,pre,code,.tutor-answer,[contenteditable],.nw';
function tieEnds(root) {
  for (const e of root.querySelectorAll('*')) {
    if (e.matches(TIE_SKIP) || e.closest('svg,script,style,textarea,select,pre,.tutor-answer,.nw') || e.querySelector(':scope > .nw')) continue;
    let n = e.lastChild; if (!n || n.nodeType !== 3 || !n.textContent.trim()) continue;
    if (e.textContent.trim().split(/\s+/).length < 3) continue;   // a block of one or two words cannot strand a word
    const cs = getComputedStyle(e), d = cs.display;
    if (/flex|grid|contents|table(?!-cell)/.test(d) || cs.whiteSpace === 'nowrap' || cs.whiteSpace === 'pre') continue;
    const m = n.textContent.match(/^([\s\S]*\S)\s+(\S+\s*)$/); if (!m) continue;
    const head = m[1], tail = m[2], k = head.search(/\S+$/); if (k < 0) continue;
    const pair = head.slice(k) + ' ' + tail; if (pair.trim().length > 26) continue;   // a long pair would push the page sideways on a phone
    const sp = document.createElement('span'); sp.className = 'nw'; sp.textContent = pair;
    n.textContent = head.slice(0, k); n.after(sp);
  }
}
