(() => {
'use strict';
// ---------- data ----------
const S = window.THVScore;
// Served by the classroom server, the page carries no answers; the evidence arrives after a call is locked.
const PUBLIC = !!BANK.public;
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
const FORMAT_NAME = { choice: 'Pick one', causal: 'Find the cause', multi: 'Pick two', estimate: 'Estimate', forecast: 'Forecast', rank: 'Rank', allocate: 'Allocate', delegate: 'Delegate' };

// ---------- helpers ----------
const qs = s => document.querySelector(s);
const qa = s => [...document.querySelectorAll(s)];
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const pct = x => Math.round(x * 100);
const sbar = v0 => { const v = Math.max(-100, Math.min(100, v0)); return v < 0 ? `left:${50 + v / 2}%;width:${-v / 2}%` : `left:50%;width:${v / 2}%` };   // scores run from -100 to 100 around a zero line
const mn = v => String(v).replace(/^-/, '\u2212');   // a true minus sign in displayed numbers
function hash(str) { let h = 2166136261; for (let i = 0; i < str.length; i++) h = Math.imul(h ^ str.charCodeAt(i), 16777619); return h >>> 0 }
function rng(seed) { let x = seed >>> 0; return () => { x += 0x6D2B79F5; let t = x; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296 } }
function shuffle(a, r) { a = [...a]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1));[a[i], a[j]] = [a[j], a[i]] } return a }
const store = {
  get(k, d) { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? d } catch { return d } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)) } catch { } },
  del(k) { try { localStorage.removeItem(k) } catch { } }
};
async function ensureFull(id) {
  const c = BY_ID[id]; if (!PUBLIC || !c || c.answerTitle) return true;
  try { const r = await fetch('/api/reveal/' + encodeURIComponent(id), { headers: { 'X-Client-Id': clientId() } }); const d = await r.json(); if (!r.ok) { if (d.class_lock) CLASS_LOCK = true; notice(d.error || 'The evidence could not be loaded.'); return false } mergeFull(c, d); return true }
  catch { notice('The evidence could not be loaded. Check your connection and lock again.'); return false }
}
// Source takeaways and notes state findings, so the server sends them with the evidence.
function mergeFull(c, d) {
  const notes = d.sourceNotes || {}; delete d.sourceNotes; Object.assign(c, d);
  for (const [sid, n] of Object.entries(notes)) if (SOURCE[sid]) { const { note, ...rest } = n; Object.assign(SOURCE[sid], rest); if (note) SOURCE[sid].verification = { ...SOURCE[sid].verification, note } }
}
let libraryLoaded = !PUBLIC;
async function loadLibrary() {
  if (libraryLoaded) return; libraryLoaded = true;
  try { const r = await fetch('/api/library', { headers: { 'X-Client-Id': clientId() } }); const d = await r.json(); for (const x of d.challenges || []) if (BY_ID[x.id]) mergeFull(BY_ID[x.id], x); if (d.themes && d.themes.length) BANK.themes = d.themes; render() } catch { libraryLoaded = false }
}
function cite(id) { const s = SOURCE[id]; return s ? `${s.authors} (${s.year})` : id }
function srcStatus(s) { const v = s.verification || {}; return v.status === 'verified_full_text' ? ['Checked against the published full text', ''] : v.status === 'verified_accepted_manuscript' ? ['Checked against the authors’ accepted manuscript', ''] : v.status === 'verified_published_excerpts' ? ['Checked against the publisher’s abstract and figure legends', ''] : ['Checked against the published abstract', 'abstract'] }

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
let CLASS_LOCK = false;
function refreshLock() { if (!PUBLIC) return; fetch('/api/health').then(r => r.ok ? r.json() : null).then(d => { const was = CLASS_LOCK; CLASS_LOCK = !!(d && d.class_lock); if (was !== CLASS_LOCK && st.view === 'play') render() }).catch(() => { }) }
function start(pool, n) {
  refreshLock();
  st.deck = buildDeck(pool, n, st.seed); st.i = 0; st.session = []; resetCard(); st.view = 'play'; render(true);
}
function startTrack() { const pool = st.track === 'Mixed' ? ALL : ALL.filter(c => c.track === st.track); start(pool.length ? pool : ALL, st.length) }
function resetCard() {
  const c = card(); st.tab = 'questions'; st.phase = 'predict'; st.touched = false; st.conf = 60; st.confTouched = false; st.tutor = { busy: false, text: '', cites: [] };
  if (!c) { st.resp = null; return }
  st.resp = c.format === 'multi' ? [] : c.format === 'rank' ? shuffle(c.options.map((_, i) => i), rng(hash(c.id + st.seed))) :
    c.format === 'allocate' ? evenSplit(c) : c.format === 'delegate' ? c.delegate.tasks.map(() => null) :
      c.format === 'forecast' ? 50 : c.format === 'estimate' ? null : null;
  if (c.format === 'rank' && c.rankAnswer) { const R = rng(hash(c.id + st.seed + 'r')); for (let k = 0; k < 20 && S.score(c, st.resp).correct; k++) st.resp = shuffle(st.resp, R) }   // never start on the answer; a fresh shuffle, so the start order carries no hint
}
function evenSplit(c) { const k = c.options.length, t = c.allocate.total, step = c.allocate.step || 10; const base = Math.floor(t / k / step) * step; const a = Array(k).fill(base); let rest = t - base * k; const ord = optionOrder(c).map(o => o.i); for (let j = 0; rest > 0; j = (j + 1) % k) { a[ord[j]] += step; rest -= step } return a }   // any remainder follows the shuffled display order
function optionOrder(c) { return shuffle(c.options.map((t, i) => ({ t, i })), rng(hash(c.id + '-' + st.seed))) }

const okRoute = (t, m) => m === t.answer || (t.also || []).includes(m);
function needsTouch(c) { return ['forecast', 'rank', 'allocate'].includes(c.format) }
// Forecasts and allocations are probability statements already, so they take no separate confidence.
const noConf = c => c.format === 'forecast' || c.format === 'allocate';
// What "right" means for the confidence question, per format (matches S.score().correct).
function confQuestion(c) {
  return ({ choice: 'How sure are you that this is right?', causal: 'How sure are you that this is right?', multi: 'How sure are you that both picks are right?',
    estimate: `How sure are you that you land within ${c.estimate ? c.estimate.tolerance : ''}${c.estimate && (c.estimate.unit ?? '%') === '%' ? ' points' : ''} of the study value?`,
    rank: 'How sure are you of the exact order?', delegate: 'How sure are you that every task is routed right?' })[c.format] || 'How sure are you?';
}
function lockReady(c) { return S.ready(c, st.resp) && (!needsTouch(c) || st.touched) && (noConf(c) || st.confTouched) }
function lockHint(c) {
  if (!S.ready(c, st.resp) || (needsTouch(c) && !st.touched)) return c.format === 'forecast' ? 'Move the slider to state a probability' : c.format === 'rank' ? 'Put the items in your order' : c.format === 'allocate' ? 'Split the budget your way' : 'Make your call';
  if (!noConf(c) && !st.confTouched) return 'Now say how sure you are';
  return '';
}
function syncLock() { const c = card(); const b = qs('#lock-btn'); if (!c || !b) return; b.disabled = !lockReady(c); const h = qs('.actionbar .kicker'); if (h) h.textContent = lockHint(c) }
let locking = false;
async function lock() {
  const c = card(); if (!c || !lockReady(c) || locking) return;
  if (st.room) {  // the server holds the evidence until the instructor reveals it
    st.pending = { response: st.resp, confidence: noConf(c) ? null : st.conf };
    st.phase = 'reveal'; render(true); roomSubmit(c, st.pending); return;
  }
  locking = true; const b = qs('#lock-btn'); if (b) { b.disabled = true; b.textContent = PUBLIC ? 'Checking the evidence' : 'Locked' }
  qs('.focus-card')?.classList.add('is-locked');
  const okFull = await ensureFull(c.id);
  if (!okFull) { locking = false; syncLock(); if (b) b.textContent = CLASS_LOCK ? 'Results open after the class reveal' : 'Try again';
    if (CLASS_LOCK && !qs('#skip-locked')) b?.insertAdjacentHTML('beforebegin', '<button class="btn btn-quiet" id="skip-locked" data-act="skip-locked">Next decision</button>'); qs('.focus-card')?.classList.remove('is-locked'); return }
  if (!matchMedia('(prefers-reduced-motion: reduce)').matches) await new Promise(z => setTimeout(z, 420));
  locking = false;
  finalize(c, st.resp, noConf(c) ? null : st.conf);
  st.phase = 'reveal'; render(true);
}
function finalize(c, response, confidence) {
  const res = S.score(c, response);
  const rec = { id: c.id, format: c.format, score: Math.round(res.score * 1000) / 1000, correct: res.correct, confidence, response, at: new Date().toISOString(), seed: st.seed, detail: res.detail, title: c.title, answerTitle: c.answerTitle, implication: c.implication };
  if (c.format === 'forecast') rec.outcome = c.forecast.truth ? 1 : 0;
  rec.base = S.baseline(c);   // computed while the evidence is loaded
  if (c.format === 'allocate' && Array.isArray(response)) { const cr = S.toCalibrationRecord(c, { format: 'allocate', response, correct: res.correct }); if (cr) rec.topBest = cr.outcome === 1 }   // stored now: the served bank has no answers after a reload
  st.session.push(rec); records.push(rec); records = records.slice(-3000); store.set(REC_KEY, records);
  return rec;
}
function next() { if (st.i >= st.deck.length - 1) { st.view = 'record'; st.deck = []; render(true); return } st.i++; resetCard(); render(true) }

// ---------- views ----------
const glyph = `<svg class="brand-glyph" viewBox="0 0 26 26" aria-hidden="true"><rect x="1" y="1" width="24" height="24" rx="7" fill="#14203a"/><line x1="6" y1="17" x2="20" y2="17" stroke="#cbd3dd" stroke-width="1.5"/><circle cx="9.5" cy="17" r="3" fill="#2f54eb"/><circle cx="16.5" cy="17" r="3" fill="#e0a01c"/><path d="M9.5 12.5V8.5M16.5 12.5V8.5" stroke="#fff" stroke-width="1.5" stroke-linecap="round"/></svg>`;

// One tick per decision in the path, filled once played: the path's length and your progress, and nothing else.
function pathStrip(p, done) {
  const k = p.items.length, w = 3, g = 3;   // a word-sized graphic beside the count
  return `<svg class="strip" viewBox="0 0 ${k * (w + g) - g} 12" width="${k * (w + g) - g}" height="12" aria-hidden="true">${p.items.map((id, i) => `<rect x="${i * (w + g)}" y="0" width="${w}" height="12" class="${done.has(id) ? 'on' : ''}"/>`).join('')}</svg>`;
}
// The home page's one bold element: the game in a single gesture, on a measuring scale the width of the page.
// Ticks every point, labels every ten; after the lock the study's value, its band and the gap are drawn on the same scale.
function ruler(min, max, you, ev, band, unit = '%', step = 1) {
  const pos = v => (v - min) / (max - min) * 100, ticks = [], span = max - min;
  const on = (v, m) => Math.abs(v / m - Math.round(v / m)) < 1e-6, MAJ = [1, 2, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000];
  const major = MAJ.find(m => span / m <= 8 && on(min, m) && on(max, m)) || MAJ.find(m => span / m <= 8) || span;   // labels land on both ends when a round step allows it
  const minor = [major / 10, major / 5, major / 2, major].find(m => span / m <= 120 && m >= step - 1e-9 && on(m, step) && Number.isInteger(m * 1000)) || major;   // never finer than the slider's own step
  const mid = on(major / 2, minor) ? major / 2 : major / 5;   // the medium tick that survives on phones
  const grid = []; for (let v = Math.ceil(min / minor - 1e-9) * minor; v <= max + 1e-9; v += minor) grid.push(+v.toFixed(6));
  if (Math.abs(grid[0] - min) > 1e-9) grid.unshift(min); if (Math.abs(grid[grid.length - 1] - max) > 1e-9) grid.push(max);   // both ends always get a tick and a label, even off the grid (audit 37)
  for (const vv of grid) { const lab = on(vv, major) && Math.min(vv - min, max - vv) >= major * .7 || Math.abs(vv - min) < 1e-9 || Math.abs(vv - max) < 1e-9; const end = Math.abs(vv - min) < 1e-9 || Math.abs(vv - max) < 1e-9, show = lab && (ev === null || ev === undefined || end && Math.abs(pos(vv) - pos(ev)) >= 16); ticks.push(`<i class="${on(vv, major) || lab ? 'l' : on(vv, mid) ? 'm' : ''}" style="left:${pos(vv)}%"></i>${show ? `<em class="${Math.abs(vv - min) < 1e-9 ? 'e0' : Math.abs(vv - max) < 1e-9 ? 'e1' : `${Math.abs(Math.round(vv / major)) % 2 ? 'alt' : ''}${Math.min(vv - min, max - vv) < major - 1e-9 ? ' near' : ''}`}" style="left:${pos(vv)}%">${esc(mn(vv + unit))}</em>` : ''}`) }   // both ends always labelled; a round value too close to an end gives way
  const has = x => x !== null && x !== undefined;
  const lo = has(ev) && has(band) ? Math.max(min, ev - band) : null, hi = has(ev) && has(band) ? Math.min(max, ev + band) : null;
  const gap = has(you) && has(ev) ? Math.abs(you - ev) : null, a = has(gap) ? Math.min(you, ev) : 0, b = has(gap) ? Math.max(you, ev) : 0;
  return `<div class="ruler-scale" aria-hidden="true">${ticks.join('')}${has(lo) ? `<span class="r-band" style="left:${pos(lo)}%;width:${pos(hi) - pos(lo)}%"></span>` : ''}${has(gap) && gap > 0 ? `<span class="r-gap" style="left:${pos(a)}%;width:${pos(b) - pos(a)}%"><b>${+gap.toFixed(2)}${unit === '%' ? (gap === 1 ? ' point' : ' points') : ' ' + unit}</b></span>` : ''}${has(you) && has(ev) ? `<span class="r-mark you" style="left:${pos(you)}%"><b>You ${esc(mn(you + unit))}</b></span>` : ''}${has(ev) ? `<span class="r-mark ev" style="left:${pos(ev)}%"></span><em class="ev-lab ${pos(ev) < 12 ? 'e0' : pos(ev) > 88 ? 'e1' : ''}" style="left:${pos(ev)}%">Study ${esc(mn(ev + unit))}</em>` : ''}</div>`;   // once the study value is shown it takes the axis row (ends stay unless it sits on one), so it never collides with the player's label above
}
function heroTry() {
  const c = BY_ID.ai01; if (!c || !isLive(SOURCE[c.sources[0]])) return '';
  const h = st.hero, e = c.estimate, v = h.value, src = SOURCE[c.sources[0]];
  const gap = v === null ? 0 : Math.abs(v - e.target);
  return `<section class="try-ruler" aria-labelledby="try-q">
    <div class="tr-head"><h1 id="try-q">Professionals were randomly given ChatGPT for short writing tasks. How much less time did they take?</h1>
    <p class="tr-read ${h.done ? 'ev' : ''}"><b class="num ${v === null ? 'empty' : ''}" id="hero-read">${h.done ? e.target + '%' : v === null ? '00%' : v + '%'}</b><span class="hero-unit">${h.done ? 'less time, the study' : v === null ? 'Slide the scale to answer' : 'less time, your call'}</span></p></div>
    <div class="ruler ${h.done ? 'done' : ''}">${h.done ? ruler(e.min, e.max, v, e.target, e.tolerance) : `${ruler(e.min, e.max, null, null, null)}<label class="sr-only" for="hero-range">Your estimate of the time saved, in percent</label>
    <input id="hero-range" type="range" min="${e.min}" max="${e.max}" step="1" value="${v ?? Math.round((e.min + e.max) / 2)}" class="${v === null ? 'untouched' : ''}" style="--fill:${v === null ? 0 : (v - e.min) / (e.max - e.min) * 100}%">`}</div>
    <div class="tr-foot"><p class="try-result" aria-live="polite">${h.done ? `They took ${e.target}% less time. ${gap === 0 ? 'You were exactly right.' : `You were ${gap} ${gap === 1 ? 'point' : 'points'} off.`}` : ''}</p>${h.done ? `<button class="btn btn-solid" data-act="start-quick">Play five more</button><button class="link-btn" data-act="hero-reset">Try again</button>` : `<button class="btn btn-you" data-act="hero-lock" ${v === null ? 'disabled' : ''}>Lock my estimate</button>`}<span class="try-src">${esc(src.authors)}, ${esc(src.venue)} ${src.year}</span></div>
  </section>`;
}



