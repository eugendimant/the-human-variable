"""Top-10 item 1: concept glossary for the no-key tutor. Plain textbook definitions of the named concepts (no study numbers, no new
claims about any paper). 'what is the endowment effect?' now gets its definition, because these terms are concepts, not measures
of the study on screen (tutorRoutes.glossaryThe). Idempotent. Run tools/tutor_golden.py after."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp = ROOT / 'src/bank.json'; B = json.loads(bp.read_text())
T = B['tutorRoutes']; G = T['glossary']
NEW = [
 (r'algorithm aversion', 'Algorithm aversion is the tendency to prefer a human judgment to an algorithm’s, often after seeing the algorithm make a mistake.'),
 (r'(the )?endowment effects?', 'The endowment effect is valuing something more once you own it. People ask more to give an item up than they would pay to get it.'),
 (r'loss aversion', 'Loss aversion is the tendency for a loss to weigh more than a gain of the same size.'),
 (r'choice overload', 'Choice overload is the idea that too many options make a decision harder. People may choose less, or put the decision off.'),
 (r'overconfidence', 'Overconfidence means being more sure of your answers than your accuracy justifies.'),
 (r'calibration|calibrated', 'Calibration compares how sure people say they are with how often they are right. A well-calibrated person who says 70% is right about 70% of the time.'),
 (r'anchoring|anchor(s|ing effect)?', 'Anchoring is when an early number pulls later estimates toward it, even when the number is irrelevant.'),
 (r'defaults?|default effects?', 'A default is the option that applies when a person makes no choice. Many people keep it, so the choice of default can change outcomes.'),
 (r'inertia|status quo bias', 'Inertia is staying with the current option when switching would be easy.'),
 (r'sunk[- ]costs?( fallacy)?', 'The sunk-cost fallacy is continuing something because of what you already spent, not because of what it will return.'),
 (r'planning fallacy', 'The planning fallacy is the habit of underestimating how long a task will take and what it will cost.'),
 (r'pluralistic ignorance', 'Pluralistic ignorance is when most people privately doubt a norm but wrongly believe that most others accept it.'),
 (r'(social |descriptive |injunctive )?norms?', 'A social norm is a shared rule about what people do (descriptive) or about what they should do (injunctive).'),
 (r'out[- ]?group hate|in[- ]?group love|in[- ]?group favou?ritism', 'Out-group hate is hostility or harm toward people outside your own group. In-group love is help for your own group. The two are different motives.'),
 (r'polari[sz]ation', 'Polarization is a growing distance between groups, such as parties, in beliefs, attitudes or trust.'),
 (r'motivated (beliefs?|reasoning)', 'Motivated beliefs are beliefs shaped by what a person wants to be true.'),
 (r'confirmation bias', 'Confirmation bias is favoring evidence that fits what you already believe.'),
 (r'framing( effects?)?', 'A framing effect is when the same facts, described differently, lead to different choices.'),
 (r'nudges?', 'A nudge changes how options are presented, not the options or their prices, to steer choices.'),
 (r'present bias', 'Present bias is giving too much weight to the near future against the later future.'),
 (r'deterrence', 'Deterrence is the idea that a sanction, or the threat of one, reduces unwanted behavior. Severity is how harsh the sanction is. Certainty is how likely it is to be applied.'),
 (r'spill ?overs?', 'A spillover is an effect that reaches people or outcomes beyond the ones targeted.'),
 (r'homophily', 'Homophily is the tendency to connect with people who are similar to you.'),
 (r'echo chambers?', 'An echo chamber is a setting where people mainly meet views like their own.'),
 (r'wisdom of (the )?crowds?', 'The wisdom of crowds is the finding that the average of many independent estimates is often more accurate than most single estimates.'),
 (r'conformity|social proof', 'Conformity is changing your behavior to match what others do.'),
 (r'reciprocity', 'Reciprocity is returning a good or a bad act in kind.'),
 (r'base rates?', 'A base rate is how common something is in the whole population, before any specific information.'),
 (r'placebo', 'A placebo is an inactive treatment given to a comparison group, so that the effect of the real treatment can be told apart from expectation.'),
 (r'human[- ]in[- ]the[- ]loop', 'Human-in-the-loop means a person reviews or approves what an automated system produces.'),
 (r'hallucinations?', 'A hallucination is a fluent but false statement produced by a language model.'),
 (r'(large language models?|llms?)', 'A large language model is a program trained on large amounts of text to predict and generate text.'),
 (r'a/?b tests?|split tests?', 'An A/B test shows two versions to different users at random and compares an outcome.'),
 (r'jagged frontier', 'The jagged frontier is the uneven line between tasks that AI does well and tasks it does poorly. It does not follow how hard a task looks to a person.'),
 (r'megastud(y|ies)', 'A megastudy tests many interventions at once on the same outcome, with one large sample.'),
 (r'naive diversification', 'Naive diversification is spreading choices evenly across the options on offer, whatever their merits.'),
 (r'proxy( variables?)?', 'A proxy stands in for something that is hard to measure, such as using cost as a stand-in for need.'),
 (r'attrition', 'Attrition is when participants drop out of a study before it ends. It matters when the people who leave differ from those who stay.'),
 (r'crowding out', 'Crowding out is when an outside reward or rule reduces a person’s own motivation to do the right thing.'),
 (r'intention[- ]to[- ]treat|itt', 'Intention to treat compares people by the group they were assigned to, whether or not they used the treatment.'),
 (r'opt[- ]out( defaults?)?|opt[- ]in( defaults?)?', 'An opt-out default enrolls people unless they say no. An opt-in default enrolls them only if they say yes.'),
 (r'algorithm appreciation', 'Algorithm appreciation is the tendency to rely on an algorithm’s advice more than on advice from a person.'),
 (r'celerity', 'Celerity is how quickly a sanction follows the act.'),
 (r'willingness to (pay|accept)', 'Willingness to pay is the most a person would pay for something. Willingness to accept is the least they would take to give it up.'),
 (r'heterogeneity|heterogeneous effects?', 'Heterogeneity means the effect differs between groups of people, not only on average.'),
 (r'selection bias', 'Selection bias is when the people in a study differ from the wider group in a way that affects the result.'),
 (r'external validity|generali[sz]ability', 'External validity is how far a result holds for other people, places and times than the ones studied.'),
]
have = {rx for rx, _ in G}
for rx, d in NEW:
    if rx not in have: G.append([rx, d])
G[:] = [g for g in G if g[0] not in (r'brier scores?', r'(a )?(tight|loose) (norms?|cultures?)', r'overconfidence|overprecision')]
T['glossaryThe'] = '|'.join(rx for rx, _ in NEW)
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
# the 'setting' route (where was it run, which firm or platform): added in the same pass, idempotent
B = json.loads(bp.read_text()); R = B['tutorRoutes']['routes']
if not any(n == 'setting' for n, _ in R):
    i = [n for n, _ in R].index('funding')
    R.insert(i + 1, ['setting', r"\bwhere (was|were|did) (it|this|the (study|experiment|trial|test|data))\b.*\b(run|conducted|done|carried out|take place|collected|happen)|\bwhich (country|city|university|school|state|company|firm|platform|marketplace|market|hotels?|website|app|bank|hospital)\b|\bwhat (country|city|platform|company|firm|marketplace) (was|were|is)\b|\bwhere (in the world|was this)\b"])
    bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
# more question families from review 53's misses (who was surveyed, is N percent a lot, low and high performers). Idempotent.
B = json.loads(bp.read_text()); R = B['tutorRoutes']['routes']
ADD = {
    'who': r'\bwho (was|were) (surveyed|interviewed|sampled|asked|tested|recruited|in (the|this) (\w+ )?(study|experiment|trial|sample|survey))\b',
    'size': r'\bis [\d.,]+ ?(percent|%|points?|pp)? (a lot|large|big|small|high|low|much|meaningful)\b',
    'subgroup': r'\b(low|high)[- ](and|or)[- ](low|high)\b|\b(top|bottom|best|worst|weak(est)?|strong(est)?) (performers?|workers|students|players)\b|\btop performers?\b',
}
for name, add in ADD.items():
    i = next(k for k, (n, _) in enumerate(R) if n == name)
    if add not in R[i][1]: R[i][1] += '|' + add
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')

# review 54: a duration question is not "stick with"; the setting answer reads the summary's own boundary
B = json.loads(bp.read_text()); R = B['tutorRoutes']['routes']
i = next(k for k, (n, _) in enumerate(R) if n == 'duration')
R[i][1] = R[i][1].replace('|stick)', '|(did|does|will) it stick|stick(s)? around)')
bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n')
