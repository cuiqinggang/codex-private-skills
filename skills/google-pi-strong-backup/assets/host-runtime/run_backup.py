"""Versioned strong-backup adapter: accepted Pi runtime, original ACL and native resume."""
import argparse,importlib.util,json,os,pathlib,re,subprocess,sys,yaml,hashlib,shutil
ROOT=pathlib.Path(__file__).resolve().parent
PI=pathlib.Path(r'C:\Users\A\Documents\DSH-Workspace\pi-capability-enhancement-20261028\launch_pi.py')
CORE=pathlib.Path(r'C:\Users\A\Documents\DSH-Workspace\pi-unified-upgrade-20261030\unified_runtime.py')
OLD=pathlib.Path(r'C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent\skills\google-deepseek-strong-backup\scripts\run_backup.py')
def preflight():
    checks={'pi_entry':PI.is_file(),'accepted_core':CORE.is_file(),'binding_policy':(ROOT/'HOST-POLICY.md').is_file(),'legacy_rollback':OLD.is_file()}
    return {'version':'2.0.0-pi-google','executor':'Official Oh My Pi / existing DeepSeek provider','status':'PASS' if all(v for k,v in checks.items() if k!='legacy_rollback') else 'BLOCKED','checks':checks,'scope':'presence only; business acceptance separate'}
def readonly_root(cwd):
    key=hashlib.sha256(str(cwd).lower().encode()).hexdigest()[:20]
    state=ROOT/'readonly-runtime'/key
    if state.is_relative_to(cwd) or cwd.is_relative_to(state):
        state=pathlib.Path(os.environ['LOCALAPPDATA'])/'Pi-StrongBackup-V2'/'readonly'/key
    return state
def validate_session(cwd,session,permission='workspace-write'):
    root=(readonly_root(cwd)/'.omp/sessions' if permission=='read-only' else cwd/'.omp/sessions').resolve()
    candidate=pathlib.Path(session)
    if candidate.is_absolute() or '/' in session or '\\' in session:
        candidate=candidate.resolve(strict=True)
        if not candidate.is_relative_to(root):raise ValueError('OMP session must belong to original cwd session directory')
        candidates=[candidate]
    else:
        if not re.fullmatch(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}',session):
            raise ValueError('Use a full native OMP session UUID; DSH sessions are not interchangeable')
        candidates=[p for p in root.glob('*.jsonl') if session.lower() in p.name.lower()]
    for p in candidates:
        with p.open(encoding='utf-8-sig') as f:
            for _ in range(8):
                line=f.readline()
                if not line:break
                value=json.loads(line)
                if value.get('type')=='session':
                    if pathlib.Path(value.get('cwd','')).resolve()!=cwd:raise ValueError('Native OMP session cwd mismatch')
                    if not (candidate.is_absolute() or '/' in session or '\\' in session) and value.get('id')!=session:raise ValueError('Native OMP session ID mismatch')
                    return session
                if value.get('type')!='title':break
    raise ValueError('Native OMP session header not found in original cwd')

def command(cwd,task,session=None,permission='workspace-write'):
    spec=importlib.util.spec_from_file_location('accepted_pi_core',CORE)
    core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
    run_cwd=readonly_root(cwd) if permission=='read-only' else cwd
    run_cwd.mkdir(parents=True,exist_ok=True)
    cmd,env=core.command(run_cwd,task,session)
    # Keep the accepted runtime policy verbatim, add only the strong-backup binding.
    i=cmd.index('--append-system-prompt')+1
    profile=run_cwd/'.omp/agent'; policy=profile/'strong-backup-policy.md'
    config_path=profile/'config.yml';config=yaml.safe_load(config_path.read_text(encoding='utf-8'))
    config['skills']['customDirectories']=[str(ROOT/'skills'),*config['skills']['customDirectories']]
    config['skills']['includeSkills']=list(dict.fromkeys([*config['skills'].get('includeSkills',[]),'google-pi-strong-backup']))
    config_path.write_text(yaml.safe_dump(config,allow_unicode=True,sort_keys=False),encoding='utf-8')
    policy.write_text(pathlib.Path(cmd[i]).read_text(encoding='utf-8')+'\n'+(ROOT/'HOST-POLICY.md').read_text(encoding='utf-8'),encoding='utf-8')
    cmd[i]=str(policy)
    runner_mode=cmd.index('--mode')+1
    assert cmd[runner_mode]=='workspace-write'
    # The mature runner grants writes only to run_cwd. For read-only business
    # operations run_cwd is a separate metadata directory, never the input cwd.
    cmd[runner_mode]='workspace-write'
    if permission=='read-only':
        assert pathlib.Path(cmd[cmd.index('--workspace')+1]).resolve()==run_cwd.resolve()
        assert not cwd.is_relative_to(run_cwd) and not run_cwd.is_relative_to(cwd)
        cmd[-1:-1]=['--cwd',str(cwd)]
    for key in ('OPENAI_API_KEY','CODEX_API_KEY','ANTHROPIC_API_KEY'):env.pop(key,None)
    return cmd,env