function home() {
  const nSrc = Object.values(SOURCE).filter(isLive).length;
  const dimant = Object.values(SOURCE).filter(s => isLive(s) && /Dimant/.test(s.authors_full || s.authors));
  const paths = (BANK.paths || []).map(p => ({ ...p, items: p.ids.filter(id => ALL.some(c => c.id === id)) })).filter(p => p.items.length);
  const done = new Set(records.map(r => r.id));
  const resume = paths.find(p => { const n = p.items.filter(id => done.has(id)).length; return n > 0 && n < p.items.length });
  return `${resume ? `<div class="resume wrap"><span>Continue <strong>${esc(resume.title)}</strong>: ${resume.items.filter(id => done.has(id)).length} of ${resume.items.length} played.</span><button class="btn btn-quiet" data-path="${esc(resume.id)}" data-resume="1">Continue</button></div>` : ''}<section class="hero wrap">${heroTry()}
    <div class="hero-foot"><div class="hero-actions"><button class="btn btn-solid btn-lg" data-act="go-start">Start playing</button>${location.protocol.startsWith('http') ? '<button class="link-btn" data-act="join">Join a live class</button>' : ''}</div>
    <p class="hero-meta">${ALL.length} decisions on AI, work and behavior, drawn from ${nSrc} peer-reviewed studies. Original concept by Eugen Dimant.</p></div></section>
  <section class="section wrap" id="start" aria-labelledby="paths-h"><div class="row-head"><h2 id="paths-h">Choose a path</h2><button class="link-btn" data-act="toggle-custom" aria-expanded="${st.custom ? 'true' : 'false'}">${st.custom ? 'Hide custom round' : 'Or build a custom round'}</button></div>
    ${st.custom ? customRound() : ''}
    <div class="paths">${paths.map((p, pi) => { const n = p.items.filter(id => done.has(id)).length; return `<button class="path" data-path="${esc(p.id)}" data-kind="${['leading-ai', 'ai-customers', 'trust-algo', 'truth'].includes(p.id) ? 'ai' : 'bx'}"><strong>${esc(p.title)}</strong><span>${esc(p.blurb)}</span><small>${pathStrip(p, done)}${pi === 0 ? 'Start here. ' : ''}${p.items.length} decisions${p.case ? ', with a multi-step case' : ''}${n ? `, ${n} played` : ''}</small></button>` }).join('')}</div>
  </section>
  ${dimant.length ? `<section class="section wrap dimant-band"><div class="dimant"><div><h2>Research by Eugen Dimant</h2><p>How the shape of a norm, the visibility of peers and political identity change what people do at work and in society.</p><p class="dimant-stat">${ALL.filter(c => c.sources.some(id => dimant.some(d => d.id === id))).length} decisions in the game draw on ${dimant.length} of his published papers, in Management Science, PNAS Nexus, Scientific Reports and other journals.</p><button class="btn btn-line" data-path="dimant-lab">Play this path</button></div>
    <ul class="paper-list">${dimant.slice(0, 6).map(s => `<li><button data-source="${esc(s.id)}"><strong>${esc(paperTitle(s) || ALL.find(c => c.sources.includes(s.id))?.title || s.venue)}</strong><small>${esc(s.venue)}, ${s.year}</small></button></li>`).join('')}</ul></div></section>` : ''}`;
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
    return `${c.format === 'causal' && c.dag ? dag(c.dag, rev) + (rev ? '' : '<p class="hint dag-hint">The factors in play. The reveal draws the links the study found.</p>') : ''}<div class="opts" role="group" aria-label="Answer options">${optionOrder(c).map((o, j) => `<button class="opt ${rev && isEv(o.i) ? 'is-ev' : ''}" data-choice="${o.i}" aria-pressed="${picked(o.i)}" ${rev ? 'disabled' : ''}><span class="k" aria-hidden="true">${j + 1}</span><span>${esc(o.t)}</span>${rev && (isEv(o.i) || picked(o.i)) ? `<span class="mark">${picked(o.i) ? '<span class="k-you">Your call</span>' : ''}${isEv(o.i) ? '<span class="k-ev">Evidence</span>' : ''}</span>` : ''}</button>`).join('')}</div>`;
  }
  if (c.format === 'estimate') {
    const e = c.estimate, v = r ?? Math.round((e.min + e.max) / 2);
    return `<div class="meter est-meter"><div class="meter-read"><span class="est-label" id="est-label">${esc(e.label)}</span><b class="${r === null ? 'empty' : ''}" id="est-read">${r === null ? '00%' : esc(mn(r + (e.unit ?? '%')))}</b></div>
      <div class="ruler">${ruler(e.min, e.max, null, null, null, e.unit ?? '%', e.step || 1)}<input type="range" id="est" aria-labelledby="est-label" min="${e.min}" max="${e.max}" step="${e.step || 1}" value="${v}" class="${r === null ? 'untouched' : ''}" style="--fill:${r === null ? 0 : (v - e.min) / (e.max - e.min) * 100}%" ${rev ? 'disabled' : ''}></div></div>`;   // the same measuring scale as the home page (redesign, round 36)
  }
  if (c.format === 'forecast') {
    return `<div class="meter est-meter"><div class="meter-read"><span class="est-label" id="fc-label">Probability the claim is true</span><b class="${st.touched ? '' : 'empty'}" id="fc-read">${st.touched ? r + '%' : '00%'}</b></div>
      <div class="ruler">${ruler(0, 100, null, null, null, '%', 5)}<input type="range" id="fc" aria-labelledby="fc-label" min="0" max="100" step="5" value="${r}" class="${st.touched ? '' : 'untouched'}" style="--fill:${st.touched ? r : 0}%" ${rev ? 'disabled' : ''}></div>
      <div class="axis"><span>certainly false</span><span>certainly true</span></div></div>`;
  }
  if (c.format === 'rank') {
    return `<p class="hint">First place goes at the top. Use the arrows to reorder.</p><ol class="rank-list">${r.map((oi, k) => `<li class="rank-item"><span class="pos">${k + 1}</span><span>${esc(c.options[oi])}</span><span class="rank-move"><button data-rank="${k}" data-dir="-1" aria-label="Move ${esc(c.options[oi])} up" ${k === 0 || rev ? 'disabled' : ''}>↑</button><button data-rank="${k}" data-dir="1" aria-label="Move ${esc(c.options[oi])} down" ${k === r.length - 1 || rev ? 'disabled' : ''}>↓</button></span></li>`).join('')}</ol>`;
  }
  if (c.format === 'allocate') {
    const a = c.allocate, sum = r.reduce((x, y) => x + y, 0);
    return `<div class="alloc">${optionOrder(c).map(({ t: o, i: k }) => `<div class="alloc-row"><label for="al${k}">${esc(o)}</label><input type="range" id="al${k}" data-alloc="${k}" min="0" max="${a.total}" step="${a.step || 10}" value="${r[k]}" style="--fill:${r[k] / a.total * 100}%" ${rev ? 'disabled' : ''}><output for="al${k}" class="num">${a.prefix || ''}${r[k]}${a.suffix || ''}</output></div>`).join('')}
      <p class="hint">Moving one slider shifts points from the others, so the total stays at ${a.total}.</p><div class="alloc-total ${sum === a.total ? 'ok' : ''}" aria-live="polite"><span>${esc(a.label)}</span><span class="num">${a.prefix || ''}${sum}${a.suffix || ''} of ${a.prefix || ''}${a.total}${a.suffix || ''}${sum === a.total ? '' : sum > a.total ? ', too many' : ', still to place'}</span></div></div>`;
  }
  if (c.format === 'delegate') {
    return `<div class="deleg">${c.delegate.tasks.map((t, k) => `<div class="deleg-row" role="group" aria-label="${esc(t.text)}"><p>${esc(t.text)}</p><div class="deleg-opts">${c.delegate.choices.map((ch, m) => `<button data-deleg="${k}" data-pick="${m}" aria-pressed="${r[k] === m}" aria-label="${esc(short(t.text, 60))}: ${esc(ch)}" class="${rev && okRoute(t, m) ? 'is-ev' : ''}" ${rev ? 'disabled' : ''}>${esc(ch)}</button>`).join('')}</div>${rev ? `<p class="deleg-why">${okRoute(t, r[k]) ? 'Matches the evidence. ' : 'Evidence points to ' + [t.answer, ...(t.also || [])].map(i => esc(c.delegate.choices[i])).join(' or ') + '. '}${esc(t.why)}</p>` : ''}</div>`).join('')}</div>`;
  }
  return '';
}

// Before the reveal, the accessible description lists boxes and arrows only; the written explanation (d.alt) states the answer.
function dagAlt(d) {
  const lab = n => n.mask ? 'an unknown factor' : n.label, by = Object.fromEntries(d.nodes.map(n => [n.id, n]));
  return `Causal diagram. Factors in play: ${d.nodes.map(lab).join(', ')}. The links appear after your call.`;
}
const DAG_DRAWN = new WeakSet();   // the arrows animate once per reveal, not on every re-render
function dag(d, rev) {
  const fresh = rev && !DAG_DRAWN.has(d); if (rev) DAG_DRAWN.add(d);
  // The stored layout is stretched to a 700-wide canvas and 1.5 times taller, so every link runs at least about 100 units between pills (review 29, m1)
  const narrow = innerWidth < 640, xs = d.nodes.map(n => n.x), ys = d.nodes.map(n => n.y), x0 = Math.min(...xs), x1s = Math.max(...xs), y0 = Math.min(...ys), y1s = Math.max(...ys), W = narrow ? 360 : 700, SY = 1.5;
  const cols = [...new Set(xs)].sort((a, b) => a - b);   // on a phone the diagram runs top to bottom: each stored column becomes a row (review 30, m5)
  const nodes = d.nodes.map(n => narrow ? { ...n, x: n.px ?? (y1s > y0 ? 70 + (n.y - y0) * (W - 140) / (y1s - y0) : W / 2), y: n.py ?? 40 + cols.indexOf(n.x) * 125 }
    : { ...n, x: x1s > x0 ? 70 + (n.x - x0) * (W - 140) / (x1s - x0) : W / 2, y: 40 + (n.y - y0) * SY });
  const H = Math.max(...nodes.map(n => n.y)) + 40;
  const node = Object.fromEntries(nodes.map(n => [n.id, n]));
  const edge = ([a, b, style0], i) => { const style = rev ? style0 : ''; const A = node[a], B = node[b]; const dx = B.x - A.x, dy = B.y - A.y, L = Math.hypot(dx, dy), ux = dx / L, uy = dy / L; const t = Math.min(Math.abs(ux) > 1e-9 ? 76 / Math.abs(ux) : 1e9, Math.abs(uy) > 1e-9 ? 34 / Math.abs(uy) : 1e9); const x1 = A.x + ux * t, y1 = A.y + uy * t, x2 = B.x - ux * t, y2 = B.y - uy * t;   // each end stops at its pill's edge
    // Before the reveal the diagram shows which factors are in play, not which way the arrows run.
    // Before the reveal the diagram shows only the factors in play; links would narrow the options. The reveal draws them one by one.
    if (!rev) return '';
    return `<line ${fresh ? 'class="ed"' : ''} x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${style === 'q' ? '#e0a01c' : '#14203a'}" stroke-width="${style === 'q' ? 4 : 2}" ${style === 'q' ? 'stroke-dasharray="7 5"' : ''} marker-end="url(#${style === 'q' ? 'ahq' : 'ah'})"/>` };
  return `<svg class="dag" viewBox="-6 0 ${W + 12} ${H}" role="img" aria-label="${esc(rev ? d.alt : dagAlt(d))}"><defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="#14203a"/></marker><marker id="ahq" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="#e0a01c"/></marker></defs>${d.edges.map(edge).join('')}${nodes.map(n0 => { const n = !rev && n0.mask ? { ...n0, label: '?', hidden: true } : n0; return `<g>${(() => { const lab = dagLabel(n, 17), hh = lab.includes('data-two') ? 30 : 24; return `<rect x="${n.x - 70}" y="${n.y - hh}" width="140" height="${2 * hh}" rx="24" fill="${n.hidden ? '#fff' : '#14203a'}" stroke="#14203a" stroke-width="1.5" ${n.hidden ? 'stroke-dasharray="4 4"' : ''}/>${lab}` })()}</g>` }).join('')}</svg>`;
}

// A node label fits its 140-wide pill: one line if it fits, else two balanced lines, shrunk only as far as needed (review 27: bz12 at 390 px)
// Width of a label in the node font, measured once per string and size (falls back to an average glyph width)
const TW = {}; let TWC = null;
function textWidth(t, f) { const k = f + '|' + t; if (k in TW) return TW[k]; try { TWC = TWC || document.createElement('canvas').getContext('2d'); TWC.font = `650 ${f}px "Schibsted Grotesk", system-ui, sans-serif`; return (TW[k] = TWC.measureText(String(t)).width) } catch { return String(t).length * f * .58 } }
function dagLabel(n, base) {
  const fill = n.hidden ? '#14203a' : '#fff', wid = (t, f) => textWidth(t, f), words = String(n.label).split(' ');
  const attrs = f => `text-anchor="middle" font-size="${f}" font-weight="650" font-family="Schibsted Grotesk,system-ui" fill="${fill}"`;
  if (wid(n.label, base) <= 128 || words.length < 2) { const f = Math.min(base, Math.floor(base * 128 / wid(n.label, base))); return `<text x="${n.x}" y="${n.y + f * .3}" ${attrs(f)}>${esc(n.label)}</text>` }
  let best = null; for (let k = 1; k < words.length; k++) { const a = words.slice(0, k).join(' '), b = words.slice(k).join(' '), m = Math.max(wid(a, base), wid(b, base)); if (!best || m < best.m) best = { a, b, m } }
  const f = Math.min(base, Math.floor(base * 128 / best.m));   // a two-line label gets a taller pill (60 high) rather than smaller type
  return `<text data-two="1" x="${n.x}" y="${n.y - f * .42}" ${attrs(f)}>${esc(best.a)}</text><text x="${n.x}" y="${n.y + f * .8}" ${attrs(f)}>${esc(best.b)}</text>`;
}

// The gap: player's call (blue) and the evidence (amber) on one axis.
function gapAxis({ min, max, unit = '%', you, ev, band, evLabel = 'Evidence', id = 'g', fmt: fmt0 = x => x + unit, evText = null }) {
  const fmt = x => mn(fmt0(x));   // every number on the plate takes a true minus (review 26, I12)
  const narrow = innerWidth < 640, W = narrow ? 360 : 640, fs = narrow ? 14 : 19, L = 18, R = W - 18, y = 52, sx = v => L + (v - min) / (max - min) * (R - L);
  const has = v => v !== null && v !== undefined;
  const anchor = x => x < L + (narrow ? 40 : 60) ? 'start' : x > R - (narrow ? 40 : 60) ? 'end' : 'middle';
  const lab = (x, txt, color, up) => `<text x="${Math.min(R, Math.max(L, x))}" y="${up ? y - 22 : y + 36}" text-anchor="${anchor(x)}" font-size="${fs}" font-weight="750" class="${color}" font-family="Schibsted Grotesk,system-ui">${esc(txt)}</text>`;
  return `<svg class="axis-svg" viewBox="0 0 ${W} 118" role="img" aria-label="${has(you) ? 'Your call ' + fmt(you) : 'No call yet'}${has(ev) ? ', evidence ' + fmt(ev) : ''}${has(band) && has(ev) ? ', hit band ' + fmt(+(Math.max(min, ev - band)).toFixed(1)) + ' to ' + fmt(+(Math.min(max, ev + band)).toFixed(1)) : ''}">
    <line x1="${L}" y1="${y}" x2="${R}" y2="${y}" class="ax-track" stroke-width="2"/>${(() => { const span = max - min, major = [1, 2, 5, 10, 20, 25, 50, 100, 200, 500].find(m => span / m <= 8) || span, minor = major / (major % 5 === 0 ? 5 : 2), out = []; for (let v = Math.ceil(min / minor) * minor; v <= max + 1e-9; v += minor) { const isM = Math.abs(v / major - Math.round(v / major)) < 1e-9; out.push(`<line x1="${sx(v)}" y1="${y - (isM ? 9 : 5)}" x2="${sx(v)}" y2="${y + (isM ? 9 : 5)}" class="ax-tickm${isM ? ' maj' : ''}"/>`) } return out.join('') })()}
    ${has(band) && has(ev) ? `<rect x="${sx(Math.max(min, ev - band))}" y="${y - 9}" width="${sx(Math.min(max, ev + band)) - sx(Math.max(min, ev - band))}" height="18" rx="4" class="ax-band" stroke-width="1.2"/>` : ''}
    ${has(you) && has(ev) ? `<line x1="${sx(you)}" y1="${y}" x2="${sx(ev)}" y2="${y}" class="ax-gap" stroke-width="2.5" stroke-dasharray="3 4"/>` : ''}
    ${has(you) ? `<circle cx="${sx(you)}" cy="${y}" r="12" fill="#2f54eb" stroke="#fff" stroke-width="3"/>${lab(sx(you), 'You ' + fmt(you), 'ax-you', true)}` : ''}
    ${has(ev) ? `<g class="ev-mark" id="${id}-ev" data-from="${has(you) ? sx(you) - sx(ev) : 0}"><circle cx="${sx(ev)}" cy="${y}" r="12" fill="#e0a01c" stroke="#fff" stroke-width="3"/>${lab(sx(ev), evText ?? evLabel + ' ' + fmt(ev), 'ax-ev', false)}</g>` : ''}
    ${has(band) && has(ev) ? (() => { const m = narrow ? 134 : 140, bx = Math.min(R - m, Math.max(L + m, sx(ev))); return `<text x="${bx}" y="114" font-size="${narrow ? 15 : 17}" text-anchor="middle" class="ax-band-lab" font-family="Schibsted Grotesk,system-ui">hit band ${esc(fmt(+(Math.max(min, ev - band)).toFixed(1)))} to ${esc(fmt(+(Math.min(max, ev + band)).toFixed(1)))}</text>` })() : ''}
    <text x="${L}" y="114" font-size="${narrow ? 14 : 16}" class="ax-tick" font-family="Schibsted Grotesk,system-ui">${esc(fmt(min))}</text><text x="${R}" y="114" font-size="${narrow ? 14 : 16}" class="ax-tick" text-anchor="end" font-family="Schibsted Grotesk,system-ui">${esc(fmt(max))}</text></svg>`;
}

