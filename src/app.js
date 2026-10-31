(() => {
'use strict';
// ---------- data ----------
const S = window.THVScore;
const SOURCE = BANK.sources;
const isLive = s => s && s.verification && s.verification.status !== 'quarantined';
// Scored play uses only challenges whose every source passed the audit.
const ALL = BANK.challenges.filter(c => c.sources.every(id => isLive(SOURCE[id])));
const BY_ID = Object.fromEntries(BANK.challenges.map(c => [c.id, c]));
const TRACKS = ['AI × Business', 'Business', 'Culture & Society', 'Judgment'];
const TRACK_NOTE = {
  'AI × Business': 'Adoption, delegation, trust in algorithms',
  'Business': 'Defaults, framing, pricing, hiring',
  'Culture & Society': 'Norms, polarization, contagion',
  'Judgment': 'Forecasts, anchors, confidence'
};
const FORMAT_NAME = { choice: 'Call it', causal: 'Find the cause', multi: 'Pick two', estimate: 'Estimate', forecast: 'Forecast', rank: 'Rank', allocate: 'Allocate', delegate: 'Delegate' };

// ---------- helpers ----------
const qs = s => document.querySelector(s);
const qa = s => [...document.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const pct = x => Math.round(x * 100);
function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619); return h >>> 0 }
function rng(seed) { let x = seed >>> 0; return () => { x += 0x6D2B79F5; let t = x; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296 } }
function shuffle(a, r) { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
const store = {
  get(k, d) { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d } catch { return d } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)) } catch { } },
  del(k) { try { localStorage.removeItem(k) } catch { } }
};
function cite(id) { const s = SOURCE[id]; return s ? `${s.authors} (${s.year})` : id }
function srcStatus(s) { const v = s.verification || {}; return v.status === 'verified_full_text' ? ['Checked against full text', ''] : ['Checked against published abstract', 'abstract'] }

// ---------- state ----------
const PARAM = new URLSearchParams(location.search);
const REC_KEY = 'thv:v2:records', NOTE_KEY = 'thv:v1:notes';
let records = store.get(REC_KEY, null);
if (!Array.isArray(records)) { // migrate v1 records (binary correct + confidence) once
  records = (store.get('thv:v1:results', []) || []).filter(r => r && BY_ID[r.id] && typeof r.correct === 'boolean').map(r => ({ id: r.id, format: BY_ID[r.id].format, score: r.correct ? 1 : 0, correct: r.correct, confidence: r.confidence, at: r.at, seed: r.seed }));
  store.set(REC_KEY, records);
}
records = records.filter(r => r && typeof r.id === 'string' && BY_ID[r.id]).slice(-3000);
let notes = store.get(NOTE_KEY, {}); if (!notes || typeof notes !== 'object' || Array.isArray(notes)) notes = {};

const st = {
  view: 'home', track: TRACKS.includes(PARAM.get('track')) ? PARAM.get('track') : 'Mixed', length: [5, 8, 12].includes(+PARAM.get('n')) ? +PARAM.get('n') : 8,
  seed: (Number(PARAM.get('seed')) || Math.floor(Math.random() * 2147483647)) >>> 0,
  deck: [], i: 0, phase: 'predict', resp: null, touched: false, conf: 60, confTouched: false, session: [],
  atlasTrack: 'All', atlasQuery: '', atlasFormat: 'All', tutor: { busy: false, text: '', cites: [] }, menu: false,
  hero: { value: null, done: false }, room: null
};
const card = () => st.deck[st.i];

// ---------- deck ----------
// Cases (multi-step scenarios) stay together and in order.
function buildDeck(pool, n, seed) {
  const units = []; const seen = new Set();
  for (const c of pool) {
    if (c.case) { if (seen.has(c.case.id)) continue; seen.add(c.case.id); units.push(pool.filter(x => x.case && x.case.id === c.case.id).sort((a, b) => a.case.step - b.case.step)) }
    else units.push([c]);
  }
  const out = [];
  for (const u of shuffle(units, rng(seed))) { if (out.length >= n) break; out.push(...u) }
  return out;
}
function start(pool, n) {
  st.deck = buildDeck(pool, n, st.seed); st.i = 0; st.session = []; resetCard(); st.view = 'play'; render(true);
}
function startTrack() { const pool = st.track === 'Mixed' ? ALL : ALL.filter(c => c.track === st.track); start(pool.length ? pool : ALL, st.length) }
function resetCard() {
  const c = card(); st.tab = 'questions'; st.phase = 'predict'; st.touched = false; st.conf = 60; st.confTouched = false; st.tutor = { busy: false, text: '', cites: [] };
  if (!c) { st.resp = null; return }
  st.resp = c.format === 'multi' ? [] : c.format === 'rank' ? shuffle(c.options.map((_, i) => i), rng(hash(c.id + st.seed))) :
    c.format === 'allocate' ? evenSplit(c) : c.format === 'delegate' ? c.delegate.tasks.map(() => null) :
      c.format === 'forecast' ? 50 : c.format === 'estimate' ? null : null;
  if (c.format === 'rank' && S.score(c, st.resp).correct) st.resp.reverse(); // never start on the answer
}
function evenSplit(c) { const k = c.options.length, t = c.allocate.total, step = c.allocate.step || 10; const base = Math.floor(t / k / step) * step; const a = Array(k).fill(base); let rest = t - base * k; for (let i = 0; rest > 0; i = (i + 1) % k) { a[i] += step; rest -= step } return a }
function optionOrder(c) { return shuffle(c.options.map((t, i) => ({ t, i })), rng(hash(c.id + '-' + st.seed))) }

function lock() {
  const c = card(); if (!c || !S.ready(c, st.resp)) return;
  if (c.format === 'forecast' && !st.touched) { notice('Move the slider to state a probability first.'); return }
  const res = S.score(c, st.resp);
  const rec = { id: c.id, format: c.format, score: Math.round(res.score * 1000) / 1000, correct: res.correct, confidence: c.format === 'forecast' ? null : st.conf, response: st.resp, at: new Date().toISOString(), seed: st.seed, detail: res.detail };
  st.session.push(rec); records.push(rec); records = records.slice(-3000); store.set(REC_KEY, records);
  st.phase = 'reveal'; render(true);
  if (st.room) roomSubmit(c, rec);
}
function next() { if (st.i >= st.deck.length - 1) { st.view = 'record'; st.deck = []; render(true); return } st.i++; resetCard(); render(true) }

// ---------- views ----------
const glyph = `<svg class="brand-glyph" viewBox="0 0 26 26" aria-hidden="true"><rect x="1" y="1" width="24" height="24" rx="7" fill="#14203a"/><line x1="6" y1="17" x2="20" y2="17" stroke="#cbd3dd" stroke-width="1.5"/><circle cx="9.5" cy="17" r="3" fill="#2f54eb"/><circle cx="16.5" cy="17" r="3" fill="#e0a01c"/><path d="M9.5 12.5V8.5M16.5 12.5V8.5" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>`;

function heroTry() {
  const c = BY_ID.ai01; if (!c || !isLive(SOURCE[c.sources[0]])) return '';
  const h = st.hero, e = c.estimate, v = h.value, src = SOURCE[c.sources[0]];
  const gap = v === null ? 0 : Math.abs(v - e.target);
  return `<section class="panel try" aria-labelledby="try-q">
    <span class="kicker">Try one now</span>
    <h2 id="try-q">Professionals were randomly given ChatGPT for short writing tasks. How much less time did they take?</h2>
    ${h.done ? `<div class="try-axis">${gapAxis({ min: e.min, max: e.max, unit: '%', you: v, ev: e.target, band: e.tolerance, evLabel: 'Study', id: 'hero' })}</div>`
      : `<div class="try-read"><b class="num ${v === null ? 'empty' : ''}" id="hero-read">${v === null ? '?' : v + '%'}</b><span>less time</span></div>
    <label class="sr-only" for="hero-range">Your estimate of the time saved, in percent</label>
    <input id="hero-range" type="range" min="${e.min}" max="${e.max}" step="1" value="${v ?? Math.round((e.min + e.max) / 2)}" class="${v === null ? 'untouched' : ''}" style="--fill:${v === null ? 0 : (v - e.min) / (e.max - e.min) * 100}%">
    <div class="axis"><span>${e.min}%</span><span>${e.max}%</span></div>`}
    <p class="try-result" aria-live="polite">${h.done ? `They took ${e.target}% less time, and graders rated the work 18% better. ${gap === 0 ? 'You were exactly right.' : `You were ${gap} points off.`}` : ''}</p>
    <div class="try-foot">${h.done ? `<button class="btn btn-solid" data-act="start-quick">Play five more</button><button class="link-btn" data-act="hero-reset">Try again</button>` : `<button class="btn btn-you" data-act="hero-lock" ${v === null ? 'disabled' : ''}>Lock my estimate</button>`}<span class="try-src">${esc(src.authors)}, ${esc(src.venue)} ${src.year}</span></div>
  </section>`;
}

