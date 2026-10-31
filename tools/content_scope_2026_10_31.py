"""Restate the scope of Eugen Dimant's studies as what each study covers (RULE 0: never downplay the contribution)."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
bank = json.loads((ROOT / 'src/bank.json').read_text()); C = {c['id']: c for c in bank['challenges']}
NEW = {
 'social01': 'Incentivized coordination games with a representative US sample, varying the shape of the norm while holding its average fixed.',
 'social03': 'Coordination games in which the spread of the norm was set by design; whether variety helps depends on the task.',
 'social07': 'A norm-drawing method applied to seven policy issues with about 1,000 US respondents.',
 'social15': 'Five preregistered studies with more than 8,600 participants on US political identity.',
 'social16': 'The tested nudges raised prosocial behavior overall, and the gap between Trump supporters and opponents remained.',
 'social20': 'A measurement method for tight, loose and polarized norms built on incentivized elicitation of each person’s beliefs.',
 'dimant-requiem-forecast': 'One-line messages before a die-reporting game with undetectable lies, in a high-powered preregistered study.',
 'dimant-notalie-causal': 'Incentivized experiment in which lying paid money and beliefs concerned the other participants.',
 'dimant-proximity-estimate': 'Repeated giving game with Penn students; proximity was a minimal shared-identity cue.',
 'dimant-contagion-multi': 'Experiment with pro- and anti-social choices and peers who varied in social proximity.',
 'dimant-deviant-choice': 'Lab trust game combining a weak penalty with norm messages at two levels of compliance cost.',
 'dimant-enforcers-rank': 'Bribery vignette with 225 US adults, alongside a main study with monetary punishments.',
 'dimant-observability-choice': 'Charity-giving experiments in which participants observed each other’s choices.',
 'dimant-motivated-estimate': 'US participants choosing information sources in an undetectable lying game, with partisan identity as the group cue.',
 'dimant-conspiracy-choice': 'A pilot and three preregistered experiments with a simulated social-media sharing task.',
 'dimant-hate-choice': 'Incentivized experiments on US polarization around Donald Trump, compared with other social identities.',
 'dimant-polarizednorms-choice': 'Strategic coordination game with a representative US sample, with norm distributions set by design.',
}
for k, v in NEW.items(): C[k]['boundary'] = v
(ROOT / 'src/bank.json').write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print(len(NEW), 'scope lines')
