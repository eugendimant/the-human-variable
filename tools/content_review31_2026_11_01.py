"""Review 31 content fixes. Idempotent; edits by text, never by index."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bp, ep = ROOT / 'src/bank.json', ROOT / 'src/evidence.json'
B = json.loads(bp.read_text()); E = json.loads(ep.read_text()); C = {c['id']: c for c in B['challenges']}

# M1: genai2 keys what the design supports (edited prompts matched the originals); the best-of-three figure is the authors' after-the-fact upper bound
c = C['genai2']
c['forecast']['claim'] = 'With an edited prompt alone, GPT-3 articles drew about as much agreement as the human-written originals.'
c['forecast']['truth'] = True
c['answerTitle'] = 'Edited prompts matched the originals: 46% against 47%'
c['explain'] = ('With an edited prompt, GPT-3 articles reached 46.4% agreement, level with the human-written originals: the difference was small and not statistically significant. '
                'Picking the best of three outputs per topic after the fact reached 52.7%, the authors’ upper bound for a propagandist who curates.')   # the unedited figure is axe04's answer
c['implication'] = 'Expect AI drafts from a well-built prompt to persuade about as well as a human writer’s; test several drafts on a small sample before scaling any one.'
for f in c['follow']:
    if f['q'] in ('Was prompt editing alone enough?', 'How did unedited GPT-3 do?'):
        f['q'] = 'What did the study measure?'; f['a'] = 'Whether each of 8,221 US respondents agreed or strongly agreed with an article’s thesis, against a group shown no article.'
    if f['q'] == 'How much did curation matter?':
        f['a'] = 'Picking, per topic, the draft that performed best reached 52.7%. That pick used the measured agreement itself, so an editor choosing before publication should expect less.'
ch = c['chart']
if 'AI article, curated' in ch['labels']:
    i = ch['labels'].index('AI article, curated'); ch['labels'][i] = 'AI article, edited prompt'; ch['values'][i] = 46.4
    ch['note'] = 'Share agreeing with the article’s main claim. Best of three drafts, picked after the fact: 52.7%.'
q = 'the difference between 46.4 and 47.4% was small and not statistically significant'
assert any(x.get('quote') == q for x in E['genai2'])

# m1: biz01's follow-up states its default without a number no stored quote carries
for f in C['biz01']['follow']:
    f['a'] = f['a'].replace('New hires were enrolled at a 3% contribution rate, invested entirely in the money market fund.', 'New hires were enrolled at the plan’s default contribution rate, invested entirely in the money market fund.')
# m2: a header from Dimant (2019) is not evidence for the 2022 paper
E['dimant-proximity-estimate'] = [x for x in E['dimant-proximity-estimate'] if x.get('quote') != 'Journal of Economic Psychology 73 (2019) 66–88']
# m11: statistics stay in the Source tab; the explanation says it in words
c = C['dimant-masks-forecast']; c['explain'] = c['explain'].replace('Forecasters overestimated the effects overall (z = 4.40, p < 0.001), most of all for Democrats.', 'Forecasters reliably overestimated the effects, most of all for Democrats.')
c = C['dimant-enforcers-rank']; c['explain'] = (c['explain'].replace(' when the bribe created inequity (P < 0.005)', ' when the bribe created inequity, a reliable difference')
    .replace(' when it restored equity (marginal, P = 0.074)', ' when it restored equity, a weaker difference').replace(' (77.8% vs 62.3%, P < 0.001)', ' (77.8% vs 62.3%)'))
# m12: axe01 asks what the study measured: which source customers prefer
C['axe01']['question'] = C['axe01']['question'].replace('For each recommendation, which source should customers see?', 'For each recommendation, which source will customers prefer?')

# audit 40: the unedited bar (43.5) is axe04's answer, so genai2's chart drops it; biz01's default follow-up asks what the paper does report
ch = C['genai2']['chart']
if 'AI article, unedited' in ch['labels']:
    i = ch['labels'].index('AI article, unedited'); ch['labels'].pop(i); v = ch['values'].pop(i)
    ch['highlight'] = ch['labels'].index('AI article, edited prompt')
for f in C['biz01']['follow']:
    if f['q'] == 'What was the default?':
        f['q'] = 'How fast did enrollment build?'; f['a'] = 'Under automatic enrollment, 86% of employees were in the 401(k) after 3 to 15 months, against 37% of those not enrolled automatically.'

bp.write_text(json.dumps(B, ensure_ascii=False, indent=1) + '\n'); ep.write_text(json.dumps(E, ensure_ascii=False, indent=1) + '\n')
print('review 31 content applied')