function home() {
  const nSrc = Object.values(SOURCE).filter(isLive).length;
  const dimant = Object.values(SOURCE).filter(s => isLive(s) && /Dimant/.test(s.authors));
  const paths = (BANK.paths || []).map(p => ({ ...p, items: p.ids.filter(id => ALL.some(c => c.id === id)) })).filter(p => p.items.length);
  const done = new Set(records.map(r => r.id));
  return `<section class="hero wrap"><div class="hero-grid">
    <div><h1>Predict what people do. Then see the evidence.</h1>
    <p class="hero-lede">Bet on the outcome of a real experiment on AI, work and human behavior. Then see how far your call landed from the result, and what a manager should do about it.</p>
    <div class="hero-actions"><button class="btn btn-solid btn-lg" data-act="go-start">Start playing</button>${location.protocol.startsWith('http') ? '<button class="link-btn" data-act="join">Join a live class</button>' : ''}</div>
    <p class="hero-meta">${ALL.length} decisions from ${nSrc} peer-reviewed studies. Original concept by Eugen Dimant.</p></div>
    ${heroTry()}</div></section>
  <section class="section wrap" id="start" aria-labelledby="paths-h"><div class="row-head"><h2 id="paths-h">Choose a path</h2><button class="link-btn" data-act="toggle-custom" aria-expanded="${st.custom ? 'true' : 'false'}">${st.custom ? 'Hide custom round' : 'Or build a custom round'}</button></div>
    ${st.custom ? customRound() : ''}
    <div class="paths">${paths.map(p => { const n = p.items.filter(id => done.has(id)).length; return `<button class="path" data-path="${esc(p.id)}">${p.case ? '<em class="path-flag">Start here</em>' : ''}<strong>${esc(p.title)}</strong><span>${esc(p.blurb)}</span><small>${p.items.length} decisions${p.case ? ', with a multi-step case' : ''}${n ? `. ${n} played` : ''}</small><i class="path-bar" style="--p:${Math.round(100 * n / p.items.length)}%"></i></button>` }).join('')}</div>
  </section>
  ${dimant.length ? `<section class="section wrap dimant-band"><div class="dimant"><div><h2>Research by Eugen Dimant</h2><p>How the shape of a norm, the visibility of peers and political identity change what people do at work and in society.</p><button class="btn btn-line" data-path="dimant-lab">Play this path</button></div>
    <ul class="paper-list">${dimant.slice(0, 6).map(s => `<li><button data-source="${esc(s.id)}"><strong>${esc(s.title)}</strong><small>${esc(s.venue)}, ${s.year}</small></button></li>`).join('')}</ul></div></section>` : ''}`;
}
function customRound() {
  const counts = Object.fromEntries(TRACKS.map(t => [t, ALL.filter(c => c.track === t).length]));
  return `<div class="custom panel"><div class="custom-row" role="group" aria-label="Area"><span class="kicker">Area</span>${['Mixed', ...TRACKS].map(t => `<button class="seg" data-track="${esc(t)}" aria-pressed="${st.track === t}">${esc(t === 'Mixed' ? 'All areas' : t)}${t === 'Mixed' ? '' : ` <small>${counts[t]}</small>`}</button>`).join('')}</div>
    <div class="custom-row" role="group" aria-label="Length"><span class="kicker">Length</span>${[[5, '5 decisions'], [8, '8 decisions'], [12, '12 decisions']].map(([n, l]) => `<button class="seg" data-length="${n}" aria-pressed="${st.length === n}">${l}</button>`).join('')}<button class="btn btn-solid" data-act="start">Start</button></div></div>`;
}
// ----- play -----
function instrument(c) {
  const r = st.resp, rev = st.phase === 'reveal';
  if (c.format === 'choice' || c.format === 'causal' || c.format === 'multi') {
    const isEv = i => c.format === 'multi' ? c.multiAnswers.includes(i) : i === c.answer;
    const picked = i => Array.isArray(r) ? r.includes(i) : r === i;
    return `${c.format === 'causal' && c.dag ? dag(c.dag) : ''}<div class="opts" role="group" aria-label="Answer options">${optionOrder(c).map((o, j) => `<button class="opt ${rev && isEv(o.i) ? 'is-ev' : ''}" data-choice="${o.i}" aria-pressed="${picked(o.i)}" ${rev ? 'disabled' : ''}><span class="k" aria-hidden="true">${j + 1}</span><span>${esc(o.t)}</span>${rev && (isEv(o.i) || picked(o.i)) ? `<span class="mark">${picked(o.i) ? '<span class="dot dot-you"></span>Your call' : ''}${isEv(o.i) ? '<span class="dot dot-ev"></span>Evidence' : ''}</span>` : ''}</button>`).join('')}</div>`;
  }
  if (c.format === 'estimate') {
    const e = c.estimate, v = r ?? Math.round((e.min + e.max) / 2);
    return `<div class="meter"><div class="meter-read"><span class="kicker" id="est-label">${esc(e.label)}</span><b class="${r === null ? 'empty' : ''}" id="est-read">${r === null ? '—' : r + (e.unit ?? '%')}</b></div>
      <input type="range" id="est" aria-labelledby="est-label" min="${e.min}" max="${e.max}" step="${e.step || 1}" value="${v}" class="${r === null ? 'untouched' : ''}" style="--fill:${r === null ? 0 : (v - e.min) / (e.max - e.min) * 100}%" ${rev ? 'disabled' : ''}>
      <div class="axis"><span>${e.min}${e.unit ?? '%'}</span><span>${e.max}${e.unit ?? '%'}</span></div></div>`;
  }
  if (c.format === 'forecast') {
    return `<div class="meter"><div class="meter-read"><span class="kicker" id="fc-label">Probability the claim is true</span><b class="${st.touched ? '' : 'empty'}" id="fc-read">${st.touched ? r + '%' : '—'}</b></div>
      <input type="range" id="fc" aria-labelledby="fc-label" min="0" max="100" step="5" value="${r}" class="${st.touched ? '' : 'untouched'}" style="--fill:${st.touched ? r : 0}%" ${rev ? 'disabled' : ''}>
      <div class="axis"><span>0%, certainly false</span><span>100%, certainly true</span></div></div>`;
  }
  if (c.format === 'rank') {
    return `<p class="hint">${esc(c.rankLabel)}. Use the arrows to reorder.</p><ol class="rank-list">${r.map((oi, k) => `<li class="rank-item"><span class="pos">${k + 1}</span><span>${esc(c.options[oi])}</span><span class="rank-move"><button data-rank="${k}" data-dir="-1" aria-label="Move ${esc(c.options[oi])} up" ${k === 0 || rev ? 'disabled' : ''}>↑</button><button data-rank="${k}" data-dir="1" aria-label="Move ${esc(c.options[oi])} down" ${k === r.length - 1 || rev ? 'disabled' : ''}>↓</button></span></li>`).join('')}</ol>`;
  }
  if (c.format === 'allocate') {
    const a = c.allocate, sum = r.reduce((x, y) => x + y, 0);
    return `<div class="alloc">${c.options.map((o, k) => `<div class="alloc-row"><label for="al${k}">${esc(o)}</label><input type="range" id="al${k}" data-alloc="${k}" min="0" max="${a.total}" step="${a.step || 10}" value="${r[k]}" style="--fill:${r[k] / a.total * 100}%" ${rev ? 'disabled' : ''}><output for="al${k}" class="num">${a.prefix || ''}${r[k]}${a.suffix || ''}</output></div>`).join('')}
      <div class="alloc-total ${sum === a.total ? 'ok' : ''}" aria-live="polite"><span>${esc(a.label)}</span><span class="num">${a.prefix || ''}${sum}${a.suffix || ''} of ${a.prefix || ''}${a.total}${a.suffix || ''}${sum === a.total ? '' : sum > a.total ? ', over budget' : ', unassigned'}</span></div></div>`;
  }
  if (c.format === 'delegate') {
    return `<div class="deleg">${c.delegate.tasks.map((t, k) => `<div class="deleg-row" role="group" aria-label="${esc(t.text)}"><p>${esc(t.text)}</p><div class="deleg-opts">${c.delegate.choices.map((ch, m) => `<button data-deleg="${k}" data-pick="${m}" aria-pressed="${r[k] === m}" class="${rev && t.answer === m ? 'is-ev' : ''}" ${rev ? 'disabled' : ''}>${esc(ch)}</button>`).join('')}</div>${rev ? `<p class="deleg-why">${r[k] === t.answer ? 'Matches the evidence. ' : 'Evidence points to ' + esc(c.delegate.choices[t.answer]) + '. '}${esc(t.why)}</p>` : ''}</div>`).join('')}</div>`;
  }
  return '';
}

function dag(d) {
  const W = 520, H = d.height || 200;
  const node = Object.fromEntries(d.nodes.map(n => [n.id, n]));
  const edge = ([a, b, style]) => { const A = node[a], B = node[b]; const dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L; const pad = 72; return `<line x1="${A.x + ux * pad}" y1="${A.y + uy * pad * .45}" x2="${B.x - ux * pad}" y2="${B.y - uy * pad * .45}" stroke="${style === 'q' ? '#9aa6b6' : '#14203a'}" stroke-width="2" ${style === 'q' ? 'stroke-dasharray="5 5"' : ''} marker-end="url(#ah)"/>` };
  return `<svg class="dag" viewBox="0 0 ${W} ${H}" role="img" aria-label="${esc(d.alt)}"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#14203a"/></marker></defs>${d.edges.map(edge).join('')}${d.nodes.map(n => `<g><rect x="${n.x - 70}" y="${n.y - 24}" width="140" height="48" rx="24" fill="${n.hidden ? '#fff' : '#14203a'}" stroke="#14203a" stroke-width="1.5" ${n.hidden ? 'stroke-dasharray="4 4"' : ''}/><text x="${n.x}" y="${n.y + 5}" text-anchor="middle" font-size="17" font-weight="650" font-family="Schibsted Grotesk,system-ui" fill="${n.hidden ? '#14203a' : '#fff'}">${esc(n.label)}</text></g>`).join('')}</svg>`;
}

