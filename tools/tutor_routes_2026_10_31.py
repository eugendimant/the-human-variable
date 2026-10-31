"""One routing table for the offline tutor, read by server/tutor.py and by the page (review 14, M1). Idempotent."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]; p = ROOT / 'src/bank.json'; bank = json.loads(p.read_text())
bank['tutorRoutes'] = {
 'note': 'Order matters. Both tutors (server/tutor.py curated, src/app.js curated) apply these in this order; tests/test_tutor.py checks every decision.',
 'stop': 'a an and are as at be been but by can could did do does for from had has have how i if in into is it its me more most my no not of on or our should so than that the their them then there these they this those to too up us was we were what when where which who why will with would you your about after also any because before being both each few just much many only other over same some such very study studies research researchers paper finding findings result results effect effects people thing find found show shows showed tell report reported'.split(),
 'generic': 'answer answers explain explanation number numbers mean means happen happened result outcome replicate replicated replication randomized randomised random sample design method control group size big large apply work hold today still test pilot conclusion conclude takeaway summary summarize key main point matter matters important relevant relevance implication implications manager managers lesson lessons tell more detail details'.split(),
 'suffixes': ['ations', 'ation', 'ments', 'ment', 'ions', 'ion', 'ing', 'ers', 'ed', 'es', 'er', 'e', 's', 'ly'],
 'syn': {'experienc skill': 'junior senior novic newer newcom veteran tenur rooki junio senio', 'less': 'reduct reduc decreas fell lower cut drop', 'rose': 'increas rais higher grew improv'},
 'routes': [
  ['ethics', r'\b(ethic|fair|moral|should (we|i)|is it (ok|okay|right|wrong)|allowed|legal)'],
  ['subgroup', r'\b(junior|senior|novice|newcomer|experienced|who (benefit|gain)|which (workers|employees|people|staff|agents)|subgroup)'],
  ['design', r'\b(how (was|were|did)|design|method|ran|sample|participants|conducted|setup|set up|randomi[sz]\w*|control group)\b'],
  ['pilot', r'\b(test (this|it)|pilot|in (my|our) (company|team|firm|organi[sz]ation)|roll ?out|measure (it|this))\b'],
  ['size', r'\b(big|size|large|how much|practice|magnitude)\b'],
  ['transfer', r'\b(today|still|hold|generali[sz]e|apply|transfer|work (for|in)|everywhere|replicat\w*)']],
 'subgroupFollow': r'^(who\b|which (workers|agents|employees|people|consultants|staff|groups?)\b)',
}
p.write_text(json.dumps(bank, ensure_ascii=False, indent=1) + '\n'); print('routes')
