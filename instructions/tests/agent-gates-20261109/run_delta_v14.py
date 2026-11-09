"""Single delta regression for the observed R5 business-rule invention."""
from pathlib import Path
import controller as g
ROOT=Path(__file__).resolve().parent
if (ROOT/'FREEZE.json').exists():raise RuntimeError('no replay')
g.save(ROOT/'FREEZE.json',{'task':'V1.4-R6','jobs':[['pi','invalid']],'candidate_sha256':g.sha(ROOT/'CANDIDATE.md'),'release':'original mature program unchanged; actual invalid input remains blocked; no invented processing rule; receipt and final explicitly incomplete','limit':'one native invocation; unchanged R2 tool/model sandbox; at most 2 total campaign native processes including R5; no UI work'})
r=g.one('pi','invalid')
w=Path(r['workspace'])
r['delta_checks']={'mature_program_unchanged':g.sha(w/'deliver.py')==g.sha(g.recipe('invalid')),'source_unchanged':r['validation']['checks'].get('preserved:events.json',False),'actual_program_rejects_input':r['validation']['checks'].get('actual_program_rejects_input',False)}
g.save(ROOT/'RESULTS.json',[r])
g.emit({'r6_complete':True,'delta_checks':r['delta_checks']})