function gapFigure(c, rec) {
  const r = rec.response; let body = '', cap = '';
  if (c.format === 'estimate') { const e = c.estimate; const u = (e.unit ?? '%') === '%' ? ' points' : e.unit, f = x => mn(x + (e.unit ?? '%')); body = (e.label ? `<p class="plate-h">${esc(e.label)}</p>` : '') + gapHead(f(r), f(e.target), rec.detail.gap <= e.tolerance ? 'Inside the band' : `${rec.detail.gap}${u} off`) + gapAxis({ min: e.min, max: e.max, unit: e.unit ?? '%', you: r, ev: e.target, band: e.tolerance, evLabel: 'Study' }); cap = c.chart ? '' : srcLine(c) }
  else if (c.format === 'forecast') { body = gapHead(r + '%', c.forecast.truth ? 'True' : 'False', `${Math.abs(r - (c.forecast.truth ? 100 : 0))} points from the truth`, 'You gave it', 'The claim') + `<p class="gap-claim">“${esc(c.forecast.claim)}”</p>` + gapAxis({ min: 0, max: 100, you: r, ev: c.forecast.truth ? 100 : 0, evText: c.forecast.truth ? 'Claim true' : 'Claim false', fmt: x => x + '%' }); cap = `A confident correct call earns 100, saying 50% earns 50, and a confident miss goes below zero.${c.chart ? '' : ' ' + srcLine(c)}` }
  else if (c.format === 'rank') {
    const truth = c.rankAnswer, ties = c.rankTies || [];
    const tied = (a, b) => ties.some(t => t.includes(a) && t.includes(b));
    // Items the study did not separate share a rank, shown as "2=".
    // A pair the study did not separate is marked on the lower row; its order is not scored.
    const tieUp = t => t > 0 && tied(truth[t - 1], truth[t]);
    const rkPlace = t => { let k = t; while (k > 0 && tieUp(k)) k--; return k };   // a tied row shares the place of the first row in its group
    const pctVals = c.rankValues && c.rankValues.every(v => /^[\u2212-]?\d+(\.\d+)?%$/.test(v)) ? c.rankValues.map(v => parseFloat(v.replace('\u2212', '-'))) : null;   // percentages share one 0 to 100 axis: plot them (review 26)
    body = `${pctVals && c.chart && c.chart.note ? `<p class="plate-h">${esc(c.chart.note.replace(/\.$/, ''))}, 0 to 100%</p>` : ''}<div class="rc-cols" aria-hidden="true"><span>${esc(c.rankLabel ? 'Order by ' + c.rankLabel.charAt(0).toLowerCase() + c.rankLabel.slice(1) : 'Measured order')}, top first</span><span class="k-ev">Study</span><span class="k-you">You</span></div><ol class="rank-cmp">${truth.map((oi, t) => { const k = r.indexOf(oi); return `<li class="${tieUp(t) ? 'tie' : ''}"><span class="rc-name">${esc(c.options[oi])}${pctVals ? `<span class="rc-dot" style="--v:${pctVals[oi]}%"><i aria-hidden="true" style="left:${pctVals[oi]}%"></i><b style="left:${pctVals[oi]}%">${esc(mn(c.rankValues[oi]))}</b></span>` : c.rankValues ? `<small>${esc(c.rankValues[oi])}</small>` : ''}</span><span class="rc-badge ${rkPlace(t) === 0 ? 'ev' : 'evn'}" title="Measured rank">${rkPlace(t) + 1}${tieUp(t) || tieUp(t + 1) ? '=' : ''}</span><span class="rc-badge you ${k === t || (tieUp(t) && k === t - 1) || (tieUp(t + 1) && k === t + 1) ? 'same' : ''}" title="Your rank">${k + 1}</span></li>` }).join('')}</ol>`;   // column heads over the numbers: no colour key
    cap = `${rec.detail.agree} of ${rec.detail.total} scored pairs in the measured order.${ties.length ? ' Places marked = were not told apart by the study, so their order is not scored.' : ''}${c.chart && !c.rankValues ? '' : ' ' + srcLine(c)}`
  }
  else if (c.format === 'allocate') {
    const a = c.allocate, tot = r.reduce((x, y) => x + y, 0) || 1, hi = Math.max(...a.values), evNum = k => { const m = String(a.valueLabels ? a.valueLabels[k] : a.values[k]).replace('−', '-').match(/-?\d+(\.\d+)?/); return m ? Math.max(0, parseFloat(m[0])) : 0 }, evNs = k => /n\.s\./.test(String(a.valueLabels ? a.valueLabels[k] : '')), evSigned = k => { const m = String(a.valueLabels ? a.valueLabels[k] : a.values[k]).replace('−', '-').match(/-?\d+(\.\d+)?/); return m ? parseFloat(m[0]) : 0 }, evLo = Math.min(0, ...c.options.map((_, k) => evSigned(k))), evHi = Math.max(1, ...c.options.map((_, k) => evSigned(k))), evSpan = evHi - evLo, evZero = -evLo / evSpan * 100, evMax = Math.max(1, ...c.options.map((_, k) => evNum(k))), isBest = k => a.best ? a.best.includes(k) : a.values[k] === hi;
    body = `${a.valueName ? `<p class="plate-h">Your points, and the study\u2019s ${esc(a.valueName.replace(/ \(non-significant[^)]*\)/, '')).replace(/\b(\w+-\w+)\b/g, '<span class="nw">$1</span>')}</p>` : ''}<div class="hbars alloc-cmp" role="img" aria-label="Your points per option; the option that worked best is marked">${optionOrder(c).map(({ t: o, i: k }, pos) => `<div class="hb-row two"><span class="hb-label">${esc(o)}${isBest(k) ? ' <em class="ev-note">worked best</em>' : ''}</span><span class="hb-track"><i class="grow you" style="width:${Math.max(1.5, r[k] / tot * 100)}%"></i></span><b class="num you">${pct(r[k] / tot)} pts</b><span class="hb-track efx">${evLo < 0 ? `<b class="zero" style="left:${evZero}%"></b>` : ''}<i class="dotv${isBest(k) ? ' ev' : ''}${evNs(k) ? ' ns' : ''}" style="left:${(evSigned(k) - evLo) / evSpan * 100}%"></i></span><b class="num ev${evNs(k) ? ' ns' : ''}">${esc(a.valueLabels ? a.valueLabels[k] : a.values[k])}</b></div>`).join('')}${(() => { const u = String((a.valueLabels || a.values).find(v => /\d/.test(String(v))) || '').match(/%|pp|points?/) || [''], f = v => mn((Math.round(v * 10) / 10) + (u[0] === '%' ? '%' : u[0] ? ' ' + u[0] : '')); return `<div class="hb-row hb-ends" aria-hidden="true"><span class="hb-scale" style="grid-area:t">${evLo < 0 && evZero <= 9 ? '<em></em>' : `<em>${f(evLo)}</em>`}${evLo < 0 && evHi > 0 ? `<em class="${evZero < 25 || evZero > 75 ? 'z-near' : ''}" style="left:${evZero}%">0</em>` : ''}${evLo < 0 && evZero >= 91 ? '<em></em>' : `<em>${f(evHi)}</em>`}</span></div>` })()}</div>`;   // the effect track's scale, at both ends (review 28)   // your points over the study's measured result, per option
    cap = `Score ${mn(pct(rec.score))}: 100 when all points sit on the option that worked best. ${srcLine(c)}`
  }
  else if (c.format === 'delegate') { body = `<p class="plate-h">Each task, routed as the evidence suggests; you matched ${rec.detail.right} of ${rec.detail.total}</p><ul class="deleg-cmp">${c.delegate.tasks.map((t, k) => `<li class="${okRoute(t, r[k]) ? 'ok' : ''}"><span>${esc(short(t.text, 70))}${t.why ? `<small class="deleg-why">${esc(t.why)}</small>` : ''}</span><span class="chip-row"><span class="chip you">You: ${esc(c.delegate.choices[r[k]] ?? '–')}</span>${okRoute(t, r[k]) ? '' : `<span class="chip ev">Evidence: ${[t.answer, ...(t.also || [])].map(i => esc(c.delegate.choices[i])).join(' or ')}</span>`}</span></li>`).join('')}</ul>`; cap = '' }
  else if (c.chart) { body = bars(c.chart); cap = srcLine(c) }
  else { body = `<p class="big-stat">${rec.correct ? 'Match' : rec.score > 0 ? 'Partial' : 'Miss'}</p>`; cap = '' }
  if (c.chart && ['forecast', 'rank', 'estimate', 'delegate', 'allocate'].includes(c.format) && !(c.format === 'rank' && c.rankValues)) { body += `<div class="plate-more"><p class="plate-h">${esc((c.chart.note || '').replace(/\.$/, ''))}</p>${bars(c.chart)}<p class="small">${esc(srcLine(c))}</p></div>` }   // the paper's own figure under the format's gap view
  const opt = ['choice', 'causal', 'multi'].includes(c.format), plate = !(opt && !c.chart);   // the evidence sits on a dark plate; a plain option list stays light
  const legend = opt && c.chart ? `<p class="plate-h">${esc((c.chart.note || '').replace(/\.$/, ''))}</p>` : '';   // no colour keys: every mark is labelled where it sits
  const main = opt && !c.chart ? instrument(c) : body, caption = opt && !c.chart || !cap ? '' : `<p class="gap-caption">${esc(cap)}</p>`;
  return `<figure class="gap${plate ? ' has-plate' : ''}" aria-labelledby="gap-h"><figcaption class="sr-only" id="gap-h">Your call against the evidence</figcaption>${plate ? `<div class="plate">${legend}${main}${caption}</div>` : `${legend}${main}${caption}`}${opt && c.chart ? `<div class="opts-recap">${instrument(c)}</div>` : ''}${SHORT_FIG.has(c.format) ? themeStrip(c, rec) : ''}</figure>`;   // the study card and the principle strip sit under the finding (review 32, m9)
}
// The signature moment of a numeric reveal: your number against the study's, large, with the gap between them.
function gapHead(you, ev, gap, youLab = 'Your call', evLab = 'The study') {
  return `<div class="gap-head"><div class="gh-cell"><span>${esc(youLab)}</span><b class="num gh-you">${esc(you)}</b></div><div class="gh-cell"><span>${esc(evLab)}</span><b class="num gh-ev">${esc(ev)}</b></div><p class="gh-gap">${esc(gap)}</p></div>`;
}
// The study at a glance, under the evidence: who, how, where it was published and how it was checked.
// Wide reveals: this call beside your other calls on the same principle, on one skill scale (review 25 to 27: the empty right column; Tufte: a second comparison at the same scale)
const SHORT_FIG = new Set(['estimate', 'forecast', 'delegate']);   // short evidence figures keep the principle strip beside them; tall ones send it to the left column (audit 43)
function themeStrip(c, rec) {
  const th = (BANK.themes || []).find(t => t.id === c.theme); if (!th) return '';
  const sk = r => { const b = typeof r.base === 'number' ? r.base : S.baseline(BY_ID[r.id]); return Math.max(-1, Math.min(1, b >= 1 ? 0 : (r.score - b) / (1 - b))) };
  const others = firstTries().filter(r => r.id !== c.id && BY_ID[r.id] && BY_ID[r.id].theme === c.theme);
  if (others.length < 2) return '';
  const W = 520, L = 16, R = W - 16, y = 40, sx = v => L + (v + 1) / 2 * (R - L), me = sx(sk(rec));
  const key = v => Math.round(v * 20), groups = {}; others.forEach(r => { const k = key(sk(r)); (groups[k] = groups[k] || []).push(r) });   // calls within 5 skill points share a column
  const mine = key(sk(rec)), dots = Object.entries(groups).map(([k, rs]) => { const x = sx(+k / 20), start = +k === mine ? 1 : 0, n = rs.length, shown = Math.min(n, 3 - start);
    return Array.from({ length: shown }, (_, i) => `<circle cx="${x}" cy="${y + (start + i) * 13}" r="6" class="ts-o"/>`).join('') + (n > shown ? `<text x="${x + 10}" y="${y + (start + shown - 1) * 13 + 5}" class="ts-tick">+${n - shown}</text>` : '') }).join('');   // ties stack under this call; past three, a count   // calls with the same skill stack instead of hiding each other
  return `<div class="theme-strip"><p class="plate-h">Your calls on the principle “${esc(th.title)}”, as skill points versus guessing</p><svg viewBox="0 0 ${W} 104" role="img" aria-label="${esc(`This call ${mn(Math.round(sk(rec) * 100))}; your ${others.length} other calls on this principle: ${others.map(r => mn(Math.round(sk(r) * 100))).join(', ')}`)}"><line x1="${L}" y1="${y}" x2="${R}" y2="${y}" class="ts-ax"/><line x1="${sx(0)}" y1="${y - 14}" x2="${sx(0)}" y2="${y + 14}" class="ts-zero"/>${dots}<circle cx="${me}" cy="${y}" r="8" class="ts-me"/><text x="${Math.min(R - 40, Math.max(L + 40, me))}" y="${y - 16}" text-anchor="middle" class="ts-lab">this call</text><text x="${L}" y="${y + 56}" class="ts-tick">\u2212100</text><text x="${sx(0)}" y="${y + 56}" text-anchor="middle" class="ts-tick">0, guessing</text><text x="${R}" y="${y + 56}" text-anchor="end" class="ts-tick">100</text></svg><p class="small ts-cap">${(() => { const avg = others.reduce((t, r) => t + sk(r), 0) / others.length, d = Math.round((sk(rec) - avg) * 100); return `The small dots are your ${others.length} other calls on this principle. This call is ${Math.abs(d) < 5 ? 'close to their average' : `${Math.abs(d)} points ${d > 0 ? 'above' : 'below'} their average`}.` })()}</p></div>`;   // the marks explained in words, no colour key (review 28)
}
function studyCard(c, checked = true) {
  const d = c.study || {}, s = SOURCE[c.sources[0]] || {}, rows = [['Design', d.design], ['Sample', sampleLine(c)], ['Published', s.venue ? `${s.venue}, ${s.year}` : ''], ['Checked', checked ? srcStatus(s)[0] : '']].filter(r => r[1]);
  return `<dl class="study-card">${rows.map(([k, v]) => `<div><dt>${k}</dt><dd>${esc(v)}</dd></div>`).join('')}</dl>`;
}
function srcLine(c) { const s = SOURCE[c.sources[0]] || {}; return s.authors ? `Source: ${s.authors} (${s.year}), ${s.venue}.` : '' }
function short(s, n) { s = String(s); return s.length > n ? s.slice(0, n - 1) + '…' : s }
function fmtU(v, u) { u = u || ''; return /^[$€£]/.test(u) ? u + v : v + u }   // currency before the number
function bars(ch) {
  const share = ch.unit === '%' && ch.values.every(v => v >= 0 && v <= 100) && Math.max(...ch.values) >= 20;   // shares read on a 0 to 100 scale
  const lo = Math.min(0, ...ch.values), hi = share ? 100 : Math.max(0, ...ch.values), span = (hi - lo) || 1, zero = -lo / span * 100;   // signed values get a zero line; losses run left
  const lab = v => mn(fmtU(ch.decimals !== undefined ? Number(v).toFixed(ch.decimals) : v, ch.unit));
  return `<div class="hbars" role="img" aria-label="${esc(ch.labels.map((l, i) => l + ' ' + lab(ch.values[i])).join(', '))}">${ch.values.map((v, i) => `<div class="hb-row"><span class="hb-label">${esc(ch.labels[i])}</span><span class="hb-track">${lo < 0 ? `<b class="zero" style="left:${zero}%"></b>` : ''}<i class="grow ${[].concat(ch.highlight).includes(i) ? 'ev' : ''}${(ch.ns || []).includes(i) ? ' ns' : ''}${v < 0 ? ' neg' : ''}" style="left:${(Math.min(v, 0) - lo) / span * 100}%;width:${Math.max(1.5, Math.abs(v) / span * 100)}%"></i></span><b class="num">${esc(lab(v))}</b></div>`).join('')}</div>`;
}