// The gap: player's call (blue) and the evidence (amber) on one axis.
function gapAxis({ min, max, unit = '%', you, ev, band, evLabel = 'Evidence', id = 'g', fmt = x => x + unit }) {
  const narrow = innerWidth < 640, W = narrow ? 360 : 640, fs = narrow ? 14 : 19, L = 18, R = W - 18, y = 52, sx = v => L + (v - min) / (max - min) * (R - L);
  const has = v => v !== null && v !== undefined;
  const anchor = x => x < L + (narrow ? 40 : 60) ? 'start' : x > R - (narrow ? 40 : 60) ? 'end' : 'middle';
  const lab = (x, txt, color, up) => `<text x="${Math.min(R, Math.max(L, x))}" y="${up ? y - 22 : y + 36}" text-anchor="${anchor(x)}" font-size="${fs}" font-weight="750" fill="${color}" font-family="Schibsted Grotesk,system-ui">${esc(txt)}</text>`;
  return `<svg class="axis-svg" viewBox="0 0 ${W} 118" role="img" aria-label="${has(you) ? 'Your call ' + fmt(you) : 'No call yet'}${has(ev) ? ', evidence ' + fmt(ev) : ''}">
    <line x1="${L}" y1="${y}" x2="${R}" y2="${y}" stroke="#cbd3dd" stroke-width="8" stroke-linecap="round"/>
    ${has(band) && has(ev) ? `<rect x="${sx(Math.max(min, ev - band))}" y="${y - 9}" width="${sx(Math.min(max, ev + band)) - sx(Math.max(min, ev - band))}" height="18" rx="4" fill="#fbefd2" stroke="#e0a01c" stroke-width="1.2"/>` : ''}
    ${has(you) && has(ev) ? `<line x1="${sx(you)}" y1="${y}" x2="${sx(ev)}" y2="${y}" stroke="#14203a" stroke-width="2.5" stroke-dasharray="3 4"/>` : ''}
    ${has(you) ? `<circle cx="${sx(you)}" cy="${y}" r="12" fill="#2f54eb" stroke="#fff" stroke-width="3"/>${lab(sx(you), 'You ' + fmt(you), '#1f3cc2', true)}` : ''}
    ${has(ev) ? `<g class="ev-mark" id="${id}-ev" data-from="${has(you) ? sx(you) - sx(ev) : 0}"><circle cx="${sx(ev)}" cy="${y}" r="12" fill="#e0a01c" stroke="#fff" stroke-width="3"/>${lab(sx(ev), evLabel + ' ' + fmt(ev), '#7d5200', false)}</g>` : ''}
    <text x="${L}" y="114" font-size="${narrow ? 12 : 14}" fill="#56617a" font-family="Schibsted Grotesk,system-ui">${esc(fmt(min))}</text><text x="${R}" y="114" font-size="${narrow ? 12 : 14}" fill="#56617a" text-anchor="end" font-family="Schibsted Grotesk,system-ui">${esc(fmt(max))}</text></svg>`;
}

function gapFigure(c, rec) {
  const r = rec.response; let body = '', cap = '';
  if (c.format === 'estimate') { const e = c.estimate; body = gapAxis({ min: e.min, max: e.max, unit: e.unit ?? '%', you: r, ev: e.target, band: e.tolerance, evLabel: 'Study' }); cap = `Shaded band: within ${e.tolerance}${e.unit ?? '%'} of the study value counts as a hit. You were ${rec.detail.gap}${e.unit ?? '%'} away.` }
  else if (c.format === 'forecast') { body = gapAxis({ min: 0, max: 100, you: r, ev: c.forecast.truth ? 100 : 0, evLabel: c.forecast.truth ? 'True' : 'False', fmt: x => x + '%' }); cap = `Brier score ${rec.detail.brier.toFixed(2)} (0 is perfect, 0.25 is a coin flip at 50%, 1 is confidently wrong).` }
  else if (c.format === 'rank') {
    const truth = c.rankAnswer;
    body = `<ol class="rank-cmp">${truth.map((oi, t) => { const k = r.indexOf(oi); return `<li><span class="rc-name">${esc(c.options[oi])}${c.rankValues ? `<small>${esc(c.rankValues[oi])}</small>` : ''}</span><span class="rc-badge ev" title="Measured rank">${t + 1}</span><span class="rc-badge you ${k === t ? 'same' : ''}" title="Your rank">${k + 1}</span></li>` }).join('')}</ol><div class="rc-head"><span>Measured order, top first</span><span><i class="dot dot-ev"></i>Study <i class="dot dot-you"></i>You</span></div>`;
    cap = `${rec.detail.agree} of ${rec.detail.total} pairs in the measured order.`
  }
  else if (c.format === 'allocate') {
    const a = c.allocate, tot = r.reduce((x, y) => x + y, 0) || 1, mx = Math.max(...a.values);
    body = `<svg viewBox="0 0 340 ${c.options.length * 58 + 10}" role="img" aria-label="Your allocation compared with reported effects">${c.options.map((o, k) => { const y = 8 + k * 58; return `<text x="0" y="${y + 10}" font-size="12" font-weight="650" fill="#14203a">${esc(short(o, 44))}</text><rect x="0" y="${y + 17}" width="${Math.max(2, r[k] / tot * 250)}" height="10" rx="5" fill="#2f54eb"/><text x="${Math.max(2, r[k] / tot * 250) + 6}" y="${y + 26}" font-size="11" fill="#1f3cc2" font-weight="700">${pct(r[k] / tot)}% of budget</text><rect x="0" y="${y + 32}" width="${Math.max(2, a.values[k] / mx * 250)}" height="10" rx="5" fill="#e0a01c"/><text x="${Math.max(2, a.values[k] / mx * 250) + 6}" y="${y + 41}" font-size="11" fill="#7d5200" font-weight="700">${esc(a.valueLabels ? a.valueLabels[k] : a.values[k])}</text>` }).join('')}</svg>`;
    cap = `Blue: your split. Amber: ${esc(a.valueName)}. Score ${pct(rec.score)}: share of the maximum payoff your split captures under the reported effects.`
  }
  else if (c.format === 'delegate') { body = `<p class="big-stat">${rec.detail.right} of ${rec.detail.total}</p><ul class="deleg-cmp">${c.delegate.tasks.map((t, k) => `<li class="${r[k] === t.answer ? 'ok' : ''}"><span>${esc(short(t.text, 70))}</span><span class="chip-row"><span class="chip you">${esc(c.delegate.choices[r[k]] ?? '–')}</span>${r[k] === t.answer ? '' : `<span class="chip ev">${esc(c.delegate.choices[t.answer])}</span>`}</span></li>`).join('')}</ul>`; cap = 'Blue: your routing. Amber: the route the evidence supports, shown where they differ.' }
  else if (c.chart) { body = bars(c.chart); cap = c.chart.note }
  else { body = `<p class="big-stat">${rec.correct ? 'Match' : rec.score > 0 ? 'Partial' : 'Miss'}</p>`; cap = 'Blue marks your call, amber the evidence, in the options on the left.' }
  return `<figure class="gap" aria-labelledby="gap-h"><figcaption class="sr-only" id="gap-h">Your call against the evidence</figcaption><div class="gap-legend" aria-hidden="true"><span><i class="dot dot-you"></i>Your call</span><span><i class="dot dot-ev"></i>The evidence</span></div>${['choice', 'causal', 'multi'].includes(c.format) && !c.chart ? instrument(c) : body}<p class="gap-caption">${['choice', 'causal', 'multi'].includes(c.format) && !c.chart ? 'Blue marks your call, amber the evidence.' : cap}</p>${['choice', 'causal', 'multi'].includes(c.format) && c.chart ? `<div class="opts-recap">${instrument(c)}</div>` : ''}</figure>`;
}
function short(s, n) { s = String(s); return s.length > n ? s.slice(0, n - 1) + '…' : s }
function bars(ch) {
  const mx = Math.max(...ch.values) * 1.12;
  return `<svg viewBox="0 0 340 ${ch.values.length * 46 + 6}" role="img" aria-label="${esc(ch.labels.map((l, i) => l + ' ' + ch.values[i] + (ch.unit || '')).join(', '))}">${ch.values.map((v, i) => { const y = 4 + i * 46, w = v / mx * 280; return `<text x="0" y="${y + 11}" font-size="12" font-weight="650" fill="#14203a">${esc(ch.labels[i])}</text><rect x="0" y="${y + 17}" width="300" height="14" rx="7" fill="#e2e7ed"/><rect class="rv-bar-grow" x="0" y="${y + 17}" width="${w}" height="14" rx="7" fill="${i === ch.highlight ? '#e0a01c' : '#14203a'}"/><text x="${w + 6}" y="${y + 29}" font-size="12" font-weight="800" fill="#14203a">${esc(v + (ch.unit || ''))}</text>` }).join('')}</svg>`;
}

