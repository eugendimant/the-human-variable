// Scoring for every challenge format. Pure functions: no DOM, no storage.
// Loaded in the browser as a global (THVScore) and in Node tests via require().
(function (root) {
  'use strict';
  const clamp = (x, a, b) => Math.min(b, Math.max(a, x));

  // Every scorer returns {score: 0..1, correct: boolean, detail: {...}}.
  // `score` is partial credit; `correct` is the binary outcome used for calibration.
  function choice(c, answer) {
    const ok = answer === c.answer;
    return { score: ok ? 1 : 0, correct: ok, detail: {} };
  }

  function multi(c, answer) {
    const set = new Set(Array.isArray(answer) ? answer : []);
    const hits = c.multiAnswers.filter(i => set.has(i)).length;
    const ok = hits === c.multiAnswers.length && set.size === c.multiAnswers.length;
    return { score: hits / c.multiAnswers.length, correct: ok, detail: { hits } };
  }

  function estimate(c, value) {
    const e = c.estimate;
    const gap = Math.abs(value - e.target);
    const span = Math.max(1e-9, e.max - e.min);
    // Full credit inside the tolerance band, then linear decay to zero at half the scale.
    const score = gap <= e.tolerance ? 1 : clamp(1 - (gap - e.tolerance) / (span / 2), 0, 1);
    return { score, correct: gap <= e.tolerance, detail: { gap: Math.round(gap * 10) / 10 } };
  }

  // Probability forecast on a binary proposition. Brier score: 0 is perfect, 1 is worst.
  function forecast(c, p) {
    const prob = clamp(Number(p) / 100, 0, 1);
    const truth = c.forecast.truth ? 1 : 0;
    const brier = (prob - truth) ** 2;
    return { score: 1 - brier, correct: (prob >= 0.5) === (truth === 1) && prob !== 0.5, detail: { brier: Math.round(brier * 1000) / 1000 } };
  }

  // Ranking: share of item pairs placed in the evidence order (Kendall agreement).
  function rank(c, order) {
    const truth = c.rankAnswer;
    if (!Array.isArray(order) || order.length !== truth.length) return { score: 0, correct: false, detail: { pairs: 0 } };
    const pos = new Map(order.map((v, i) => [v, i]));
    let agree = 0, total = 0;
    for (let i = 0; i < truth.length; i++) for (let j = i + 1; j < truth.length; j++) {
      total++; if (pos.get(truth[i]) < pos.get(truth[j])) agree++;
    }
    const score = total ? agree / total : 0;
    return { score, correct: score === 1, detail: { agree, total } };
  }

  // Allocation: payoff of the user's split under the effects the study reported,
  // rescaled so that all-on-worst = 0 and all-on-best = 1.
  function allocate(c, shares) {
    const v = c.allocate.values;
    const total = (shares || []).reduce((a, b) => a + Number(b || 0), 0);
    if (!total) return { score: 0, correct: false, detail: {} };
    const ev = shares.reduce((a, s, i) => a + (Number(s || 0) / total) * v[i], 0);
    const lo = Math.min(...v), hi = Math.max(...v);
    const score = hi === lo ? 1 : clamp((ev - lo) / (hi - lo), 0, 1);
    return { score, correct: score >= (c.allocate.pass ?? 0.8), detail: { ev: Math.round(ev * 100) / 100 } };
  }

  // Delegation: one routing decision per task; score = share routed as the evidence suggests.
  function delegate(c, picks) {
    const tasks = c.delegate.tasks;
    const right = tasks.filter((t, i) => Array.isArray(picks) && picks[i] === t.answer).length;
    return { score: right / tasks.length, correct: right === tasks.length, detail: { right, total: tasks.length } };
  }

  const scorers = { choice, causal: choice, multi, estimate, forecast, rank, allocate, delegate };

  function score(c, response) {
    const fn = scorers[c.format];
    if (!fn) throw new Error('Unknown format ' + c.format);
    return fn(c, response);
  }

  // Is a response complete enough to lock?
  function ready(c, r) {
    switch (c.format) {
      case 'choice': case 'causal': return Number.isInteger(r) && r >= 0 && r < c.options.length;
      case 'multi': return Array.isArray(r) && r.length === c.multiAnswers.length;
      case 'estimate': return typeof r === 'number' && isFinite(r);
      case 'forecast': return typeof r === 'number' && r >= 0 && r <= 100;
      case 'rank': return Array.isArray(r) && r.length === c.rankAnswer.length && new Set(r).size === r.length;
      case 'allocate': return Array.isArray(r) && r.reduce((a, b) => a + b, 0) === c.allocate.total;
      case 'delegate': return Array.isArray(r) && r.length === c.delegate.tasks.length && r.every(x => Number.isInteger(x));
      default: return false;
    }
  }

  // The probability the player assigned to "my answer is right".
  // For forecasts the stated probability is about the claim, so it is used directly.
  function statedProbability(c, response, confidence) {
    return c.format === 'forecast' ? Number(response) : Number(confidence);
  }

  // Reliability table and Brier score over records [{p: 0..100, outcome: 0|1}].
  function calibration(records, bins = 5) {
    const rows = Array.from({ length: bins }, (_, i) => ({ lo: i * 100 / bins, hi: (i + 1) * 100 / bins, n: 0, sumP: 0, hits: 0 }));
    let brier = 0;
    for (const r of records) {
      const p = clamp(r.p, 0, 100);
      const i = Math.min(bins - 1, Math.floor(p / (100 / bins)));
      rows[i].n++; rows[i].sumP += p; rows[i].hits += r.outcome;
      brier += (p / 100 - r.outcome) ** 2;
    }
    return {
      n: records.length,
      brier: records.length ? brier / records.length : null,
      bins: rows.map(b => ({ lo: b.lo, hi: b.hi, n: b.n, meanP: b.n ? b.sumP / b.n : null, hitRate: b.n ? 100 * b.hits / b.n : null })),
      overconfidence: records.length ? (records.reduce((a, r) => a + r.p, 0) / records.length) - 100 * records.reduce((a, r) => a + r.outcome, 0) / records.length : null
    };
  }

  // A forecast converts to a calibration record about the claim; other formats about the answer.
  function toCalibrationRecord(c, rec) {
    if (c.format === 'forecast') return { p: rec.response, outcome: c.forecast.truth ? 1 : 0 };
    return { p: rec.confidence, outcome: rec.correct ? 1 : 0 };
  }

  const api = { score, ready, statedProbability, calibration, toCalibrationRecord, formats: Object.keys(scorers) };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.THVScore = api;
})(typeof window !== 'undefined' ? window : globalThis);
