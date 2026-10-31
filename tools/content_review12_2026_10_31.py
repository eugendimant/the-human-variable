"""Fixes from independent review 12 (2026-10-31). Idempotent."""
import json, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
ev = json.loads((ROOT / 'src/evidence.json').read_text())
# M1: the towel-sign original is contested; biz04 already teaches the contest
if 'biz03' in C:
    bank['challenges'] = [c for c in bank['challenges'] if c['id'] != 'biz03']
    bank['retired'].append({'id': 'biz03', 'title': C['biz03']['title'], 'sources': C['biz03']['sources'],
                            'reason': 'Review 12: keyed the original towel-sign effect that biz04 shows failed to replicate; contested findings enter only as items about the contest.'})
    for p in bank['paths']: p['ids'] = [i for i in p['ids'] if i != 'biz03']
    ev.pop('biz03', None)
# minor 1: rival claims instead of absolute or null distractors
def swap(cid, old, new):
    if cid in C and 'options' in C[cid]: C[cid]['options'] = [new if o == old else o for o in C[cid]['options']]
swap('social13', 'No effect, though estimates were noisy', 'Large gains, concentrated in early rounds')
swap('social14', 'Neither side wanted more contact with the other', 'Each side said it feared open conflict')
swap('social15', 'Both showed up in feelings, neither in behavior', 'Love and hate showed mainly in feelings')
swap('axb10', 'No design changed agreement with wrong advice', "Showing the AI's confidence with each suggestion")
swap('bz01', 'They understated the lift every time', 'They understated the lift by a steady margin')
swap('bz12', 'No change: staff already knew peer pay', 'Below-median earners: more motivated to catch up')
swap('axe13', 'No effect on either product', 'Lowered spending intent for both products')
swap('genai3', 'Source and label make no difference', 'Human replies feel more heard, whatever the label')
swap('misperceived-norms-action', 'No change: beliefs moved, behavior did not', 'Fell slightly as husbands pushed back')
swap('misperceived-norms-action', 'Rose for husbands’ own job searches, not wives’', 'Fell slightly as husbands pushed back')
if 'Both worked equally well' in C['forecast-training']['options']:
    c = C['forecast-training']; keep = c['options'][c['answer']]
    c['options'] = [o for o in c['options'] if o != 'Both worked equally well']; c['answer'] = c['options'].index(keep)
# minor 6: duplicate and mirror distractors
c = C['bz14']
if 'Separate review, judged on more information' in c['options']:
    keep = c['options'][c['answer']]
    c['options'] = [o for o in c['options'] if o not in ('Separate review, judged on more information', 'Neither: both leaned on interview impressions')]
    c['answer'] = c['options'].index(keep)
c = C['dimant-contagion-multi']
c['options'] = [{'Anti-social individuals resisted their anti-social peers most': 'Pro-social individuals were the most easily swayed by their peers',
                 'Distant peers’ bad behavior spread most': 'Closeness made people copy good and bad choices equally'}.get(o, o) for o in c['options']]
# minor 7
swap('social20', 'Ask each person what they think colleagues believe', 'Ask each person how views are spread across colleagues')
# minor 3: sibling spoilers
C['civic-wallet-experts']['explain'] = 'Among 279 economists, 49% predicted a decrease and 29% an increase; among 299 laypeople, 18% predicted an increase.'
for f in C['misperceived-norms-support']['follow']:
    if f['q'] == 'Is this pattern seen elsewhere?':
        f['a'] = 'Yes. Gaps between private views and what people assume their peers think have been documented in many settings, which is why measuring the actual share matters.'
# minor 5: axe11 scored only 2 of 6 rank pairs; a pick-two states both tested contrasts
c = C['axe11']
if c['format'] == 'rank':
    for k in ('rankAnswer', 'rankTies', 'rankValues', 'rankLabel', 'permuted'): c.pop(k, None)
    c['format'] = 'multi'; c['question'] = 'Which two statements match what readers did?'
    c['options'] = ['True tweets by GPT-3 were judged correctly more often', 'False tweets by GPT-3 slipped past readers slightly more often',
                    'Readers took longer to judge GPT-3 tweets than human tweets', 'Readers could tell which tweets GPT-3 had written']
    c['multiAnswers'] = [0, 1]
# minor 8: scenes describe the real design, not an invented firm or meeting
SCENE = {
 'axe12': 'In a series of experiments, people evaluated workers who had done the same work, some of them described as getting help from AI.',
 'axb09': 'In experiments, people rated true and false headlines. Some carried an "AI-generated" label, including true headlines written by people.',
 'ai11': 'In experiments, people chose between an algorithm and a person, either to recommend a practical product or to judge a highly personal aesthetic preference.',
 'genai3': 'In an experiment, people described a personal situation and got a reply from Bing Chat or from a person. Some replies were labeled as AI-written, others as human.',
 'rollout2': 'In a staggered rollout of an AI assistant to 5,172 customer-support agents, the assistant also reached the most experienced, highest-skilled agents. A common expectation is that it lifts their work as much as newer agents’.',
 'axb13': 'A firm rolled out a generative-AI assistant that suggests replies to its customer-support agents, in stages across 5,172 agents. A common expectation is calmer customers.',
 'dimant-opioid-forecast': 'A program paid US veterans cash to return unused opioid pills. Researchers randomly added two reminder cards built on timely reminders, planning prompts and loss framing. A common expectation is that such cards pay for themselves.',
 'axe10': 'Researchers generated 10,320 marketing images with seven text-to-image models from 2,400 human-made images, then ran a live ad test with over 173,000 impressions. Many marketers expect a machine-made image can win.',
}
for k, s in SCENE.items(): C[k]['scene'] = s
# minor 4: an even split can be entered
C['axb08']['allocate']['step'] = 5
C['axf01']['allocate']['step'] = 1
# minor 11: evidence hygiene
ev['biz05'] = [q for q in ev.get('biz05', []) if 'extracted text shows' not in q['quote']]
ev['dimant-contagion-multi'] = [q for q in ev.get('dimant-contagion-multi', []) if q.get('source') != 'prox22']
ev['genai3'] = [q for q in ev.get('genai3', []) if q.get('source') != 'reif25']
for k, qs in ev.items():
    if not isinstance(qs, list) or k not in C: continue
    for q in qs:
        if not q.get('source'):
            if len(C[k]['sources']) == 1: q['source'] = C[k]['sources'][0]
            elif k == 'social10' and 'PubMed 20929725' in q.get('location', ''): q['source'] = 'team10'
(ROOT / 'src/evidence.json').write_text(json.dumps(ev, ensure_ascii=False, indent=1) + '\n')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
# minor 9: a few targets sit near the middle of their axes, so "avoid the middle" is not a strategy
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
# the per-item midpoint gate keeps every target at least 1.5 tolerances from the axis centre, so 0.41 is as central as a target can sit
for cid, mx in (('social12', 130), ('bz07', 90), ('axe06', 85), ('lies-in-disguise', 95), ('bz03', 34)): C[cid]['estimate']['max'] = mx
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
