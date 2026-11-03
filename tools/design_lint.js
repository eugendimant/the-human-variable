// In-page detectors for qa/DESIGN_RULES.md. Returns [[rule, where, detail], ...]. Run by tools/design_lint.py.
() => {
  const out = [], push = (r, w, d) => out.push([r, w, String(d).slice(0, 70)]);
  const vis = e => { const r = e.getBoundingClientRect(), s = getComputedStyle(e); return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none' && +s.opacity !== 0 };
  const name = e => e.tagName.toLowerCase() + (e.id ? '#' + e.id : '') + (typeof e.className === 'string' && e.className.trim() ? '.' + e.className.trim().split(/\s+/).slice(0, 3).join('.') : '');
  const own = e => [...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join('').trim();
  const rgb = c => (c.match(/[\d.]+/g) || []).map(Number);
  const grey = c => { const [r, g, b, a = 1] = rgb(c); return a === 0 || Math.max(r, g, b) - Math.min(r, g, b) < 28 };
  const all = [...document.querySelectorAll('body *')].filter(e => !(e.closest('svg') && e.tagName.toLowerCase() !== 'svg') && !e.closest('script,style,template,.sr-only') && vis(e));
  for (const e of all) {
    const s = getComputedStyle(e), t = own(e), r = e.getBoundingClientRect(), fs = parseFloat(s.fontSize);
    if (t && /[a-z]/i.test(t) && s.textTransform === 'uppercase') push('R03', name(e), t);
    if (s.backgroundClip === 'text' || s.webkitBackgroundClip === 'text') push('R04', name(e), 'gradient text');
    if (/(linear|radial|conic)-gradient/.test(s.backgroundImage) && !/repeating-/.test(s.backgroundImage) && e.tagName !== 'INPUT' && r.width > 160 && r.height > 24) push('R04', name(e), s.backgroundImage);
    if (s.backdropFilter && s.backdropFilter !== 'none') push('R05', name(e), s.backdropFilter);
    if (s.boxShadow !== 'none') for (const sh of s.boxShadow.split(/,(?![^(]*\))/)) {
      const col = (sh.match(/rgba?\([^)]*\)/) || ['rgb(0, 0, 0)'])[0], px = sh.replace(/rgba?\([^)]*\)/, '').match(/-?[\d.]+px/g) || [], blur = parseFloat(px[2] || 0);
      if (!/inset/.test(sh) && !grey(col) && blur > 2) push('R06', name(e), 'coloured shadow');
      if (!/inset/.test(sh) && blur >= 20 && parseFloat(s.borderTopWidth) > 0 && s.borderTopStyle !== 'none' && !grey(s.borderTopColor) === false && s.borderTopColor !== s.backgroundColor) push('R06', name(e), 'border plus wide shadow');
    }
    const bl = parseFloat(s.borderLeftWidth);
    if (bl >= 3 && s.borderLeftStyle !== 'none' && parseFloat(s.borderRightWidth) < bl && r.height > 20) push('R07', name(e), 'left stripe ' + s.borderLeftColor);
    if (/repeating-/.test(s.backgroundImage)) push('R08', name(e), 'stripe fill');
    if (/gradient/.test(s.backgroundImage) && s.backgroundSize && !/^(auto|auto auto|100% 100%)$/.test(s.backgroundSize)) push('R08', name(e), 'patterned background ' + s.backgroundSize);
    if (t.length > 60 && r.width < 150 && r.width > 0) push('R18', name(e), 'squeezed text, ' + Math.round(r.width) + 'px wide');
    if (!t && !e.children.length && !e.closest('.hbars, .rc-dot, [role=img]') && r.width >= 4 && r.width <= 14 && Math.abs(r.width - r.height) < 1 && parseFloat(s.borderRadius) >= r.width / 2 - .5 && !['INPUT', 'BUTTON'].includes(e.tagName) && s.backgroundColor !== 'rgba(0, 0, 0, 0)') push('R09', name(e), 'dot');
    for (const pe of ['::before', '::after']) {
      const ps = getComputedStyle(e, pe); if (!ps.content || ps.content === 'none' || ps.content === 'normal') continue;
      const w = parseFloat(ps.width), h = parseFloat(ps.height);
      if (w >= 4 && w <= 14 && Math.abs(w - h) < 1 && parseFloat(ps.borderRadius) >= w / 2 - .5) push('R09', name(e) + pe, 'dot');
      if (w >= 8 && h <= 4 && ps.content === '""' && !grey(ps.backgroundColor)) push('R01', name(e) + pe, 'coloured dash before a label');
    }
    if (s.animationName !== 'none' && s.animationIterationCount === 'infinite') push('R09', name(e), 'looping animation');
    if (t && fs < 12) push('R16', name(e), fs + 'px ' + t);
    if (t && parseFloat(s.letterSpacing) < -0.035 * fs - 0.01) push('R17', name(e), (parseFloat(s.letterSpacing) / fs).toFixed(3) + 'em ' + t);
    if (t && fs <= 18 && parseFloat(s.letterSpacing) > 0.04 * fs) push('R17', name(e), 'wide tracking ' + t);
    if (e.tagName === 'P' && t.length > 160 && r.width / fs > 40) push('R18', name(e), Math.round(r.width / fs) + 'em wide');
    if (t && s.textAlign === 'justify') push('R18', name(e), 'justified');
    const wrap = s.textWrap || s.textWrapStyle || '';
    if (/^H[1-3]$/.test(e.tagName) && /balance/.test(wrap)) push('R19', name(e), 'heading wrap balance leaves the line short');   // owner, 2026-11-01: headings fill each line (rule 11)
    if (e.tagName === 'P' && t.length > 160 && !/pretty|balance/.test(wrap)) push('R19', name(e), 'paragraph wrap ' + wrap);
  }
  for (const tx of document.querySelectorAll('svg text')) {   // rule 9 for SVG text, at its rendered size
    const sv = tx.ownerSVGElement, r = sv && sv.getBoundingClientRect(); if (!r || !r.width || !vis(sv) || !tx.textContent.trim()) continue;
    const vb = sv.viewBox && sv.viewBox.baseVal, k = vb && vb.width ? r.width / vb.width : 1, px = parseFloat(getComputedStyle(tx).fontSize) * k;
    if (px < 11.5) push('R16', name(sv) + ' text', px.toFixed(1) + 'px ' + tx.textContent.trim());
  }
  for (const sv of document.querySelectorAll('svg')) {   // labels in a figure never sit on each other or on a data mark (audit 28b)
    if (!vis(sv)) continue;
    const box = e => e.getBoundingClientRect(), hit = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;
    const texts = [...sv.querySelectorAll('text')].filter(x => x.textContent.trim() && !x.getAttribute('transform')), marks = [...sv.querySelectorAll('circle')];
    for (let i = 0; i < texts.length; i++) {
      for (let j = i + 1; j < texts.length; j++) if (hit(box(texts[i]), box(texts[j]))) push('R31', name(sv), 'labels overlap: ' + texts[i].textContent.trim() + ' / ' + texts[j].textContent.trim());
      for (const m of marks) if (hit(box(texts[i]), box(m)) && !m.closest('g.ev-mark')) push('R31', name(sv), 'label on a mark: ' + texts[i].textContent.trim());
    }
  }
  const tw = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT); let n;
  while ((n = tw.nextNode())) {
    const p = n.parentElement, x = n.textContent; if (!p || p.closest('script,style,svg,.sr-only') || !vis(p) || !x.trim()) continue;
    if (/\p{Extended_Pictographic}/u.test(x.replace(/[↑↓←→×✓]/g, ''))) push('R10', name(p), x.trim());
    if (/\s·\s/.test(x)) push('R11', name(p), x.trim());
    if (/[→›»]\s*$/.test(x) && p.closest('button,a')) push('R12', name(p), x.trim());
    if (/—|\s–\s/.test(x)) push('R13', name(p), x.trim());
    if (/\b(not just|isn['’]t just|more than just|unlock|seamless|elevate|dive into|game[- ]changer|empower|supercharge|revolutioni[sz]e|cutting[- ]edge|harness the power)\b/i.test(x)) push('R14', name(p), x.trim());
    if (p.matches('h1,h2,h3,.hero *') && /[.!]\s+Then\s/.test(x)) push('R14', name(p), 'two-beat slogan: ' + x.trim().slice(0, 60));   // "Do X. Then Y." headlines (owner, 2026-11-01)
    if (/(^|[^\d.,])1 (points|decisions|studies|players|answers|people|calls|steps)\b/.test(x)) push('R14', name(p), 'plural after 1: ' + x.trim().slice(0, 60));   // "1 points" (audit 36)
    if (/^\s*0\d\s*$/.test(x)) push('R15', name(p), x.trim());
  }
  const headish = [...document.querySelectorAll('h1,h2,h3')].concat(all.filter(e => !/^H[1-6]$/.test(e.tagName) && !e.matches('.num, .num *') && /\S\s+\S/.test(own(e)) && own(e).length > 3 && parseFloat(getComputedStyle(e).fontSize) >= 20 && +getComputedStyle(e).fontWeight >= 650));
  for (const h of headish) {
    if (!vis(h) || h.closest('.sr-only')) continue; const pv = h.previousElementSibling;
    if (pv && vis(pv) && !pv.matches('h1,h2,h3,h4,button,a,nav,img,svg,input,label,form,ol,ul,figure,section,div.art,.rev-art') && pv.textContent.trim() && pv.textContent.trim().length < 60 && pv.getBoundingClientRect().height < 40)
      push(pv.matches('.tag,.badge,.pill,.verdict') || pv.querySelector('.tag,.badge,.pill') ? 'R02' : 'R01', name(pv) + ' above ' + h.tagName.toLowerCase(), pv.textContent.trim());
  }
  const h1 = [...document.querySelectorAll('.hero h1')].find(vis);   // the hero headline only
  if (h1 && innerWidth >= 1200) { const hs = getComputedStyle(h1), lh = parseFloat(hs.lineHeight) || parseFloat(hs.fontSize) * 1.2, lines = Math.round(h1.getBoundingClientRect().height / lh); if (lines > 3) push('R20', name(h1), lines + ' lines') }
  const bgOf = e => { while (e) { const b = getComputedStyle(e).backgroundColor; if (b && b !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(b)) return b; e = e.parentElement } return 'rgb(255, 255, 255)' };
  const tinted = e => { const s = getComputedStyle(e), b = s.backgroundColor; return !e.matches('button,input,select,textarea,a,label,summary,svg,img,canvas,svg *') && b && b !== 'transparent' && !/rgba\([^)]*,\s*0\)$/.test(b) && e.parentElement && b !== bgOf(e.parentElement) && parseFloat(s.borderTopLeftRadius) > 0 };   // a filled, rounded box with no border is a tile too (review 26)
  const boxed = e => { const s = getComputedStyle(e), r = e.getBoundingClientRect(); return r.width > 120 && r.height > 50 && ((parseFloat(s.borderTopWidth) > 0 && s.borderTopStyle !== 'none' && parseFloat(s.borderBottomWidth) > 0 && parseFloat(s.borderLeftWidth) > 0) || s.boxShadow !== 'none' || tinted(e)) };
  const nested = new Set();
  for (const e of all) { if (!boxed(e)) continue; let a = e.parentElement; while (a && a !== document.body) { if (boxed(a)) { nested.add(name(e) + ' inside ' + name(a)); break } a = a.parentElement } }
  nested.forEach(x => push('R21', x, 'card in card'));
  for (const e of all) {
    if (!/grid|flex/.test(getComputedStyle(e).display)) continue; const kids = [...e.children].filter(vis).filter(boxed);
    if (kids.length >= 6) { const sizes = new Set(kids.map(k => Math.round(k.getBoundingClientRect().width / 8) + 'x' + Math.round(k.getBoundingClientRect().height / 8))); if (sizes.size <= 2) push('R22', name(e), kids.length + ' identical boxes') }
  }
  const radii = new Set();
  for (const e of all) { const v = parseFloat(getComputedStyle(e).borderTopLeftRadius), r = e.getBoundingClientRect(); if (v > 0 && v < Math.min(r.width, r.height) / 2 - 1) radii.add(Math.round(v)) }
  if (radii.size > 4) push('R23', 'page', [...radii].sort((a, b) => a - b).join(', ') + ' px');
  const hues = new Set();
  for (const e of all) { const s = getComputedStyle(e); for (const c of [s.color, s.backgroundColor, s.borderTopColor]) { const [r, g, b, a = 1] = rgb(c); if (a < .2 || grey(c)) continue; const mx = Math.max(r, g, b), mn = Math.min(r, g, b), d = mx - mn; let h = mx === r ? ((g - b) / d) % 6 : mx === g ? (b - r) / d + 2 : (r - g) / d + 4; hues.add(Math.round(((h * 60) + 360) % 360)) } }
  const hs = [...hues].sort((a, b) => a - b), fam = hs.length ? hs.reduce((n, h, i) => n + (i && h - hs[i - 1] > 40 ? 1 : 0), 1) - (hs.length > 1 && hs[0] + 360 - hs[hs.length - 1] <= 40 ? 1 : 0) : 0;
  if (fam > 3) push('R24', 'page', fam + ' hue families: ' + hs.join(', '));
  // figures (rules 26 to 29)
  const vt = e => e.innerText || '';
  for (const e of all) { const x = own(e); if (/\b(blue|amber|orange|green|grey|gray)\b[^.]{0,40}\b(you|your|evidence|study|routing)/i.test(x)) push('R26', name(e), 'colour key instead of a direct label: ' + x) }
  for (const e of document.querySelectorAll('.gap-legend')) if (vis(e)) push('R26', name(e), 'legend');
  for (const e of document.querySelectorAll('.plate-h')) if (vis(e) && /^what the study (measured|found)$/i.test(vt(e).trim())) push('R27', name(e), 'generic chart title');
  for (const f of document.querySelectorAll('figure.gap')) if (vis(f) && f.querySelector('.hbars') && !/Source: /.test(vt(f))) push('R28', name(f), 'chart without its source');
  for (const f of document.querySelectorAll('figure.gap')) if (vis(f) && (vt(f).match(/Source: /g) || []).length > 1) push('R28', name(f), 'source repeated inside one figure');
  for (const e of document.querySelectorAll('.plate-h')) if (vis(e) && /\((19|20)\d\d\)/.test(vt(e))) push('R27', name(e), 'chart title carries a citation: ' + vt(e).slice(0, 50));
  for (const h of document.querySelectorAll('.hbars')) if (vis(h) && /(^|\s)[−-]\d/.test(h.innerText) && !h.querySelector('.zero')) push('R29', name(h), 'signed values without a zero line');
  for (const h of document.querySelectorAll('.hbars')) if (vis(h) && /(^|\s)-\d/.test(h.innerText)) push('R13', name(h), 'hyphen used as a minus sign');
  for (const h of document.querySelectorAll('svg text, .num, .gap-head b, .big, [class*=stat] b')) if (vis(h) && /(^|[\s(])-\d/.test(h.textContent)) push('R13', name(h), 'hyphen used as a minus sign: ' + h.textContent.trim().slice(0, 30));   // review 26: SVG and display numbers too
  for (const h of document.querySelectorAll('.hbars:not(.alloc-cmp)')) if (vis(h) && h.querySelectorAll('i.ev').length > 1) push('R29', name(h), h.querySelectorAll('i.ev').length + ' highlighted bars');
  // R31: a mark drawn outside its SVG's viewBox is clipped and misreads (audit 31: a stacked dot strip ran off the top)
  for (const sv of document.querySelectorAll('svg[viewBox]')) { if (!vis(sv)) continue; const vb = sv.viewBox.baseVal; if (!vb || !vb.height) continue;
    for (const m of sv.querySelectorAll('circle, rect, text')) { if (m.hasAttribute('transform')) continue; let b; try { b = m.getBBox() } catch (e) { continue } if (!b.width && !b.height) continue; if (b.y + b.height < vb.y - 1 || b.y > vb.y + vb.height + 1 || b.x + b.width < vb.x - 1 || b.x > vb.x + vb.width + 1 || b.y < vb.y - 4 || (m.tagName === 'text' && (b.x + b.width > vb.x + vb.width + 1 || b.x < vb.x - 1))) { push('R31', name(sv), 'mark outside the drawing area'); break } } }
  // R31: a label wider than the pill it sits in (review 27: causal node labels at 390 px)
  for (const g of document.querySelectorAll('svg g')) { const rc = g.querySelector(':scope > rect'), ts = g.querySelectorAll(':scope > text'); if (!rc || !ts.length || !vis(g)) continue; let rb; try { rb = rc.getBBox() } catch (e) { continue }
    for (const t of ts) { const tb = t.getBBox(); if (tb.x < rb.x - 1 || tb.x + tb.width > rb.x + rb.width + 1) { push('R31', name(g), 'label wider than its box: ' + t.textContent.trim().slice(0, 24)); break } } }
  // R33: a heading that wraps while its own line box stops well short of the space it has (owner, 2026-11-01: "fill the space; no line break where there shouldn't be one")
  for (const h of document.querySelectorAll('h1, h2, h3, .q, .reveal-title, .study-line')) { if (!vis(h) || h.closest('svg, .sr-only')) continue;
    const cs = getComputedStyle(h), lh = parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.2, r = h.getBoundingClientRect(); if (r.height < lh * 1.8) continue;
    const par = h.parentElement, pcs = getComputedStyle(par), avail = par.getBoundingClientRect().width - parseFloat(pcs.paddingLeft) - parseFloat(pcs.paddingRight);
    const rg = document.createRange(); rg.selectNodeContents(h); const used = Math.max(...[...rg.getClientRects()].map(x => x.right)) - r.left;
    const capped = cs.maxWidth !== 'none' || /grid|flex/.test(pcs.display) === false;   // in a grid or flex row the track sets the width; elsewhere the parent does
    if (cs.display !== 'inline' && capped && !(/grid|flex/.test(pcs.display) && cs.maxWidth === 'none') && r.width < avail * .82 && avail - used > parseFloat(cs.fontSize) * 4) push('R33', name(h), 'wraps with ' + Math.round(avail - used) + 'px unused: ' + h.textContent.trim().slice(0, 40)) }
  // R31 for HTML: two pieces of visible text drawn on top of each other (review 26: a grid override stacked a label on a strip on phones)
  const pinned = e => { for (let a = e; a && a !== document.body; a = a.parentElement) { const ps = getComputedStyle(a).position; if (ps === 'fixed' || ps === 'sticky') return true } return false };   // pinned bars float over the page by design
  { const leaves = [...document.querySelectorAll('body *')].filter(e => !e.closest('svg,.sr-only,[aria-hidden=true] svg') && [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) && vis(e) && !e.closest('[hidden]') && !(e.closest('details:not([open])') && !e.closest('summary')) && (!e.checkVisibility || e.checkVisibility({ contentVisibilityAuto: true, opacityProperty: true, visibilityProperty: true })) && !pinned(e))
      .map(e => { const rg = document.createRange(); rg.selectNodeContents(e); const r = rg.getBoundingClientRect(); return { e, r } }).filter(x => x.r.width > 2 && x.r.height > 2);
    const ov = (a, b) => Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) * Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
    for (let i = 0; i < leaves.length; i++) for (let j = i + 1; j < leaves.length; j++) { const A = leaves[i], B = leaves[j]; if (A.e.contains(B.e) || B.e.contains(A.e)) continue; const o = ov(A.r, B.r); if (o > 0.25 * Math.min(A.r.width * A.r.height, B.r.width * B.r.height) ) push('R31', name(A.e) + ' / ' + name(B.e), 'text overlaps text: ' + A.e.textContent.trim().slice(0, 24) + ' / ' + B.e.textContent.trim().slice(0, 24)) } }
  // R31: text clipped by its own box or an overflow-hidden ancestor (review 34: "(not signifi" on the allocate plate)
  for (const e of document.querySelectorAll('body *')) { if (!vis(e) || e.closest('svg,.sr-only,input,textarea,select')) continue; if (![...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim())) continue;
    const cs = getComputedStyle(e); if (/hidden|clip/.test(cs.overflowX) && e.scrollWidth > e.clientWidth + 2 && cs.textOverflow !== 'ellipsis') push('R31', name(e), 'clipped text: ' + e.textContent.trim().slice(0, 40)) }
  return out;
}
