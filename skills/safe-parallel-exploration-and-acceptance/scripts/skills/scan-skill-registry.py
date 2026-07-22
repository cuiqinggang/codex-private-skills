from __future__ import annotations
import argparse, csv, json, re
from datetime import datetime, timezone
from pathlib import Path

EXCLUDE_PARTS={'.git','__pycache__','node_modules','.venv','venv','dist','build','.cache','cache'}
BACKUP_WORDS=('backup','backups','archive','archives','old','deprecated','quarantine','before-')
L3_WORDS=('ultrafusion','long-coding','orchestrator','system-evolution','knowledgebrain','knowledge-brain','complete-claude','super-tool','fugu','ecc-','multi-agent','parallel-exploration','hooks')
L2_WORDS=('video','ppt','browser','computer-use','automation','github','website','site','saas','obsidian','playwright','docker','recovery','repair','governance','pipeline','production')
P0_WORDS=('ultrafusion-low-cost-multi-model-extreme-fusion','ultrafusion-v8-minimal-pressure-chain','safe-parallel-exploration-and-acceptance')
P1_WORDS=('long-coding-flow','knowledgebrain','knowledge-brain','indie-site-reference-factory','one-person-saas-os','video-production-and-editing','ppt-video-router','cursor-kilo-supertool')

def frontmatter(text:str):
    if not text.startswith('---'):
        return {},False
    parts=text.split('---',2)
    if len(parts)<3:return {},False
    data={}
    for line in parts[1].splitlines():
        if ':' in line:
            k,v=line.split(':',1);data[k.strip()]=v.strip().strip('"\'')
    return data,bool(data.get('name') and data.get('description'))

def find_repo(path:Path):
    for p in (path,*path.parents):
        if (p/'.git').exists():return str(p)
    return ''

def iter_files(root:Path):
    for p in root.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(root)
        if any(x in EXCLUDE_PARTS for x in rel.parts):continue
        yield p,rel

