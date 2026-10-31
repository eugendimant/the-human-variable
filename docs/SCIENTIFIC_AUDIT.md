# Scientific audit

Generated from `src/bank.json` by `tools/make_audit_doc.py`. Audit date: 2026-10-31.

## Standard

- Scored answers rest only on peer-reviewed journal articles (no working papers or preprints).
- Every source: metadata matched against its Crossref record (authors, year of the version of record, title, journal, volume, pages).
- Every number used in a decision appears in text the auditor read. The record states what was read: the full text or the published abstract. Where a number came from an earlier version of the same paper, that is stated.
- Contested findings appear only as items about the contest (for example, choice overload and the sign-first replication). A source whose central claim is disputed and has no such item is quarantined from scored play.
- Scenes are teaching adaptations; they describe the real design (population, task, setting).

## Summary

- Decisions in scored play: 112 (formats: choice 37, estimate 25, forecast 19, multi 11, rank 7, causal 6, delegate 5, allocate 2).
- Sources: 99 (45 checked against full text, 53 against the published abstract, 1 quarantined).
- Corrections applied to the 28 carried-forward sources and their 60 decisions: 25 logged changes (`docs/audit/corrections_2026-10-31.json`).
- Decisions retired with reasons: 29 (listed below).
- Track balance: AI × Business 45, Culture & Society 31, Business 29, Judgment 7.

## Sources

