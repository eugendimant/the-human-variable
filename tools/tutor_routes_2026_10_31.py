"""One routing table for the offline tutor, read by server/tutor.py and by the page (review 14, M1). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/bank.json'; bank = json.loads(p.read_text())
bank['tutorRoutes'] = {
 'note': 'Order matters. Both tutors (server/tutor.py curated, src/app.js curated) apply these in this order; tests/test_tutor.py checks every decision.',
 'stop': 'a an and are as at be been but by can could did do does for from had has have how i if in into is it its me more most my no not of on or our should so than that the their them then there these they this those to too up us was we were what when where which who why will with would you your about after also any because before being both each few just much many only other over same some such very study studies research researchers paper finding findings result results effect effects people thing find found show shows showed tell report reported'.split(),
 'generic': 'answer answers explain explanation number numbers mean means happen happened result outcome replicate replicated replication randomized randomised random sample design method control group size big large apply work hold today still test pilot conclusion conclude takeaway summary summarize key main point matter matters important relevant relevance implication implications manager managers lesson lessons tell more detail details five write better bill boss simple plain terms please could you'.split(),
 'suffixes': ['ations', 'ation', 'ments', 'ment', 'ions', 'ion', 'ing', 'ers', 'ed', 'es', 'er', 'e', 's', 'ly'],
 'syn': {'experienc skill': 'junior senior novic newer newcom veteran tenur rooki junio senio', 'less': 'reduct reduc decreas fell lower cut drop', 'rose': 'increas rais higher grew improv'},
 'routes': [
  ['offtopic', r'\b(poem|haiku|limerick|joke|weather|recipe|capital of|song|lyrics|horoscope|stock (tip|price)|share price|world cup|super bowl|tax return|homework|movie|write (me )?(code|python|javascript|an essay)|translate|bitcoin)\b'],
  ['action', r'\b(what should (i|we) do|what do (i|we) do|next steps?|monday( morning)?|what would you do|how (do|should|can) (i|we) (use|apply|act on) (this|it))\b'],
  ['ethics', r'\b(ethic|fair|moral|should (we|i)|is it (ok|okay|right|wrong)|allowed|legal)'],
  ['models', r'\b(which|what) (ai )?(models?|tools?|systems?|chatbots?|llms?)\b'],
  ['who', r'\b(who (was|were) (studied|in it|tested|the participants)|participants?|how many (people|participants|subjects|workers|agents)|sample size|who took part|population)\b'],
  ['catch', r'\b(catch|backfire|downside|drawback|limit\w*|risk|caveat|fail\w*|weakness|criticis\w*|question(ed)? this|later work)\b'],
  ['summary', r'\b(summar\w*|explain|eli5|like i.?m (five|5)|like i am (five|5)|my boss|brief(ly)?|tl;?dr|in plain|simple terms|key (point|takeaway)|bottom line)\b'],
  ['duration', r'\b(how long|last(ed)?|persist\w*|fade\w*|long[- ]term|over time|stick)\b'],
  ['subgroup', r'\b(junior|senior|novice|newcomer|experienced|who (benefit|gain)|which (workers|employees|people|staff|agents)|subgroup)'],
  ['design', r'\b(how (was|were|did)|design|method|ran|sample|participants|conducted|setup|set up|randomi[sz]\w*|control group)\b'],
  ['pilot', r'\b(test (this|it)|pilot|in (my|our) (company|team|firm|organi[sz]ation)|roll ?out|measure (it|this))\b'],
  ['size', r'\b(big|size|large|how much|practice|magnitude)\b'],
  ['transfer', r'\b(today|still|hold|generali[sz]e|apply|transfer|work (for|in)|everywhere|replicat\w*)']],
 'subgroupFollow': r'^(who\b.*\b(gain|gained|benefit|benefited|most|least|helped|lost)|which (workers|agents|employees|people|consultants|staff|groups?)\b)',
}
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('routes')