function studyLine(c) {
  const src = SOURCE[c.sources[0]]; const d = c.study || {};
  const who = d.n && !/not (stated|confirmed)/i.test(d.n) ? d.n : '';
  return [d.design, who].filter(Boolean).join(', ') + (d.design || who ? '. ' : '') + `${src.venue}, ${src.year}.`;
}
function play() {
  const c = card();
  if (st.room && (!c || st.room.challenge !== c.id || st.room.phase === 'lobby')) return roomWait();
  if (!c) { st.view = 'home'; return home() }
  if (st.room && st.phase === 'reveal' && st.room.phase !== 'revealed') return roomLocked(c);
  const rev = st.phase === 'reveal', rec = st.session[st.session.length - 1];
  const steps = st.deck.map((_, k) => `<i class="${k < st.i || (k === st.i && rev) ? 'done' : k === st.i ? 'now' : ''}"></i>`).join('');
  const top = `<div class="focus-top"><button class="x" data-act="leave" aria-label="${st.room ? 'Leave the live class' : 'Leave the round'}"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button><div class="steps" aria-hidden="true">${steps}</div><span class="count num" aria-live="polite">${st.i + 1} of ${st.deck.length}</span></div>`;
  const label = `<p class="eyebrow-line">${c.case ? `<span class="tag tag-you">${esc(c.case.title)}, step ${c.case.step} of ${c.case.of}</span>` : ''}<span class="fmt">${FORMAT_NAME[c.format]}</span><span class="track">${esc(c.track)}</span></p>`;
  if (!rev) {
    const ready = S.ready(c, st.resp) && (c.format !== 'forecast' || st.touched);
    const conf = c.format === 'forecast' ? '' : `<div class="conf-row"><label for="conf">How sure are you?</label><input type="range" id="conf" min="${c.format === 'choice' || c.format === 'causal' ? Math.round(100 / c.options.length / 5) * 5 : 0}" max="100" step="5" value="${st.conf}" style="--fill:${st.conf}%"><output id="conf-read" class="num" for="conf">${st.conf}%</output></div>`;
    const verb = { estimate: 'estimate', allocate: 'budget', rank: 'ranking', delegate: 'routing', forecast: 'forecast' }[c.format] || 'answer';
    return `<section class="focus">${top}<article class="focus-card" aria-labelledby="q-h">${label}
      <p class="scene">${esc(c.scene)}</p><p class="study-line">${esc(studyLine(c))}</p>
      ${c.format === 'forecast' ? `<p class="hint fc-ask">How likely is it that the study found this?</p><h1 class="q q-claim" id="q-h" tabindex="-1">“${esc(c.forecast.claim)}”</h1>` : `<h1 class="q" id="q-h" tabindex="-1">${esc(c.question)}</h1>`}${c.format === 'multi' ? '<p class="hint">Choose two.</p>' : ''}
      ${instrument(c)}${conf}</article>
      <div class="actionbar"><div class="actionbar-in"><span class="kicker">${ready ? 'Ready when you are' : c.format === 'forecast' ? 'Move the slider to state a probability' : 'Make your call'}</span><button class="btn btn-you btn-lg" data-act="lock" id="lock-btn" ${ready ? '' : 'disabled'}>Lock my ${verb}</button></div></div></section>`;
  }
  const tabs = [['questions', 'Questions'], ['scope', 'Where the evidence comes from'], ['source', 'Source'], ['note', 'Your note']];
  const tab = st.tab || 'questions';
  const src = SOURCE[c.sources[0]], [stLabel, stCls] = srcStatus(src);
  const panel = tab === 'questions' ? `<div class="follow">${c.follow.map(f => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join('')}</div>${tutorPanel(c)}`
    : tab === 'scope' ? `<p class="deep-text">${esc(c.boundary)}</p>`
    : tab === 'source' ? c.sources.map(id => { const s = SOURCE[id], [l, k] = srcStatus(s); return `<div class="src"><p class="src-title">${esc(s.title)}</p><p>${esc(s.authors)}, <i>${esc(s.venue)}</i> ${esc(s.volume || '')}, ${s.year}.</p><p class="row"><span class="status ${k}">${l}</span> <button class="link-btn" data-source="${esc(id)}">More on this source</button> <a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Open the article</a></p></div>` }).join('')
    : `<div class="note-box"><label for="note">Which decision in your work would you revisit, and what would you measure first?</label><textarea id="note" maxlength="480">${esc(notes[c.id] || '')}</textarea><button class="btn btn-quiet" data-act="save-note">Save on this device</button></div>`;
  const nextLabel = st.i >= st.deck.length - 1 ? 'See how you did' : c.case && c.case.step < c.case.of ? 'Next step' : 'Next decision';
  return `<section class="focus">${top}<article class="focus-card reveal" aria-labelledby="r-h">${label}
      ${st.room && st.room.agg ? classPanel(c, st.room.agg) : ''}
      <p class="verdict"><span class="tag ${rec.correct ? 'tag-ev' : ''}">${rec.correct ? 'You called it' : rec.score >= .75 ? 'Close' : 'The evidence surprised you'}</span><span class="num">Score ${pct(rec.score)}${rec.confidence !== null ? `, at ${rec.confidence}% confidence` : ''}</span></p>
      <h1 class="reveal-title" id="r-h" tabindex="-1">${esc(c.answerTitle)}</h1>
      ${gapFigure(c, rec)}
      <p class="reveal-body">${esc(c.explain)}</p>
      <div class="action-note"><h2>What a manager does with this</h2><p>${esc(c.implication)}</p></div>
      <div class="deep"><div class="tabs" role="tablist" aria-label="Go deeper">${tabs.map(([k, l]) => `<button role="tab" id="tab-${k}" aria-selected="${tab === k}" aria-controls="tabpanel" data-tab="${k}" tabindex="${tab === k ? 0 : -1}">${l}</button>`).join('')}</div><div class="tabpanel" id="tabpanel" role="tabpanel" aria-labelledby="tab-${tab}">${panel}</div></div>
    </article>
    <div class="actionbar"><div class="actionbar-in"><span class="kicker">${st.room ? `Live class ${esc(st.room.code)}. Your instructor opens the next decision.` : `${st.session.filter(r => r.correct).length} of ${st.session.length} called right so far`}</span>${st.room ? '' : `<button class="btn btn-solid btn-lg" data-act="next" id="next-btn">${nextLabel}</button>`}</div></div></section>`;
}
// ----- tutor -----
let TUTOR_REMOTE = null; // set when a protected server endpoint answers /api/tutor/status
function tutorPanel(c) {
  const t = st.tutor;
  return `<div class="tutor" aria-labelledby="tutor-h"><h3 id="tutor-h">Ask your own question</h3>
    <form class="tutor-line" data-form="tutor"><label class="sr-only" for="tutor-in">Your question about this study</label><input id="tutor-in" maxlength="300" placeholder="For example: would this hold in a sales team?" autocomplete="off"><button class="btn btn-quiet" ${t.busy ? 'disabled' : ''}>${t.busy ? 'Thinking' : 'Ask'}</button></form>
    <div class="tutor-chips">${['How big is this effect in practice?', 'Would this hold with AI tools today?', 'How would I test this in my company?'].map(q => `<button data-ask="${esc(q)}">${esc(q)}</button>`).join('')}</div>
    ${t.text ? `<div class="tutor-answer" aria-live="polite">${esc(t.text)}${t.cites.length ? '\n\n' + t.cites.map(x => `<cite>${esc(x)}</cite>`).join(' ') : ''}</div>` : ''}
    <p class="small">${TUTOR_REMOTE ? 'AI answers use only the lab’s checked sources. Check details in the source.' : 'Answers come from the lab’s checked summaries.'}</p></div>`;
}
function curated(q, c) {
  const stop = new Set('what which where when does that this with from about have should would there their these they them then into could work study research finding found people your thing much more make'.split(' '));
  const terms = (q.toLowerCase().match(/[a-z]{4,}/g) || []).filter(w => !stop.has(w));
  const fields = x => [x.concept, x.title, x.explain, x.boundary, x.implication, x.scene, ...(x.follow || []).map(f => f.q + ' ' + f.a)].join(' ').toLowerCase();
  const scoreOf = x => terms.reduce((s, t) => s + (fields(x).includes(t) ? 1 : 0), 0) + (x.id === c.id ? 1.5 : 0);
  const best = ALL.map(x => ({ x, s: scoreOf(x) })).sort((a, b) => b.s - a.s)[0];
  const fq = (c.follow || []).map(f => ({ f, s: terms.filter(t => (f.q + ' ' + f.a).toLowerCase().includes(t)).length })).sort((a, b) => b.s - a.s)[0];
  if (/test|pilot|company|measure|experiment/i.test(q)) return { text: `Start with a small randomized pilot: assign the change to some teams and not others, fix the outcome metric in advance, and compare. ${c.implication}\n\nThe study itself: ${c.explain}`, cites: [cite(c.sources[0])] };
  if (/today|hold|still|generali|apply|everywhere|always/i.test(q)) return { text: `${c.boundary}\n\n${c.explain}`, cites: [cite(c.sources[0])] };
  if (fq && fq.s >= 1) return { text: fq.f.a, cites: [cite(c.sources[0])] };
  if (best && best.x.id !== c.id && best.s >= 2) return { text: `A related study in the lab: ${best.x.explain}\n\nWhere it applies: ${best.x.implication}`, cites: [cite(best.x.sources[0])] };
  return { text: `${c.explain}\n\n${c.boundary}`, cites: [cite(c.sources[0])] };
}
async function ask(q) {
  q = String(q || '').trim().slice(0, 300); const c = card(); if (!c || st.tutor.busy) return;
  if (q.length < 4) { notice('Type a question of at least four characters.'); return }
  st.tutor = { busy: true, text: '', cites: [] }; render();
  if (TUTOR_REMOTE) {
    try {
      const ctl = new AbortController(), to = setTimeout(() => ctl.abort(), 15000);
      const res = await fetch(TUTOR_REMOTE, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ question: q, challenge: c.id, client: clientId() }), signal: ctl.signal });
      clearTimeout(to); const d = await res.json();
      if (res.ok && typeof d.answer === 'string' && d.answer.trim()) { st.tutor = { busy: false, text: d.answer.slice(0, 1600), cites: (d.citations || []).map(x => x.label).slice(0, 4) }; render(); return }
    } catch { }
  }
  const a = curated(q, c); st.tutor = { busy: false, text: a.text, cites: a.cites }; render();
}
function clientId() { let id = store.get('thv:client', null); if (!id) { id = Math.random().toString(36).slice(2, 12); store.set('thv:client', id) } return id }