function sampleLine(c) {   // the sample on the question screen; never a number inside an estimate's scoring band (audit 37, invariant I4)
  const n = (c.study || {}).n || '';
  if (!n || /^(none|not (stated|confirmed)|multiple studies|studies\b)/i.test(n)) return '';
  if (c.format === 'estimate' && (n.replace(/,/g, '').match(/-?\d+(?:\.\d+)?/g) || []).some(m => Math.abs(+m - c.estimate.target) <= c.estimate.tolerance)) return '';
  return n;
}
function play() {
  const c = card();
  if (st.room && (!c || st.room.challenge !== c.id || st.room.phase === 'lobby')) return roomWait();
  if (!c) { st.view = 'home'; return home() }
  if (st.room && st.phase === 'reveal' && st.room.phase !== 'revealed') return roomLocked(c);
  if (st.room && st.room.phase === 'revealed' && !st.session.some(r => r.id === c.id && r.room === st.room.code) && c.answerTitle) { st.phase = 'reveal' }
  const rev = st.phase === 'reveal', rec = st.session.filter(r => r.id === c.id).slice(-1)[0] || { score: 0, correct: false, confidence: null, response: null, detail: {}, missed: true };
  const steps = st.deck.map((_, k) => `<i class="${k < st.i || (k === st.i && rev) ? 'done' : k === st.i ? 'now' : ''}"></i>`).join('');
  const top = `<div class="focus-top"><button class="x" data-act="leave" aria-label="${st.room ? 'Leave the live class' : 'Leave the round'}"><svg width="14" height="14" viewBox="0 0 14 14" aria-hidden="true"><path d="M1 1l12 12M13 1L1 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></button><div class="steps" aria-hidden="true">${steps}</div>${st.room ? `<span class="count" id="room-conn" aria-live="polite">${st.room.misses ? 'Reconnecting…' : `Live class ${esc(st.room.code || '')}`}</span>` : `<span class="count num" aria-live="polite">${st.i + 1} of ${st.deck.length}</span>`}</div>`;
  const label = c.case ? `<p class="case-line">${esc(c.case.title)}, step ${c.case.step} of ${c.case.of}</p>` : '';
  if (!rev) {
    const ready = lockReady(c);
    const conf = noConf(c) ? '' : `<div class="conf-row"><label for="conf">${confQuestion(c)}</label>${(() => { const mn = c.format === 'choice' || c.format === 'causal' ? Math.round(100 / c.options.length / 5) * 5 : 0; return `<input type="range" id="conf" min="${mn}" max="100" step="5" value="${st.conf}" class="${st.confTouched ? '' : 'untouched'}" style="--fill:${st.confTouched ? (st.conf - mn) / (100 - mn) * 100 : 0}%"><output id="conf-read" class="num ${st.confTouched ? '' : 'empty'}" for="conf">${st.confTouched ? st.conf + '%' : '?'}</output>` })()}</div>`;
    const verb = { estimate: 'estimate', allocate: 'split', rank: 'ranking', delegate: 'routing', forecast: 'forecast' }[c.format] || 'answer';
    return `<section class="focus">${top}<article class="focus-card" aria-labelledby="q-h">${CLASS_LOCK && !st.room && !BY_ID[c.id].answerTitle ? '<p class="lock-note" role="note">A live class is running on this server, so results for decisions it has not reached open after it reveals them. You can still make your call now.</p>' : ''}
      <div class="q-col"><p class="scene">${esc(c.scene)}</p>
      ${c.format === 'forecast' ? `<h1 class="q q-claim" id="q-h" tabindex="-1">“${esc(c.forecast.claim)}”</h1><p class="hint fc-ask">How likely is it that the study found this?</p>` : `<h1 class="q" id="q-h" tabindex="-1">${esc(c.question)}</h1>`}<p class="study-line">${c.case ? `${esc(c.case.title)}, step ${c.case.step} of ${c.case.of}. ` : ''}${esc([(c.study || {}).design, sampleLine(c), `${SOURCE[c.sources[0]].venue} ${SOURCE[c.sources[0]].year}`].filter(Boolean).map(x => x.replace(/\.$/, '')).join('. '))}.</p>${c.format === 'multi' ? '<p class="hint">Choose two.</p>' : c.format === 'allocate' ? `<p class="hint">Spread ${(c.allocate && c.allocate.total) || 100} points by how likely each option is to be the one that worked best.</p>` : ''}
      </div><div class="a-col">${instrument(c)}${conf}</div></article>
      <div class="actionbar"><div class="actionbar-in"><span class="kicker">${lockHint(c)}</span><button class="btn btn-you btn-lg" data-act="lock" id="lock-btn" ${ready ? '' : 'disabled'}>Lock my ${verb}</button></div></div></section>`;
  }
  const tabs = [['questions', 'Questions'], ['scope', 'Scope'], ['source', 'Source'], ['note', 'Your note']];
  const tab = st.tab || 'questions';
  const src = SOURCE[c.sources[0]], [stLabel, stCls] = srcStatus(src);
  const panel = tab === 'questions' ? `<div class="follow">${c.follow.map(f => `<details><summary>${esc(f.q)}</summary><p>${esc(f.a)}</p></details>`).join('')}</div>${tutorPanel(c)}`
    : tab === 'scope' ? `<p class="deep-text">${esc(c.boundary)}</p>`
    : tab === 'source' ? c.sources.map(id => { const s = SOURCE[id], [l, k] = srcStatus(s); return `<div class="src"><p class="src-title">${esc(paperTitle(s) || 'Title shown once you have played every decision built on this paper')}</p><p>${esc(s.authors)}, <i>${esc(s.venue)}</i>${s.volume ? ' ' + esc(s.volume) : ''}, ${s.year}.</p><p class="row"><span class="status ${k}">${l}</span> <button class="link-btn" data-source="${esc(id)}">More on this source</button> <a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Open the article</a></p></div>` }).join('') + `<div class="sc-phone">${studyCard(c, false)}</div>`
    : `<div class="note-box"><label for="note">Which decision in your work would you revisit, and what would you measure first?</label><textarea id="note" maxlength="480">${esc(notes[c.id] || '')}</textarea><button class="btn btn-quiet" data-act="save-note">Save on this device</button></div>`;
  const nextLabel = st.i >= st.deck.length - 1 ? 'See how you did' : c.case && c.case.step < c.case.of ? 'Next step' : 'Next decision';
  return `<section class="focus">${top}<article class="focus-card reveal" aria-labelledby="r-h">
      <h1 class="reveal-title" id="r-h" tabindex="-1">${esc(c.answerTitle)}</h1>
      <p class="verdict">${rec.missed ? '<strong>You did not answer this one.</strong>' : `<strong class="${rec.correct ? 'v-ok' : ''}">${rec.correct ? 'Matches the study.' : (['multi', 'delegate'].includes(c.format) ? rec.score > 0 && rec.score > (typeof rec.base === 'number' ? rec.base : S.baseline(c)) : c.format !== 'forecast' && rec.score >= .5 && rec.score > (typeof rec.base === 'number' ? rec.base : S.baseline(c))) ? 'Partly right.' : 'Not what the study found.'}</strong> <span class="num">Score ${mn(pct(rec.score))}</span>${rec.confidence !== null ? `<span class="conf-in">${rec.confidence}% sure</span>` : ''}`}</p>${c.case ? label : ''}
      ${rec.missed ? '' : gapFigure(c, rec)}
      ${st.room && st.room.agg ? classPanel(c, st.room.agg) : ''}
      <p class="reveal-body">${esc(c.explain)}</p>
      <p class="action-note"><strong>For a manager:</strong> ${esc(c.implication)}</p>
      <div class="rev-meta">${studyCard(c)}${rec.missed || SHORT_FIG.has(c.format) ? '' : themeStrip(c, rec)}</div>
      <div class="deep"><div class="tabs" role="tablist" aria-label="Go deeper">${tabs.map(([k, l]) => `<button role="tab" id="tab-${k}" aria-selected="${tab === k}" aria-controls="tabpanel" data-tab="${k}" tabindex="${tab === k ? 0 : -1}">${l}</button>`).join('')}</div><div class="tabpanel" id="tabpanel" role="tabpanel" aria-labelledby="tab-${tab}">${panel}</div></div>
    </article>
    <div class="actionbar"><div class="actionbar-in"><span class="kicker">${st.room ? `Live class ${esc(st.room.code)}. Your instructor opens the next decision.` : `${st.session.filter(r => r.correct).length} of ${st.session.length} matched the study, average score ${st.session.length ? mn(pct(st.session.reduce((a, r) => a + r.score, 0) / st.session.length)) : 0}`}</span>${st.room ? '' : `<button class="btn btn-solid btn-lg" data-act="next" id="next-btn">${nextLabel}</button>`}</div></div></section>`;
}
// ----- tutor -----
let TUTOR_REMOTE = null; // the server endpoint, when the page is served
let TUTOR_AI = false;   // true only when the server reports a configured model
function tutorPanel(c) {
  const t = st.tutor;
  return `<div class="tutor" aria-labelledby="tutor-h"><h2 id="tutor-h">Ask your own question</h2>
    <form class="tutor-line" data-form="tutor"><label class="sr-only" for="tutor-in">Your question about this study</label><input id="tutor-in" maxlength="300" placeholder="For example: would this hold in a sales team?" autocomplete="off"><button class="btn btn-quiet" ${t.busy ? 'disabled' : ''}>${t.busy ? 'Thinking' : 'Ask'}</button></form>
    ${t.suggest && t.suggest.length ? '' : `<div class="tutor-chips">${['How big is this effect in practice?', 'Would this hold with AI tools today?', 'How would I test this in my company?'].map(q => `<button data-ask="${esc(q)}">${esc(q)}</button>`).join('')}</div>`}
    ${t.text ? `<div class="tutor-answer" aria-live="polite">${esc(t.text)}${t.cites.length ? '\n\n' + t.cites.map(x => `<cite>${esc(x)}</cite>`).join(' ') : ''}</div>` : ''}
    ${t.suggest && t.suggest.length ? `<div class="tutor-chips tutor-suggest">${t.suggest.map(q => `<button data-ask="${esc(q)}">${esc(q)}</button>`).join('')}</div>` : ''}
    <p class="small">${TUTOR_AI ? 'AI answers use only the lab’s checked sources. Check details in the source.' : 'Answers come from the lab’s checked summaries.'}</p></div>`;
}
// Offline tutor. The same routing table and order as server/tutor.py curated (BANK.tutorRoutes), so both tutors agree.
const TR = BANK.tutorRoutes || { stop: [], generic: [], suffixes: [], syn: {}, routes: [], subgroupFollow: '^who\\b' };
let TR_COMPW_ = null; const compw = () => TR_COMPW_ || (TR_COMPW_ = new Set(trTokens('better worse outperform outperforms outperformed beat beats accurate smarter good effective useful fast faster more less fewer than')));
const stripYN = a => { const m = String(a).match(/^(Yes|No)[.,]\s*([\s\S]*)$/); return m && /^[A-Z0-9]/.test(m[2]) ? m[2] : a };   // audit 31: keep "Yes, partly"
const TR_STOP = new Set(TR.stop), TR_SYN = {}; for (const [k, ws] of Object.entries(TR.syn)) for (const w of ws.split(' ')) TR_SYN[w] = k.split(' ');
function trStem(w) { for (const s of TR.suffixes) if (w.endsWith(s) && w.length - s.length >= 4) return w.slice(0, -s.length); return w }
function trTokens(s) {
  const out = (String(s).replace(/[\u2018\u2019]/g, "'").normalize('NFKD').replace(/[̀-ͯ]/g, '').toLowerCase().match(/[a-z0-9]+(?:'[a-z]+)?/g) || []).filter(w => !TR_STOP.has(w) && (w.length > 2 || /^\d+$/.test(w) || w === 'ai')).map(trStem);
  return out.concat(out.flatMap(w => TR_SYN[w] || []));
}
const TR_GENERIC = new Set(TR.generic.map(trStem)), TR_COMMON = new Set(TR.common || []);
const trNorm = s => (String(s).toLowerCase().match(/[a-z0-9]+/g) || []).join(' ');
function trNames(q, x) {   // whole surnames, unstemmed: "bill" must not match "Biller-Andorno"
  const words = s => (String(s).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().match(/[a-z]{4,}/g) || []).filter(w => !TR_STOP.has(w) && w !== 'with' && w !== 'others');
  const rest = q.trim().includes(' ') ? q.trim().slice(q.trim().indexOf(' ') + 1) : ''; const qw = new Set(words(q).filter(w => { const W = w[0].toUpperCase() + w.slice(1); return !(TR.wordSurnames || []).includes(w) || new RegExp('\\b' + W + '\\b').test(rest) || new RegExp('^' + W + "(\\s+et al|['’]s\\b|\\s+and\\s+[A-Z]|\\s*\\()").test(q.trim()) })); const short = a => (String(a).normalize('NFKD').replace(/[\u0300-\u036f]/g, '').toLowerCase().match(/[a-z]+/g) || []).filter(w => w.length === 3).map(w => w[0].toUpperCase() + w.slice(1)); return x.sources.some(id => SOURCE[id] && (words(SOURCE[id].authors).some(a => qw.has(a)) || short(SOURCE[id].authors).some(w => new RegExp('\\b' + w + '\\b').test(rest) || new RegExp('^' + w + "(\\s+et al|['’]s\\b|\\s+and\\s+[A-Z]|\\s*\\()").test(q.trim())))) }
function trBody(x) { return new Set(trTokens([x.title, x.scene, x.question, x.answerTitle, x.explain, x.implication, x.boundary, ...(x.follow || []).map(f => f.q + ' ' + f.a)].join(' '))) }
const TR_FILL = '((so|and|okay|ok|but|also|hmm|well|quick question:?)[,\\s]+)*';
function isOpen(ql) { const q = ql.trim(); if (new RegExp('^' + TR_FILL + '((can|could|would|will) you )?(tell|list|describe|explain)\\b').test(q)) return true; return /\b(what|which|who|whom|whose|how|why|when|where)\b/.test(q) && !new RegExp('^' + TR_FILL + '(is|are|was|were|do|does|did|can|could|will|would|has|have|had|should|shall|may|might|must)\\b').test(q) }
function curated(q, c) {
  const qt = new Set(trTokens(q)), topic = [...qt].filter(w => !TR_GENERIC.has(w)), ql = q.toLowerCase(); let fol = c.follow || [];
  const cs = x => [cite(x.sources[0])], off = { text: 'That is outside what this lab covers. Ask about this study: how it was run, how big the effect was, or how to test it in your organization.', cites: [] };
  if (/\bcan (i|we) (trust|rely on|count on|use)\b.*\b(our|my|a|the|this) (\w+ )?(vendor|supplier|tool|provider|system|model)s?\b|\bshould (my|our|we|i)\b (?!(believe|buy|take|worry|care|be (worried|concerned|afraid))\b)\w+|\bdoes (this|that|it) mean (that )?(we|i|my|our|managers?|companies|firms|organi[sz]ations?|doctors|clinicians|hospitals|teams?|employers|leaders)\b.{0,40}\bshould\b(?! (hold|generali[sz]e|apply|work|be trusted))/.test(ql) && !/\b(is|would|be) (this|it|that)( be)? (really |even |actually )?(ethic\w*|fair|moral\w*|right|wrong|ok|okay|allowed|legal)\b|\bit'?s (really )?(fair|ok|okay|allowed|legal)\b|\bare we allowed\b|\bthe right thing\b|\bunethical\b|\b(ethic\w*|unfair\w*|immoral\w*|legal(?!\s+(team|department|counsel|staff|work))(ity)?)\b|\b(fire[ds]?|lay(ing)? off|cut (jobs|staff|headcount)|replace (our |my )?(staff|workers|people|writers|agents|analysts|reps))\b|\bhire (fewer|less)\b|\bfewer (staff|people|workers|agents|employees|consultants|writers|hires|humans|jobs|reps|analysts)\b/.test(ql)) return { text: `${c.implication}\n\nWhy: ${c.explain}\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) };   // a recommendation question goes to the manager's action
  const bare = ql.trim().replace(new RegExp('^' + TR_FILL), ''); const exact = fol.find(f => trNorm(f.q) === trNorm(q) || trNorm(f.q) === trNorm(bare)); if (exact) return { text: exact.a, cites: cs(c) };
  if (/\b(ethic\w*|unethical|moral\w*|fair to|unfair\w*|allowed|legal(?!\s+(team|department|counsel|staff|work))\w*)\b|\bis (it|this|that) (really )?(fair|right|wrong|ok|okay)\b/.test(ql)) { const jq = f => { const ft = new Set(trTokens(f.q)); return [...ft].filter(w => qt.has(w)).length / Math.max(1, new Set([...ft, ...qt]).size) }; const fe = fol.find(f => /\b(ethic\w*|unethical|moral\w*|fair|unfair\w*|allowed|legal\w*)\b/i.test(f.q) && jq(f) >= 0.3); if (fe) return { text: fe.a, cites: cs(c) } }
  if (/\b(ethic\w*|unethical|moral\w*|fair to|unfair\w*|allowed|legal(?!\s+(team|department|counsel|staff|work))\w*)\b|\bis (it|this|that) (really )?(fair|right|wrong|ok|okay)\b/.test(ql)) return { text: `The study measures what happened, not what is right; that call is yours. What it covers: ${c.boundary}\n\nWhat a manager can do with it: ${c.implication}`, cites: cs(c) };
  if (isOpen(ql)) fol = fol.filter(f => !/^(Yes|No)\b/.test(f.a));
  const jac = f => { const ft = new Set(trTokens(f.q)); const inter = [...ft].filter(w => qt.has(w)).length; return inter / Math.max(1, new Set([...ft, ...qt]).size) };
  const near = fol.slice().sort((a, b) => jac(b) - jac(a))[0]; const ynSkip = new Set(trTokens(TR.filler.join(' '))); const yn = f => [...qt].every(w => trTokens(f.q).includes(w) || TR_GENERIC.has(w) || ynSkip.has(w)) ? f.a : stripYN(f.a); if (near && jac(near) >= 0.6) return { text: yn(near), cites: cs(c) };
  const has = w => [...qt].some(x => w === x || (Math.min(w.length, x.length) >= 3 && (w.startsWith(x) || x.startsWith(w)))); const sub = fol.filter(f => { const ft = trTokens(f.q); return new Set(ft).size >= 2 && ft.every(has) }).sort((a, b) => trTokens(b.q).length - trTokens(a.q).length)[0]; if (sub) return { text: yn(sub), cites: cs(c) };
  const named = trNames(q, c) ? [] : ALL.filter(x => x.explain && !x.sources.some(s => c.sources.includes(s)) && trNames(q, x));
  if (named.length) { const ov = x => topic.filter(w => trTokens([x.title || '', x.answerTitle, x.explain, x.question, x.scene || ''].join(' ')).includes(w)).length; const b = named.sort((a, z) => ov(z) - ov(a))[0]; const s0 = SOURCE[b.sources[0]] || {}; return { text: `From ${s0.authors || 'another study'} (${s0.year || ''}): ${b.explain}\n\n${b.implication}`, cites: cs(b) } }
  const st0 = c.study || {}, rare = topic.filter(w => !TR_COMMON.has(w)), hits = (s, ws) => { const ts = new Set(trTokens(s)); return ws.filter(w => ts.has(w)).length };
  if (c.delegate) { const ov = tk => trTokens(tk.text).filter((w, i, a) => qt.has(w) && a.indexOf(w) === i).length; const tk = c.delegate.tasks.slice().sort((a, b) => ov(b) - ov(a))[0]; if (tk && tk.why && (ov(tk) >= 2 || (ov(tk) >= 1 && /\bwhy\b/.test(ql)))) return { text: tk.why, cites: cs(c) } }   // a question about one task gets that task's evidence
  let whyq = false, defq = false;
  const qla = ql.normalize('NFKD').replace(/[\u0300-\u036f]/g, '');   // JavaScript's \b treats é as a boundary; Python's does not (audit 39: "write me a résumé")
  for (const [name, rx] of TR.routes) {
    if (!new RegExp(rx, 'i').test(ql) && !new RegExp(rx, 'i').test(qla)) continue;
    if (name === 'offtopic') return off;
    const item = new Set(trTokens([c.question, c.scene || '', c.answerTitle, c.explain, ...(c.follow || []).map(f => f.q + ' ' + f.a)].join(' ')));
    if (name === 'compare' && !/\bor not\b/.test(ql) && rare.some(w => !compw().has(w) && !item.has(w) && !(TR_SYN[w] || []).some(x => item.has(x)))) return { text: `I could not match that exact comparison to this study’s summary. Here is what the study found: ${c.answerTitle}. ${c.explain}`, cites: cs(c) };   // audit 31c, M1   // audit 31, M2
    if (name === 'compare') { const ovq = f => hits(f.q + ' ' + f.a, [...qt]); const fc = fol.find(f => /\b(than|higher|lower|better|worse|outperform\w*|beat)\b/.test(f.a) && hits(f.q, rare) > 0) || fol.filter(f => ovq(f) >= 3 && hits(f.q, rare) > 0).sort((a, b) => ovq(b) - ovq(a))[0]; return { text: `${c.answerTitle}. ${c.explain}${fc ? ' ' + stripYN(fc.a) : ''}`, cites: cs(c) } }   // review 26 M1, audit 31 M1
    if (name === 'control') { const fcg = (c.follow || []).find(f => /\bcontrol\b/i.test(f.q)); if (fcg) return { text: /\b(is|was|were) there\b|\bhave an? control\b|\bany control\b/.test(ql) ? fcg.a : stripYN(fcg.a), cites: cs(c) }; continue }
    if (name === 'whatif') return { text: `The study's design: ${st0.design || 'see the paper'}. What it covers: ${c.boundary} The finding: ${c.explain}`, cites: cs(c) };   // audit 31b, M1
    if (name === 'foresight') { const fp = fol.find(f => /\b(predict\w*|expect\w*|forecast\w*|experts?|anticipat\w*)/i.test(f.q + ' ' + f.a)); if (fp) return { text: fp.a, cites: cs(c) }; continue }
    if (name === 'detect') { const fd = fol.find(f => /\b(tell|detect\w*|spot|notice[ds]?|identif(y|ied)|recogni\w*)\b/i.test(f.q)); if (fd) return { text: fd.a, cites: cs(c) }; continue }
    if (name === 'signif') return { text: c.explain, cites: cs(c) };   // the main contrast first
    if (name === 'task') return { text: `${c.scene || ''}\n\nDesign: ${st0.design || 'see the paper'}.`, cites: cs(c) };
    if (name === 'meaning') { const m = ql.match(/mean(?:t)? by ['"]?(\w+)|does (?:the )?(?:word |term )?['"]?(\w+)['"]? mean/), w = m ? (m[1] || m[2] || '') : ''; const sw = w ? trStem(w) : ''; const pre = s => !!sw && trTokens(s).some(x => x.startsWith(sw)); const fm = fol.find(f => pre(f.q)); if (fm) return { text: fm.a, cites: cs(c) }; if (pre(c.answerTitle + ' ' + c.explain + ' ' + (c.scene || ''))) return { text: `In this study: ${c.scene || ''}\n\n${c.answerTitle}. ${c.explain}`, cites: cs(c) }; continue }
    if (name === 'define') { const m = ql.match(/^what(?:.s| is) (?:an? |the )?(\w+)\??$/), w = m ? m[1] : '', sw = w ? trStem(w) : ''; const fdq = sw && !TR_GENERIC.has(sw) && fol.find(f => /\bmean\b|^what (is|are) (an? |the )?\w+\??$|^why call/.test(f.q.toLowerCase()) && trTokens(f.q).some(x => x.startsWith(sw))); if (fdq) return { text: fdq.a, cites: cs(c) }; if (sw && !TR_GENERIC.has(sw) && trTokens(c.answerTitle + ' ' + c.explain + ' ' + (c.scene || '')).some(x => x.startsWith(sw))) return { text: `In this study: ${c.scene || ''}\n\n${c.answerTitle}. ${c.explain}`, cites: cs(c) }; defq = true; continue }
    if (name === 'contest') { const fd = fol.find(f => /\b(design|differ|contrast|both)/i.test(f.q + ' ' + f.a)); return { text: `${c.explain}${fd ? '\n\n' + fd.a : ''}\n\n${c.implication}`, cites: cs(c) } }   // both sides of a contested finding
    if (name === 'why') { const has2 = s => trTokens(s).some(w => rare.includes(w)), whys = fol.filter(f => /^why/i.test(f.q)); const fw = whys.find(f => has2(f.q + ' ' + f.a)) || (whys.length === 1 && /\b(didn.?t|did not|fail)/.test(ql) && /\b(not|no|never|fail\w*|n't|miss\w*|hid\w*|mask\w*|appear\w*)\b/.test(whys[0].a) ? whys[0] : null) || fol.find(f => /\b(because|read (this|it)? ?as|reason|motive|concern|suggest)/i.test(f.a) && has2(f.a)); if (fw) return { text: fw.a, cites: cs(c) }; whyq = true; continue }
    if (name === 'authors') return { text: `${c.sources.map(id => SOURCE[id] ? `${SOURCE[id].authors} (${SOURCE[id].year}), ${SOURCE[id].venue}` : '').filter(Boolean).join('; ')}. Design: ${st0.design || 'see the paper'}.`, cites: cs(c) };
    if (name === 'voluntary') return { text: `Design: ${st0.design || 'see the paper'}.${st0.n ? ` Sample: ${st0.n}.` : ''}\n\nSetting: ${c.scene}\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) };
    if (name === 'stakes') { const fm = fol.find(f => /(\$|\bmoney\b|\bpaid\b|\bbonus|\bincentiv)/i.test(f.q + ' ' + f.a)); if (fm) return { text: fm.a, cites: cs(c) } }
    if (name === 'stakes') return { text: `Design: ${st0.design || 'see the paper'}.${st0.n ? ` Sample: ${st0.n}.` : ''}\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) };
    if (name === 'population') return { text: `What the study covers: ${c.boundary}${st0.n ? ` Sample: ${st0.n}.` : ''} Whether it holds elsewhere is a question to test locally.`, cites: cs(c) };
    if (name === 'action') return { text: `${c.implication}\n\nWhy: ${c.explain}\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) };
    if (name === 'models') { const fm = fol.find(f => /\b(GPT|Claude|Llama|Gemini|ChatGPT|Bing|DALL|Midjourney)/.test(f.a)) || fol.find(f => /\b(models?|tools?)\b/i.test(f.q)); if (fm) return { text: fm.a, cites: cs(c) }; continue }
    if (name === 'numbers') { if (/\d/.test(c.explain)) return { text: c.explain, cites: cs(c) }; continue }
    if (name === 'who') return { text: `Who was studied: ${st0.n || 'see the paper'}. Design: ${st0.design || 'see the paper'}.\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) };
    if (name === 'catch') { const fd = fol.find(f => /\b(downside|backfire|risk|cost|worse|harm|limit|fail)/i.test(f.q + ' ' + f.a)); return { text: `What the study covers: ${c.boundary}${fd ? '\n\n' + fd.a : ''}\n\nThe finding itself: ${c.explain}`, cites: cs(c) } }
    if (name === 'summary') return { text: `${c.answerTitle}. ${c.explain}\n\nWhat a manager does with it: ${c.implication}`, cites: cs(c) };
    if (name === 'duration') { const fl = fol.find(f => /\b(long|last|later|weeks?|months?|years?|fade|persist|after)\b/i.test(f.q + ' ' + f.a)); return { text: fl ? fl.a : `Design: ${st0.design || 'see the paper'}.${st0.n ? ` Sample: ${st0.n}.` : ''}\n\nWhat the study covers: ${c.boundary}`, cites: cs(c) } }
    if (name === 'ethics') return { text: `The study measures what happened, not what is right; that call is yours. What it covers: ${c.boundary}\n\nWhat a manager can do with it: ${c.implication}`, cites: cs(c) };
    if (name === 'subgroup') { const fh = fol.find(f => new RegExp(TR.subgroupFollow, 'i').test(f.q)); if (fh) return { text: fh.a, cites: cs(c) }; if (new RegExp(TR.routes.find(r => r[0] === 'numbers')[1], 'i').test(ql) && /\d/.test(c.explain)) return { text: c.explain, cites: cs(c) }; return { text: `The lab's summary of this study does not break results down that way. What it covers: ${c.boundary}`, cites: cs(c) } }
    if (name === 'design' && !/\b(my|our)\b/.test(ql)) return { text: `Design: ${st0.design || 'see the paper'}.${st0.n ? ` Sample: ${st0.n}.` : ''}\n\n${c.explain}`, cites: cs(c) };
    if (name === 'pilot') return { text: `Run a small randomized pilot: give the change to some teams or customers and not to others, fix one outcome metric in advance, and compare after a set period. For this finding: ${c.implication}\n\nWhat the study measured: ${c.explain}`, cites: cs(c) };
    if (name === 'size') return { text: `${c.explain}\n\nIn practice: ${c.implication}`, cites: cs(c) };
    if (name === 'transfer') return { text: `${c.boundary}\n\nThe study itself: ${c.explain}`, cites: cs(c) };
  }
  const QTY = /^(how (large|big|much|many|fast|long|often|high|low)|what (size|share|percent\w*|amount))\b/;
  const fillT = new Set(trTokens(TR.filler.join(' '))), core = rare.filter(w => !fillT.has(w)), shared = f => { const ft = trTokens(f.q); return core.filter(w => ft.includes(w) || (TR_SYN[w] || []).some(x => ft.includes(x))).length }; const fq = defq ? null : fol.filter(f => (shared(f) >= 2 || (shared(f) > 0 && 3 * shared(f) >= 2 * core.length)) && !(whyq && QTY.test(f.q.toLowerCase()))).sort((a, b) => (hits(b.q, rare) - hits(a.q, rare)) || (hits(b.q, [...qt]) - hits(a.q, [...qt])))[0]; if (fq) return { text: yn(fq), cites: cs(c) };   // a follow-up is borrowed only when its own question shares two distinctive words
  if (whyq) return { text: `${c.explain} What a manager does with it: ${c.implication}`, cites: cs(c) };
  if (rare.length) return { text: `I could not match that question to this study’s summary. Here is what the study found: ${c.answerTitle}. ${c.explain} Its summary answers the questions below.`, cites: cs(c), suggest: (c.follow || []).map((f, i) => ({ f, i, o: trTokens(f.q + ' ' + f.a).filter((w, j, arr) => qt.has(w) && arr.indexOf(w) === j).length })).sort((a, b) => b.o - a.o || a.i - b.i).map(x => x.f.q).slice(0, 3) };   // closest first (audit 33)   // a weak match is not an answer (review 27)
  return { text: `${c.answerTitle}. ${c.explain}\n\nWhat a manager does with it: ${c.implication}`, cites: cs(c) };
}
async function ask(q) {
  q = String(q || '').trim().slice(0, 300); const c = card(); if (!c || st.tutor.busy) return;
  if (q.length < 4) { notice('Type a question of at least four characters.'); return }
  st.tutor = { busy: true, text: '', cites: [] }; render();
  if (TUTOR_REMOTE) {
    try {
      const ctl = new AbortController(), to = setTimeout(() => ctl.abort(), 15000);
      const res = await fetch(TUTOR_REMOTE, { method: 'POST', headers: { 'Content-Type': 'application/json', 'X-Client-Id': clientId() }, body: JSON.stringify({ question: q, challenge: c.id, client: clientId() }), signal: ctl.signal });
      clearTimeout(to); const d = await res.json();
      if (res.ok && typeof d.answer === 'string' && d.answer.trim()) { st.tutor = { busy: false, text: d.answer.slice(0, 1600), cites: (d.citations || []).map(x => x.label).slice(0, 4), suggest: Array.isArray(d.suggest) ? d.suggest.slice(0, 3).map(String) : null }; render(); return }
    } catch { }
  }
  const a = curated(q, c); st.tutor = { busy: false, text: a.text, cites: a.cites, suggest: a.suggest || null }; render();
}
function clientId() { let id = store.get('thv:client', null); if (!id) { id = Math.random().toString(36).slice(2, 12); store.set('thv:client', id) } return id }

// ----- atlas -----
function atlas() {
  const q = st.atlasQuery.trim().toLowerCase();
  const m = ALL.filter(c => (st.atlasTrack === 'All' || c.track === st.atlasTrack) && (st.atlasFormat === 'All' || FORMAT_NAME[c.format] === st.atlasFormat) && (!q || [c.title, c.scene, c.question, c.concept, c.explain, cite(c.sources[0])].join(' ').toLowerCase().replace(/[\u2018\u2019]/g, "'").includes(q.replace(/[\u2018\u2019]/g, "'"))));
  return `<section class="atlas-head wrap">${libHead()}
    <div class="atlas-tools"><label class="search"><span aria-hidden="true">⌕</span><span class="sr-only">Search</span><input id="atlas-q" type="search" value="${esc(st.atlasQuery)}" placeholder="Try defaults, Dimant, algorithm, norms" autocomplete="off"></label>
    <label class="sr-only" for="atlas-track">Area</label><select id="atlas-track" class="seg">${['All', ...TRACKS].map(t => `<option value="${esc(t)}" ${st.atlasTrack === t ? 'selected' : ''}>${t === 'All' ? 'All areas' : esc(t)}</option>`).join('')}</select>
    <label class="sr-only" for="atlas-format">Format</label><select id="atlas-format" class="seg">${['All', ...new Set(Object.values(FORMAT_NAME))].map(t => `<option value="${esc(t)}" ${st.atlasFormat === t ? 'selected' : ''}>${t === 'All' ? 'All formats' : esc(t)}</option>`).join('')}</select></div>
    <p class="kicker" aria-live="polite" id="atlas-count">${m.length} of ${ALL.length} decisions</p></section>
    <section class="wrap"><div class="atlas-grid" id="atlas-grid">${m.length ? m.map(c => { const best = records.filter(r => r.id === c.id).reduce((a, r) => Math.max(a, r.score), -1); return `<button class="entry" data-play="${esc(c.id)}"><span class="entry-title">${esc(c.title)}</span><span class="entry-best num">${best >= 0 ? `best ${mn(pct(best))}` : ''}</span><span class="entry-q">${esc(c.format === 'forecast' && c.forecast && c.forecast.claim ? c.forecast.claim : c.question)}</span><span class="entry-meta">${FORMAT_NAME[c.format]}, ${esc(c.track)}. ${esc(cite(c.sources[0]))}, ${esc(SOURCE[c.sources[0]].venue)}</span></button>` }).join('') : `<div class="empty-state">No decision matches “${esc(st.atlasQuery)}”. Clear the search or try an author’s name.</div>`}</div></section>`;
}


// ----- library: principles (almanac) and all decisions (atlas) -----
function libHead() {
  return `<h1>Library</h1><div class="lib-tabs" role="tablist" aria-label="Library"><button role="tab" aria-selected="${st.view === 'almanac'}" data-nav="almanac">Principles</button><button role="tab" aria-selected="${st.view === 'atlas'}" data-nav="atlas">All decisions</button></div>`;
}
function almanac() {
  const themes = BANK.themes || [], played = new Set(records.map(r => r.id));
  return `<section class="atlas-head wrap">${libHead()}
</section>
    <section class="wrap" style="padding-bottom:64px">${(() => {
      const first = firstTries(), rows = themes.map(t => ({ t, cs: ALL.filter(c => c.theme === t.id) })).filter(x => x.cs.length).map(x => ({ ...x, seen: x.cs.filter(c => played.has(c.id)).length }));
      const opened = rows.filter(x => x.seen), closed = rows.filter(x => !x.seen);
      // an opened principle leads with the player's own result on it (review 26: no block repeated ten times)
      const full = ({ t, cs, seen }) => { const sk = pooledSkill(first.filter(r => cs.some(c => c.id === r.id))), line = !t.principle ? (libraryLoaded ? 'Held back while a live class is running on this server.' : 'Loading…') : esc(t.principle);
        return `<article class="theme" id="theme-${esc(t.id)}"><div class="theme-head"><h2>${esc(t.title)}</h2><p class="theme-you">${seen >= 3 ? `You: <b class="num">${sk === null ? '–' : mn(sk)}</b> skill points versus guessing on ${seen} of ${cs.length}` : `${seen} of ${cs.length} played`}${seen < cs.length ? ` <button class="link-btn" data-theme-round="${esc(t.id)}">Play the other ${cs.length - seen}</button>` : ''}</p><p>${line}<small class="theme-count">${pathStrip({ items: cs.map(c => c.id) }, played)}</small></p></div>
      <details class="theme-more"><summary>The decisions behind it</summary><ul class="findings">${cs.map(c => `<li><div>${played.has(c.id) && c.explain ? `<strong>${esc(c.answerTitle)}.</strong> ${esc(c.explain)}<br><small>${esc(cite(c.sources[0]))}, ${esc(SOURCE[c.sources[0]].venue)}. ${esc(c.boundary)}</small>` : `<strong>${esc(c.title)}</strong><br><small>${esc(cite(c.sources[0]))}, ${esc(SOURCE[c.sources[0]].venue)}. The finding opens after your call.</small>`}</div><button class="btn btn-quiet" data-play="${esc(c.id)}">Play</button></li>`).join('')}</ul></details>
      </article>` };
      // an unopened principle is one line: its name, its size, and the way in
      const one = ({ t, cs }) => `<li class="theme-row" id="theme-${esc(t.id)}"><h2>${esc(t.title)}</h2><span class="theme-n">${cs.length} decisions</span><button class="btn btn-line" data-theme-round="${esc(t.id)}">Play these ${cs.length}</button></li>`;
      return (opened.some(x => x.seen < 3) ? '<p class="lib-note">Your score on a principle appears after three calls on it, as in your record.</p>' : '') + opened.map(full).join('') + (closed.length ? `<section class="theme-closed"><h2 class="theme-closed-h">${opened.length ? 'Not opened yet' : 'Principles open after your first call on them'}</h2><ul class="theme-rows">${closed.map(one).join('')}</ul></section>` : '');
    })()}</section>`;
}

// Pooled skill above guessing: (mean score - mean chance level) / (1 - mean chance level), on first tries only.
function pooledSkill(xs) { if (!xs.length) return null; const raw = xs.reduce((a, r) => a + r.score, 0) / xs.length, base = xs.reduce((a, r) => a + (typeof r.base === 'number' ? r.base : S.baseline(BY_ID[r.id])), 0) / xs.length; return pct(base >= 1 ? 0 : (raw - base) / (1 - base)) }
const firstTries = () => { const seen = new Set(); return records.filter(r => BY_ID[r.id] && !seen.has(r.id) && seen.add(r.id)) };

// ----- record -----
function record() {
  // Lifetime figures count the first try at each decision only, so replays with the answer known do not inflate them.
  const seen = new Set(), all = records.filter(r => BY_ID[r.id] && !seen.has(r.id) && seen.add(r.id)), last = st.session.length ? st.session : records.filter(r => BY_ID[r.id]).slice(-12);
  const cal = S.calibration(all.map(r => S.toCalibrationRecord(BY_ID[r.id], r)));
  // Headline figures are skill above guessing, so formats with different chance levels compare fairly.
  // Pooled: (mean score - mean chance level) / (1 - mean chance level), so one confident miss cannot swamp a set of good calls.
  const avg = pooledSkill;
  const meanScore = avg(all);
  // How the headline moved, call by call (pooled skill over the calls so far), so the big number has a history.
  const series = all.slice(-40).map((_, k, xs) => avg(xs.slice(0, k + 1)));
  const spark = series.length < 3 ? '' : (() => { const W = 220, H = 56, lo = Math.min(-100, ...series), hi = 100, x = k => 4 + k * (W - 8) / (series.length - 1), y = v => 4 + (hi - v) / (hi - lo) * (H - 8);
    return `<svg class="spark" viewBox="0 0 ${W + 58} ${H}" role="img" aria-label="Skill after each of your last ${series.length} calls, from ${series[0]} to ${series[series.length - 1]}"><line x1="4" x2="${W - 4}" y1="${y(0)}" y2="${y(0)}" stroke="#9aa6b6" stroke-dasharray="3 4"/><text x="${W + 2}" y="${y(0) + (Math.abs(series[series.length - 1]) < 25 ? 16 : 4)}" font-size="12" fill="#56617a">guessing</text><polyline fill="none" stroke="#2f54eb" stroke-width="2.5" stroke-linejoin="round" points="${series.map((v, k) => x(k) + ',' + y(v)).join(' ')}"/><circle cx="${x(series.length - 1)}" cy="${y(series[series.length - 1])}" r="4.5" fill="#2f54eb"/></svg>` })();
  const sess = st.session.length ? avg(st.session.filter(r => BY_ID[r.id])) : null;
  const byTrack = TRACKS.map(t => { const x = all.filter(r => BY_ID[r.id].track === t); return [t, x.length, avg(x)] });
  let summary = '';
  if (st.session.length) {
    const worst = st.session.reduce((a, r) => r.score < a.score ? r : a), best = st.session.reduce((a, r) => r.score > a.score ? r : a);
    const sc = S.calibration(st.session.map(r => S.toCalibrationRecord(BY_ID[r.id], r)));
    summary = `<div class="summary">${best.score > worst.score ? `<div class="panel lesson-card"><h2 class="card-h">Best call: ${esc(best.title || BY_ID[best.id].title)}</h2><p>${esc(best.answerTitle || BY_ID[best.id].answerTitle)}. Score ${mn(pct(best.score))}.</p></div>` : ''}<div class="panel lesson-card"><h2 class="card-h">Biggest surprise: ${esc(worst.title || BY_ID[worst.id].title)}</h2><p>${esc(worst.answerTitle || BY_ID[worst.id].answerTitle)}. ${esc(worst.implication || BY_ID[worst.id].implication)}</p><button class="link-btn" data-play="${esc(worst.id)}">Play it again</button></div></div>`;
  }
  const played = byTrack.filter(t => t[1]);
  const gapLine = cal.overconfidence === null ? '' : cal.overconfidence > 3 ? `${Math.round(cal.overconfidence)} points more confident than accurate` : cal.overconfidence < -3 ? `${Math.round(-cal.overconfidence)} points less confident than accurate` : 'Confidence matches accuracy';
  if (!all.length && !st.session.length) return `<section class="rec-head wrap"><h1>Your record</h1><p class="hero-lede">Nothing here yet. Your skill score, your calibration and every call you make appear after your first decision.</p><div class="tools"><button class="btn btn-solid btn-lg" data-act="replay">Play a round</button></div></section>`;
  return `<section class="rec-head wrap"><h1>${st.session.length ? 'Round complete' : 'Your record'}</h1>
    <div class="score-strip"><div class="score-big"><div class="score-row"><b class="num">${typeof (sess ?? meanScore) === 'number' ? mn(sess ?? meanScore) : '–'}</b><span class="score-unit">skill points<br>versus guessing</span>${sess === null ? spark : ''}</div><span>${sess !== null ? `Skill this round, ${st.session.length} call${st.session.length === 1 ? '' : 's'}` : `Skill over ${all.length} call${all.length === 1 ? '' : 's'}`}${(sess !== null ? st.session.length : all.length) < 5 ? ' (a few calls swing it widely)' : ''}: 0 is guessing, 100 is perfect, and a confident miss can fall far below 0. A confident forecast miss costs more than a wrong pick.</span></div>
${sess !== null ? `<dl class="score-meta"><div><dt>Decisions played on this device</dt><dd class="num">${all.length}</dd></div></dl>` : ''}</div>
    ${summary}</section>
    <section class="wrap"><div class="rec-grid">
      <div class="rec-col"><div class="panel rec-panel"><h2>${gapLine ? (/^\d/.test(gapLine) ? 'You were ' + gapLine : gapLine) : 'Calibration'}</h2><p>How sure you said you were, against how often you were right. Dots on the diagonal mean your confidence can be trusted.</p>${calPlot(cal)}</div>${played.length > 1 ? `<div class="panel rec-panel"><h2>By area</h2><ul class="hist">${played.map(([t, n, sc]) => `<li><span>${esc(t)}<br><small>${n} call${n === 1 ? '' : 's'}</small></span><span class="num">${n < 3 ? '<small>Score shows after 3 calls</small>' : `${mn(sc)}<span class="bar-score"><b class="zero"></b><i style="${sbar(sc)}"></i></span>`}</span></li>`).join('')}</ul></div>` : ''}</div>
      <div class="rec-col"><div class="panel rec-panel"><h2>${st.session.length ? 'This round' : 'Recent calls'}</h2><p class="small">Scores per decision; the big number above subtracts what guessing earns.</p><ul class="hist">${last.length ? last.slice().reverse().map(r => { const c = BY_ID[r.id]; return `<li><span><button class="link-quiet" data-play="${esc(r.id)}">${esc(c.title)}</button><br><small>${FORMAT_NAME[r.format]}, ${esc(c.track)}</small></span><span class="num">${mn(pct(r.score))}<span class="bar-score"><b class="zero"></b><i style="${sbar(pct(r.score))}"></i></span></span></li>` }).join('') : '<li><span>No calls yet. Play a path to start your record.</span></li>'}</ul></div></div>
    </div>
    <details class="how"><summary>How scoring works</summary><p>The headline is skill above guessing: each score is rescaled so that what a no-information strategy earns on that format (a 50% forecast, a random order, an even split, a random pick, the best blind estimating strategy across all estimates, such as always answering the same number) counts as 0 and a perfect call as 100. Below it, each decision's own score works as follows. Decisions score 0 to 100 with partial credit, except forecasts and point splits, which run from −100 to 100. An estimate inside the shaded band earns 100, and credit falls to zero at twice the band's half-width. Ranks score the share of pairs in the measured order. Point splits use the same proper rule as forecasts: all points on the option that worked best earn 100, and spreading points pays when you are unsure. Forecasts use a proper scoring rule built on the Brier score, the standard in forecasting tournaments: a confident correct call earns 100, saying 50% earns 50, and a confident wrong call costs up to 100 points, so stating your true belief always pays best. Your stated confidence does not change a decision's score; the calibration plot compares it with how often you were right (for forecasts, the probability is the statement). This is a learning record, not a validated assessment.</p></details>
    <div class="tools"><button class="btn btn-solid btn-lg" data-act="replay">Play another round</button><span class="tool-links"><button class="link-btn" data-act="csv">Export CSV</button><button class="link-btn" data-act="json">Export JSON</button><button class="link-btn" data-act="erase">Erase this device’s record</button></span></div></section>`;
}
// Each dot's call count goes on the first side (right, left, above, below) where it touches no dot and no other label (review 27, rule 31).
function calLabels(pts, sx, sy, P, W) {
  const rad = b => 5 + Math.min(10, Math.sqrt(b.n) * 2), dots = pts.map(b => ({ x: sx(b.meanP), y: sy(b.hitRate), r: rad(b) })), placed = [];
  const hitsBox = (bx, d) => { const cx = Math.max(bx.x0, Math.min(d.x, bx.x1)), cy = Math.max(bx.y0, Math.min(d.y, bx.y1)); return (cx - d.x) ** 2 + (cy - d.y) ** 2 < (d.r + 2) ** 2 };
  const over = (a, b) => a.x0 < b.x1 && b.x0 < a.x1 && a.y0 < b.y1 && b.y0 < a.y1;
  return pts.slice().sort((a, b) => b.n - a.n).map(b => { const x = sx(b.meanP), y = sy(b.hitRate), r = rad(b), txt = `${b.n} call${b.n === 1 ? '' : 's'}`, w = txt.length * 6.6, h = 13;
    const opts = [[x + r + 4, y + 4, 'start'], [x - r - 4, y + 4, 'end'], [x, y - r - 5, 'middle'], [x, y + r + 13, 'middle']].map(([tx, ty, a]) => ({ tx, ty, a, bx: { x0: a === 'start' ? tx : a === 'end' ? tx - w : tx - w / 2, x1: a === 'start' ? tx + w : a === 'end' ? tx : tx + w / 2, y0: ty - h + 2, y1: ty + 2 } }));
    const diag = bx => [0, .25, .5, .75, 1].some(t => { const X = bx.x0 + (bx.x1 - bx.x0) * t, Y = sy((X - sx(0)) / (sx(100) - sx(0)) * 100); return Y > bx.y0 - 2 && Y < bx.y1 + 2 });   // the diagonal is an obstacle too (review 31, m7)
    const cost = o => (o.bx.x0 > P + 2 && o.bx.x1 < W - 2 && o.bx.y0 > 2 && o.bx.y1 < W - P - 2 ? 0 : 100) + 10 * dots.filter(d => hitsBox(o.bx, d)).length + 5 * placed.filter(q => over(q, o.bx)).length + 4 * diag(o.bx);
    const o = opts.reduce((m, x) => cost(x) < cost(m) ? x : m); placed.push(o.bx);
    return `<text x="${o.tx}" y="${o.ty}" font-size="12" fill="#36425e" text-anchor="${o.a}">${txt}</text>` }).join('');
}
function calPlot(cal) {
  const W = 320, P = 34, M = 16, sx = v => P + M + v / 100 * (W - P - 22 - M), sy = v => W - P - M - v / 100 * (W - P - 22 - M);   // M keeps the largest dot off the axis labels
  const pts = cal.bins.filter(b => b.n);
  return `<svg viewBox="0 0 ${W} ${W}" role="img" aria-label="Calibration plot: ${pts.map(b => `stated ${Math.round(b.meanP)}%, right ${Math.round(b.hitRate)}% over ${b.n} calls`).join('; ') || 'no data yet'}" style="max-width:420px;width:100%;display:block;margin:0 auto">
    <path d="M${P} 22 V${W - P} H${W - 22}" fill="none" stroke="#cbd3dd"/>
    ${[0, 25, 50, 75, 100].map(v => `<text x="${sx(v)}" y="${W - P + 15}" font-size="12" text-anchor="middle" fill="#56617a">${v}</text><text x="${P - 6}" y="${sy(v) + 3}" font-size="12" text-anchor="end" fill="#56617a">${v}</text>`).join('')}
    <line x1="${sx(0)}" y1="${sy(0)}" x2="${sx(100)}" y2="${sy(100)}" stroke="#9aa6b6" stroke-dasharray="4 4"/><text x="${sx(8)}" y="${sy(8) - 7}" font-size="12" fill="#56617a" text-anchor="start" stroke="#eceff3" stroke-width="4" paint-order="stroke" transform="rotate(-45 ${sx(8)} ${sy(8) - 7})">as sure as right</text>
    ${pts.map(b => { const r = 5 + Math.min(10, Math.sqrt(b.n) * 2); return `<circle cx="${sx(b.meanP)}" cy="${sy(b.hitRate)}" r="${r}" fill="#2f54eb" fill-opacity=".85" stroke="#fff" stroke-width="2"/>` }).join('')}${calLabels(pts, sx, sy, P, W)}
    <text x="${(W + P) / 2}" y="${W - 4}" font-size="12" text-anchor="middle" fill="#36425e">Stated confidence (%)</text>
    <text x="10" y="${(W - P) / 2}" font-size="12" text-anchor="middle" fill="#36425e" transform="rotate(-90 10 ${(W - P) / 2})">Share right (%)</text></svg><p class="small cal-cap">${pts.length ? '' : 'Points appear after your first calls.'}</p>`;
}

// ----- modals -----
let lastFocus = null;
function modal(html, label) {
  lastFocus = document.activeElement;
  qs('#overlay').innerHTML = `<div class="modal-back" data-close="1"><div class="modal" role="dialog" aria-modal="true" aria-label="${esc(label)}"><button class="close" data-close="1" aria-label="Close">×</button>${html}</div></div>`;
  qs('#overlay .close').focus();
}
function closeModal() { if (!qs('#overlay').innerHTML) return; qs('#overlay').innerHTML = ''; lastFocus && lastFocus.focus && lastFocus.focus() }
// A paper's title often states its finding, so it shows once every decision built on the paper has been played.
function paperTitle(s) { const used = ALL.filter(c => c.sources.includes(s.id)); return s.title && used.every(c => records.some(r => r.id === c.id)) ? s.title : null }
function sourceModal(id) {
  const s = SOURCE[id]; if (!s) return; const v = s.verification || {}; const used = ALL.filter(c => c.sources.includes(id));
  modal(`<h2>${esc(paperTitle(s) || `${s.authors} (${s.year})`)}</h2>${paperTitle(s) ? '' : '<p class="small">The paper’s title appears once you have played every decision built on it, because titles often state the finding.</p>'}<p><strong>${esc(s.authors)}</strong> (${s.year}). <i>${esc(s.venue)}</i>${s.volume ? `, ${esc(s.volume)}` : ''}${s.pages ? `, ${esc(s.pages)}` : ''}.</p>
    ${s.takeaway && used.every(c => records.some(r => r.id === c.id)) ? `<p><strong>What the lab uses.</strong> ${esc(s.takeaway)}</p>` : `<p>The paper’s finding appears here once you have played ${used.length > 1 ? 'every decision' : 'the decision'} built on it.</p>`}
    <p><strong>How it was checked.</strong> ${esc(srcStatus(s)[0])}${v.checked ? ' on ' + esc(v.checked) : ''}. Metadata matched against the DOI registry.${v.note ? ' ' + esc(v.note) : ''}</p>
    ${used.length ? `<p><strong>Decisions built on it:</strong> ${used.map(c => `<button class="link-btn" data-play="${esc(c.id)}">${esc(c.title)}</button>`).join(', ')}.</p>` : ''}
    <p><a href="${esc(s.url)}" target="_blank" rel="noopener noreferrer">Open the article (DOI ${esc(s.doi)})</a></p>`, 'Source details');
}
function methodsModal() {
  const live = Object.values(SOURCE).filter(isLive), q = Object.values(SOURCE).filter(s => !isLive(s));
  modal(`<h2>Research standard</h2>
    <p>Scored answers come only from peer-reviewed journal articles or scholarly books. Each source was matched against the DOI registry, and every number used in a decision was checked against the published abstract or full text. ${live.length} sources passed${q.length ? `; ${q.length} are held back until their claims can be checked` : ''}.</p>
    <p>Scenarios are teaching adaptations written for managers. They describe the study design accurately but do not replicate it. Charts appear only where the study reported the values shown.</p>
    <p>A single study is evidence about one population, task and time. Each decision states the population, task and setting the evidence comes from.</p>
    <p>Original concept by Eugen Dimant. A teaching tool, not a validated assessment.</p>`, 'Research standard');
}

// ----- export -----
async function download(name, text, mime) {   // inside a claude.ai page the viewer's own save dialog; elsewhere a plain browser download
  try { const d = window.claude && window.claude.use ? await window.claude.use('downloads') : null; if (d) { try { await d.save({ filename: name, data: text }) } catch (e) { if (e && e.code !== 'declined') notice('That file cannot be saved here.') } return } } catch { }
  const b = new Blob([text], { type: mime }); const u = URL.createObjectURL(b); const a = document.createElement('a'); a.href = u; a.download = name; document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(u), 4000) }
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
      let r, d;
      for (let i = 0; i < 6; i++) {   // a whole class joining at once: wait and retry when the server asks
        r = await fetch(`/api/rooms/${code}/join`, { method: 'POST', headers: roomHeaders(true), body: '{}' }); d = await r.json();
        if (r.status !== 429) break; await new Promise(res => setTimeout(res, 1500 + Math.random() * 2000));
      }
      if (!r.ok) throw Error(d.error || 'Could not join'); tok = d.token; sessionStorage.setItem('thv:room:' + code, tok); sessionStorage.setItem('thv:room:' + code + ':n', d.number);
    }
    st.seed = hash(code) >>> 0;
    st.room = { code, token: tok, number: sessionStorage.getItem('thv:room:' + code + ':n'), phase: 'lobby', challenge: null, etag: '', agg: null, misses: 0 };
    st.view = 'play'; st.deck = []; closeModal(); render(true); roomPoll();
  } catch (e) { modal(`<h2>You are not in the class yet</h2><p>${esc(e.message)}</p><p>Ask your instructor to reopen joining or check the code, then open the class link again.</p><button class="btn btn-solid" data-close="1">Close</button>`, 'Could not join the class') }   // stays until closed, unlike a toast
}
async function roomPoll() {
  if (!st.room) return; const R = st.room;
  try {
    const r = await fetch(`/api/rooms/${R.code}?v=${encodeURIComponent(R.etag)}`, { headers: roomHeaders() });
    if (r.status === 404) { st.room = null; st.view = 'home'; render(true); modal('<h2>This live session has ended</h2><p>Your instructor ended the class. Your answers stay in your record on this device.</p><button class="btn btn-solid" data-close="1">Close</button>', 'Class ended'); return }   // a dialog, so the end is not missed
    if (!r.ok) throw Error('poll ' + r.status);   // a 429 or error body is not class state: keep the current card and answer
    const d = await r.json(); if (R.misses) { const rc = qs('#room-conn'); if (rc) rc.textContent = 'Live class ' + R.code } R.misses = 0;   // the question screen says when the phone lost the class (review 35, m10)
    if (!d.same && d.phase) {
      const changed = d.challenge !== R.challenge, phaseChanged = d.phase !== R.phase;
      R.etag = d.etag; R.phase = d.phase; R.agg = d.aggregate || null; R.participants = d.participants; R.responses = d.responses; R.title = d.title;
      if (d.evidence && BY_ID[d.evidence.id]) Object.assign(BY_ID[d.evidence.id], d.evidence);
      if (changed && d.challenge && BY_ID[d.challenge]) { R.challenge = d.challenge; st.view = 'play'; st.deck = [BY_ID[d.challenge]]; st.i = 0; st.pending = null; resetCard(); render(true) }
      else if (phaseChanged || d.phase === 'revealed') {
        R.challenge = d.challenge; st.view = 'play';
        const c = card();
        if (d.phase === 'revealed' && c && st.pending && c.answerTitle && !st.session.some(r => r.id === c.id && r.room === R.code)) { const rec = finalize(c, st.pending.response, st.pending.confidence); rec.room = R.code; st.pending = null }
        render(phaseChanged);
      }
      else { const live = qs('#room-live'); if (live) live.textContent = roomLine() }
    }
    const f = R.failed;   // a stranded answer: checked on every good poll, including an unchanged room (audit 49, M2)
    if (f && (R.challenge !== f.cid || R.phase === 'revealed')) { R.failed = null; if (st.view === 'play') render() }   // the class moved on: never file it under another decision (audit 49, M1)
    else if (f && !R.resending && R.phase === 'open' && Date.now() >= f.next && f.tries < 10) { R.resending = true; roomSubmit(f.c, f.rec, true).finally(() => { if (st.room) st.room.resending = false }) }
  } catch { R.misses++; if (R.misses === 1) { const live = qs('#room-live'); if (live) live.textContent = 'Reconnecting…'; const rc = qs('#room-conn'); if (rc) rc.textContent = 'Reconnecting…' } }   // announced once, not on every failed poll (audit 49, m3)
  clearTimeout(R.timer); R.timer = setTimeout(roomPoll, document.hidden ? 6000 : Math.min(8000, 2000 * (1 + R.misses)));
}
function roomLine() { const R = st.room; return `${R.participants ?? '–'} joined. ${R.phase === 'open' ? (R.responses ?? 0) + ' answered so far.' : ''}` }
async function roomSubmit(c, rec, auto = false) {
  const R = st.room, prev = R.failed;
  if (!auto) { R.sent = false; R.failed = null; render(); roomFocus() }
  let wait = 800, busy = false;
  for (let k = 0; k < (auto ? 1 : 6); k++) {   // about 20 s in all, honouring Retry-After (review 28); one quiet try per poll once stranded
    if (st.room !== R || R.challenge !== c.id) return;   // the instructor moved on: the answer belongs to its own decision only
    try {
      const r = await fetch(`/api/rooms/${R.code}/responses`, { method: 'POST', headers: roomHeaders(true), body: JSON.stringify({ token: R.token, challenge: c.id, answer: rec.response, confidence: rec.confidence }) });
      const ra = +r.headers.get('Retry-After') || 2, st0 = r.status; let d = {}; try { d = await r.json() } catch { }
      if (r.ok && typeof d.accepted !== 'boolean') throw Error('not the class server')   // a captive portal or proxy page is not a receipt (review 36, m2)
      if (r.ok) { R.failed = null; R.sent = true; R.sentMsg = d.accepted ? 'Your answer is in.' : d.message; render(); roomFocus(); clearTimeout(R.timer); roomPoll(); return }   // refresh the room count now, not at the next poll
      if (r.status === 409 || r.status === 400 || r.status === 403) { R.failed = null; R.sent = true; R.sentMsg = d.error; render(); roomFocus(); return }
      wait = st0 === 429 ? Math.max(800, 1000 * ra) : 800 * (k + 1); busy = st0 === 429;
    } catch { wait = 800 * (k + 1); busy = false }
    if (!auto && k < 5) await new Promise(z => setTimeout(z, wait + Math.random() * 400));
  }
  const tries = auto && prev ? prev.tries + 1 : 0;
  R.failed = { c, rec, cid: c.id, tries, next: Date.now() + 1000 * [5, 10, 20, 40, 60][Math.min(tries, 4)] };   // its own decision, with backoff, then the button alone (audit 49, M1 and m1)
  const msg = busy ? 'The class server is busy. Your answer is kept on this page and goes out again on its own, or send it now.' : 'Your answer did not reach the class. It is kept on this page and goes out again on its own when the connection returns, or send it now.';
  if (!auto || R.sentMsg !== msg || !prev) { R.sentMsg = msg; R.sent = true; render() }   // a quiet retry that fails again changes nothing on screen
}
function roomFocus() { const h = qs('.room-wait h1'); if (h && (document.activeElement === document.body || !document.activeElement || !document.contains(document.activeElement))) h.focus() }   // focus stays in the card after a re-render (audit 49, m2)
function roomWait() {
  const R = st.room;
  return `<section class="play wrap"><div class="panel card room-wait" aria-live="polite">
    <h1 class="q" tabindex="-1">${R.phase === 'lobby' || !R.challenge ? 'You are in. The first decision appears when your instructor opens it.' : 'Waiting for the next decision.'}</h1><p class="room-id">Live class ${esc(R.code)}${R.number ? ', you are participant ' + esc(R.number) : ''}.</p>
    <p class="scene">Keep this page open. Your answers count toward the class picture, not toward a grade, and the instructor sees only participant numbers.</p>
    <p class="kicker" id="room-live">${roomLine()}</p><button class="btn btn-quiet" data-act="leave-room">Leave the live class</button></div></section>`;
}
function roomLocked(c) {
  const R = st.room;
  return `<section class="play wrap"><div class="panel card room-wait" aria-live="polite">
    <h1 class="q" tabindex="-1">${R.failed && R.phase !== 'open' ? 'Not counted.' : R.failed ? 'Not sent yet.' : R.sent ? esc(R.sentMsg || 'Your answer is in.') : 'Sending your answer…'}</h1><p class="room-id">Live class ${esc(R.code)}, decision: ${esc(c.title)}${/[?!.]$/.test(c.title) ? '' : '.'}</p>
    <p class="scene">${R.failed && R.phase !== 'open' ? 'Answers closed for this decision before your answer reached the class.' : R.failed ? esc(R.sentMsg) : 'The evidence appears for everyone when your instructor reveals it.'}</p><p class="kicker" id="room-live">${roomLine()}</p><div class="room-acts">${R.failed && R.phase === 'open' ? '<button class="btn btn-solid" data-act="resend">Send my answer again</button>' : ''}<button class="btn btn-quiet" data-act="leave-room">Leave the live class</button></div></div></section>`;   // a failed send gets a short headline and its reason below (review 35, M1)   // no badge above the headline (review 27, rule 2)
}
function classPanel(c, a) {
  const f = c.format; let body = '';
  const hbars = (labels, vals, ev, show, tag) => { const mx = Math.max(1, ...vals); return `<div class="hbars" role="img" aria-label="Class answers">${labels.map((l, i) => `<div class="hb-row"><span class="hb-label">${esc(l)}${tag && ev && ev.includes(i) ? ` <em class="ev-note">${tag}</em>` : ''}</span><span class="hb-track${ev && ev.includes(i) ? ' ev-row' : ''}"><i class="grow ${ev && ev.includes(i) ? 'ev' : 'room'}" style="width:${Math.max(1.5, vals[i] / mx * 100)}%"></i></span><b class="num">${show ? show[i] : vals[i]}</b></div>`).join('')}</div>` };
  if (a.counts) { const o = optionOrder(c); body = hbars(o.map(x => x.t), o.map(x => a.counts[x.i]), o.map((x, k) => (f === 'multi' ? c.multiAnswers.includes(x.i) : x.i === c.answer) ? k : -1).filter(k => k >= 0), null, f === 'multi' ? 'in the study' : 'the study’s answer') }   // marked even when nobody picked it (review 36, M1)
  else if (a.hist) { const lo = a.lo, hi = a.hi, w = (hi - lo) / a.hist.length, mx = Math.max(1, ...a.hist), ev = f === 'estimate' ? c.estimate.target : (c.forecast.truth ? 100 : 0); body = `<svg viewBox="0 0 340 130" role="img" aria-label="Class distribution, median ${a.median}">${a.hist.map((h, i) => `<rect x="${10 + i * 32}" y="${100 - h / mx * 80}" width="28" height="${h / mx * 80}" rx="3" fill="#5b6b86" fill-opacity=".8"/>`).join('')}<line x1="${10 + (ev - lo) / (hi - lo) * 320}" y1="10" x2="${10 + (ev - lo) / (hi - lo) * 320}" y2="104" stroke="#e0a01c" stroke-width="3"/><text x="10" y="122" font-size="12" fill="#56617a">${lo}</text><text x="330" y="122" font-size="12" fill="#56617a" text-anchor="end">${hi}</text><text x="${Math.min(300, 14 + (ev - lo) / (hi - lo) * 320)}" y="20" font-size="12" font-weight="700" fill="#7d5200">Evidence</text></svg><p class="gap-caption">Class median ${a.median}${f === 'estimate' ? (c.estimate.unit ?? '%') : '%'}.</p>` }
  else if (a.meanPosition) body = '<p class="plate-h">The room’s average rank, 1 is the top</p>' + hbars(c.options, a.meanPosition.map(p => p == null ? 0 : +(c.options.length + 1 - p).toFixed(2)), ((c.rankTies || []).find(g => g.includes(c.rankAnswer[0])) || [c.rankAnswer[0]]), a.meanPosition.map(p => p == null ? '–' : Number(p).toFixed(1)));
  else if (a.meanShare) body = hbars(c.options, a.meanShare, (c.allocate.best || [c.allocate.values.indexOf(Math.max(...c.allocate.values))]), a.meanShare.map(v => v == null ? '–' : v + ' pts'));   // the same unit as the player's own split (review 30, m15)
  else if (a.taskCounts) body = `<p class="plate-h">Classmates who routed each task as the evidence suggests</p><ul class="hist">${c.delegate.tasks.map((t, i) => `<li><span>${esc(short(t.text, 60))}</span><span class="num">${[t.answer, ...(t.also || [])].reduce((x, j) => x + (a.taskCounts[i][j] || 0), 0)} of ${a.n}</span></li>`).join('')}</ul>`;
  return `<section class="panel gap" aria-labelledby="class-h"><h2 id="class-h">The room, ${a.n} ${a.n === 1 ? 'answer' : 'answers'}</h2><p class="gap-caption" style="margin:0 0 8px">Average score ${a.meanScore === null || a.meanScore === undefined ? '–' : mn(a.meanScore)}. ${a.shareCorrect ?? 0}% matched the evidence${a.meanConfidence !== null ? `, at ${a.meanConfidence}% average confidence` : ''}.</p>${body}</section>`;
}
function joinModal() {
  modal(`<h2>Join the live class with the code on the screen</h2><form data-form="join" class="tutor-line"><label class="sr-only" for="join-code">Session code</label><input id="join-code" maxlength="8" autocomplete="off" autocapitalize="characters" placeholder="For example K7QPM" style="text-transform:uppercase;font-size:20px;letter-spacing:.12em"><button class="btn btn-solid">Join</button></form><p>No name or account needed. The instructor sees answers by participant number only.</p>`, 'Join a live class');
  setTimeout(() => qs('#join-code')?.focus(), 20);
}

// ---------- render ----------
let toastT;
function notice(s) { const t = qs('#toast'); t.textContent = s; t.classList.add('show'); clearTimeout(toastT); toastT = setTimeout(() => t.classList.remove('show'), 3200) }
// Browser Back and Forward move between views; #library, #studies and #record are linkable.
const HASH = { almanac: '#library', atlas: '#studies', record: '#record', play: '#play', home: '' };
const fromHash = h => (Object.entries(HASH).find(([, x]) => x && x === h) || ['home'])[0];
function syncHash() {
  if (st.room) return; const want = HASH[st.view] ?? '';
  if ((location.hash || '') === want) return;
  try { history.pushState(null, '', want || location.pathname + location.search) } catch { }
}
addEventListener('popstate', () => {
  if (st.room) return; const v = fromHash(location.hash);
  st.view = v === 'play' && !st.deck.length ? 'home' : v; closeModal(); render(true);
});
function render(moveFocus) {
  syncHash();
  const v = qs('#view');
  if (st.view === 'almanac' && !libraryLoaded) loadLibrary();
  v.innerHTML = st.view === 'home' ? home() : st.view === 'atlas' ? atlas() : st.view === 'almanac' ? almanac() : st.view === 'record' ? record() : play();
  document.body.classList.toggle('in-play', st.view === 'play');
  balanceReveal();
  qa('.nav button').forEach(b => b.setAttribute('aria-current', (b.dataset.nav === st.view || (b.dataset.nav === 'almanac' && st.view === 'atlas')) ? 'page' : 'false'));
  qs('.nav').classList.toggle('open', st.menu);
  const c = card();
  document.title = (st.view === 'play' && c ? (st.phase === 'reveal' ? c.answerTitle : c.title) + ', ' : st.view === 'atlas' ? 'All decisions, ' : st.view === 'almanac' ? 'Principles, ' : st.view === 'record' ? 'Your record, ' : '') + 'The Human Variable';
  if (moveFocus && (st.phase === 'reveal' || st.hero.done)) animateReveal();
  if (moveFocus) { scrollTo({ top: 0, behavior: 'instant' in document.documentElement.style ? 'instant' : 'auto' }); const h = qs('#view h1'); if (h) { if (!h.hasAttribute('tabindex')) h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }) } }
}
function balanceReveal() {   // the shorter column takes the study card and the principle strip (review 33, m9); a class, not a DOM move, so reading order stays put (audit 45)
  const rv = qs('.reveal'); if (!rv) return; rv.classList.remove('meta-right'); const m0 = qs('.reveal>.rev-meta'); if (m0) m0.style.marginTop = '';
  const fig = qs('.reveal>figure.gap'), meta = qs('.reveal>.rev-meta'), left = qs('.reveal>.action-note');
  if (!fig || !meta || !left || innerWidth < 1200 || qs('.reveal>section.gap')) return;   // a live-class panel already lengthens the right column
  const fb = fig.getBoundingClientRect().bottom, lb = left.getBoundingClientRect().bottom, mh = meta.getBoundingClientRect().height;
  if (lb - fb > mh * .3) { rv.classList.add('meta-right'); const gap = meta.getBoundingClientRect().top - fig.getBoundingClientRect().bottom - 24; if (gap > 0) meta.style.marginTop = -gap + 'px' }   // pulled up to sit under the figure, not in a row below the left column (audit 47)
}
let balT; addEventListener('resize', () => { clearTimeout(balT); balT = setTimeout(balanceReveal, 150) });
function animateReveal() {
  if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  // the study's number counts up from the player's call: the one orchestrated moment of the reveal
  qa('.gap-head').forEach(h => { const ev = h.querySelector('.gh-ev'), you = h.querySelector('.gh-you'); if (!ev || !you) return; const m = ev.textContent.match(/^(-?\d+(?:\.\d+)?)(.*)$/), a = parseFloat(you.textContent); if (!m || isNaN(a)) return;
    const to = parseFloat(m[1]), dec = (m[1].split('.')[1] || '').length, t0 = performance.now(), D = 900;
    const step = now => { const k = Math.min(1, (now - t0) / D), e = 1 - Math.pow(1 - k, 3); ev.textContent = (a + (to - a) * e).toFixed(dec) + m[2]; if (k < 1) requestAnimationFrame(step) }; requestAnimationFrame(step) });
  qa('.ev-mark[data-from]').forEach(g => { const d = +g.dataset.from; if (!d) return; g.style.transition = 'none'; g.style.transform = `translateX(${d}px)`; g.style.opacity = '.3'; requestAnimationFrame(() => requestAnimationFrame(() => { g.style.transition = ''; g.style.transform = ''; g.style.opacity = '' })) });

}
function setRange(el) { el.classList.remove('untouched'); el.style.setProperty('--fill', (el.value - el.min) / (el.max - el.min) * 100 + '%') }

