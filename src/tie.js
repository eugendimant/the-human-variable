// Shared by the game and the classroom pages (build.py puts it in front of app.js and classroom.js).
// Owner, 2026-11-12: no word alone on the last line, anywhere. In every text block the last two words stay together (a nowrap span; the text itself does not change).
// Iteration 73: the tied pair is measured. If it is wider than 85% of its box it is put back, because it would push a long word to the next line and leave the line above short (review 45, m-I1; a long pair in a narrow column breaks one word per line).
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
    const pair = head.slice(k) + ' ' + tail; if (pair.trim().length > 40) continue;
    const sp = document.createElement('span'); sp.className = 'nw'; sp.textContent = pair;
    n.textContent = head.slice(0, k); n.after(sp);
    if (sp.offsetWidth > e.clientWidth) { sp.remove(); n.textContent = m[0] }   // a pair wider than its box would push the page sideways: it stays as it was
  }
}

function fitHeadings(root) {   // a heading with a line of one word (beside the tied pair, or last) is set smaller, 5% at a time up to 34%, until none is (review 45, m-I1). Call after the fonts load and after every resize.
  for (const h of root.querySelectorAll('h1,h2,h3')) {
    h.style.fontSize = ''; if (!stranded(h)) continue;
    let f = parseFloat(getComputedStyle(h).fontSize);
    for (let i = 0; i < 8 && stranded(h); i++) { f *= .95; h.style.fontSize = f + 'px' }
    if (stranded(h)) h.style.fontSize = '';
  }
}
function stranded(e) {   // true when a line of the block holds one word and is not the only line
  const r = document.createRange(), lines = []; let top = null;
  const w = document.createTreeWalker(e, NodeFilter.SHOW_TEXT); let t;
  while ((t = w.nextNode())) for (const m of t.textContent.matchAll(/\S+/g)) { r.setStart(t, m.index); r.setEnd(t, m.index + m[0].length); const y = Math.round(r.getBoundingClientRect().top / 4); if (y !== top) { lines.push(0); top = y } lines[lines.length - 1]++ }
  return lines.length > 1 && lines.some(c => c === 1);
}