def main():
    p=argparse.ArgumentParser(description='Strong backup V2: Pi primary; Google on demand; DSH explicit rollback only')
    p.add_argument('--check',action='store_true');p.add_argument('--cwd',type=pathlib.Path)
    p.add_argument('--task-file',type=pathlib.Path);p.add_argument('--google-plan',type=pathlib.Path)
    p.add_argument('--session-id','--resume',dest='session');p.add_argument('--permission',choices=['read-only','workspace-write'],default='workspace-write')
    p.add_argument('--json',action='store_true');p.add_argument('--print',dest='one_shot',action='store_true')
    p.add_argument('--mode',choices=['auto','browser','deep','delivery','docs','automation'],default='auto',help='Task category hint; Pi uses unified native routing')
    p.add_argument('task',nargs='*');a=p.parse_args()
    check=preflight()
    if a.check or check['status']!='PASS':
        print(json.dumps(check,ensure_ascii=True));return 0 if check['status']=='PASS' else 2
    if a.session and not a.cwd:p.error('Resume requires original --cwd')
    if a.google_plan:
        plan=a.google_plan.read_text(encoding='utf-8-sig')
        if not plan.startswith('GOOGLE_BRAIN_PLAN_V1') or not 100<=len(plan)<=18000:p.error('Invalid Google plan envelope')
        if re.search(r'sk-[A-Za-z0-9_-]{24,}|AIza[A-Za-z0-9_-]{25,}|BEGIN (?:RSA |OPENSSH )?PRIVATE KEY|(?:password|api.?key)\s*[:=]\s*\S{10,}',plan,re.I):p.error('Plan may contain credentials')
        task='User-authorized Google plan, external advice; verify against local facts and authorized scope. Origin not independently authenticated:\n'+plan
    elif a.task_file:task=a.task_file.read_text(encoding='utf-8-sig')
    else:task=' '.join(a.task) if a.task else input('Task: ').strip()
    if not task.strip():p.error('Empty task')
    entered = input('Workspace (Enter = existing DSH-Workspace): ').strip().strip('"') if not a.cwd else None
    cwd=(a.cwd or pathlib.Path(entered or r'C:\Users\A\Documents\DSH-Workspace')).resolve(strict=True)
    if not cwd.is_dir():p.error('Workspace must be an existing authorized directory')
    if a.session:
        try:validate_session(cwd,a.session,a.permission)
        except (ValueError,OSError) as ex:p.error(str(ex))
    if a.mode!='auto':task='Task category hint: '+a.mode+'; use native Pi routing.\n'+task
    cmd,env=command(cwd,task,a.session,a.permission)
    if not a.json:
        i=cmd.index('--mode',cmd.index('--')+1)
        assert cmd[i+1]=='json';del cmd[i:i+2]
    if not (a.one_shot or a.task_file or a.google_plan):cmd.remove('--print')
    return subprocess.call(cmd,cwd=cwd,env=env,stdin=subprocess.DEVNULL if a.one_shot else None)
if __name__=='__main__':raise SystemExit(main())