// ----- atlas -----
function atlas() {
  const q = st.atlasQuery.trim().toLowerCase();
  const m = ALL.filter(c => (st.atlasTrack === 'All' || c.track === st.atlasTrack) && (st.atlasFormat === 'All' || FORMAT_NAME[c.format] === st.atlasFormat) && (!q || [c.title, c.scene, c.question, c.concept, c.explain, cite(c.sources[0]), SOURCE[c.sources[0]].title].join(' ').toLowerCase().includes(q)));
  return `<section class="atlas-head wrap">${libHead()}
    <div class="atlas-tools"><label class="search"><span aria-hidden="true">⌕</span><span class="sr-only">Search</span><input id="atlas-q" type="search" value="${esc(st.atlasQuery)}" placeholder="Try defaults, Dimant, algorithm, norms" autocomplete="off"></label>
    <label class="sr-only" for="atlas-track">Area</label><select id="atlas-track" class="seg">${['All', ...TRACKS].map(t => `<option ${st.atlasTrack === t ? 'selected' : ''}>${esc(t)}</option>`).join('')}</select>
    <label class="sr-only" for="atlas-format">Format</label><select id="atlas-format" class="seg">${['All', ...new Set(Object.values(FORMAT_NAME))].map(t => `<option ${st.atlasFormat === t ? 'selected' : ''}>${esc(t)}</option>`).join('')}</select></div>
    <p class="kicker" aria-live="polite" id="atlas-count">${m.length} of ${ALL.length} decisions</p></section>
    <section class="wrap"><div class="atlas-grid" id="atlas-grid">${m.length ? m.map(c => `<button class="entry" data-play="${esc(c.id)}"><span class="meta"><span class="tag">${esc(c.track)}</span><span class="tag">${FORMAT_NAME[c.format]}</span></span><h3>${esc(c.title)}</h3><p>${esc(c.question)}</p><span class="cite">${esc(cite(c.sources[0]))}, ${esc(SOURCE[c.sources[0]].venue)}</span></button>`).join('') : `<div class="empty">No decision matches “${esc(st.atlasQuery)}”. Clear the search or try an author’s name.</div>`}</div></section>`;
}


// ----- library: principles (almanac) and all decisions (atlas) -----
function libHead() {
  return `<h1>Library</h1><div class="lib-tabs" role="tablist" aria-label="Library"><button role="tab" aria-selected="${st.view === 'almanac'}" data-nav="almanac">Principles</button><button role="tab" aria-selected="${st.view === 'atlas'}" data-nav="atlas">All decisions</button></div>`;
}
function almanac() {
  const themes = BANK.themes || [];
  return `<section class="atlas-head wrap">${libHead()}
    <nav class="theme-index" aria-label="Themes">${themes.map(t => `<a href="#theme-${esc(t.id)}">${esc(t.title)}</a>`).join('')}</nav></section>
    <section class="wrap" style="padding-bottom:64px">${themes.map(t => { const cs = ALL.filter(c => c.theme === t.id); if (!cs.length) return ''; return `<article class="theme panel" id="theme-${esc(t.id)}"><div class="theme-head"><h2>${esc(t.title)}</h2><p>${esc(t.principle)}</p></div>
      <details class="theme-more"><summary>The ${cs.length} findings behind it</summary><ul class="findings">${cs.map(c => `<li><div><strong>${esc(c.answerTitle)}.</strong> ${esc(c.explain)}<br><small>${esc(cite(c.sources[0]))}, ${esc(SOURCE[c.sources[0]].venue)}. ${esc(c.boundary)}</small></div><button class="btn btn-quiet" data-play="${esc(c.id)}">Play</button></li>`).join('')}</ul></details>
      <button class="btn btn-line" data-theme-round="${esc(t.id)}">Play these ${cs.length}</button></article>` }).join('')}</section>`;
}

// ----- record -----
function record() {
  const all = records, last = st.session.length ? st.session : all.slice(-12);
  const cal = S.calibration(all.map(r => S.toCalibrationRecord(BY_ID[r.id], r)));
  const meanScore = all.length ? pct(all.reduce((a, r) => a + r.score, 0) / all.length) : null;
  const sess = st.session.length ? pct(st.session.reduce((a, r) => a + r.score, 0) / st.session.length) : null;
  const byTrack = TRACKS.map(t => { const x = all.filter(r => BY_ID[r.id].track === t); return [t, x.length, x.length ? pct(x.reduce((a, r) => a + r.score, 0) / x.length) : null] });
  let summary = '';
  if (st.session.length) {
    const worst = st.session.reduce((a, r) => r.score < a.score ? r : a), best = st.session.reduce((a, r) => r.score > a.score ? r : a);
    const sc = S.calibration(st.session.map(r => S.toCalibrationRecord(BY_ID[r.id], r)));
    summary = `<div class="summary">${best.score > worst.score ? `<div class="panel lesson-card"><span class="kicker">Best call</span><h3>${esc(BY_ID[best.id].title)}</h3><p>${esc(BY_ID[best.id].answerTitle)}. Score ${pct(best.score)}.</p></div>` : ''}<div class="panel lesson-card"><span class="kicker">Biggest surprise</span><h3>${esc(BY_ID[worst.id].title)}</h3><p>${esc(BY_ID[worst.id].answerTitle)}. ${esc(BY_ID[worst.id].implication)}</p><button class="link-btn" data-play="${esc(worst.id)}">Play it again</button></div></div>`;
  }
  const played = byTrack.filter(t => t[1]);
  const gapLine = cal.overconfidence === null ? '' : cal.overconfidence > 3 ? `${Math.round(cal.overconfidence)} points more confident than accurate` : cal.overconfidence < -3 ? `${Math.round(-cal.overconfidence)} points less confident than accurate` : 'Confidence matches accuracy';
  return `<section class="rec-head wrap"><h1>${st.session.length ? 'Round complete.' : 'Your record.'}</h1>
    <div class="score-strip"><div class="score-big"><b class="num">${sess ?? meanScore ?? '–'}</b><span>${sess !== null ? 'score this round' : 'average score'}, out of 100</span></div>
      <dl class="score-meta"><div><dt>Brier score</dt><dd class="num">${cal.brier === null ? '–' : cal.brier.toFixed(2)}</dd></div><div><dt>Calibration</dt><dd>${gapLine || '–'}</dd></div><div><dt>Calls on this device</dt><dd class="num">${all.length}</dd></div></dl></div>
    ${summary}</section>
    <section class="wrap"><div class="rec-grid">
      <div class="panel rec-panel"><h2>Calibration</h2><p>How sure you said you were, against how often you were right. Dots on the diagonal mean your confidence can be trusted.</p>${calPlot(cal)}</div>
      <div class="panel rec-panel"><h2>${st.session.length ? 'This round' : 'Recent calls'}</h2><ul class="hist">${last.length ? last.slice().reverse().map(r => { const c = BY_ID[r.id]; return `<li><span><button class="link-quiet" data-play="${esc(r.id)}">${esc(c.title)}</button><br><small>${FORMAT_NAME[r.format]}, ${esc(c.track)}</small></span><span class="num">${pct(r.score)}<span class="bar-score"><i style="width:${pct(r.score)}%"></i></span></span></li>` }).join('') : '<li><span>No calls yet. Play a path to start your record.</span></li>'}</ul></div>
      ${played.length > 1 ? `<div class="panel rec-panel"><h2>By area</h2><ul class="hist">${played.map(([t, n, sc]) => `<li><span>${esc(t)}<br><small>${n} calls</small></span><span class="num">${sc}<span class="bar-score"><i style="width:${sc}%"></i></span></span></li>`).join('')}</ul></div>` : ''}
    </div>
    <details class="how"><summary>How scoring works</summary><p>Each decision scores 0 to 100 with partial credit. An estimate inside the shaded band earns 100, and credit falls with distance. Ranks score the share of pairs in the measured order. Budgets score the share of the best possible payoff under the reported effects. Forecasts use the Brier rule, the standard in forecasting tournaments: 0 is perfect, 0.25 is always saying 50%. The calibration plot uses your stated confidence, except for forecasts, where the probability is the statement. This is a learning record, not a validated assessment.</p></details>
    <div class="tools"><button class="btn btn-solid btn-lg" data-act="replay">Play another round</button><span class="tool-links"><button class="link-btn" data-act="csv">Export CSV</button><button class="link-btn" data-act="json">Export JSON</button><button class="link-btn" data-act="erase">Erase this device’s record</button></span></div></section>`;
}
function calPlot(cal) {
  const W = 320, P = 34, sx = v => P + v / 100 * (W - P - 10), sy = v => W - P - v / 100 * (W - P - 10);
  const pts = cal.bins.filter(b => b.n);
  return `<svg viewBox="0 0 ${W} ${W}" role="img" aria-label="Calibration plot: ${pts.map(b => `stated ${Math.round(b.meanP)}%, right ${Math.round(b.hitRate)}% over ${b.n} calls`).join('; ') || 'no data yet'}" style="max-width:420px;width:100%">
    <rect x="${P}" y="10" width="${W - P - 10}" height="${W - P - 10}" fill="#f4f6f9" stroke="#cbd3dd"/>
    ${[0, 25, 50, 75, 100].map(v => `<line x1="${sx(v)}" y1="10" x2="${sx(v)}" y2="${W - P}" stroke="#e2e7ed"/><line x1="${P}" y1="${sy(v)}" x2="${W - 10}" y2="${sy(v)}" stroke="#e2e7ed"/><text x="${sx(v)}" y="${W - P + 15}" font-size="10" text-anchor="middle" fill="#56617a">${v}</text><text x="${P - 6}" y="${sy(v) + 3}" font-size="10" text-anchor="end" fill="#56617a">${v}</text>`).join('')}
    <line x1="${sx(0)}" y1="${sy(0)}" x2="${sx(100)}" y2="${sy(100)}" stroke="#9aa6b6" stroke-dasharray="4 4"/>
    ${pts.map(b => `<circle cx="${sx(b.meanP)}" cy="${sy(b.hitRate)}" r="${5 + Math.min(10, Math.sqrt(b.n) * 2)}" fill="#2f54eb" fill-opacity=".85" stroke="#fff" stroke-width="2"/>`).join('')}
    <text x="${(W + P) / 2}" y="${W - 4}" font-size="11" text-anchor="middle" fill="#36425e">Stated confidence (%)</text>
    <text x="10" y="${(W - P) / 2}" font-size="11" text-anchor="middle" fill="#36425e" transform="rotate(-90 10 ${(W - P) / 2})">Share right (%)</text></svg>${pts.length ? '' : '<p class="kicker">Points appear after your first calls.</p>'}`;
}