| Source | Venue | Check | Decisions | Note |
|---|---|---|---|---|
| Abeler, Nosenzo & Raymond (2019). *Preferences for Truth-Telling*. [doi:10.3982/ECTA14673](https://doi.org/10.3982/ECTA14673) | Econometrica 87(4) 1115-1153 | Full text | truth-telling-gains |  |
| Adams et al. (2021). *People systematically overlook subtractive changes*. [doi:10.1038/s41586-021-03380-y](https://doi.org/10.1038/s41586-021-03380-y) | Nature 592(7853) 258-261 | Abstract | biz07, biz08 |  |
| Allcott, Braghieri, Eichmeyer & Gentzkow (2020). *The Welfare Effects of Social Media*. [doi:10.1257/aer.20190658](https://doi.org/10.1257/aer.20190658) | American Economic Review 110(3) 629-676 | Full text | facebook-deactivation | ["Effect sizes (SD units, minutes, WTA) were read in the authors' final manuscript dated Nov 2019, not the typeset AER pages; direction of every effect is confirmed by the AER abstract."] |
| Altay & Gilardi (2024). *People are skeptical of headlines labeled as AI-generated, even if true or human-made, because they assume full AI automation*. [doi:10.1093/pnasnexus/pgae403](https://doi.org/10.1093/pnasnexus/pgae403) | PNAS Nexus 3(10) pgae403 | Full text | axb09 |  |
| Ayers et al. (2023). *Comparing Physician and Artificial Intelligence Chatbot Responses to Patient Questions Posted to a Public Social Media Forum*. [doi:10.1001/jamainternmed.2023.1838](https://doi.org/10.1001/jamainternmed.2023.1838) | JAMA Internal Medicine 183(6) 589 | Full text | axe02, axe05 | Evaluators were blinded but were also coauthors; accuracy was not separately assessed and longer chatbot answers may have inflated empathy ratings (authors' own limitations). |
| Bail et al. (2018). *Exposure to opposing views on social media can increase political polarization*. [doi:10.1073/pnas.1804840115](https://doi.org/10.1073/pnas.1804840115) | Proceedings of the National Academy of Sciences 115(37) 9216-9221 | Full text | opposing-views-bot |  |
| Bastani et al. (2025). *Generative AI without guardrails can harm learning: Evidence from high school mathematics*. [doi:10.1073/pnas.2422633122](https://doi.org/10.1073/pnas.2422633122) | Proceedings of the National Academy of Sciences 122(26) e2422633122 | Full text | rollout4 | Correction (PNAS 2025, doi:10.1073/pnas.2518204122) fixes one author affiliation only; findings unchanged. |
| Benartzi & Thaler (2001). *Naive Diversification Strategies in Defined Contribution Saving Plans*. [doi:10.1257/aer.91.1.79](https://doi.org/10.1257/aer.91.1.79) | American Economic Review 91(1) 79-98 | Abstract | bz16 |  |
| Bertrand & Mullainathan (2004). *Are Emily and Greg More Employable Than Lakisha and Jamal? A Field Experiment on Labor Market Discrimination*. [doi:10.1257/0002828042002561](https://doi.org/10.1257/0002828042002561) | American Economic Review 94(4) 991-1013 | Abstract | social12 |  |
| Bertrand et al. (2010). *What's Advertising Content Worth? Evidence from a Consumer Credit Marketing Field Experiment*. [doi:10.1162/qjec.2010.125.1.263](https://doi.org/10.1162/qjec.2010.125.1.263) | The Quarterly Journal of Economics 125(1) 263-305 | Abstract | bz09 |  |
| Bicchieri, Dimant & Sonderegger (2023). *It's not a lie if you believe the norm does not apply: Conditional norm-following and belief distortion*. [doi:10.1016/j.geb.2023.01.005](https://doi.org/10.1016/j.geb.2023.01.005) | Games and Economic Behavior 138 321-354 | Abstract | dimant-notalie-causal |  |
| Bicchieri, Dimant & Xiao (2021). *Deviant or wrong? The effects of norm information on the efficacy of punishment*. [doi:10.1016/j.jebo.2021.04.002](https://doi.org/10.1016/j.jebo.2021.04.002) | Journal of Economic Behavior & Organization 188 209-235 | Abstract | dimant-deviant-choice |  |
| Bicchieri, Dimant, Gächter & Nosenzo (2022). *Social proximity and the erosion of norm compliance*. [doi:10.1016/j.geb.2021.11.012](https://doi.org/10.1016/j.geb.2021.11.012) | Games and Economic Behavior 132 59-72 | Full text | dimant-proximity-estimate, dimant-contagion-multi |  |
| Bloom et al. (2015). *Does Working from Home Work? Evidence from a Chinese Experiment*. [doi:10.1093/qje/qju032](https://doi.org/10.1093/qje/qju032) | The Quarterly Journal of Economics 130(1) 165-218 | Abstract | bz05 |  |
| Bloom, Han & Liang (2024). *Hybrid working from home improves retention without damaging performance*. [doi:10.1038/s41586-024-07500-2](https://doi.org/10.1038/s41586-024-07500-2) | Nature 630(8018) 920-925 | Full text | bz07 |  |
| Bohnet, van Geen & Bazerman (2016). *When Performance Trumps Gender Bias: Joint vs. Separate Evaluation*. [doi:10.1287/mnsc.2015.2186](https://doi.org/10.1287/mnsc.2015.2186) | Management Science 62(5) 1225-1234 | Abstract | bz14 |  |
| Bolton, Dimant & Schmidt (2021). *Observability and social image: On the robustness and fragility of reciprocity*. [doi:10.1016/j.jebo.2021.09.018](https://doi.org/10.1016/j.jebo.2021.09.018) | Journal of Economic Behavior & Organization 191 946-964 | Abstract | dimant-observability-choice |  |
| Breza, Kaur & Shamdasani (2018). *The Morale Effects of Pay Inequality*. [doi:10.1093/qje/qjx041](https://doi.org/10.1093/qje/qjx041) | The Quarterly Journal of Economics 133(2) 611-663 | Abstract | bz13 |  |
| Brynjolfsson, Li & Raymond (2025). *Generative AI at Work*. [doi:10.1093/qje/qjae044](https://doi.org/10.1093/qje/qjae044) | Quarterly Journal of Economics 140(2) 889-942 | Abstract | ai04, axb13, rollout1, rollout2 |  |
| Buehler, Griffin & Ross (1994). *Exploring the "planning fallacy": Why people underestimate their task completion times*. [doi:10.1037/0022-3514.67.3.366](https://doi.org/10.1037/0022-3514.67.3.366) | Journal of Personality and Social Psychology 67(3) 366-381 | Full text | bz04 |  |
| Bursztyn, González & Yanagizawa-Drott (2020). *Misperceived Social Norms: Women Working Outside the Home in Saudi Arabia*. [doi:10.1257/aer.20180975](https://doi.org/10.1257/aer.20180975) | American Economic Review 110(10) 2997-3029 | Full text | misperceived-norms-support, misperceived-norms-action |  |
| Buçinca, Malaya & Gajos (2021). *To Trust or to Think: Cognitive Forcing Functions Can Reduce Overreliance on AI in AI-assisted Decision-making*. [doi:10.1145/3449287](https://doi.org/10.1145/3449287) | Proceedings of the ACM on Human-Computer Interaction (CSCW1) 5(CSCW1) 1-21 | Abstract | axb10 |  |
| Card et al. (2012). *Inequality at Work: The Effect of Peer Salaries on Job Satisfaction*. [doi:10.1257/aer.102.6.2981](https://doi.org/10.1257/aer.102.6.2981) | American Economic Review 102(6) 2981-3003 | Abstract | bz12 |  |
| Castelo, Bos & Lehmann (2019). *Task-Dependent Algorithm Aversion*. [doi:10.1177/0022243719851788](https://doi.org/10.1177/0022243719851788) | Journal of Marketing Research 56(5) 809-825 | Abstract | ai11 |  |
| Centola (2010). *The Spread of Behavior in an Online Social Network Experiment*. [doi:10.1126/science.1185231](https://doi.org/10.1126/science.1185231) | Science 329(5996) 1194-1197 | Full text | social08 |  |
| Cohn, Maréchal, Tannenbaum & Zünd (2019). *Civic honesty around the globe*. [doi:10.1126/science.aau8712](https://doi.org/10.1126/science.aau8712) | Science 365(6448) 70-73 | Full text | civic-wallet-rank, civic-wallet-experts | ["Cross-country rankings rest on owner email responses; Yang et al. (2023, PNAS 120(29), e2213824120, doi:10.1073/pnas.2213824120) report email response rates were inversely related to collectivism and that a China replication found higher wallet recovery than email responses implied. Items here use |
| Costello, Pennycook & Rand (2024). *Durably reducing conspiracy beliefs through dialogues with AI*. [doi:10.1126/science.adq1814](https://doi.org/10.1126/science.adq1814) | Science 385(6714) eadq1814 | Abstract | axb15 | Science published an Editorial Expression of Concern on 11 June 2026 (doi 10.1126/science.aej2383); the authors released a corrected reanalysis reporting the same direction, significance and size (Zenodo record 22754984). Included on 2026-10-31 at Eugen Dimant's instruction that the concern no longe |
| Cui et al. (2026). *The Effects of Generative AI on High-Skilled Work: Evidence from Three Field Experiments with Software Developers*. [doi:10.1287/mnsc.2025.00535](https://doi.org/10.1287/mnsc.2025.00535) | Management Science  mnsc.2025.00535 (published online 27 February 2026) | Abstract | axe02, axe06 | Authors note each experiment is noisy and results vary across experiments (SE 10.3% on the pooled estimate). |
| Dell’Acqua et al. (2026). *Navigating the Jagged Technological Frontier: Field Experimental Evidence of the Effects of Artificial Intelligence on Knowledge Worker Productivity and Quality*. [doi:10.1287/orsc.2025.21838](https://doi.org/10.1287/orsc.2025.21838) | Organization Science 37(2) 403-423 | Full text | axb14, rollout3 |  |
| Dietvorst & Bharti (2020). *People Reject Algorithms in Uncertain Decision Domains Because They Have Diminishing Sensitivity to Forecasting Error*. [doi:10.1177/0956797620948841](https://doi.org/10.1177/0956797620948841) | Psychological Science 31(10) 1302-1314 | Abstract | axe07 |  |
| Dietvorst, Simmons & Massey (2015). *Algorithm aversion: People erroneously avoid algorithms after seeing them err*. [doi:10.1037/xge0000033](https://doi.org/10.1037/xge0000033) | Journal of Experimental Psychology: General 144(1) 114-126 | Full text | ai09 |  |
| Dietvorst, Simmons & Massey (2018). *Overcoming Algorithm Aversion: People Will Use Imperfect Algorithms If They Can (Even Slightly) Modify Them*. [doi:10.1287/mnsc.2016.2643](https://doi.org/10.1287/mnsc.2016.2643) | Management Science 64(3) 1155-1170 | Full text | axb02 | An earlier manuscript on a Wharton site (marketing.wharton.upenn.edu) has a different Study 2 (state rankings, N = 1,040, 47/75/77%); do not use those numbers. Numbers here follow the deposit tied to the published version (Study 2, N = 816). |
| Dimant (2019). *Contagion of pro- and anti-social behavior among peers and the role of social proximity*. [doi:10.1016/j.joep.2019.04.009](https://doi.org/10.1016/j.joep.2019.04.009) | Journal of Economic Psychology 73 66-88 | Abstract | dimant-contagion-multi |  |
| Dimant (2023). *Beyond average: A method for measuring the tightness, looseness, and polarization of social norms*. [doi:10.1016/j.econlet.2023.111417](https://doi.org/10.1016/j.econlet.2023.111417) | Economics Letters 233 111417 | Abstract | social20 |  |
| Dimant (2024). *Hate Trumps Love: The Impact of Political Polarization on Social Preferences*. [doi:10.1287/mnsc.2023.4701](https://doi.org/10.1287/mnsc.2023.4701) | Management Science 70(1) 1-31 | Abstract | social15, social16, dimant-hate-choice |  |
| Dimant & Gesche (2023). *Nudging enforcers: how norm perceptions and motives for lying shape sanctions*. [doi:10.1093/pnasnexus/pgad224](https://doi.org/10.1093/pnasnexus/pgad224) | PNAS Nexus 2(7) pgad224 | Full text | dimant-enforcers-rank |  |
| Dimant et al. (2022). *Politicizing mask-wearing: predicting the success of behavioral interventions among republicans and democrats in the U.S.*. [doi:10.1038/s41598-022-10524-1](https://doi.org/10.1038/s41598-022-10524-1) | Scientific Reports 12 7575 | Full text | dimant-masks-forecast |  |
| Dimant, Galeotti & Villeval (2024). *Motivated information acquisition and social norm formation*. [doi:10.1016/j.euroecorev.2024.104778](https://doi.org/10.1016/j.euroecorev.2024.104778) | European Economic Review 167 104778 | Full text | dimant-motivated-estimate |  |
| Dimant, Gelfand, Hochleitner & Sonderegger (2025). *Strategic Behavior with Tight, Loose, and Polarized Norms*. [doi:10.1287/mnsc.2023.01022](https://doi.org/10.1287/mnsc.2023.01022) | Management Science 71(3) 2245-2263 | Full text | social01, social03, dimant-polarizednorms-choice |  |
| Dimant, van Kleef & Shalvi (2020). *Requiem for a Nudge: Framing effects in nudging honesty*. [doi:10.1016/j.jebo.2020.02.015](https://doi.org/10.1016/j.jebo.2020.02.015) | Journal of Economic Behavior & Organization 172 247-266 | Abstract | dimant-requiem-forecast |  |
| Doshi & Hauser (2024). *Generative AI enhances individual creativity but reduces the collective diversity of novel content*. [doi:10.1126/sciadv.adn5290](https://doi.org/10.1126/sciadv.adn5290) | Science Advances 10(28) eadn5290 | Abstract | ai07 |  |
| Fischbacher & Föllmi-Heusi (2013). *Lies in Disguise: An Experimental Study on Cheating*. [doi:10.1111/jeea.12014](https://doi.org/10.1111/jeea.12014) | Journal of the European Economic Association 11(3) 525-547 | Abstract | lies-in-disguise |  |
| Fügener, Grahl, Gupta & Ketter (2022). *Cognitive Challenges in Human–Artificial Intelligence Collaboration: Investigating the Path Toward Productive Delegation*. [doi:10.1287/isre.2021.1079](https://doi.org/10.1287/isre.2021.1079) | Information Systems Research 33(2) 678-696 | Abstract | axe03 |  |
| Gneezy & Rustichini (2000). *A Fine is a Price*. [doi:10.1086/468061](https://doi.org/10.1086/468061) | The Journal of Legal Studies 29(1) 1-17 | Full text | bz08 |  |
| Goldin & Rouse (2000). *Orchestrating Impartiality: The Impact of "Blind" Auditions on Female Musicians*. [doi:10.1257/aer.90.4.715](https://doi.org/10.1257/aer.90.4.715) | American Economic Review 90(4) 715-741 | Abstract | social13 |  |
| Goldstein, Chao, Grossman, Stamos & Tomz (2024). *How persuasive is AI-generated propaganda?*. [doi:10.1093/pnasnexus/pgae034](https://doi.org/10.1093/pnasnexus/pgae034) | PNAS Nexus 3(2) pgae034 | Full text | axe04, genai2 |  |
| Goldstein, Cialdini & Griskevicius (2008). *A Room with a Viewpoint: Using Social Norms to Motivate Environmental Conservation in Hotels*. [doi:10.1086/586910](https://doi.org/10.1086/586910) | Journal of Consumer Research 35(3) 472-482 | Abstract | biz03, biz04 |  |
| Gordon et al. (2019). *A Comparison of Approaches to Advertising Measurement: Evidence from Big Field Experiments at Facebook*. [doi:10.1287/mksc.2018.1135](https://doi.org/10.1287/mksc.2018.1135) | Marketing Science 38(2) 193-225 | Full text | bz01 | ["Articles-in-Advance pagination differs from print; print 38(2):193-225 per Crossref."] |
| Granulo, Fuchs & Puntoni (2019). *Psychological reactions to human versus robotic job replacement*. [doi:10.1038/s41562-019-0670-y](https://doi.org/10.1038/s41562-019-0670-y) | Nature Human Behaviour 3(10) 1062-1069 | Abstract | axe09 |  |
| Grove et al. (2000). *Clinical versus mechanical prediction: A meta-analysis*. [doi:10.1037/1040-3590.12.1.19](https://doi.org/10.1037/1040-3590.12.1.19) | Psychological Assessment 12(1) 19-30 | Full text | axb04 |  |
| Gächter & Schulz (2016). *Intrinsic honesty and the prevalence of rule violations across societies*. [doi:10.1038/nature17160](https://doi.org/10.1038/nature17160) | Nature 531(7595) 496-499 | Full text | rule-violations-honesty | ["Numbers read from the author manuscript; confirm against the typeset Nature version before display if possible."] |
| Hallsworth, List, Metcalfe & Vlaev (2017). *The behavioralist as tax collector: Using natural field experiments to enhance tax compliance*. [doi:10.1016/j.jpubeco.2017.02.003](https://doi.org/10.1016/j.jpubeco.2017.02.003) | Journal of Public Economics 148 14-31 | Abstract | tax-letter-norms |  |
| Hartmann, Exner & Domdey (2025). *The power of generative marketing: Can generative AI create superhuman visual marketing content?*. [doi:10.1016/j.ijresmar.2024.09.002](https://doi.org/10.1016/j.ijresmar.2024.09.002) | International Journal of Research in Marketing 42(1) 13-31 | Abstract | axe10 |  |
| Hoffman, Kahn & Li (2018). *Discretion in Hiring*. [doi:10.1093/qje/qjx042](https://doi.org/10.1093/qje/qjx042) | The Quarterly Journal of Economics 133(2) 765-800 | Abstract | axb06 |  |
| Hui, Reshef & Zhou (2024). *The Short-Term Effects of Generative Artificial Intelligence on Employment: Evidence from an Online Labor Market*. [doi:10.1287/orsc.2023.18441](https://doi.org/10.1287/orsc.2023.18441) | Organization Science 35(6) 1977-1989 | Abstract | axe08 |  |
| Iyengar & Lepper (2000). *When choice is demotivating: Can one desire too much of a good thing?*. [doi:10.1037/0022-3514.79.6.995](https://doi.org/10.1037/0022-3514.79.6.995) | Journal of Personality and Social Psychology 79(6) 995-1006 | Full text | bz10 | ["Contested on average: Scheibehenne, Greifeneder & Todd (2010) meta-analysis finds a mean effect near zero. Used only in an item about that contest."] |
| Jakesch, Hancock & Naaman (2023). *Human heuristics for AI-generated language are flawed*. [doi:10.1073/pnas.2208839120](https://doi.org/10.1073/pnas.2208839120) | Proceedings of the National Academy of Sciences 120(11) e2208839120 | Full text | axb07 |  |
| Jia, Luo, Fang & Liao (2024). *When and How Artificial Intelligence Augments Employee Creativity*. [doi:10.5465/amj.2022.0426](https://doi.org/10.5465/amj.2022.0426) | Academy of Management Journal 67(1) 5-32 | Abstract | axe02 |  |
| Johnson & Goldstein (2004). *Defaults and Donation Decisions*. [doi:10.1097/01.TP.0000149788.10382.B2](https://doi.org/10.1097/01.TP.0000149788.10382.B2) | Transplantation 78(12) 1713-1716 | Full text | bz15 | ["Cited instead of Johnson & Goldstein (2003) Science 302:1338-1339 because the Science text could not be accessed; exact opt-in/opt-out percentages appear only in a figure and are not used."] |
| Kahneman & Tversky (1979). *Prospect Theory: An Analysis of Decision under Risk*. [doi:10.2307/1914185](https://doi.org/10.2307/1914185) | Econometrica 47(2) 263-292 | Full text | judg09 |  |
| Kahneman, Knetsch & Thaler (1990). *Experimental Tests of the Endowment Effect and the Coase Theorem*. [doi:10.1086/261737](https://doi.org/10.1086/261737) | Journal of Political Economy 98(6) 1325-1348 | Full text | bz06 |  |
| Kleinberg et al. (2018). *Human Decisions and Machine Predictions*. [doi:10.1093/qje/qjx032](https://doi.org/10.1093/qje/qjx032) | The Quarterly Journal of Economics 133(1) 237-293 | Abstract | axb03 |  |
| Kristal et al. (2020). *Signing at the beginning versus at the end does not decrease dishonesty*. [doi:10.1073/pnas.1911695117](https://doi.org/10.1073/pnas.1911695117) | Proceedings of the National Academy of Sciences 117(13) 7103-7107 | Abstract | bz11 | ["Crossref lists a correction notice (doi:10.1073/pnas.2610441123, 29 June 2026); its body text could not be read, so what it changes is unknown."] |
| Lambrecht & Tucker (2019). *Algorithmic Bias? An Empirical Study of Apparent Gender-Based Discrimination in the Display of STEM Career Ads*. [doi:10.1287/mnsc.2018.3093](https://doi.org/10.1287/mnsc.2018.3093) | Management Science 65(7) 2966-2981 | Abstract | axb12 |  |
| Lees & Cikara (2020). *Inaccurate group meta-perceptions drive negative out-group attributions in competitive contexts*. [doi:10.1038/s41562-019-0766-4](https://doi.org/10.1038/s41562-019-0766-4) | Nature Human Behaviour 4(3) 279-286 | Full text | meta-perception-causal | ["Crossref API returned an error; bibliographic data taken from the Springer Nature page (online 11 Nov 2019, issue March 2020). Experiment-level numbers come from the DASH manuscript, not the typeset article."] |
| Lewis & Rao (2015). *The Unfavorable Economics of Measuring the Returns to Advertising*. [doi:10.1093/qje/qjv023](https://doi.org/10.1093/qje/qjv023) | The Quarterly Journal of Economics 130(4) 1941-1973 | Abstract | bz02 |  |
| Logg, Minson & Moore (2019). *Algorithm appreciation: People prefer algorithmic to human judgment*. [doi:10.1016/j.obhdp.2018.12.005](https://doi.org/10.1016/j.obhdp.2018.12.005) | Organizational Behavior and Human Decision Processes 151 90-103 | Abstract | ai10 |  |
| Longoni & Cian (2022). *Artificial Intelligence in Utilitarian vs. Hedonic Contexts: The "Word-of-Machine" Effect*. [doi:10.1177/0022242920957347](https://doi.org/10.1177/0022242920957347) | Journal of Marketing 86(1) 91-108 | Abstract | axe01 |  |
| Longoni, Bonezzi & Morewedge (2019). *Resistance to Medical Artificial Intelligence*. [doi:10.1093/jcr/ucz013](https://doi.org/10.1093/jcr/ucz013) | Journal of Consumer Research 46(4) 629-650 | Abstract | ai12 |  |
| Luo, Tong, Fang & Qu (2019). *Frontiers: Machines vs. Humans: The Impact of Artificial Intelligence Chatbot Disclosure on Customer Purchases*. [doi:10.1287/mksc.2019.1192](https://doi.org/10.1287/mksc.2019.1192) | Marketing Science 38(6) 937-947 | Abstract | axe02, axe14 |  |
| Madrian & Shea (2001). *The Power of Suggestion: Inertia in 401(k) Participation and Savings Behavior*. [doi:10.1162/003355301753265543](https://doi.org/10.1162/003355301753265543) | Quarterly Journal of Economics 116(4) 1149-1187 | Full text | biz01, biz02 |  |
| Matz et al. (2024). *The potential of generative AI for personalized persuasion at scale*. [doi:10.1038/s41598-024-53755-0](https://doi.org/10.1038/s41598-024-53755-0) | Scientific Reports 14 4692 | Full text | axe13 |  |
| Mellers et al. (2014). *Psychological Strategies for Winning a Geopolitical Forecasting Tournament*. [doi:10.1177/0956797614524255](https://doi.org/10.1177/0956797614524255) | Psychological Science 25(5) 1106-1115 | Full text | forecast-teams-rank, forecast-training | ["The paper reports test statistics, not percentage accuracy gains; no percentages are derived here."] |
| Moore & Healy (2008). *The trouble with overconfidence*. [doi:10.1037/0033-295X.115.2.502](https://doi.org/10.1037/0033-295X.115.2.502) | Psychological Review 115(2) 502-517 | Full text | overconfidence-hard-task |  |
| Noy & Zhang (2023). *Experimental evidence on the productivity effects of generative artificial intelligence*. [doi:10.1126/science.adh2586](https://doi.org/10.1126/science.adh2586) | Science 381(6654) 187-192 | Abstract | ai01, ai02 |  |
| Obermeyer, Powers, Vogeli & Mullainathan (2019). *Dissecting racial bias in an algorithm used to manage the health of populations*. [doi:10.1126/science.aax2342](https://doi.org/10.1126/science.aax2342) | Science 366(6464) 447-453 | Abstract | axb05 |  |
| Panizza, Dimant, Kimbrough & Vostroknutov (2024). *Measuring norm pluralism and perceived polarization in US politics*. [doi:10.1093/pnasnexus/pgae413](https://doi.org/10.1093/pnasnexus/pgae413) | PNAS Nexus 3(10) pgae413 | Full text | social07 |  |
| Pennycook et al. (2021). *Shifting attention to accuracy can reduce misinformation online*. [doi:10.1038/s41586-021-03344-2](https://doi.org/10.1038/s41586-021-03344-2) | Nature 592(7855) 590-595 | Full text | accuracy-prompt | ["Accuracy-prompt effects are small and debated: a preregistered direct replication of the authors' earlier study (Roozenbeek, Freeman & van der Linden 2021, Psychological Science 32(7), 1169-1178, doi:10.1177/09567976211024535) failed at its first stage (n = 701, p = .67) and found only a small, un |
| Prentice & Miller (1993). *Pluralistic ignorance and alcohol use on campus: Some consequences of misperceiving the social norm*. [doi:10.1037/0022-3514.64.2.243](https://doi.org/10.1037/0022-3514.64.2.243) | Journal of Personality and Social Psychology 64(2) 243-256 | Abstract | social04, misperceived-norms-support |  |
| Reif, Larrick & Soll (2025). *Evidence of a social evaluation penalty for using AI*. [doi:10.1073/pnas.2426766122](https://doi.org/10.1073/pnas.2426766122) | Proceedings of the National Academy of Sciences 122(19) e2426766122 | Full text | axe12 |  |
| Ren, Dimant & Schweitzer (2023). *Beyond belief: How social engagement motives influence the spread of conspiracy theories*. [doi:10.1016/j.jesp.2022.104421](https://doi.org/10.1016/j.jesp.2022.104421) | Journal of Experimental Social Psychology 104 104421 | Abstract | dimant-conspiracy-choice |  |
| Salvi, Horta Ribeiro, Gallotti & West (2025). *On the conversational persuasiveness of GPT-4*. [doi:10.1038/s41562-025-02194-6](https://doi.org/10.1038/s41562-025-02194-6) | Nature Human Behaviour 9(8) 1645-1653 | Full text | axb08 |  |
| Scheibehenne, Greifeneder & Todd (2010). *Can There Ever Be Too Many Options? A Meta-Analytic Review of Choice Overload*. [doi:10.1086/651235](https://doi.org/10.1086/651235) | Journal of Consumer Research 37(3) 409-425 | Full text | bz10 |  |
| Schultz et al. (2007). *The Constructive, Destructive, and Reconstructive Power of Social Norms*. [doi:10.1111/j.1467-9280.2007.01917.x](https://doi.org/10.1111/j.1467-9280.2007.01917.x) | Psychological Science 18(5) 429-434 | Abstract | biz05, biz06 |  |
| Shelton & Richeson (2005). *Intergroup contact and pluralistic ignorance*. [doi:10.1037/0022-3514.88.1.91](https://doi.org/10.1037/0022-3514.88.1.91) | Journal of Personality and Social Psychology 88(1) 91-107 | Abstract | social14 |  |
| Shu et al. (2012). *Signing at the beginning makes ethics salient and decreases dishonest self-reports in comparison to signing at the end*. [doi:10.1073/pnas.1209746109](https://doi.org/10.1073/pnas.1209746109) | Proceedings of the National Academy of Sciences 109(38) 15197-15200 | Abstract | bz11 | ["RETRACTED 13 September 2021 (doi:10.1073/pnas.2115397118). Cited only as the retracted original in a replication item."] |
| Spitale, Biller-Andorno & Germani (2023). *AI model GPT-3 (dis)informs us better than humans*. [doi:10.1126/sciadv.adh1850](https://doi.org/10.1126/sciadv.adh1850) | Science Advances 9(26) eadh1850 | Full text | axe11 |  |
| Thaler & Benartzi (2004). *Save More Tomorrow: Using Behavioral Economics to Increase Employee Saving*. [doi:10.1086/380085](https://doi.org/10.1086/380085) | Journal of Political Economy 112(S1) S164-S187 | Abstract | bz03 | ["First implementation is a non-randomized company rollout."] |
| Toma et al. (2026). *Promoting Safe Opioid Disposal: Experimental Evidence on Behavioral Messaging With Financial Incentives*. [doi:10.1002/hec.70085](https://doi.org/10.1002/hec.70085) | Health Economics 35(7) 1023-1032 | Abstract | dimant-opioid-forecast |  |
| Tong, Jia, Luo & Fang (2021). *The Janus face of artificial intelligence feedback: Deployment versus disclosure effects on employee performance*. [doi:10.1002/smj.3322](https://doi.org/10.1002/smj.3322) | Strategic Management Journal 42(9) 1600-1631 | Abstract | axe03 |  |
| Tversky & Kahneman (1974). *Judgment under Uncertainty: Heuristics and Biases*. [doi:10.1126/science.185.4157.1124](https://doi.org/10.1126/science.185.4157.1124) | Science 185(4157) 1124-1131 | Full text | biz11 |  |
| Tversky & Kahneman (1981). *The framing of decisions and the psychology of choice*. [doi:10.1126/science.7455683](https://doi.org/10.1126/science.7455683) | Science 211(4481) 453-458 | Full text | judg05 |  |
| Vaccaro, Almaatouq & Malone (2024). *When combinations of humans and AI are useful: A systematic review and meta-analysis*. [doi:10.1038/s41562-024-02024-1](https://doi.org/10.1038/s41562-024-02024-1) | Nature Human Behaviour 8(12) 2293-2303 | Full text | axb01 |  |
| Vosoughi, Roy & Aral (2018). *The spread of true and false news online*. [doi:10.1126/science.aap9559](https://doi.org/10.1126/science.aap9559) | Science 359(6380) 1146-1151 | Abstract | false-news-spread |  |
| Walasek & Stewart (2015). *How to make loss aversion disappear and reverse: Tests of the decision by sampling origin of loss aversion*. [doi:10.1037/xge0000039](https://doi.org/10.1037/xge0000039) | Journal of Experimental Psychology: General 144(1) 7-11 | Quarantined | judg02 | Reversal finding contested by a reanalysis (Andre & de Langhe, 2021, JEP: General 150(12), 2659-2665). Withheld from scored play. |
| Woolley et al. (2010). *Evidence for a Collective Intelligence Factor in the Performance of Human Groups*. [doi:10.1126/science.1193147](https://doi.org/10.1126/science.1193147) | Science 330(6004) 686-688 | Abstract | social10 |  |
| Yeomans, Shah, Mullainathan & Kleinberg (2019). *Making sense of recommendations*. [doi:10.1002/bdm.2118](https://doi.org/10.1002/bdm.2118) | Journal of Behavioral Decision Making 32(4) 403-414 | Abstract | axb11 |  |
| Yin, Jia & Wakslak (2024). *AI can help people feel heard, but an AI label diminishes this impact*. [doi:10.1073/pnas.2319112121](https://doi.org/10.1073/pnas.2319112121) | Proceedings of the National Academy of Sciences 121(14) e2319112121 | Full text | genai3 |  |
| Zhou & Lee (2024). *Generative artificial intelligence, human creativity, and art*. [doi:10.1093/pnasnexus/pgae052](https://doi.org/10.1093/pnasnexus/pgae052) | PNAS Nexus 3(3) pgae052 | Full text | genai1 | Abstract reports a 25% productivity gain while Results describe a 50% rise at adoption; items avoid the productivity size. |

## Corrections to carried-forward content

- **ai01**, scene: Scene says 'A firm gives professionals an AI assistant'; the study was a preregistered online experiment with randomized ChatGPT access, not a firm deployment. Numbers (453, 40%, 18%) are correct.
- **ai06**, title: Title 'When expertise backfires' is loose: the paper shows AI use backfiring outside the frontier, not human expertise backfiring. Consider 'When AI help backfires'.
- **ai09**, scene: Scene says the model outperforms 'a human expert'; in the studies the human forecaster was the participant herself or another anonymous participant, not an expert.
- **biz11**, boundary: Boundary/follow answer says anchor effects depend on incentives; the cited paper reports the opposite for incentives. It also states experienced researchers are prone to the same biases when thinking intuitively, so 'expertise' as a moderat
- **biz11**, follow[1]: Boundary/follow answer says anchor effects depend on incentives; the cited paper reports the opposite for incentives. It also states experienced researchers are prone to the same biases when thinking intuitively, so 'expertise' as a moderat
- **social02**, explain: Explain says 'many'; paper says 'most' (understatement, optional fix).
- **biz08**, question: Question wording is ambiguous: 'affect overlooked subtraction' reads as asking about overlooking, which load INCREASES; a reader could pick 'more likely'. Suggest rewording.; Text read: abstract only; load manipulation in the scene ('juggli
- **social04**, follow[2]: follow[2] answer (source takeaway) says 'consequences for individual behavior'; abstract reports consequences for attitudes (men shifted toward perceived norm) and campus alienation, not drinking behavior.; Text read: abstract only.
- **social05**, follow[2]: Same follow[2] overstatement ('consequences for individual behavior') as social04.; Answer key fine: study measured own attitudes and estimates of average student's attitudes (both levels). Boundary about correction is not from this paper (
- **social07**, explain: Minor: 'substantial heterogeneity within each party' slightly overstates for Democrats; Fig. 4 caption: "Democrats tend to agree much more than Republicans on all issues, except for immigration policy." Consider softening.; Scene ('agree on
- **social12**, explain: Estimate target 50 (tolerance 10) and index chart 100 vs 150 match ratio 1.50.; Minor terminology: 'audit experiment' in explain; design is a correspondence (resume) field experiment. 'Comparable résumés' acceptable: names randomly assigned
- **social14**, explain: Minor: the feared rejection was race-based; groups were White and Black participants.
- **social15**, scene: Scene misdescribes the design: not a workplace collaboration study; five preregistered studies (15 behavioral experiments, >8,600 participants) on Trump supporters vs opponents.
- **social19**, scene: Scene contrasts a close colleague with 'a stranger'; the design contrasted an anonymous peer described as more vs less similar (high vs low proximity), with an unknown-proximity control. All peers were anonymous.
- **social21**, options[0]: Option 0 wording ('How many different normative positions') slightly mischaracterizes the method, which elicits the shape/spread of the belief distribution, not a count. Suggested tweak only.
- **biz05**, scene: Delivery details (door hangers) rest on a secondary source; neutral wording keeps only what the abstract states.
- **biz06**, scene: Approval cue described as in the published abstract; not a utility bill.
- **social04**, follow[2]: Abstract reports attitude change and alienation, not drinking behavior.
- **social05**, follow[2]: Abstract reports attitude change and alienation, not drinking behavior.
- **hate23**, year: Version of record: Management Science 70(1), 1-31, January 2024 (online 2023).
- **norms24**, year: Version of record: Management Science 71(3), 2245-2263, March 2025 (online 2024).
- **cast19**, title: Crossref title case.
- **blind00**, title: Crossref title has quotation marks.
- **plural93**, takeaway: Abstract reports attitudes and alienation, not behavior.
- **loss15**, verification.status: Contested reversal; challenge judg02 removed from scored play.

## Retired decisions

- biz09 (Same outcome, different decision): Duplicate of judg05 framing item; concept label only.
- biz10 (A decision memo rewrite): Advice the paper did not test as a remedy.
- biz12 (The vivid case): Concept-label question with a non-serious distractor.
- biz13 (The cost of not deciding): Concept-label question; no measured outcome.
- biz14 (Keep the incumbent): Concept-label question; no measured outcome.
- judg01 (The risky offer): Concept-label question.
- judg03 (A convincing story): Concept-label question.
- judg04 (The first estimate): Advice the paper did not test as a remedy.
- judg06 (The memorable failure): Concept-label question.
- judg07 (Different baselines): Concept-label question.
- judg08 (Waiting for perfect data): Concept-label question.
- ai03 (Who captures the upside?): Superseded by the rollout case (same source, sharper design).
- ai05 (The jagged frontier): Superseded by axb14 and rollout3 with measured outcomes.
- ai06 (When AI help backfires): Superseded by rollout3 with measured outcomes.
- ai08 (The hidden portfolio risk): Advice item without a measured outcome.
- ai13 (Human error, model error): Duplicate of ai09.
- ai14 (Creative homogenization): Advice item without a measured outcome.
- ai15 (Hidden distributional returns): Duplicate of rollout case.
- ai16 (Bias in a faster funnel): Generic advice; replaced by axb05 and axb12 with measured outcomes.
- ai17 (The AI rollout norm): Advice item without a measured outcome.
- social02 (The polarized team): Superseded by dimant-polarizednorms-choice.
- social05 (The silence trap): Advice item without a measured outcome.
- social06 (One number, many norms): Concept-label question.
- social09 (One influencer or a cluster?): Duplicate of social08.
- social11 (The socially attuned team): Duplicate of social10.
- social17 (Expect the worst): Superseded by dimant-hate-choice.
- social18 (Bad behavior travels): Superseded by dimant-contagion-multi.
- social19 (The near-peer effect): Superseded by dimant-contagion-multi.
- social21 (Beyond a single norm): Concept-label question.

## Not verified

- No independent human expert has reviewed this audit. Checks were run by AI agents that read the published texts listed above; each quote and location is stored in `src/evidence.json` and `docs/audit/`.
- Abstract-level checks confirm the numbers and directions that appear in abstracts; design details beyond the abstract were taken only from full texts where marked.
