from __future__ import annotations
import argparse, json
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument('--project-path',required=True); p.add_argument('--task-description',required=True)
p.add_argument('--risk',choices=['low','medium','high','critical'],default='medium'); p.add_argument('--file-count',type=int,default=1)
p.add_argument('--stable-version',action='store_true'); p.add_argument('--multiple-solutions',action='store_true'); p.add_argument('--parallel',action='store_true')
p.add_argument('--rollback-required',action='store_true'); p.add_argument('--formal-delivery',action='store_true'); p.add_argument('--default-level',choices=['L0','L1','L2','L3','UNKNOWN'],default='UNKNOWN')
a=p.parse_args(); score={'low':0,'medium':2,'high':4,'critical':6}[a.risk]
score += 2*a.stable_version + 3*a.multiple_solutions + 3*a.parallel + 2*a.rollback_required + 2*a.formal_delivery + (a.file_count>5) + (a.file_count>20)
score=max(score, {'L2':4,'L3':7}.get(a.default_level,0))
mode='MODE-A' if a.risk=='low' and not a.multiple_solutions and not a.parallel and a.file_count<=2 else ('MODE-C' if score>=7 else 'MODE-B')
print(json.dumps({'schema_version':'1.0','project_path':str(Path(a.project_path).resolve()),'task_description':a.task_description,'score':score,'mode':mode,'git_required':mode!='MODE-A','worktree_required':mode!='MODE-A','three_round_tests':mode=='MODE-C' or a.formal_delivery,'screenshots_required':a.formal_delivery,'zip_required':a.formal_delivery,'manual_review_required':a.risk in ('high','critical') or a.stable_version,'integration_candidate_required':mode=='MODE-C'},ensure_ascii=False,indent=2))

