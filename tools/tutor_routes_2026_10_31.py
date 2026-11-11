"""One routing table for the offline tutor, read by server/tutor.py and by the page (review 14, M1). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/bank.json'; bank = json.loads(p.read_text())
bank['tutorRoutes'] = {
 'note': 'Order matters. Both tutors (server/tutor.py curated, src/app.js curated) apply these in this order; tests/test_tutor.py checks every decision.',
 'stop': 'a an and are as at be been but by can could did do does for from had has have how i if in into is it its me more most my no not of on or our should so than that the their them then there these they this those to too up us was we were what when where which who why will with would you your about after also any because before being both each few just much many only other over same some such very study studies research researchers paper finding findings result results effect effects people thing find found show shows showed tell report reported'.split(),
 'generic': 'answer answers explain explanation number numbers mean means happen happened result outcome replicate replicated replication randomized randomised random sample design method control group size big large apply work hold today still test pilot conclusion conclude takeaway summary summarize key main point matter matters important relevant relevance implication implications manager managers lesson lessons tell more detail details five write better bill boss simple plain terms please could you'.split(),
 'suffixes': ['ations', 'ation', 'ments', 'ment', 'ions', 'ion', 'ing', 'ers', 'ed', 'es', 'er', 'e', 's', 'ly'],
 'syn': {'experienc skill': 'junior senior novic newer newcom veteran tenur rooki junio senio', 'less': 'reduct reduc decreas fell lower cut drop', 'rose': 'increas rais higher grew improv', 'ai': 'bot chatbot', 'alon': 'itself', 'cent': 'centr', 'physician': 'doctor doc', 'expert': 'expertis', 'fixed': 'fix repair remedi', 'persist': 'last', 'african': 'black', 'color': 'colour', 'behavior': 'behaviour', 'behavioral': 'behavioural', 'organiz': 'organis', 'favor': 'favour', 'labor': 'labour', 'program': 'programm', 'analyz': 'analys', 'optimiz': 'optimis', 'personaliz': 'personalis', 'recogniz': 'recognis'},   # British spellings meet US ones (review 26, M1)
 'routes': [
  ['offtopic', r'\b(poem|haiku|limerick|joke|weather|recipe|capital of|song|lyrics|horoscope|stock (tip|price|market)|bitcoin|crypto\w*|exchange rate|lottery|share price|world cup|super bowl|tax return|homework|movie|(^(please )?|(can|could|would|will) you (please )?|help me |i need you to )(write|draft) (me |us )?(my |a |an |the )?([a-z]+ ){0,2}(code|python|javascript|essay|cover letter|r[eé]sum[eé]|cv|email|speech|blog post|linkedin post|sales pitch|pitch|ad copy|script)|translate|bitcoin)\b'],
  ['action', r'\b(what should (i|we|my \w+( team)?|our \w+( team)?) do|what do (i|we) do|next steps?|monday( morning)?|what would you do|how (do|should|can) (i|we) (use|apply|act on) (this|it)|mean for (my|our|me|us)\b|for (my|our) (\w+ )?(team|company|firm|organi[sz]ation|business|unit|department|staff|people|managers?)\b|learn (for|from) (this|it|my|our))\b'],   # review 27, M1
  ['ethics', r'\b(ethic|fair|moral|should (we|i)(?! (believe|trust|buy|take))|(we|i) should (replace|fire|cut|lay off|hire fewer|downsize)|(we|i) (can|could) (cut|reduce|replace|lay off|shed) (our |the |\w+ )?(headcount|staff|jobs|people|workers|employees|team)|(can|could|should) (we|i) (cut|reduce|replace|lay off|shed) (our |the |\w+ )?(headcount|staff|jobs|people|workers|employees|team)|is it (ok|okay|right|wrong)|allowed|legal(?! (team|department|counsel|staff|work)))'],
  ['models', r'\b(which|what) (ai )?(models?|tools?|systems?|chatbots?|llms?)\b'],
  ['compare', r'\b(better|worse|more accurate|less accurate|smarter|outperform\w*|beat|beats)\b.*\bthan\b|\bas (good|effective|accurate|well|useful|fast) as\b|\b(more|fewer|less) \w+ than\b|\boutperform\w*\b|\bor not\b'],   # review 26, M1: "is GPT-4 better than doctors?", "do people hate the other side or not?"
  ['whatif', r'\bwhat if\b|\bwhat would (have )?happen\w*\b(?!\s+(in|for|at)\b)(?!\s+with\s+(\w+\s+)?(women|men|gender|older|younger|novices?|newcomers?|experienced|junior|senior|weaker|stronger|less skilled|(low|high)[- ]skill\w*)\b)|\bwould (it|this|that|they|the \w+) (have )?(work\w*|happen\w*|change\w*|differ\w*|be different) if\b'],
  ['control', r'\bcontrol (group|condition|arm|centers?|centres?|sites?|schools?|teams?|firms?|stores?|branches|participants)\b'],   # review 26, M1: "what happened in the control centres"
  ['detect', r'\b(could|can|did|do) (they|people|participants|users|customers|readers) (tell|detect|spot|notice|identify|recogni[sz]e)\b|\b(could|can|did|do|would) (they|people|participants|users|customers|readers|consumers|students|subjects|respondents|raters|workers) (know|reali[sz]e)\b.*\b(ai|gpt\S*|bot|chatbot|machine|model|algorithm|human|person)\b'],
  ['contest', r'\b(who is right|who.?s right|who is correct|which (one|side|study|paper) is right|who wins|(do|did) they (disagree|contradict))\b'],
  ['funding', r'\b(who (paid|pays|funded|financed|sponsored)|fund(ed|ing|ers?)\b|sponsor\w*)'],   # review 36/37: funding is not in the lab's summary
  ['raters', r'\bwho (rated|evaluated|judged|scored|graded|assessed|coded|reviewed)\b|\b(raters?|evaluators?|judges|coders|graders) (were|was|are)\b|\b(were|was|are) the (raters?|evaluators?|judges|coders|graders)\b'],
  ['scope', r'\bwhat does (the|this) (study|paper|experiment|research) cover\b|\bscope\b'],
  ['prereg', r'\bpre-?regist\w*'],
  ['replicated', r'\b(who|has|have|had|was|were|been|anyone|any)\b.{0,40}\breplicat(ed|ions?)\b|\bdid\b.{0,30}\breplicate\b|\breplicated (by|elsewhere|since|again)\b'],   # review 40: 'who replicated it' is not a question about scope
  ['peer', r'\bpeer[- ]?review\w*|\bwhere (was|is) (it|this|the study|the paper) published\b|\bwhich journal\b'],   # review 38, m2
  ['causal', r'\b(is|was) (it|this|that) (causal|a causal \w+)\b|\bcorrelation or causation\b|\bcausal or correlational\b'],
  ['authors', r'\b(who (did|ran|conducted|carried out|is behind|made|performed) (the|this) [\w-]+|who wrote|authors?|which paper|what paper|citation|cite|reference|published where|which journal)\b'],
  ['voluntary', r'\b(voluntary|volunteer\w*|randomly assigned|chose to|opt(ed)? in|self[- ]selected|vignette|real (bribe|job|firm|company)|real world|in the field|lab or field)\b'],
  ['stakes', r'\b(real money|paid|incentiv\w*|hypothetical|just a survey|for real|stakes)\b'],
  ['foresight', r'\b((experts?|economists?|forecasters?|anyone|people) (see|saw|predict\w*|expect\w*|anticipate\w*)|see (this|it) coming|predicted)\b'],
  ['population', r'\b(countries|which country|what country|where (was|were) (it|this|they)|american|americans|u\.?s\.? only|other countries|another country|culture|cultures|europe|asia|outside the us|elsewhere|just an? \w+ thing)\b'],
  ['task', r'\b(what (was|were) (the|their) (\w+ )?(task|game|procedure|experiment)|what did participants have to do)\b'],
  ['who', r'\b(who (was|were) (studied|in it|tested|the participants)|(were|was) (these|they|those|the participants|the subjects) (all )?(students|workers|professionals|managers|employees|experts|consumers|patients|real \w+)|participants?|how many (people|participants|subjects|workers|agents|guests|customers|patients|employees|students|clinicians|physicians|doctors|nurses|managers|firms|teams|forecasters|respondents|users|writers|developers|consultants|households|adults)|sample size|who took part|population)\b'],
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
# review 40: method words a manager asks about get one plain definition, the same in the page and on the server
bank['tutorRoutes']['glossary'] = [
 [r'p[- ]?values?', 'A p-value is the chance of seeing a result at least this far from zero if the true effect were zero. By convention, below 0.05 is called statistically significant. It is not the chance that the finding is true.'],
 [r'confidence intervals?|ci', 'A confidence interval is the range of effect sizes the data are compatible with. A 95% interval comes from a method that covers the true value in 95 of 100 repeated studies. A wide interval means an imprecise estimate.'],
 [r'(statistical(ly)? )?significan(t|ce)|statistical significance', 'Statistically significant means the result would be unlikely, by convention under a 5% chance, if the true effect were zero. It does not say the effect is large enough to matter.'],
 [r'(control|comparison) groups?|controls', 'A control group is the set of participants who do not get the intervention. Comparing them with those who do shows what the intervention changed.'],
 [r'randomi[sz]ed( controlled)?( field)? (trials?|experiments?|stud(y|ies))|rcts?|randomi[sz]ation|random assignment|randomi[sz]ed', 'In a randomized experiment, chance decides who gets the intervention, so the groups differ only by it on average. A difference in outcomes can then be read as the effect of the intervention.'],
 [r'pre-?regist(ered|ration|ering|er)', 'Preregistered means the authors recorded their hypotheses and analysis plan publicly before they collected the data, so the tests reported are the tests planned.'],
 [r'effect sizes?', 'An effect size says how big a difference is, and not only whether one exists: for example a change in percentage points, in percent, or in standard deviations.'],
 [r'percentage points?|pp', 'A percentage point is the plain difference between two percentages. Going from 10% to 15% is a rise of 5 percentage points, which is a 50% increase.'],
 [r'standard deviations?|sd', 'A standard deviation measures how spread out values are around their average. By a common convention, an effect of 0.2 standard deviations is small, 0.5 medium and 0.8 large.'],
 [r'field experiments?', 'A field experiment randomizes an intervention in a real setting, such as a workplace or a market, where people make their usual decisions.'],
 [r'(natural|quasi)[- ]experiments?', 'A natural experiment uses an event outside the researchers’ control, such as a policy change, that reached some people and not others for reasons unrelated to the outcome.'],
 [r'replications?|replicat(ed|e|ing)', 'A replication repeats a study with new data to check that the result holds. A finding that replicates in other samples deserves more weight than a single study.'],
 [r'sample sizes?|n', 'Sample size is the number of participants or observations. Larger samples give more precise estimates.'],
 [r'correlations?|causation|causality|correlation (and|vs\.?|versus) causation', 'Correlation means two things move together. Causation means that changing one changes the other. A randomized experiment is the standard way to tell the two apart.'],
 [r'meta-?analys[ie]s', 'A meta-analysis pools the results of many studies of the same question into one estimate, weighting the more precise studies more.'],
]
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('routes', len(bank['tutorRoutes']['common']))
