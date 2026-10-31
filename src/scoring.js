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
    // Full credit inside the tolerance band, then linear decay to zero at two tolerances from the target.
    const score = gap <= e.tolerance ? 1 : clamp(1 - (gap - e.tolerance) / e.tolerance, 0, 1);
    return { score, correct: gap <= e.tolerance, detail: { gap: Math.round(gap * 10) / 10 } };
  }

  // Probability forecast on a binary proposition. Brier score: 0 is perfect, 1 is worst.
  function forecast(c, p) {
    const prob = clamp(Number(p) / 100, 0, 1);
    const truth = c.forecast.truth ? 1 : 0;
    const brier = (prob - truth) ** 2;
    // Proper rule (a linear transform of Brier): 100 for a confident correct call, 50 for saying 50%,
    // and down to -100 for a confident wrong call. Unclamped, so reporting your true belief is always best.
    return { score: 1 - 2 * brier, correct: (prob > 0.5) === (truth === 1) && prob !== 0.5, detail: { brier: Math.round(brier * 1000) / 1000 } };
  }

  // Ranking: share of item pairs placed in the evidence order (Kendall agreement).
  function rank(c, order) {
    const truth = c.rankAnswer;
    if (!Array.isArray(order) || order.length !== truth.length) return { score: 0, correct: false, detail: { pairs: 0 } };
    const pos = new Map(order.map((v, i) => [v, i]));
    // Pairs the study could not tell apart (rankTies) are not scored.
    const tied = (a, b) => (c.rankTies || []).some(g => g.includes(a) && g.includes(b));
    let agree = 0, total = 0;
    for (let i = 0; i < truth.length; i++) for (let j = i + 1; j < truth.length; j++) {
      if (tied(truth[i], truth[j])) continue;
      total++; if (pos.get(truth[i]) < pos.get(truth[j])) agree++;
    }
    const score = total ? agree / total : 0;
    return { score, correct: score === 1, detail: { agree, total } };
  }

  // Allocation as a probability split over "which option worked best" (a proper rule, like the forecast score).
  // Target: equal shares on the best arm(s); score = 1 - sum of squared gaps, from -1 (all on a wrong arm) to 1.
  // Spreading points is the best strategy when you are unsure, and all-in pays only when you are sure.
  function allocate(c, shares) {
    const v = c.allocate.values, hi = Math.max(...v), best = v.map((x, i) => (c.allocate.best ? c.allocate.best.includes(i) : x === hi) ? 1 : 0), nb = best.reduce((a, b) => a + b, 0);  // allocate.best: arms the study did not separate
    const total = (shares || []).reduce((a, b) => a + Number(b || 0), 0);
    if (!total) return { score: 0, correct: false, detail: {} };
    const p = shares.map(s => Number(s || 0) / total);
    const score = 1 - p.reduce((a, x, i) => a + (x - best[i] / nb) ** 2, 0);
    const top = Math.max(...p);
    return { score, correct: p.every((x, i) => x !== top || best[i]), /* every top-weighted option is a best one */ detail: { onBest: Math.round(100 * p.reduce((a, x, i) => a + (best[i] ? x : 0), 0)) } };
  }

  // Delegation: one routing decision per task; score = share routed as the evidence suggests.
  function delegate(c, picks) {
    const tasks = c.delegate.tasks;
    // t.also lists routes the study found equally good (no significant difference), which also count.
    const right = tasks.filter((t, i) => Array.isArray(picks) && (picks[i] === t.answer || (t.also || []).includes(picks[i]))).length;
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
      case 'multi': return Array.isArray(r) && r.length === (c.multiAnswers ? c.multiAnswers.length : c.pick || 2);
      case 'estimate': return typeof r === 'number' && isFinite(r);
      case 'forecast': return typeof r === 'number' && r >= 0 && r <= 100;
      case 'rank': return Array.isArray(r) && r.length === (c.rankAnswer ? c.rankAnswer.length : c.options.length) && new Set(r).size === r.length;
      case 'allocate': return Array.isArray(r) && r.reduce((a, b) => a + b, 0) === c.allocate.total;
      case 'delegate': return Array.isArray(r) && r.length === c.delegate.tasks.length && r.every(x => Number.isInteger(x));
      default: return false;
    }
  }

  // The probability the player assigned to "my answer is right".
  // For forecasts the stated probability is about the claim, so it is used directly.
  function statedProbability(c, response, confidence) {
    if (c.format === 'forecast') return Number(response);
    if (c.format === 'allocate') { const t = response.reduce((a, b) => a + b, 0) || 1; return 100 * Math.max(...response) / t }
    return Number(confidence);
  }

  // Reliability table and Brier score over records [{p: 0..100, outcome: 0|1}].
  function calibration(records, bins = 5) {
    const rows = Array.from({ length: bins }, (_, i) => ({ lo: i * 100 / bins, hi: (i + 1) * 100 / bins, n: 0, sumP: 0, hits: 0 }));
    let brier = 0;
    for (const r of records) {
      if (!r) continue;
      const p = clamp(r.p, 0, 100);
      const i = Math.min(bins - 1, Math.floor(p / (100 / bins)));
      rows[i].n++; rows[i].sumP += p; rows[i].hits += r.outcome;
      brier += (p / 100 - r.outcome) ** 2;
    }
    return {
      n: records.filter(Boolean).length,
      brier: records.filter(Boolean).length ? brier / records.filter(Boolean).length : null,
      bins: rows.map(b => ({ lo: b.lo, hi: b.hi, n: b.n, meanP: b.n ? b.sumP / b.n : null, hitRate: b.n ? 100 * b.hits / b.n : null })),
      overconfidence: (rs => rs.length ? rs.reduce((a, r) => a + r.p, 0) / rs.length - 100 * rs.reduce((a, r) => a + r.outcome, 0) / rs.length : null)(records.filter(Boolean))
    };
  }

  // A forecast converts to a calibration record about the claim; other formats about the answer.
  function toCalibrationRecord(c, rec) {
    // A forecast is folded to the side the player leaned to: 10% on a false claim is a 90% call that was right.
    if ((c && c.format === 'forecast') || rec.format === 'forecast') {
      const p = Number(rec.response), truth = rec.outcome ?? (c.forecast.truth ? 1 : 0);
      if (p === 50) return null;
      return { p: Math.max(p, 100 - p), outcome: (p > 50) === (truth === 1) ? 1 : 0 };
    }
    // An allocation states the chance that the top-weighted option is the best one.
    if (rec.format === 'allocate' && Array.isArray(rec.response)) return { p: statedProbability({ format: 'allocate' }, rec.response), outcome: rec.correct ? 1 : 0 };
    return rec.confidence === null || rec.confidence === undefined ? null : { p: rec.confidence, outcome: rec.correct ? 1 : 0 };
  }

  // Skill above guessing: 0 for what a no-information strategy earns on this format, 1 for a perfect call.
  // Makes scores comparable across formats (hedging a forecast at 50% earns 0.5 raw but 0 skill).
  function baseline(c) {
    switch (c.format) {
      case 'forecast': return 0.5;
      case 'rank': return 0.5;
      case 'choice': case 'causal': return 1 / c.options.length;
      case 'multi': { const k = (c.multiAnswers || []).length || c.pick || 2; return k / c.options.length }
      case 'delegate': return 1 / c.delegate.choices.length;
      case 'allocate': { const n = c.options.length, nb = (c.allocate && c.allocate.best && c.allocate.best.length) || 1; return 1 - 1 / nb + 1 / n }   // an even split
      default: return 0;   // estimates: the midpoint and constant guesses are capped by content gates
    }
  }
  function skill(c, raw) { const b = baseline(c); return b >= 1 ? 0 : (raw - b) / (1 - b) }

  const api = { score, ready, baseline, skill, statedProbability, calibration, toCalibrationRecord, formats: Object.keys(scorers) };
  if (typeof module !== 'undefined' && module.exports) module.exports = api; else root.THVScore = api;
})(typeof window !== 'undefined' ? window : globalThis);