def inspect(path:Path,root_rank:int):
    skill=path/'SKILL.md'
    text=skill.read_text(encoding='utf-8-sig',errors='replace')[:20000]
    fm,ok=frontmatter(text)
    files=list(iter_files(path)); names=[str(r).replace('\\','/') for _,r in files]; lower=[n.lower() for n in names]
    total=sum(p.stat().st_size for p,_ in files); latest=max((p.stat().st_mtime for p,_ in files),default=path.stat().st_mtime)
    scripts=sum(1 for n in lower if n.startswith('scripts/') or n.endswith(('.ps1','.py','.js','.ts','.cmd','.bat')))
    tests=sum(1 for n in lower if n.startswith('tests/') or 'test' in Path(n).name)
    templates=sum(1 for n in lower if n.startswith('templates/') or 'template' in n)
    examples=sum(1 for n in lower if n.startswith('examples/') or 'example' in n)
    backups=sum(1 for n in lower if any(w in n.split('/') for w in BACKUP_WORDS) or any(w in n for w in ('/backups/','/archive/','/old/','/quarantine/')))
    large=sum(1 for p,_ in files if p.stat().st_size>=10*1024*1024 or p.suffix.lower() in {'.mp4','.mov','.mkv','.onnx','.safetensors','.ckpt','.zip'})
    sensitive=sum(1 for p,_ in files if re.search(r'(^\.env($|\.)|token|credential|api[_-]?key|password|\.(pem|key|pfx|p12)$)',p.name,re.I) and p.name.lower()!='secret_handling.md')
    name=fm.get('name') or path.name; lname=name.lower()
    has_readme=any(Path(n).name.lower() in ('readme.md','readme_cn.md') for n in names)
    rollback=any('rollback' in n or '回滚' in n for n in lower)
    acceptance=tests>0 or any('acceptance' in n or '验收' in n for n in lower)
    incomplete=not ok or len(files)<1
    bloated=len(files)>300 or total>40*1024*1024 or backups>50
    if incomplete: level='MANUAL_REVIEW_REQUIRED'
    elif any(w in lname for w in L3_WORDS):level='L3'
    elif any(w in lname for w in L2_WORDS) or scripts>=3 or len(files)>25:level='L2'
    elif scripts or templates or examples or len(files)>5:level='L1'
    else:level='L0'
    priority='P0' if any(w==lname or w in lname for w in P0_WORDS) else ('P1' if any(w in lname for w in P1_WORDS) else ('P2' if level in ('L2','L3') else 'P3'))
    issues=[]
    if not ok:issues.append('invalid_or_missing_frontmatter')
    if backups:issues.append(f'backup_or_archive_files:{backups}')
    if bloated:issues.append('possible_bloat')
    if large:issues.append(f'large_files:{large}')
    if sensitive:issues.append(f'sensitive_name_review:{sensitive}')
    next_action={'L0':'basic_check_only','L1':'use_existing_shared_repo_and_one_round_validation','L2':'single_worktree_when_upgrading','L3':'prepare_baseline_and_route_plan_before_major_change','MANUAL_REVIEW_REQUIRED':'manual_structure_review'}[level]
    return {
      'skill_id':path.name,'name':name,'active_path':str(path),'root_rank':root_rank,'repository_root':find_repo(path),'is_active':True,'duplicate_paths':[],
      'version':next((m.group(1) for m in re.finditer(r'(?i)\b(?:version|v)\s*[:=]?\s*(\d+(?:\.\d+){1,3}(?:[-\w.]*)?)',text)),''),
      'last_modified':datetime.fromtimestamp(latest,timezone.utc).isoformat(),'purpose':fm.get('description','')[:500],'file_count':len(files),'total_bytes':total,
      'has_scripts':scripts>0,'script_count':scripts,'has_tests':tests>0,'test_count':tests,'has_templates':templates>0,'has_examples':examples>0,'has_readme':has_readme,
      'has_rollback':rollback,'has_acceptance':acceptance,'large_file_count':large,'sensitive_name_count':sensitive,'structure_complete':ok,'possible_bloat':bloated,
      'backup_archive_file_count':backups,'rule_duplication_review':backups>20,'obvious_incomplete':incomplete,'continuously_updated':latest>(datetime.now().timestamp()-120*86400),
      'failure_impact':'high' if level=='L3' else ('medium' if level=='L2' else 'low'),'multi_route_value':level=='L3','management_level':level,'priority':priority,
      'recommended_acceptance':'three_round_final_gate' if level=='L3' else ('route_gate' if level=='L2' else ('one_round_diff_check' if level=='L1' else 'basic_check')),
      'baseline_status':'GIT_READY' if find_repo(path) else 'BASELINE_CANDIDATE','worktree_ready':bool(find_repo(path)),'hooks_level':'LEVEL-3' if level=='L3' else ('LEVEL-2' if level=='L2' else 'LEVEL-1'),
      'environment_type':'skill','project_profile':'','last_reviewed_at':datetime.now(timezone.utc).isoformat(),'next_action':next_action,'issues':issues
    }

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--root',action='append',required=True);ap.add_argument('--output-dir',required=True);a=ap.parse_args()
    candidates=[]
    for rank,raw in enumerate(a.root):
        root=Path(raw)
        if not root.is_dir():continue
        for child in sorted(root.iterdir(),key=lambda p:p.name.lower()):
            if not child.is_dir() or not (child/'SKILL.md').is_file():continue
            if any(w in child.name.lower() for w in BACKUP_WORDS):continue
            candidates.append(inspect(child,rank))
    by_name={}
    for r in candidates:by_name.setdefault(r['name'].lower(),[]).append(r)
    active=[];duplicate_count=0
    for group in by_name.values():
        group.sort(key=lambda x:(x['root_rank'],-datetime.fromisoformat(x['last_modified']).timestamp()))
        chosen=group[0];chosen['duplicate_paths']=[x['active_path'] for x in group[1:]];duplicate_count+=len(group)-1;active.append(chosen)
    active.sort(key=lambda x:x['name'].lower())
    out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True)
    registry=out/'skill-exploration-registry.json';registry.write_text(json.dumps(active,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    fields=['skill_id','name','active_path','repository_root','is_active','duplicate_paths','version','last_modified','purpose','file_count','total_bytes','has_scripts','has_tests','has_templates','has_examples','has_readme','has_rollback','has_acceptance','large_file_count','sensitive_name_count','structure_complete','possible_bloat','backup_archive_file_count','rule_duplication_review','obvious_incomplete','continuously_updated','failure_impact','multi_route_value','management_level','priority','recommended_acceptance','baseline_status','worktree_ready','hooks_level','environment_type','project_profile','last_reviewed_at','next_action','issues']
    csvp=out/'27_现有技能包探索适配总表.csv'
    with csvp.open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
        for r in active:w.writerow({k:json.dumps(r[k],ensure_ascii=False) if isinstance(r[k],list) else r[k] for k in fields})
    md=['# 27 现有技能包探索适配总表','',f'- 原始候选：{len(candidates)}',f'- 去重后活动技能：{len(active)}',f'- 重复副本：{duplicate_count}','','| 编号 | 技能 | 活动路径 | 所属仓库 | 模式 | 优先级 | 风险 | 建议 |','|---:|---|---|---|---|---|---|---|']
    for i,r in enumerate(active,1):md.append(f"| {i} | {r['name']} | `{r['active_path']}` | `{r['repository_root']}` | {r['management_level']} | {r['priority']} | {r['failure_impact']} | {r['next_action']} |")
    (out/'27_现有技能包探索适配总表.md').write_text('\n'.join(md)+'\n',encoding='utf-8')
    labels={'L0':'28_L0无需复杂管理技能包.md','L1':'29_L1轻量版本管理技能包.md','L2':'30_L2单路线安全探索技能包.md','L3':'31_L3多路线并行探索技能包.md','MANUAL_REVIEW_REQUIRED':'32_需要人工确认技能包.md'}
    for level,file in labels.items():
        rows=[r for r in active if r['management_level']==level];lines=[f'# {level} 技能包','',f'- 数量：{len(rows)}','']+[f"- `{r['name']}` — `{r['active_path']}` — {r['priority']} — {r['next_action']}" for r in rows]
        (out/file).write_text('\n'.join(lines)+'\n',encoding='utf-8')
    dup=['# 33 重复、过期、残缺技能包报告','',f'- 去重副本数：{duplicate_count}','']
    for r in active:
        if r['duplicate_paths'] or r['obvious_incomplete'] or r['backup_archive_file_count']:
            dup.append(f"- `{r['name']}`: duplicates={r['duplicate_paths']}; incomplete={r['obvious_incomplete']}; backup/archive files={r['backup_archive_file_count']}")
    (out/'33_重复过期残缺技能包报告.md').write_text('\n'.join(dup)+'\n',encoding='utf-8')
    quality=['# 34 技能包结构与质量问题报告','']
    for r in active:
        if r['issues']:quality.append(f"- `{r['name']}`: {', '.join(r['issues'])}")
    (out/'34_技能包结构与质量问题报告.md').write_text('\n'.join(quality)+'\n',encoding='utf-8')
    counts={l:sum(r['management_level']==l for r in active) for l in labels}
    print(json.dumps({'raw_candidates':len(candidates),'active_deduplicated':len(active),'duplicate_count':duplicate_count,'counts':counts,'p0':[r['name'] for r in active if r['priority']=='P0'],'p1':[r['name'] for r in active if r['priority']=='P1'],'registry':str(registry)},ensure_ascii=False,indent=2))

if __name__=='__main__':main()
