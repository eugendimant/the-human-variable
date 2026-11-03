"""One routing table for the offline tutor, read by server/tutor.py and by the page (review 14, M1). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/bank.json'; bank = json.loads(p.read_text())
bank['tutorRoutes'] = {
 'note': 'Order matters. Both tutors (server/tutor.py curated, src/app.js curated) apply these in this order; tests/test_tutor.py checks every decision.',
 'stop': 'a an and are as at be been but by can could did do does for from had has have how i if in into is it its me more most my no not of on or our should so than that the their them then there these they this those to too up us was we were what when where which who why will with would you your about after also any because before being both each few just much many only other over same some such very study studies research researchers paper finding findings result results effect effects people thing find found show shows showed tell report reported'.split(),
 'generic': 'answer answers explain explanation number numbers mean means happen happened result outcome replicate replicated replication randomized randomised random sample design method control group size big large apply work hold today still test pilot conclusion conclude takeaway summary summarize key main point matter matters important relevant relevance implication implications manager managers lesson lessons tell more detail details five write better bill boss simple plain terms please could you'.split(),
 'suffixes': ['ations', 'ation', 'ments', 'ment', 'ions', 'ion', 'ing', 'ers', 'ed', 'es', 'er', 'e', 's', 'ly'],
 'syn': {'experienc skill': 'junior senior novic newer newcom veteran tenur rooki junio senio', 'less': 'reduct reduc decreas fell lower cut drop', 'rose': 'increas rais higher grew improv', 'ai': 'bot chatbot', 'alon': 'itself', 'cent': 'centr', 'physician': 'doctor doc', 'african': 'black', 'color': 'colour', 'behavior': 'behaviour', 'behavioral': 'behavioural', 'organiz': 'organis', 'favor': 'favour', 'labor': 'labour', 'program': 'programm', 'analyz': 'analys', 'optimiz': 'optimis', 'personaliz': 'personalis', 'recogniz': 'recognis'},   # British spellings meet US ones (review 26, M1)
 'routes': [
  ['offtopic', r'\b(poem|haiku|limerick|joke|weather|recipe|capital of|song|lyrics|horoscope|stock (tip|price)|share price|world cup|super bowl|tax return|homework|movie|(^(please )?|(can|could|would|will) you (please )?|help me |i need you to )(write|draft) (me |us )?(my |a |an |the )?([a-z]+ ){0,2}(code|python|javascript|essay|cover letter|r[eé]sum[eé]|cv|email|speech|blog post|linkedin post|sales pitch|pitch|ad copy|script)|translate|bitcoin)\b'],
  ['action', r'\b(what should (i|we|my \w+( team)?|our \w+( team)?) do|what do (i|we) do|next steps?|monday( morning)?|what would you do|how (do|should|can) (i|we) (use|apply|act on) (this|it)|mean for (my|our|me|us)\b|for (my|our) (\w+ )?(team|company|firm|organi[sz]ation|business|unit|department|staff|people|managers?)\b|learn (for|from) (this|it|my|our))\b'],   # review 27, M1
  ['ethics', r'\b(ethic|fair|moral|should (we|i)(?! (believe|trust|buy|take))|(we|i) should (replace|fire|cut|lay off|hire fewer|downsize)|(we|i) (can|could) (cut|reduce|replace|lay off|shed) (our |the |\w+ )?(headcount|staff|jobs|people|workers|employees|team)|headcount|is it (ok|okay|right|wrong)|allowed|legal(?! (team|department|counsel|staff|work)))'],
  ['models', r'\b(which|what) (ai )?(models?|tools?|systems?|chatbots?|llms?)\b'],
  ['compare', r'\b(better|worse|more accurate|less accurate|smarter|outperform\w*|beat|beats)\b.*\bthan\b|\bas (good|effective|accurate|well|useful|fast) as\b|\b(more|fewer|less) \w+ than\b|\boutperform\w*\b|\bor not\b'],   # review 26, M1: "is GPT-4 better than doctors?", "do people hate the other side or not?"
  ['whatif', r'\bwhat if\b|\bwhat would (have )?happen\w*\b(?!\s+(in|for|at)\b)(?!\s+with\s+(\w+\s+)?(women|men|gender|older|younger|novices?|newcomers?|experienced|junior|senior|weaker|stronger|less skilled|(low|high)[- ]skill\w*)\b)|\bwould (it|this|that|they|the \w+) (have )?(work\w*|happen\w*|change\w*|differ\w*|be different) if\b'],
  ['control', r'\bcontrol (group|condition|arm|centers?|centres?|sites?|schools?|teams?|firms?|stores?|branches|participants)\b'],   # review 26, M1: "what happened in the control centres"
  ['detect', r'\b(could|can|did|do) (they|people|participants|users|customers|readers) (tell|detect|spot|notice|identify|recogni[sz]e)\b|\b(could|can|did|do|would) (they|people|participants|users|customers|readers|consumers|students|subjects|respondents|raters|workers) (know|reali[sz]e)\b.*\b(ai|gpt\S*|bot|chatbot|machine|model|algorithm|human|person)\b'],
  ['contest', r'\b(who is right|who.?s right|who is correct|which (one|side|study|paper) is right|who wins|(do|did) they (disagree|contradict))\b'],
  ['authors', r'\b(who wrote|authors?|which paper|what paper|citation|cite|reference|published where|which journal)\b'],
  ['voluntary', r'\b(voluntary|volunteer\w*|randomly assigned|chose to|opt(ed)? in|self[- ]selected|vignette|real (bribe|job|firm|company)|real world|in the field|lab or field)\b'],
  ['stakes', r'\b(real money|paid|incentiv\w*|hypothetical|just a survey|for real|stakes)\b'],
  ['foresight', r'\b((experts?|economists?|forecasters?|anyone|people) (see|saw|predict\w*|expect\w*|anticipate\w*)|see (this|it) coming|predicted)\b'],
  ['population', r'\b(countries|which country|what country|where (was|were) (it|this|they)|american|americans|u\.?s\.? only|other countries|another country|culture|cultures|europe|asia|outside the us|elsewhere|just an? \w+ thing)\b'],
  ['task', r'\b(what (was|were) (the|their) (\w+ )?(task|game|procedure|experiment)|what did participants have to do)\b'],
  ['who', r'\b(who (was|were) (studied|in it|tested|the participants)|(were|was) (these|they|those|the participants|the subjects) (all )?(students|workers|professionals|managers|employees|experts|consumers|patients|real \w+)|participants?|how many (people|participants|subjects|workers|agents|guests|customers|patients|employees|students)|sample size|who took part|population)\b'],
  ['catch', r'\b(catch|backfire|downside|drawback|limit\w*|risk|caveat|fail\w*|weakness|criticis\w*|question(ed)? this|later work)\b'],
  ['summary', r'\b(what did (the|this|they|it) (\w+[- ]?)?(study |paper |analysis )?(find|show)|summar\w*|explain|eli5|like i.?m (five|5)|like i am (five|5)|my boss|brief(ly)?|tl;?dr|in plain|simple terms|key (point|takeaway)|bottom line|main (results?|findings?)|in (one|a) sentence|one[- ]liner|define|definition of|(does|did|do) (it|this|that|the [\w ]{1,30}) work(?=\W*$)|did it work|what (did|was) (it|they) find|what was found)\b'],
  ['duration', r'\b(how long|last(ed)?|persist\w*|fade\w*|long[- ]term|over time|stick)\b'],
  ['subgroup', r'\b(already (good|skilled|strong|experienced)|weaker|stronger|less skilled|(low|high)[- ]skill\w*|good writers|junior|senior|novices?|newcomers?|experienced|who (benefit|gain)|which (workers|employees|people|staff|agents)|subgroup|women|men|gender|older|younger|age group|differently)\b'],
  ['numbers', r'\b(how many|what share|what percent\w*|what proportion|what fraction|how much (more|less|higher|lower))\b'],   # review 28: a count or share the explanation states
  ['signif', r'\b(significan\w*|statistically|by chance|just noise|p[- ]?value)\b'],
  ['meaning', r'\b(what does (the )?(word |term )?[\'\"]?(\w+)[\'\"]? mean|what is meant by|what do (they|you) mean by)\b'],
  ['why', r'(^why\b|\bwhy (would|does|did|do|is|are|was|were)\b)'],
  ['design', r'\b(how (was|were|did)|design|method|ran|sample|participants|conducted|setup|set up|randomi[sz]\w*|control group)\b'],
  ['pilot', r'\b((check|test|audit|evaluate|assess) (my|our)( own)?|my own|our own|test (this|it)|pilot|in (my|our) (company|team|firm|organi[sz]ation)|roll ?out|measure (it|this))\b'],
  ['size', r'\b(big|size|large|how much|practice|magnitude)\b'],
  ['define', r'^what(.s| is) (an? |the )?(\w+)\??$'],
  ['transfer', r'\b(today|still|hold|generali[sz]e|apply|transfer|work (for|in)|everywhere|replicat\w*|believe|trust (it|this|a|the)|lab (game|study|experiment)|artificial)']],
 'filler': ['okay', 'also', 'hmm', 'well', 'quick', 'question', 'please', 'tell', 'know', 'like', 'want', 'just', 'actually', 'really', 'curious', 'wonder', 'wondering', 'whether', 'study', 'this'],   # words that do not change what a Yes or No answers (review 26)
 'subgroupFollow': r'^(who\b.*\b(gain|gained|benefit|benefited|most|least|helped|lost)|which (workers|agents|employees|people|consultants|staff|groups?)\b)',
}
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n')
# review 20: a word that appears in the follow-up questions of three or more decisions is not distinctive enough to pick a follow-up by itself
import collections, importlib, sys
sys.path.insert(0, str(p.parents[1])); from server import tutor; importlib.reload(tutor)
df = collections.Counter()
for c in bank['challenges']:
    if c.get('retired'): continue
    df.update({w for f in c.get('follow', []) for w in tutor.tokens(f['q'])})
manual = [tutor.stem(w) for w in 'effect effects study studies finding findings paper research people data work worked works'.split()]
bank['tutorRoutes']['wordSurnames'] = ['bail', 'bloom', 'card', 'list', 'west', 'powers', 'grove', 'miller', 'rand', 'tong', 'fang', 'shea', 'rouse', 'ross', 'healy']   # surnames that are also English words: they name a study only when capitalised (review 25, M2)
bank['tutorRoutes']['common'] = sorted({w for w, n in df.items() if n >= 3} | set(manual))
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('routes', len(bank['tutorRoutes']['common']))