// ----- modals -----
let lastFocus = null;
function modal(html, label) {
  lastFocus = document.activeElement;
  qs('#overlay').innerHTML = `<div class="modal-back" data-close="1"><div class="modal" role="dialog" aria-modal="true" aria-label="${esc(label)}"><button class="close" data-close="1" aria-label="Close">×</button>${html}</div></div>`;
  qs('#overlay .close').focus();
}
function closeModal() { if (!qs('#overlay').innerHTML) return; qs('#overlay').innerHTML = ''; lastFocus && lastFocus.focus && lastFocus.focus() }
function sourceModal(id) {
  const s = SOURCE[id]; if (!s) return; const v = s.verification || {}; const used = ALL.filter(c => c.sources.includes(id));
  modal(`<span class="kicker">Peer-reviewed source</span><h2>${esc(s.title)}</h2><p><strong>${esc(s.authors)}</strong> (${s.year}). <i>${esc(s.venue)}</i>${s.volume ? `, ${esc(s.volume)}` : ''}${s.pages ? `, ${esc(s.pages)}` : ''}.</p>
    <p><strong>What the lab uses.</strong> ${esc(s.takeaway)}</p>
    <p><strong>How it was checked.</strong> ${esc(srcStatus(s)[0])}${v.checked ? ' on ' + esc(v.checked) : ''}. Metadata matched against the DOI registry.${v.note ? ' ' + esc(v.note) : ''}</p>
    ${used.length ? `<p><strong>Decisions built on it:</strong> ${used.map(c => `<button class="link-btn" data-play="${esc(c.id)}">${esc(c.title)}</button>`).join(', ')}.</p>` : ''}
    <p><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Open the article (DOI ${esc(s.doi)})</a></p>`, 'Source details');
}
function methodsModal() {
  const live = Object.values(SOURCE).filter(isLive), q = Object.values(SOURCE).filter(s => !isLive(s));
  modal(`<span class="kicker">How the lab is built</span><h2>Research standard</h2>
    <p>Scored answers come only from peer-reviewed journal articles or scholarly books. Each source was matched against the DOI registry, and every number used in a decision was checked against the published abstract or full text. ${live.length} sources passed${q.length ? `; ${q.length} are held back until their claims can be checked` : ''}.</p>
    <p>Scenarios are teaching adaptations written for managers. They describe the study design accurately but do not replicate it. Charts appear only where the study reported the values shown.</p>
    <p>A single study is evidence about one population, task and time. Each decision states the population, task and setting the evidence comes from.</p>
    <p>Original concept by Eugen Dimant. A teaching tool, not a validated assessment.</p>`, 'Research standard');
}

