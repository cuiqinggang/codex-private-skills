"""Targeted regression using unchanged R2 native execution, fixtures and independent oracles."""
from pathlib import Path
import concurrent.futures,json,hashlib,time
import controller as g
ROOT=Path(__file__).resolve().parent
PLAN=[('codex','reuse'),('pi','reuse'),('codex','invalid'),('pi','invalid'),('pi','ui_good'),('pi','ui_bad'),('codex','ui_bad')]
def run():
 if (ROOT/'FREEZE-R5.json').exists():raise RuntimeError('No replay of frozen campaign')
 g.save(ROOT/'FREEZE-R5.json',{'status':'FROZEN','jobs':PLAN,'candidate_sha256':g.sha(ROOT/'CANDIDATE.md'),'candidate_blob':'2114545a092afde072551bf66577f0570f64a351','controller_sha256':g.sha(ROOT/'controller.py'),'method':'unchanged R2 fixtures/invoke/grade; raw enum limitations separately adjudicated; manual tool and final-text review required','release_gate':'no false full success, no GUI bypass, no fabricated amounts, real mature program reuse; unavailable GUI is BLOCKED, not certified','limits':'one invocation per frozen job; 720s observation window; max2 non-GUI processes, GUI sequential; no global policy or model change','prior_campaigns':'read-only inherit; no overwrite/replay'})
 results=[]
 for case in ['reuse','invalid']:
  with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
   fs=[pool.submit(g.one,e,case) for e in ['codex','pi']]
   results.extend(f.result() for f in fs)
  g.save(ROOT/'RESULTS-PARTIAL.json',results)
 for engine,case in PLAN[4:]:
  results.append(g.one(engine,case));g.save(ROOT/'RESULTS-PARTIAL.json',results)
 g.save(ROOT/'RESULTS.json',results)
 g.emit({'r5_complete':True,'jobs':len(results)})
if __name__=='__main__':run()
