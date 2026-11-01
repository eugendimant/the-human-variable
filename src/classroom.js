(() => {
'use strict';
// Instructor console for a live class. Talks to the Python server; holds the instructor key in sessionStorage only.
const qs = s => document.querySelector(s);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const FORMAT_NAME = { choice: 'Pick one', causal: 'Find the cause', multi: 'Pick two', estimate: 'Estimate', forecast: 'Forecast', rank: 'Rank', allocate: 'Allocate', delegate: 'Delegate' };
const LIVE = BANK.challenges.filter(c => c.sources.every(id => BANK.sources[id] && BANK.sources[id].verification.status !== 'quarantined'));
const BY = Object.fromEntries(LIVE.map(c => [c.id, c]));
function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619); return h >>> 0 }
function rng(seed) { let x = seed >>> 0; return () => { x += 0x6D2B79F5; let t = x; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296 } }
function shuffle(a, r) { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
// Same option order as the students' phones: seeded by the session code and the decision.
function order(c) { return shuffle(c.options.map((t, i) => ({ t, i })), rng(hash(c.id + '-' + (hash(S.code) >>> 0)))) }
let fullLoaded = !BANK.public;
async function loadFull() { if (fullLoaded || !S) return; try { const d = await api('/api/instructor/bank?code=' + S.code); d.challenges.forEach(x => { if (BY[x.id]) Object.assign(BY[x.id], x) }); fullLoaded = true; render() } catch { } }
let etag = '';
const cid = (() => { let v = sessionStorage.getItem('thv:inst'); if (!v) { v = 'inst' + Math.random().toString(36).slice(2, 10); sessionStorage.setItem('thv:inst', v) } return v })();
let S = JSON.parse(sessionStorage.getItem('thv:session') || 'null'); // {code, secret, title}
let state = null, filter = { q: '', track: 'All', format: 'All' }, timer = null, plan = JSON.parse(sessionStorage.getItem('thv:plan') || '[]');

async function api(path, body, method) {
  const h = { 'X-Client-Id': cid }; if (body !== undefined) h['Content-Type'] = 'application/json'; if (S) h['X-Instructor-Key'] = S.secret;
  let r;
  for (let i = 0; i < 5; i++) {   // a busy class network can throttle the console too: wait and retry instead of dropping the instructor's click
    r = await fetch(path, { method: method || (body === undefined ? 'GET' : 'POST'), headers: h, body: body === undefined ? undefined : JSON.stringify(body) });
    if (r.status !== 429) break; await new Promise(res => setTimeout(res, 1000 * (+(r.headers.get('Retry-After')) || 1 + i)));
  }
  const d = await r.json().catch(() => ({})); if (!r.ok) throw Error(d.error || 'Request failed (' + r.status + ')'); return d;
}
function toast(m) { const t = qs('#toast'); t.textContent = m; t.classList.add('show'); clearTimeout(t._t); t._t = setTimeout(() => t.classList.remove('show'), 3000) }
function joinURL() { return location.origin + '/?room=' + S.code }
function qr(text, cell = 6) { const q = qrcode(0, 'M'); q.addData(text); q.make(); const n = q.getModuleCount(); let p = ''; for (let r = 0; r < n; r++) for (let c = 0; c < n; c++) if (q.isDark(r, c)) p += `M${c * cell} ${r * cell}h${cell}v${cell}h-${cell}z`; const s = n * cell; return `<svg viewBox="-${cell * 2} -${cell * 2} ${s + cell * 4} ${s + cell * 4}" role="img" aria-label="QR code for the join link" class="qr"><rect x="-${cell * 2}" y="-${cell * 2}" width="${s + cell * 4}" height="${s + cell * 4}" fill="#fff"/><path d="${p}" fill="#14203a"/></svg>` }

function setup() {
  return `<section class="wrap" style="padding-top:48px;padding-bottom:64px"><div class="section-head"><h1 class="console-h">Run a live class.</h1><p>Students join on their phones with a code. You open one decision at a time, watch answers arrive, then reveal the class picture next to the evidence.</p></div>
  <form class="panel" data-form="create" style="padding:24px;max-width:620px;display:grid;gap:14px">
    <label class="kicker" for="title">Session name (shown to students)</label><input id="title" class="field" maxlength="80" placeholder="For example: Leading with AI, week 3">
    <label class="kicker" for="pass">Instructor passcode (only if your server requires one)</label><input id="pass" class="field" type="password" autocomplete="off">
    <button class="btn btn-solid">Create the session</button>
    <p class="kicker" style="margin:0">Data stays on this server, is identified only by participant numbers, and is deleted when you end the session or after 48 hours.</p></form></section>`;
}

function picker() {
  const q = filter.q.toLowerCase().replace(/[\u2018\u2019]/g, "'");   // curly and straight apostrophes match (audit 35)
  const list = LIVE.filter(c => (filter.track === 'All' || c.track === filter.track) && (filter.format === 'All' || FORMAT_NAME[c.format] === filter.format) && (!q || (c.title + ' ' + c.question + ' ' + c.concept + ' ' + BANK.sources[c.sources[0]].authors).toLowerCase().replace(/[\u2018\u2019]/g, "'").includes(q)));
  const played = new Set(state?.played || []);
  return `<div class="panel" style="padding:18px"><h2 style="font-size:18px;margin:0 0 10px">Choose a decision</h2>
    <div class="atlas-tools" style="margin:0 0 12px"><label class="search"><span class="sr-only">Search decisions</span><input id="f-q" type="search" value="${esc(filter.q)}" placeholder="Search title, idea or author"></label>
    <select id="f-track" class="seg" aria-label="Area">${['All', 'AI × Business', 'Business', 'Culture & Society', 'Judgment'].map(t => `<option ${filter.track === t ? 'selected' : ''}>${t}</option>`).join('')}</select>
    <select id="f-format" class="seg" aria-label="Format">${['All', ...new Set(Object.values(FORMAT_NAME))].map(t => `<option ${filter.format === t ? 'selected' : ''}>${t}</option>`).join('')}</select></div>
    <ul class="hist pick-list" id="pick-list">${list.map(c => `<li><span><strong>${esc(c.title)}</strong>${played.has(c.id) ? ' <span class="tag">played</span>' : ''}<br><small>${esc(c.track)}, ${FORMAT_NAME[c.format]}${c.case ? `, case step ${c.case.step} of ${c.case.of}` : ''}. ${esc(c.question)}</small></span><button class="btn btn-quiet" data-open="${c.id}">Open</button></li>`).join('') || '<li>No decision matches.</li>'}</ul></div>`;
}

function stage() {
  const s = state, c = s.challenge ? BY[s.challenge] : null;
  if (!c) return `<div class="panel card"><h2 class="q">Nothing open yet.</h2><p class="scene">Pick a decision on the right. Students see a waiting screen until you open one.</p></div>`;
  const nextInCase = c.case && c.case.step < c.case.of ? LIVE.find(x => x.case && x.case.id === c.case.id && x.case.step === c.case.step + 1) : null;
  const controls = s.phase === 'open' ? `<button class="btn btn-quiet" data-act="close">Stop answers</button><button class="btn btn-solid" data-act="reveal">Reveal to the room</button>`
    : s.phase === 'closed' ? `<button class="btn btn-solid" data-act="reveal">Reveal to the room</button>`
      : `${nextInCase ? `<button class="btn btn-solid" data-open="${nextInCase.id}">Open case step ${nextInCase.case.step}</button>` : ''}<button class="btn btn-quiet" data-act="lobby">Back to waiting screen</button>`;
  return `<div class="panel card">
    <p class="scene">${esc(c.scene)}</p><h2 class="q stage-h" tabindex="-1">${esc(c.question)}</h2><p class="stage-meta"><strong>${{ open: 'Answers are open.', closed: 'Answers are stopped.', revealed: 'Revealed.', lobby: 'Waiting screen.' }[s.phase]}</strong> ${FORMAT_NAME[c.format]}, ${esc(c.track)}${c.case ? `, case step ${c.case.step} of ${c.case.of}` : ''}.</p>
    ${c.format === 'forecast' ? `<blockquote class="claim">${esc(c.forecast.claim)}</blockquote>` : ''}
    ${c.format === 'causal' && c.dag ? `<p class="kicker proj-factors">Factors in play: ${c.dag.nodes.map(n => n.mask && s.phase !== 'revealed' ? '?' : esc(n.label)).join(', ')}</p>` : ''}
    ${['choice', 'causal', 'multi'].includes(c.format) ? `<ol class="present-opts">${order(c).map(o => `<li>${esc(o.t)}</li>`).join('')}</ol>` : ''}
    ${c.format === 'rank' ? `<ul class="present-opts">${shuffle(c.options.map((_, i) => i), rng(hash(c.id + (hash(S.code) >>> 0)))).map(i => `<li>${esc(c.options[i])}</li>`).join('')}</ul>` : ''}${c.format === 'allocate' ? `<ul class="present-opts">${order(c).map(o => `<li>${esc(o.t)}</li>`).join('')}</ul>` : ''}
    ${c.format === 'delegate' ? `<p class="kicker">Route each task to: ${c.delegate.choices.map(esc).join(', ')}</p><ul class="present-opts">${c.delegate.tasks.map(t => `<li>${esc(t.text)}</li>`).join('')}</ul>` : ''}
    <div class="count-row"><b class="num" id="resp-count">${s.responses}</b><span>of ${s.participants} participants answered</span><span class="meter-bar"><i style="width:${s.participants ? Math.round(100 * s.responses / s.participants) : 0}%"></i></span></div>
    <div class="next-row">${controls}</div>
    ${s.phase === 'revealed' && s.aggregate ? (c.answerTitle ? reveal(c, s.aggregate) : '<p class="kicker">Loading the evidence…</p>') : ''}</div>`;
}

function reveal(c, a) {
  const f = c.format; let chart = '';
  const bars = (labels, vals, ev, suffix = '', show = null, scale = null, chips = null) => { const mx = scale || Math.max(1, ...vals); return `<div class="rv-bars">${labels.map((l, i) => `<div class="rv-row"><span>${esc(l)}${chips ? `<em class="rv-chip">${esc(chips[i])}</em>` : ''}</span><span class="rv-track"><i style="width:${vals[i] / mx * 100}%" class="${ev.includes(i) ? 'ev' : ''}"></i></span><b class="num">${show ? show[i] : vals[i] + suffix}</b></div>`).join('')}</div>` };
  if (a.counts) { const o = order(c); chart = bars(o.map(x => x.t), o.map(x => a.counts[x.i]), o.map((x, k) => (f === 'multi' ? c.multiAnswers.includes(x.i) : x.i === c.answer) ? k : -1).filter(k => k >= 0), '', o.map(x => `${a.counts[x.i]} of ${a.n}`), Math.max(1, a.n)) }
  // The class's answers as stacked dots on one axis, with the study's value and the hit band marked on it (review 26, Tufte: one scale, the comparison drawn)
  const dotStrip = (a, ev, band, unit, evText) => { const W = 900, L = 24, R = W - 24, base = 180, top = 72, sx = v => L + (Math.min(a.hi, Math.max(a.lo, v)) - a.lo) / (a.hi - a.lo) * (R - L), m = x => String(x).replace(/^-/, '\u2212') + unit;
    // every answer at its own value (audit 31, M4): stacked dots while they fit the height, bars with counts when a class is too large for dots
    const pts = a.points || a.hist.map((n, i) => [a.lo + (i + .5) * (a.hi - a.lo) / a.hist.length, n]), mx = Math.max(1, ...pts.map(p => p[1])), xs = pts.map(p => sx(p[0])), gap = Math.min(40, ...xs.slice(1).map((x, i) => x - xs[i]).filter(d => d > 0));
    const r = Math.min(9, (base - top) / (2 * mx), gap / 2);
    const marks = r >= 2.5 ? pts.flatMap(([v, n]) => Array.from({ length: n }, (_, k) => `<circle cx="${sx(v)}" cy="${base - r - k * 2 * r}" r="${Math.max(1.5, r - .8)}" class="ds-dot"/>`)).join('')
      : pts.map(([v, n]) => { const h = Math.max(4, n / mx * (base - top)), bw = Math.max(2, Math.min(12, gap * .8)); return `<rect x="${sx(v) - bw / 2}" y="${base - h}" width="${bw}" height="${h}" class="ds-dot"/>${n === mx ? `<text x="${Math.min(R - 24, Math.max(L + 24, sx(v)))}" y="${base - h - 8}" text-anchor="middle" class="ds-tick">${n}</text>` : ''}` }).join('');
    const b0 = band != null ? Math.max(a.lo, ev - band) : null, b1 = band != null ? Math.min(a.hi, ev + band) : null;
    const bandRect = band != null ? `<rect x="${sx(b0)}" y="${top - 8}" width="${sx(b1) - sx(b0)}" height="${base - top + 8}" class="ds-band"/>` : '';
    const ex = sx(ev), anc = ex > R - 200 ? 'end' : ex < L + 200 ? 'start' : 'middle';
    return `<svg class="dot-strip" viewBox="0 0 ${W} 235" role="img" aria-label="${esc(`Class answers, ${a.n} in all, median ${m(a.median)}; ${evText}${band != null ? `, hit band ${m(+b0.toFixed(1))} to ${m(+b1.toFixed(1))}` : ''}`)}">${bandRect}${marks}<line x1="${L}" y1="${base}" x2="${R}" y2="${base}" class="ds-axis"/><line x1="${ex}" y1="${top - 8}" x2="${ex}" y2="${base}" class="ds-ev"/><text x="${ex}" y="32" text-anchor="${anc}" class="ds-evl">${esc(evText)}</text>${a.median != null ? `<line x1="${sx(a.median)}" y1="${base}" x2="${sx(a.median)}" y2="${base + 12}" class="ds-med"/><text x="${sx(a.median)}" y="${base + 40}" text-anchor="${sx(a.median) < L + 110 ? 'start' : sx(a.median) > R - 110 ? 'end' : 'middle'}" class="ds-medl">class median ${esc(m(a.median))}</text>` : ''}${a.median == null || sx(a.median) - L > 150 ? `<text x="${L}" y="${base + 40}" class="ds-tick">${esc(m(a.lo))}</text>` : ''}${a.median == null || R - sx(a.median) > 150 ? `<text x="${R}" y="${base + 40}" text-anchor="end" class="ds-tick">${esc(m(a.hi))}</text>` : ''}</svg>` };
  if (a.hist && f === 'estimate') { const e = c.estimate, u = e.unit ?? '%'; chart = dotStrip(a, e.target, e.tolerance ?? null, u, `Study ${String(e.target).replace(/^-/, '\u2212')}${u}`) }
  else if (a.hist) { const ev = f === 'estimate' ? c.estimate.target : c.forecast.truth ? 100 : 0, w = (a.hi - a.lo) / a.hist.length; chart = bars(a.hist.map((_, i) => `${Math.round(a.lo + i * w)} to ${Math.round(a.lo + (i + 1) * w)}`), a.hist, [Math.min(a.hist.length - 1, Math.floor((ev - a.lo) / w))], '', null, Math.max(1, a.n)) + `<p class="kicker">Class median ${a.median}. Evidence: ${f === 'estimate' ? c.estimate.target + (c.estimate.unit ?? '%') : c.forecast.truth ? 'the claim is true' : 'the claim is false'}.</p>` }
  if (a.meanPosition) chart = `<ol class="rank-proj">${c.rankAnswer.map((i, k) => `<li><span class="rp-badge">${k + 1}</span><span class="rp-name">${esc(c.options[i])}</span><span class="rp-room">Room <b class="num">${a.meanPosition[i] == null ? '–' : a.meanPosition[i]}</b></span></li>`).join('')}</ol><p class="kicker">Numbered in the study's measured order; "Room" is the class's average rank (1 = top).${(c.rankTies || []).length ? ' Not separated by the study: ' + c.rankTies.map(t => t.map(i => esc(c.options[i])).join(' and ')).join('; ') + '.' : ''}</p>`;
  if (a.meanShare) { const o = order(c), best = c.allocate.best || [c.allocate.values.indexOf(Math.max(...c.allocate.values))]; chart = bars(o.map(x => x.t), o.map(x => a.meanShare[x.i]), o.map((x, k) => best.includes(x.i) ? k : -1).filter(k => k >= 0), '%', null, 100) + `<p class="kicker">Average share of the budget. Reported effects: ${c.options.map((o, i) => { const v = String(c.allocate.valueLabels ? c.allocate.valueLabels[i] : c.allocate.values[i]); return esc(o) + (/^baseline$/i.test(v) ? ' (baseline)' : ' ' + esc(v.replace('(n.s.)', ', not significant').replace(' ,', ','))) }).join('; ')}.</p>` }
  if (a.taskCounts) { const right = c.delegate.tasks.map((t, i) => [t.answer, ...(t.also || [])].reduce((x, j) => x + (a.taskCounts[i][j] || 0), 0)), tot = a.taskCounts.map(r => Object.values(r).reduce((x, y) => x + (y || 0), 0)), n = Math.max(1, ...tot);
    chart = bars(c.delegate.tasks.map(t => t.text), right, c.delegate.tasks.map((_, i) => i), '', right.map((r, i) => `${r} of ${tot[i]}`), n, c.delegate.tasks.map(t => 'Evidence: ' + [t.answer, ...(t.also || [])].map(j => c.delegate.choices[j]).join(' or '))) + `<p class="kicker">How many routed each task the way the evidence suggests.</p>` }
  const s = BANK.sources[c.sources[0]];
  return `<div class="rv"><h3 class="reveal-title rv-lead">${esc(c.answerTitle)}</h3><div class="rv-head"><div><span class="kicker">The room</span><b class="num">${a.n}</b><span>${a.n === 1 ? 'answer' : 'answers'}</span></div><div><span class="kicker">${({ allocate: 'Most points on the best option', delegate: 'Routed every task as the evidence suggests', rank: 'Exact order' })[c.format] || 'Matched the evidence'}</span><b class="num">${a.shareCorrect ?? 0}%</b></div><div><span class="kicker">Average score</span><b class="num">${a.meanScore === null || a.meanScore === undefined ? '–' : String(a.meanScore).replace(/^-/, '\u2212')}</b></div>${a.meanConfidence !== null && a.meanConfidence !== undefined ? `<div><span class="kicker">Average confidence</span><b class="num">${a.meanConfidence}%</b></div>` : ''}</div>${chart ? `<div class="rv-chart">${chart}</div>` : ''}
    <p class="reveal-body">${esc(c.explain)}</p>
    <div class="lessons"><div class="lesson"><h3>Discussion prompt</h3><p>${esc(c.implication)} Where would this fail in your organization?</p></div><div class="lesson"><h3>Where the evidence comes from</h3><p>${esc(c.boundary)}</p></div></div><p class="kicker">${esc(s.authors)} (${s.year}), ${esc(s.venue)}.</p></div>`;
}

let showPicker = false;
const live = () => state && (state.phase === 'open' || state.phase === 'closed');
function console_() {
  return `<section class="wrap" style="padding-top:22px;padding-bottom:64px"><h1 class="sr-only">Live class ${esc(S.code)}</h1>
    <div class="join-banner panel"><div class="join-text"><span class="kicker">Students join at</span><strong class="join-url">${esc(location.host)}</strong><span class="kicker">with code</span><strong class="join-code" aria-label="Session code ${esc(S.code.split('').join(' '))}">${esc(S.code)}</strong>${S.title ? `<span class="kicker">${esc(S.title)}</span>` : ''}</div><div class="join-end"><button class="btn btn-quiet proj-exit" data-act="projector">Exit projector view</button>${qr(joinURL())}</div></div>
    <div class="play-grid" style="margin-top:16px">${stage()}<div class="side" style="top:16px">${live() && !showPicker ? `<div class="panel" style="padding:18px"><p style="margin:0 0 10px">The decision list is hidden while answers are live, so the projector shows only the question.</p><button class="btn btn-quiet" data-act="picker">Show the decision list</button></div>` : picker()}<div class="panel" style="padding:18px;display:flex;gap:8px;flex-wrap:wrap"><button class="btn btn-quiet" data-act="joining" aria-pressed="${state && state.joining === false ? 'true' : 'false'}">${state && state.joining === false ? 'Reopen joining' : 'Close joining'}</button><button class="btn btn-quiet" data-act="projector">Projector view</button><button class="btn btn-quiet" data-act="csv">Download answers (CSV)</button><button class="btn btn-quiet" data-act="copy">Copy join link</button><button class="btn btn-quiet" data-act="end">End session and delete data</button></div></div></div></section>`;
}

function render() { qs('#view').innerHTML = S ? (state ? console_() : '<p class="wrap" style="padding:40px 0">Connecting…</p>') : setup() }
function focusKey(el) { if (!el || el === document.body) return null; if (el.id) return '#' + el.id; for (const k of ['act', 'open']) if (el.dataset && el.dataset[k]) return `[data-${k}="${el.dataset[k]}"]`; return null }
function rerender() { const key = focusKey(document.activeElement), pos = qs('#pick-list')?.scrollTop, sel = document.activeElement?.selectionStart; render(); const pl = qs('#pick-list'); if (pos && pl) pl.scrollTop = pos; const el = key && qs(key); if (el) { el.focus({ preventScroll: true }); if (sel !== undefined && el.setSelectionRange) try { el.setSelectionRange(sel, sel) } catch { } } }
async function poll() {
  if (!S) return;
  try {
    const d = await api('/api/rooms/' + S.code + (etag ? '?v=' + encodeURIComponent(etag) : ''));
    if (!d.same) { state = d; etag = d.etag || ''; if (d.evidence && BY[d.evidence.id]) Object.assign(BY[d.evidence.id], d.evidence); if (!fullLoaded) loadFull(); rerender() }
  }
  catch (e) { if (/No session/.test(e.message)) { sessionStorage.removeItem('thv:session'); S = null; state = null; render(); toast('That session no longer exists.'); return } }
  clearTimeout(timer); timer = setTimeout(poll, state && state.phase === 'open' ? 1500 : 3000);
}
async function control(action, challenge) { try { state = await api(`/api/rooms/${S.code}/control`, { action, challenge }); etag = ''; rerender(); const h = qs('.stage-h'); if (action === 'open' && h) h.focus() } catch (e) { toast(e.message) } }

document.addEventListener('submit', async e => {
  if (e.target.dataset.form !== 'create') return; e.preventDefault();
  try { const d = await api('/api/rooms', { title: qs('#title').value, passcode: qs('#pass').value }); S = d; sessionStorage.setItem('thv:session', JSON.stringify(d)); render(); poll() } catch (err) { toast(err.message) }
});
document.addEventListener('click', async e => {
  const b = e.target.closest('button'); if (!b) return;
  if (b.dataset.open) { showPicker = false; await control('open', b.dataset.open); return }
  const a = b.dataset.act;
  if (a === 'close' || a === 'reveal' || a === 'lobby') { showPicker = false; await control(a); return }
  if (a === 'projector') { document.body.classList.toggle('projector'); const on = document.body.classList.contains('projector'); document.querySelectorAll('[data-act=projector]').forEach(x => x.textContent = on ? 'Exit projector view' : 'Projector view'); if (on) { scrollTo(0, 0); qs('.stage-h')?.focus({ preventScroll: true }) } return }
  if (a === 'picker') { showPicker = true; rerender(); qs('#f-q')?.focus(); return }
  if (a === 'joining') { await control(state && state.joining === false ? 'unlockjoin' : 'lockjoin'); toast(state && state.joining === false ? 'Joining closed. Students already in can keep answering.' : 'Joining is open again.'); return }
  if (a === 'copy') { try { await navigator.clipboard.writeText(joinURL()); toast('Join link copied.') } catch { toast(joinURL()) } return }
  if (a === 'csv') { try { const r = await fetch(`/api/rooms/${S.code}/export.csv`, { headers: { 'X-Instructor-Key': S.secret, 'X-Client-Id': cid } }); if (!r.ok) throw Error('Export failed'); const blob = await r.blob(); const u = URL.createObjectURL(blob); const l = document.createElement('a'); l.href = u; l.download = `human-variable-${S.code}.csv`; document.body.append(l); l.click(); l.remove(); setTimeout(() => URL.revokeObjectURL(u), 3000) } catch (err) { toast(err.message) } return }
  if (a === 'end') { if (!confirm('End the session for everyone and delete all answers? Download the CSV first if you need it.')) return; await control('end'); sessionStorage.removeItem('thv:session'); S = null; state = null; clearTimeout(timer); render(); toast('Session ended. All answers deleted.'); return }
});
document.addEventListener('input', e => { if (e.target.id === 'f-q') { filter.q = e.target.value; const tmp = document.createElement('div'); tmp.innerHTML = picker(); qs('#pick-list')?.replaceWith(tmp.querySelector('#pick-list')) } });
document.addEventListener('change', e => { if (e.target.id === 'f-track') { filter.track = e.target.value; render() } if (e.target.id === 'f-format') { filter.format = e.target.value; render() } });
if (!location.protocol.startsWith('http')) { qs('#view').innerHTML = '<section class="wrap" style="padding:48px 0"><h1 class="q">The live classroom needs the server.</h1><p class="scene">Run <code>python start_classroom.py</code> in the project folder and open http://localhost:8502/classroom, or use your hosted address.</p></section>' }
else { render(); if (S) poll() }
})();