// ----- export -----
function download(name, text, mime) { const b = new Blob([text], { type: mime }); const u = URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(u), 4000) }
function csvCell(x) { const s = String(x ?? '').replace(/^[=+@\-\t\r]/, m => "'" + m); return '"' + s.replace(/"/g, '""') + '"' }
function exportCSV() { const head = ['decision_id', 'title', 'area', 'format', 'score_0_100', 'correct', 'confidence', 'response', 'utc_time', 'seed', 'field_note']; const rows = records.map(r => [r.id, BY_ID[r.id].title, BY_ID[r.id].track, r.format, pct(r.score), r.correct ? 1 : 0, r.confidence ?? '', JSON.stringify(r.response), r.at, r.seed, notes[r.id] || ''].map(csvCell).join(',')); download('human-variable-record.csv', [head.join(','), ...rows].join('\n'), 'text/csv;charset=utf-8') }


// ----- live class (room mode) -----
function roomHeaders(json) { const h = { 'X-Client-Id': clientId() }; if (json) h['Content-Type'] = 'application/json'; return h }
async function roomJoin(code) {
  code = String(code || '').trim().toUpperCase().replace(/[^A-Z2-9]/g, '').slice(0, 8);
  if (code.length < 4) { notice('Enter the code shown on the instructor screen.'); return }
  if (!location.protocol.startsWith('http')) { notice('Live classes need the hosted version of the lab. Ask your instructor for the link.'); return }
  try {
    let tok = sessionStorage.getItem('thv:room:' + code);
    if (!tok) {
      const r = await fetch(`/api/rooms/${code}/join`, { method: 'POST', headers: roomHeaders(true), body: '{}' }); const d = await r.json();
      if (!r.ok) throw Error(d.error || 'Could not join'); tok = d.token; sessionStorage.setItem('thv:room:' + code, tok); sessionStorage.setItem('thv:room:' + code + ':n', d.number);
    }
    st.room = { code, token: tok, number: sessionStorage.getItem('thv:room:' + code + ':n'), phase: 'lobby', challenge: null, etag: '', agg: null, misses: 0 };
    st.view = 'play'; st.deck = []; closeModal(); render(true); roomPoll();
  } catch (e) { notice(e.message) }
}
async function roomPoll() {
  if (!st.room) return; const R = st.room;
  try {
    const r = await fetch(`/api/rooms/${R.code}?v=${encodeURIComponent(R.etag)}`, { headers: roomHeaders() });
    if (r.status === 404) { notice('This live session has ended.'); st.room = null; st.view = 'home'; render(true); return }
    const d = await r.json(); R.misses = 0;
    if (!d.same) {
      const changed = d.challenge !== R.challenge, phaseChanged = d.phase !== R.phase;
      R.etag = d.etag; R.phase = d.phase; R.agg = d.aggregate || null; R.participants = d.participants; R.responses = d.responses; R.title = d.title;
      if (changed && d.challenge && BY_ID[d.challenge]) { R.challenge = d.challenge; st.deck = [BY_ID[d.challenge]]; st.i = 0; resetCard(); render(true) }
      else if (phaseChanged || d.phase === 'revealed') { R.challenge = d.challenge; render(phaseChanged) }
      else { const live = qs('#room-live'); if (live) live.textContent = roomLine() }
    }
  } catch { R.misses++; const live = qs('#room-live'); if (live) live.textContent = 'Reconnecting…' }
  clearTimeout(R.timer); R.timer = setTimeout(roomPoll, document.hidden ? 6000 : Math.min(8000, 2000 * (1 + R.misses)));
}
function roomLine() { const R = st.room; return `${R.participants ?? '–'} joined. ${R.phase === 'open' ? (R.responses ?? 0) + ' answered so far.' : ''}` }
async function roomSubmit(c, rec) {
  const R = st.room; R.sent = false; render();
  for (let k = 0; k < 4; k++) {
    try {
      const r = await fetch(`/api/rooms/${R.code}/responses`, { method: 'POST', headers: roomHeaders(true), body: JSON.stringify({ token: R.token, answer: rec.response, confidence: rec.confidence }) });
      const d = await r.json();
      if (r.ok) { R.sent = true; R.sentMsg = d.accepted ? 'Your answer is in.' : d.message; render(); return }
      if (r.status === 409 || r.status === 400 || r.status === 403) { R.sent = true; R.sentMsg = d.error; render(); return }
    } catch { }
    await new Promise(z => setTimeout(z, 800 * (k + 1)));
  }
  R.sentMsg = 'Could not reach the class server. Check your connection; your answer is saved on this device.'; R.sent = true; render();
}
function roomWait() {
  const R = st.room;
  return `<section class="play wrap"><div class="panel card room-wait" aria-live="polite"><span class="tag tag-you">Live class ${esc(R.code)}${R.number ? ', you are participant ' + esc(R.number) : ''}</span>
    <h1 class="q" tabindex="-1" style="margin-top:18px">${R.phase === 'lobby' || !R.challenge ? 'You are in. The first decision appears when your instructor opens it.' : 'Waiting for the next decision.'}</h1>
    <p class="scene">Keep this page open. Your answers count toward the class picture, not toward a grade, and the instructor sees only participant numbers.</p>
    <p class="kicker" id="room-live">${roomLine()}</p><button class="btn btn-quiet" data-act="leave-room">Leave the live class</button></div></section>`;
}
function roomLocked(c) {
  const R = st.room;
  return `<section class="play wrap"><div class="panel card room-wait" aria-live="polite"><span class="tag tag-you">Live class ${esc(R.code)}</span>
    <h1 class="q" tabindex="-1" style="margin-top:18px">${R.sent ? esc(R.sentMsg || 'Your answer is in.') : 'Sending your answer…'}</h1>
    <p class="scene">The evidence appears for everyone when your instructor reveals it. ${esc(c.title)}.</p><p class="kicker" id="room-live">${roomLine()}</p></div></section>`;
}
function classPanel(c, a) {
  const f = c.format; let body = '';
  const hbars = (labels, vals, ev) => { const mx = Math.max(1, ...vals); return `<svg viewBox="0 0 340 ${labels.length * 40 + 4}" role="img" aria-label="Class answers">${labels.map((l, i) => { const y = 2 + i * 40, w = vals[i] / mx * 230; return `<text x="0" y="${y + 12}" font-size="11.5" font-weight="650" fill="#14203a">${esc(short(l, 50))}</text><rect x="0" y="${y + 18}" width="${Math.max(2, w)}" height="12" rx="6" fill="${ev && ev.includes(i) ? '#e0a01c' : '#2f54eb'}"/><text x="${Math.max(2, w) + 6}" y="${y + 28}" font-size="11.5" font-weight="800" fill="#14203a">${vals[i]}</text>` }).join('')}</svg>` };
  if (a.counts) body = hbars(c.options, a.counts, f === 'multi' ? c.multiAnswers : [c.answer]);
  else if (a.hist) { const lo = a.lo, hi = a.hi, w = (hi - lo) / a.hist.length, mx = Math.max(1, ...a.hist), ev = f === 'estimate' ? c.estimate.target : (c.forecast.truth ? 100 : 0); body = `<svg viewBox="0 0 340 130" role="img" aria-label="Class distribution, median ${a.median}">${a.hist.map((h, i) => `<rect x="${10 + i * 32}" y="${100 - h / mx * 80}" width="28" height="${h / mx * 80}" rx="3" fill="#2f54eb" fill-opacity=".8"/>`).join('')}<line x1="${10 + (ev - lo) / (hi - lo) * 320}" y1="10" x2="${10 + (ev - lo) / (hi - lo) * 320}" y2="104" stroke="#e0a01c" stroke-width="3"/><text x="10" y="122" font-size="11" fill="#56617a">${lo}</text><text x="330" y="122" font-size="11" fill="#56617a" text-anchor="end">${hi}</text><text x="${Math.min(300, 14 + (ev - lo) / (hi - lo) * 320)}" y="20" font-size="11" font-weight="700" fill="#7d5200">Evidence</text></svg><p class="gap-caption">Class median ${a.median}${f === 'estimate' ? (c.estimate.unit ?? '%') : '%'}.</p>` }
  else if (a.meanPosition) body = hbars(c.options.map((o, i) => o + ' (avg. rank ' + a.meanPosition[i] + ')'), a.meanPosition.map(p => +(c.options.length + 1 - p).toFixed(2)), [c.rankAnswer[0]]);
  else if (a.meanShare) body = hbars(c.options.map((o, i) => o + ' (' + a.meanShare[i] + '%)'), a.meanShare, [c.allocate.values.indexOf(Math.max(...c.allocate.values))]);
  else if (a.taskCounts) body = `<ul class="hist">${c.delegate.tasks.map((t, i) => `<li><span>${esc(short(t.text, 60))}</span><span class="num">${a.taskCounts[i][t.answer]} of ${a.n}</span></li>`).join('')}</ul><p class="gap-caption">Number of classmates who routed each task the way the evidence suggests.</p>`;
  return `<section class="panel gap" aria-labelledby="class-h"><h2 id="class-h">The room, ${a.n} answers</h2><p class="gap-caption" style="margin:0 0 8px">Average score ${a.meanScore ?? '–'}. ${a.shareCorrect ?? 0}% matched the evidence${a.meanConfidence !== null ? `, at ${a.meanConfidence}% average confidence` : ''}.</p>${body}</section>`;
}
function joinModal() {
  modal(`<span class="kicker">Live class</span><h2>Join with the code on the screen</h2><form data-form="join" class="tutor-line"><label class="sr-only" for="join-code">Session code</label><input id="join-code" maxlength="8" autocomplete="off" autocapitalize="characters" placeholder="For example K7QPM" style="text-transform:uppercase;font-size:20px;letter-spacing:.12em"><button class="btn btn-solid">Join</button></form><p>No name or account needed. The instructor sees answers by participant number only.</p>`, 'Join a live class');
  setTimeout(() => qs('#join-code')?.focus(), 20);
}

// ---------- render ----------
let toastT;
function notice(s) { const t = qs('#toast'); t.textContent = s; t.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('show'), 3200) }
function render(moveFocus) {
  const v = qs('#view');
  v.innerHTML = st.view === 'home' ? home() : st.view === 'atlas' ? atlas() : st.view === 'almanac' ? almanac() : st.view === 'record' ? record() : play();
  document.body.classList.toggle('in-play', st.view === 'play');
  qa('.nav button').forEach(b => b.setAttribute('aria-current', (b.dataset.nav === st.view || (b.dataset.nav === 'almanac' && st.view === 'atlas')) ? 'page' : 'false'));
  qs('.nav').classList.toggle('open', st.menu);
  const c = card();
  document.title = (st.view === 'play' && c ? (st.phase === 'reveal' ? c.answerTitle : c.title) + ' · ' : st.view === 'atlas' ? 'Studies · ' : st.view === 'almanac' ? 'Playbook · ' : st.view === 'record' ? 'Your record · ' : '') + 'The Human Variable';
  if (moveFocus && (st.phase === 'reveal' || st.hero.done)) animateReveal();
  if (moveFocus) { scrollTo({ top: 0, behavior: 'instant' in document.documentElement.style ? 'instant' : 'auto' }); const h = qs('#view h1'); if (h) { if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }) } }
}
function animateReveal() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  qa('.ev-mark[data-from]').forEach(g => { const d = +g.dataset.from; if (!d) return; g.style.transition = 'none'; g.style.transform = `translateX(${d}px)`; g.style.opacity = '.3'; requestAnimationFrame(() => requestAnimationFrame(() => { g.style.transition = ''; g.style.transform = ''; g.style.opacity = '' })) });
  qa('.rv-bar-grow').forEach(r => { const w = r.getAttribute('width'); r.setAttribute('width', 0); requestAnimationFrame(() => requestAnimationFrame(() => r.setAttribute('width', w))) });
}
function setRange(el) { el.classList.remove('untouched'); el.style.setProperty('--fill', (el.value - el.min) / (el.max - el.min) * 100 + '%') }

