from __future__ import annotations
import argparse, hashlib, json, re
from pathlib import Path
from datetime import datetime, timezone

def slug(s):return re.sub(r'[^a-z0-9._-]+','-',s.lower()).strip('-')[:80] or 'skill'
def routes(name):
    n=name.lower()
    if 'ultrafusion' in n:return [('UF-A','极低成本'),('UF-B','最高质量'),('UF-C','高性价比'),('UF-D','自动化'),('UF-E','抗臃肿'),('UF-F','人工操作极简')]
    if 'long-coding' in n or 'orchestrator' in n:return [('LF-A','完整严格版'),('LF-B','精简高性价比版'),('LF-C','失败恢复强化版'),('LF-D','检查点续跑版'),('LF-E','反自我验收版'),('LF-F','上下文压缩版')]
    if any(x in n for x in ('site','saas','website')):return [('WEB-A','高还原度'),('WEB-B','高速度生成'),('WEB-C','低成本部署'),('WEB-D','SEO与转化'),('WEB-E','合规与原创化'),('WEB-F','可维护组件化')]
    return [('A','稳定严格'),('B','低成本'),('C','高质量'),('D','失败恢复')]

def main():
    p=argparse.ArgumentParser();p.add_argument('--registry',required=True);p.add_argument('--output-dir',required=True);a=p.parse_args()
    reg=json.loads(Path(a.registry).read_text(encoding='utf-8-sig'));out=Path(a.output_dir);out.mkdir(parents=True,exist_ok=True);made=[]
    for r in reg:
        if r['priority'] not in ('P0','P1'):continue
        d=out/slug(r['skill_id']);d.mkdir(parents=True,exist_ok=True);skill=Path(r['active_path'])/'SKILL.md';sha=hashlib.sha256(skill.read_bytes()).hexdigest().upper() if skill.exists() else ''
        rs=routes(r['name']);route_lines='\n'.join(f"- {i}: {n}" for i,n in rs)
        baseline='BASELINE_READY_NEEDS_CONFIRMATION' if not r['repository_root'] else ('GIT_READY' if r['baseline_status']=='GIT_READY' else r['baseline_status'])
        profile=f"""# Project Profile

- Name: {r['name']}
- Official path: `{r['active_path']}`
- Repository root: `{r['repository_root']}`
- Current version marker: `{r['version']}`
- Management level: `{r['management_level']}`
- Priority: `{r['priority']}`
- Baseline status: `{baseline}`
- Formal project modified: no
- Worktrees created: 0
"""
        (d/'PROJECT_PROFILE.md').write_text(profile,encoding='utf-8')
        data={'schema_version':'1.0','name':r['name'],'official_path':r['active_path'],'repository_root':r['repository_root'],'version':r['version'],'skill_sha256':sha,'management_level':r['management_level'],'priority':r['priority'],'baseline_status':baseline,'recommended_routes':[{'id':i,'name':n} for i,n in rs],'formal_project_modified':False,'worktrees_created':0,'generated_at':datetime.now(timezone.utc).isoformat()}
        (d/'project-profile.json').write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        (d/'VERSION_BASELINE.md').write_text(f"# Version Baseline\n\n- SKILL SHA256: `{sha}`\n- Version marker: `{r['version']}`\n- Git repository: `{r['repository_root']}`\n- Status: `{baseline}`\n- Formal baseline commit requires user confirmation when no repository exists.\n",encoding='utf-8')
        (d/'EXPLORATION_READINESS.md').write_text(f"# Exploration Readiness\n\n- Status: `PREATTACHED_NO_WORKTREES`\n- Default level: `{r['management_level']}`\n- Baseline: `{baseline}`\n- Existing stable files untouched: yes\n- Suggested routes:\n{route_lines}\n",encoding='utf-8')
        (d/'RECOMMENDED_MODE.md').write_text(f"# Recommended Mode\n\n- Default: `{r['management_level']}`.\n- Small documentation fixes may downgrade to L1.\n- Architecture changes may upgrade to L3.\n- Actual mode must be recalculated per task.\n",encoding='utf-8')
        (d/'RISK_REGISTER.md').write_text("# Risk Register\n\n- Stable-version contamination: block by separate worktree.\n- Secret/large-file inclusion: scan names and Git index before commit.\n- Route bloat: compare context length and rule duplication.\n- False PASS: require independent evidence and final integration gate.\n- Cleanup loss: never remove dirty or unconfirmed worktrees.\n",encoding='utf-8')
        (d/'NEXT_ACTIONS.md').write_text("# Next Actions\n\n1. Confirm the authoritative stable version.\n2. Confirm or establish a formal Git baseline only with user approval.\n3. Finalize metrics and route count.\n4. Preview branches and worktree paths.\n5. Wait for explicit start confirmation.\n",encoding='utf-8')
        r['project_profile']=str(d/'PROJECT_PROFILE.md')
        made.append(str(d))
    Path(a.registry).write_text(json.dumps(reg,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'profile_count':len(made),'profiles':made},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
