// Shared by the game and the classroom pages (build.py puts it in front of app.js and classroom.js).
function tieEnds(root) {   // owner, 2026-11-12: no word alone on the last line. The last two words of each text block stay together (a nowrap span; the text itself does not change).
  for (const e of root.querySelectorAll('h1,h2,h3,h4,p,li,figcaption,small,.scene,.q,.opt>span:nth-of-type(2),.tr-q,.tr-scene,.reveal-title,.study-line,.follow summary>span,.credit>span,.try-src,.row-note')) {
    if (e.closest('svg,script,style,textarea,input,select,.tutor-answer') || e.querySelector('.nw')) continue;
    let n = e.lastChild; while (n && !(n.nodeType === 3 && n.textContent.trim()) && n.nodeType === 3) n = n.previousSibling;
    if (!n || n.nodeType !== 3) continue;
    const m = n.textContent.match(/^([\s\S]*\S)\s+(\S+\s*)$/); if (!m || !/\S\s+\S/.test(m[1] + ' ' + m[2]) ) continue;
    const head = m[1], tail = m[2], k = head.search(/\S+$/); if (k < 0) continue;
    const pair = head.slice(k) + ' ' + tail; if (pair.trim().length > 26) continue;   // a long pair would push the page sideways on a phone
    const sp = document.createElement('span'); sp.className = 'nw'; sp.textContent = pair;
    n.textContent = head.slice(0, k); n.after(sp);
  }
}