// ---------- events ----------
document.addEventListener('click', e => {
  const t = e.target.closest('button,[data-close]'); if (!t) return;
  if (t.dataset.close && (e.target === t || t.classList.contains('close'))) { closeModal(); return }
  if (t.dataset.nav) { closeModal(); if (st.room && t.dataset.nav === 'home' && st.view === 'play') { if (!confirm('Leave the live class?')) return; clearTimeout(st.room.timer); st.room = null } st.view = t.dataset.nav; st.menu = false; render(true); return }
  if (t.dataset.track) { st.track = t.dataset.track; const n = st.track === 'Mixed' ? ALL.length : ALL.filter(c => c.track === st.track).length; if (st.length > n) st.length = 5; render(); return }
  if (t.dataset.length) { st.length = +t.dataset.length; render(); return }
  if (t.dataset.themeRound) { st.seed = (Math.random() * 2 ** 32) >>> 0; start(ALL.filter(c => c.theme === t.dataset.themeRound), 99); return }
  if (t.dataset.source) { sourceModal(t.dataset.source); return }
  if (t.dataset.play) { closeModal(); const c = ALL.find(x => x.id === t.dataset.play); if (c) { st.seed = (Math.random() * 2 ** 32) >>> 0; start(c.case ? ALL.filter(x => x.case && x.case.id === c.case.id) : [c], c.case ? c.case.of : 1) } return }
  if (t.dataset.ask) { ask(t.dataset.ask); return }
  if (t.dataset.tab) { st.tab = t.dataset.tab; const y = scrollY; render(); scrollTo(0, y); qs(`[data-tab="${st.tab}"]`)?.focus(); return }
  if (t.dataset.path) { const p = BANK.paths.find(x => x.id === t.dataset.path); const list = p.ids.map(id => ALL.find(c => c.id === id)).filter(Boolean); st.deck = list; st.i = 0; st.session = []; st.view = 'play'; resetCard(); render(true); return }
  if (t.dataset.theme) { st.view = 'almanac'; st.almanacOpen = t.dataset.theme; render(true); qs('#theme-' + t.dataset.theme)?.scrollIntoView(); return }
  if (st.view === 'play' && st.phase === 'predict') {
    const c = card();
    if (t.dataset.choice !== undefined) { const i = +t.dataset.choice; if (c.format === 'multi') { const r = st.resp.includes(i) ? st.resp.filter(x => x !== i) : [...st.resp, i].slice(-c.multiAnswers.length); st.resp = r } else st.resp = i; render(); qs(`[data-choice="${i}"]`)?.focus(); return }
    if (t.dataset.rank !== undefined) { const k = +t.dataset.rank, d = +t.dataset.dir, r = st.resp, j = k + d; if (j < 0 || j >= r.length) return;[r[k], r[j]] = [r[j], r[k]]; st.touched = true; render(); const sel = qs(`[data-rank="${j}"][data-dir="${d}"]`) || qs(`[data-rank="${j}"][data-dir="${-d}"]`); sel?.focus(); return }
    if (t.dataset.deleg !== undefined) { st.resp[+t.dataset.deleg] = +t.dataset.pick; render(); qs(`[data-deleg="${t.dataset.deleg}"][data-pick="${t.dataset.pick}"]`)?.focus(); return }
  }
  const a = t.dataset.act;
  if (!a) return;
  if (a === 'leave') { if (st.room) { if (!confirm('Leave the live class?')) return; clearTimeout(st.room.timer); st.room = null } st.view = 'home'; render(true); return }
  if (a === 'toggle-custom') { st.custom = !st.custom; render(); qs('[data-act="toggle-custom"]')?.focus(); return }
  if (a === 'menu') { st.menu = !st.menu; t.setAttribute('aria-expanded', st.menu); qs('.nav').classList.toggle('open', st.menu); return }
  if (a === 'go-start') { qs('#start')?.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' }); qs('#start .path')?.focus({ preventScroll: true }); return }
  if (a === 'start' || a === 'replay') { st.seed = (Math.random() * 2 ** 32) >>> 0; startTrack(); return }
  if (a === 'start-quick') { st.seed = (Math.random() * 2 ** 32) >>> 0; st.track = 'Mixed'; start(ALL.filter(c => c.id !== 'ai01'), 5); return }
  if (a === 'dimant-round') { st.seed = (Math.random() * 2 ** 32) >>> 0; start(ALL.filter(c => c.sources.some(id => /Dimant/.test(SOURCE[id].authors))), 12); return }
  if (a === 'hero-lock') { if (st.hero.value === null) return; st.hero.done = true; render(); animateReveal(); qs('[data-act="start-quick"]')?.focus({ preventScroll: true }); return }
  if (a === 'hero-reset') { st.hero = { value: null, done: false }; render(); qs('#hero-range')?.focus(); return }
  if (a === 'lock') { lock(); return }
  if (a === 'next') { next(); return }
  if (a === 'save-note') { const c = card(), v = qs('#note')?.value || ''; notes[c.id] = v.slice(0, 480); store.set(NOTE_KEY, notes); notice('Note saved on this device.'); return }
  if (a === 'csv') { exportCSV(); return }
  if (a === 'json') { download('human-variable-record.json', JSON.stringify({ kind: 'thv-record', version: 2, exported: new Date().toISOString(), records }, null, 2), 'application/json'); return }
  if (a === 'erase') { if (confirm('Erase every saved call and field note in this browser? This cannot be undone.')) { records = []; notes = {}; st.session = []; store.del(REC_KEY); store.del(NOTE_KEY); store.del('thv:v1:results'); render(); notice('Record erased.') } return }
  if (a === 'methods') { methodsModal(); return }
  if (a === 'join') { joinModal(); return }
  if (a === 'leave-room') { clearTimeout(st.room?.timer); st.room = null; st.view = 'home'; render(true); return }
  if (a === 'about') { methodsModal(); return }
});
document.addEventListener('input', e => {
  const el = e.target, c = card();
  if (el.id === 'hero-range') { st.hero.value = +el.value; setRange(el); const hr = qs('#hero-read'); hr.textContent = el.value + '%'; hr.classList.remove('empty'); qs('[data-act="hero-lock"]').disabled = false; return }
  if (el.id === 'conf') { st.conf = +el.value; st.confTouched = true; setRange(el); qs('#conf-read').textContent = st.conf + '%'; return }
  if (!c || st.phase !== 'predict') {
    if (el.id === 'atlas-q') { st.atlasQuery = el.value; const tmp = document.createElement('div'); tmp.innerHTML = atlas(); qs('#atlas-grid').replaceWith(tmp.querySelector('#atlas-grid')); qs('#atlas-count').textContent = tmp.querySelector('#atlas-count').textContent }
    return;
  }
  if (el.id === 'est') { st.resp = +el.value; setRange(el); qs('#est-read').textContent = st.resp + (c.estimate.unit ?? '%'); qs('#est-read').classList.remove('empty'); qs('#lock-btn').disabled = false; qs('.actionbar .kicker').textContent = 'Ready when you are'; return }
  if (el.id === 'fc') { st.resp = +el.value; st.touched = true; setRange(el); qs('#fc-read').textContent = st.resp + '%'; qs('#fc-read').classList.remove('empty'); qs('#lock-btn').disabled = false; qs('.actionbar .kicker').textContent = 'Ready when you are'; return }
  if (el.dataset.alloc !== undefined) {
    const k = +el.dataset.alloc, a = c.allocate; let v = +el.value; const others = st.resp.reduce((x, y, i) => x + (i === k ? 0 : y), 0);
    if (others + v > a.total) { v = a.total - others; el.value = v }
    st.resp[k] = v; setRange(el); el.nextElementSibling.textContent = (a.prefix || '') + v + (a.suffix || '');
    const sum = st.resp.reduce((x, y) => x + y, 0), tot = qs('.alloc-total'); tot.classList.toggle('ok', sum === a.total); tot.lastElementChild.textContent = `${a.prefix || ''}${sum}${a.suffix || ''} of ${a.prefix || ''}${a.total}${a.suffix || ''}${sum === a.total ? '' : ', unassigned'}`;
    qs('#lock-btn').disabled = !S.ready(c, st.resp); return;
  }
});
document.addEventListener('change', e => {
  if (e.target.id === 'atlas-track') { st.atlasTrack = e.target.value; render(); qs('#atlas-track').focus() }
  if (e.target.id === 'atlas-format') { st.atlasFormat = e.target.value; render(); qs('#atlas-format').focus() }
});
document.addEventListener('submit', e => { if (e.target.dataset.form === 'tutor') { e.preventDefault(); ask(qs('#tutor-in').value) } if (e.target.dataset.form === 'join') { e.preventDefault(); roomJoin(qs('#join-code').value) } });
document.addEventListener('keydown', e => {
  if (qs('#overlay').innerHTML) {
    if (e.key === 'Escape') { closeModal(); return }
    if (e.key === 'Tab') { const f = qa('#overlay button, #overlay a[href]'); if (!f.length) return; const first = f[0], last = f[f.length - 1]; if (e.shiftKey && document.activeElement === first) { last.focus(); e.preventDefault() } else if (!e.shiftKey && document.activeElement === last) { first.focus(); e.preventDefault() } }
    return;
  }
  if (e.target.matches('input[type=text],input[type=search],input:not([type]),textarea,select') || e.metaKey || e.ctrlKey || e.altKey) return;
  if (e.target.matches('[role=tab][data-tab]') && (e.key === 'ArrowRight' || e.key === 'ArrowLeft')) { const t = qa('[data-tab]'), i = t.indexOf(e.target), n = t[(i + (e.key === 'ArrowRight' ? 1 : t.length - 1)) % t.length]; n.click(); e.preventDefault(); return }
  if (st.view !== 'play') return; const c = card(); if (!c) return;
  if (st.phase === 'predict') {
    if ((c.format === 'choice' || c.format === 'causal' || c.format === 'multi') && /^[1-9]$/.test(e.key)) { const o = optionOrder(c)[+e.key - 1]; if (o) qs(`[data-choice="${o.i}"]`)?.click(); return }
    if (e.key === 'Enter' && (!e.target.matches('button') || e.target.matches('.opt,[data-deleg],[data-rank]')) && S.ready(c, st.resp)) { e.preventDefault(); lock(); return }
  } else if (e.key === 'n' || e.key === 'N') { next() }
});

// ---------- boot ----------
document.body.insertAdjacentHTML('afterbegin', `<a class="skip" href="#view">Skip to content</a>`);
// Live classes need the Python server; hide their entry points in the offline file and inside Streamlit's frame.
if (!location.protocol.startsWith('http')) qa('[data-act="join"], a[href="classroom.html"]').forEach(el => el.hidden = true);
qs('#brand-glyph').outerHTML = glyph;
if (location.protocol.startsWith('http')) {
  fetch('/api/tutor/status').then(r => r.ok ? r.json() : null).then(d => { if (d && d.enabled) { TUTOR_REMOTE = '/api/tutor'; if (st.view === 'play' && st.phase === 'reveal') render() } }).catch(() => { });
}
if (PARAM.get('room')) { render(); roomJoin(PARAM.get('room')) } else if (PARAM.get('play') && BY_ID[PARAM.get('play')]) { const c = ALL.find(x => x.id === PARAM.get('play')); if (c) start([c], 1); else render() } else render();
window.THV = { st, ALL, BY_ID, records: () => records }; // test hook
})();