// ---------- events ----------
document.addEventListener('click', e => {
  if (e.target.closest('[data-home]')) { e.preventDefault(); closeModal(); st.view = 'home'; st.room = st.room; render(true); return }
  const t = e.target.closest('button,[data-close]'); if (!t) return;
  if (t.dataset.close && (e.target === t || t.classList.contains('close'))) { closeModal(); return }
  if (t.dataset.nav) { closeModal(); if (st.room && t.dataset.nav === 'home' && st.view === 'play') { if (!confirm('Leave the live class?')) return; clearTimeout(st.room.timer); st.room = null } st.view = t.dataset.nav; st.menu = false; render(true); return }
  if (t.dataset.track) { st.track = t.dataset.track; const n = st.track === 'Mixed' ? ALL.length : ALL.filter(c => c.track === st.track).length; if (st.length > n) st.length = 5; render(); return }
  if (t.dataset.length) { st.length = +t.dataset.length; render(); return }
  if (t.dataset.themeRound) { st.seed = (Math.random() * 2 ** 32) >>> 0; const done = new Set(records.map(r => r.id)), cs = ALL.filter(c => c.theme === t.dataset.themeRound), left = cs.filter(c => !done.has(c.id)); start(left.length ? left : cs, 99); return }   // "Play the other N" plays the unplayed ones (audit 31)
  if (t.dataset.source) { sourceModal(t.dataset.source); return }
  if (t.dataset.play) { closeModal(); const c = ALL.find(x => x.id === t.dataset.play); if (c) { st.seed = (Math.random() * 2 ** 32) >>> 0; start(c.case ? ALL.filter(x => x.case && x.case.id === c.case.id) : [c], c.case ? c.case.of : 1) } return }
  if (t.dataset.ask) { ask(t.dataset.ask); return }
  if (t.dataset.tab) { st.tab = t.dataset.tab; const y = scrollY; render(); scrollTo(0, y); qs(`[data-tab="${st.tab}"]`)?.focus(); return }
  if (t.dataset.path) { const p = BANK.paths.find(x => x.id === t.dataset.path); const played = new Set(records.map(r => r.id)); let list = p.ids.map(id => ALL.find(c => c.id === id)).filter(Boolean); if (t.dataset.resume) { const rest = list.filter(c => !played.has(c.id)); if (rest.length) list = rest } st.deck = list; st.i = 0; st.session = []; st.view = 'play'; resetCard(); render(true); return }
  if (t.dataset.theme) { st.view = 'almanac'; st.almanacOpen = t.dataset.theme; render(true); qs('#theme-' + t.dataset.theme)?.scrollIntoView(); return }
  if (st.view === 'play' && st.phase === 'predict') {
    const c = card();
    if (t.dataset.choice !== undefined) { const i = +t.dataset.choice; if (c.format === 'multi') { const need = c.pick || (c.multiAnswers || []).length || 2; if (st.resp.includes(i)) st.resp = st.resp.filter(x => x !== i); else if (st.resp.length < need) st.resp = [...st.resp, i]; else { notice(`You can choose ${need}. Tap a choice again to remove it.`); return } } else st.resp = i; render(); qs(`[data-choice="${i}"]`)?.focus(); return }
    if (t.dataset.rank !== undefined) { const k = +t.dataset.rank, d = +t.dataset.dir, r = st.resp, j = k + d; if (j < 0 || j >= r.length) return;[r[k], r[j]] = [r[j], r[k]]; st.touched = true; render(); const sel = qs(`[data-rank="${j}"][data-dir="${d}"]`) || qs(`[data-rank="${j}"][data-dir="${-d}"]`); sel?.focus(); return }
    if (t.dataset.deleg !== undefined) { st.resp[+t.dataset.deleg] = +t.dataset.pick; render(); qs(`[data-deleg="${t.dataset.deleg}"][data-pick="${t.dataset.pick}"]`)?.focus(); return }
  }
  const a = t.dataset.act;
  if (!a) return;
  if (a === 'skip-locked') { next(); return }
  if (a === 'leave') { if (st.room) { if (!confirm('Leave the live class?')) return; clearTimeout(st.room.timer); st.room = null } st.view = 'home'; render(true); return }
  if (a === 'toggle-custom') { st.custom = !st.custom; render(); qs('[data-act="toggle-custom"]')?.focus(); return }
  if (a === 'menu') { st.menu = !st.menu; t.setAttribute('aria-expanded', st.menu); qs('.nav').classList.toggle('open', st.menu); return }
  if (a === 'go-start') { const first = qs('#start .path'); if (first) { first.click(); return } qs('#start')?.scrollIntoView(); return }   // start the featured path straight away
  if (a === 'start' || a === 'replay') { st.seed = (Math.random() * 2 ** 32) >>> 0; startTrack(); return }
  if (a === 'start-quick') { st.seed = (Math.random() * 2 ** 32) >>> 0; st.track = 'Mixed'; start(ALL.filter(c => c.id !== 'ai01'), 5); return }
  if (a === 'dimant-round') { st.seed = (Math.random() * 2 ** 32) >>> 0; start(ALL.filter(c => c.sources.some(id => /Dimant/.test(SOURCE[id].authors_full || SOURCE[id].authors))), 12); return }
  if (a === 'hero-lock') { if (st.hero.value === null) return; ensureFull('ai01').then(ok => { if (!ok) return; st.hero.done = true; render(); animateReveal(); qs('[data-act="start-quick"]')?.focus({ preventScroll: true }) }); return; st.hero.done = true; render(); animateReveal(); qs('[data-act="start-quick"]')?.focus({ preventScroll: true }); return }
  if (a === 'hero-reset') { st.hero = { value: null, done: false }; render(); qs('#hero-range')?.focus(); return }
  if (a === 'lock') { lock(); return }
  if (a === 'next') { next(); return }
  if (a === 'save-note') { const c = card(), v = qs('#note')?.value || ''; notes[c.id] = v.slice(0, 480); store.set(NOTE_KEY, notes); notice('Note saved on this device.'); return }
  if (a === 'csv') { exportCSV(); return }
  if (a === 'json') { download('human-variable-record.json', JSON.stringify({ kind: 'thv-record', version: 2, exported: new Date().toISOString(), records }, null, 2), 'application/json'); return }
  if (a === 'erase') { if (confirm('Erase every saved call and field note in this browser? This cannot be undone.')) { records = []; notes = {}; st.session = []; store.del(REC_KEY); store.del(NOTE_KEY); store.del('thv:v1:results'); render(); notice('Record erased.') } return }
  if (a === 'methods') { methodsModal(); return }
  if (a === 'join') { joinModal(); return }
  if (a === 'resend') { const f = st.room && st.room.failed; if (f && !st.room.resending) { st.room.resending = true; roomSubmit(f.c, f.rec).finally(() => { if (st.room) st.room.resending = false }) } return }
  if (a === 'leave-room') { clearTimeout(st.room?.timer); st.room = null; st.view = 'home'; render(true); return }
  if (a === 'about') { methodsModal(); return }
});
document.addEventListener('input', e => {
  const el = e.target, c = card();
  if (el.id === 'hero-range') { st.hero.value = +el.value; setRange(el); const hr = qs('#hero-read'); hr.textContent = el.value + '%'; hr.classList.remove('empty'); const hu = qs('.hero-unit'); if (hu) hu.textContent = 'less time, your call'; if (hu) hu.hidden = false; qs('[data-act="hero-lock"]').disabled = false; return }
  if (el.id === 'conf') { st.conf = +el.value; st.confTouched = true; setRange(el); const o = qs('#conf-read'); o.textContent = st.conf + '%'; o.classList.remove('empty'); syncLock(); return }
  if (!c || st.phase !== 'predict') {
    if (el.id === 'atlas-q') { st.atlasQuery = el.value; const tmp = document.createElement('div'); tmp.innerHTML = atlas(); qs('#atlas-grid').replaceWith(tmp.querySelector('#atlas-grid')); qs('#atlas-count').textContent = tmp.querySelector('#atlas-count').textContent }
    return;
  }
  if (el.id === 'est') { st.resp = +el.value; setRange(el); qs('#est-read').textContent = mn(st.resp + (c.estimate.unit ?? '%')); qs('#est-read').classList.remove('empty'); syncLock(); return }
  if (el.id === 'fc') { st.resp = +el.value; st.touched = true; setRange(el); qs('#fc-read').textContent = st.resp + '%'; qs('#fc-read').classList.remove('empty'); syncLock(); return }
  if (el.dataset.alloc !== undefined) {
    // The points always add up to the total: raising one option takes points from the others in proportion.
    const k = +el.dataset.alloc, a = c.allocate, step = a.step || 10, before = st.resp.slice();
    let v = Math.min(a.total, Math.max(0, +el.value)), need = v - st.resp[k];
    const r = st.resp.slice(); r[k] = v;
    if (need > 0) {
      for (let guard = 0; need > 0 && guard < 100; guard++) {
        const donors = r.map((x, i) => i !== k && x > 0 ? i : -1).filter(i => i >= 0); if (!donors.length) break;
        const i = donors.reduce((m, j) => r[j] > r[m] ? j : m, donors[0]); const take = Math.min(step, r[i], need); r[i] -= take; need -= take;
      }
      if (need > 0) r[k] -= need;
    } else if (need < 0) {
      let give = -need; for (let guard = 0; give > 0 && guard < 100; guard++) { const i = r.map((x, j) => j).filter(j => j !== k).reduce((m, j) => r[j] < r[m] ? j : m, k === 0 ? 1 : 0); const add = Math.min(step, give); r[i] += add; give -= add }
    }
    if (r.some((x, i) => x !== before[i])) st.touched = true;   // only a real change counts as the player's own split
    st.resp = r;
    qa('[data-alloc]').forEach(inp => { const i = +inp.dataset.alloc; inp.value = r[i]; setRange(inp); inp.nextElementSibling.textContent = (a.prefix || '') + r[i] + (a.suffix || '') });
    const sum = r.reduce((x, y) => x + y, 0), tot = qs('.alloc-total'); tot.classList.toggle('ok', sum === a.total); tot.lastElementChild.textContent = `${a.prefix || ''}${sum}${a.suffix || ''} of ${a.prefix || ''}${a.total}${a.suffix || ''}`;
    syncLock(); return;
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
    if (e.key === 'Enter' && !e.target.matches('button, a, summary, textarea') && lockReady(c)) { e.preventDefault(); lock(); return }
  } else if ((e.key === 'n' || e.key === 'N') && !st.room) { next() }
});

