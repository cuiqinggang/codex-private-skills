"""Clean host-guidance controls: remove candidate documents from subject workspaces before invoking."""
from pathlib import Path
import concurrent.futures,hashlib,importlib.util,json,time
ROOT=Path(__file__).resolve().parent
BASE=Path('C:/Users/A/Documents/DSH-Workspace')
MAIN=BASE/'agent-guidance-gates-r2-20261109'
spec=importlib.util.spec_from_file_location('frozen_r2',MAIN/'controller.py')
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);g.ROOT=ROOT
prepare=g.prepare_case
def clean_prepare(engine,case,arm):
 w,protected=prepare(engine,case,arm)
 for n in ('GUIDANCE.md','AGENT-PLATFORM-ROUTING-V1.1.md'):
  (w/n).unlink();protected.pop(n,None)
 return w,protected
g.prepare_case=clean_prepare
def main():
 g.save(ROOT/'FREEZE.json',{'status':'FROZEN_BEFORE_EXECUTION','jobs':4,'cases':['unknown','ui_bad'],'arms':'existing host guidance only; no 159-line candidate or platform appendix in subject cwd','why':'R2 pi-unknown-control read GUIDANCE.md:1-80 despite no automatic injection. Original controls retained but disqualified from clean causal comparison.','source_r2_sha256':g.sha(MAIN/'controller.py'),'source_sha256':g.sha(Path(__file__)),'start_after':'R3 supplement complete; no resource overlap','limits':'one pair per engine for usability comparison only, not a universal latency/cost claim'})
 while not (BASE/'agent-guidance-gates-r3-20261109/RESULTS.json').exists():time.sleep(2)
 results=[]
 with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
  fs=[pool.submit(g.one,e,'unknown','control') for e in ['codex','pi']];results.extend(f.result() for f in fs)
 for e in ['codex','pi']:results.append(g.one(e,'ui_bad','control'))
 g.save(ROOT/'RESULTS.json',results);g.emit({'clean_control_complete':True,'jobs':4})
if __name__=='__main__':main()
