"""Review 2, M9: remove the length cue (correct answer longest) and absolute-word distractors."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
E = {
 ('ai09', 2): 'The model, more often than before the error',
 ('social14', 0): 'Own side fears rejection; other lacks interest',
 ('social14', 1): 'Both sides said they mainly feared being rejected',
 ('social14', 2): 'Neither side wanted more contact with the other',
 ('ai11', 1): 'Recommending a product for its practical use',
 ('biz02', 0): 'They had each worked out that it was the best plan',
 ('biz03', 0): 'The standard conservation sign',
 ('biz07', 2): 'Assigning a new owner to the process',
 ('social04', 2): 'Peers were less comfortable with drinking than they were',
 ('social07', 0): 'Near-uniform views held by members of each party',
 ('social13', 2): 'Women less likely to advance past auditions',
 ('biz05', 2): 'Below-average households cut their use further still',
 ('social01', 2): 'The average alone predicted how most people chose',
 ('social16', 2): 'The nudges closed the partisan gap on most measures',
 ('tax-letter-norms', 2): 'Injunctive norms beat descriptive norms in the letters',
 ('dimant-contagion-multi', 4): 'Anti-social individuals resisted their anti-social peers most',
 ('axe14', 3): 'Disclosed bots seemed more knowledgeable to customers',
 ('axe12', 3): 'The penalty came mainly from managers who use AI',
 ('social20', 0): 'Look at the spread of views, not the mean',
 ('social20', 2): 'Ask each team’s manager to describe the norm',
 ('dimant-deviant-choice', 3): 'Penalty plus "most others comply," with costly compliance',
 ('dimant-hate-choice', 0): 'Expecting the other side not to cooperate',
 ('axe13', 3): 'Raised spending intent for the sneakers, not the trip',
 ('genai3', 0): 'AI replies feel colder, with or without a label',
 ('genai3', 2): 'Labeling replies as AI raises trust and feeling heard',
 ('social15', 2): 'Both showed up in feelings, neither in behavior',
 ('overconfidence-hard-task', 0): 'Overestimate own score, and think they beat peers',
 ('dimant-polarizednorms-choice', 3): 'Acted as they did when norms were tight',
 ('axb11', 4): 'The algorithm beat strangers but not friends',
 ('false-news-spread', 3): 'The gap appeared for political stories, not others',
 ('dimant-contagion-multi', 3): 'Closeness spread good behavior more than bad',
 ('dimant-conspiracy-choice', 3): 'Belief: people shared what they thought was true',
}
for (cid, i), t in E.items(): C[cid]['options'][i] = t
C['bz10']['title'] = 'More options on the shelf'
for c in bank['challenges']:
    if c.get('question', '').startswith('Which TWO'): c['question'] = c['question'].replace('Which TWO', 'Which two')
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('ok')