// ---------- boot ----------
document.body.insertAdjacentHTML('afterbegin', `<a class="skip" href="#view">Skip to content</a>`);
// Live classes need the Python server; hide their entry points in the offline file and inside Streamlit's frame.
if (!location.protocol.startsWith('http')) qa('[data-act="join"], a[href="classroom.html"]').forEach(el => el.hidden = true);
qs('#brand-glyph').outerHTML = glyph;
if (PUBLIC) { TUTOR_REMOTE = '/api/tutor'; refreshLock() }
if (location.protocol.startsWith('http')) {
  fetch('/api/tutor/status').then(r => r.ok ? r.json() : null).then(d => { if (d && d.enabled) { TUTOR_REMOTE = '/api/tutor'; TUTOR_AI = true; if (st.view === 'play' && st.phase === 'reveal') render() } }).catch(() => { });
}
try { document.fonts && document.fonts.ready.then(() => { const old = { ...TW }; for (const k in TW) delete TW[k]; const moved = Object.keys(old).some(k => { const i = k.indexOf('|'); return Math.abs(textWidth(k.slice(i + 1), +k.slice(0, i)) - old[k]) > .5 }); if (moved && document.querySelector('svg.dag')) { const f = document.activeElement && document.activeElement.matches('h1, h2') ? document.activeElement.id || document.activeElement.className : null; render(); if (f) { const e = document.getElementById(f) || document.querySelector('.' + String(f).split(' ')[0]); e && e.focus() } } }) } catch { }   // redraw only if the real font measures differently, and keep focus (audit 33)
if (PARAM.get('room')) { render(); roomJoin(PARAM.get('room')) } else if (PARAM.get('play') && BY_ID[PARAM.get('play')]) { const c = ALL.find(x => x.id === PARAM.get('play')); if (c) start([c], 1); else render() } else { const v = fromHash(location.hash); if (v !== 'play') st.view = v; render(); if (PARAM.get('play')) notice('That decision link is out of date. Pick a decision from the list.') }
if (!PUBLIC || PARAM.has('debug')) window.THV = { st, ALL, BY_ID, records: () => records, curated }; // test hook (offline file only)
})();
