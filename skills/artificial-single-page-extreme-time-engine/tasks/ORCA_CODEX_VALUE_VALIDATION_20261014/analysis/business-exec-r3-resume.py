"""Bounded Orca terminal -> official Codex exec stdin T03 test. Not orchestration certification."""
import hashlib, json, os, pathlib, sqlite3, subprocess, time, shutil
import psutil
ROOT=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
TEST=ROOT/'business-exec-20261015-r3'
ASSETS=ROOT/'CEO_assets'
BUNDLE=ASSETS/'profile/orcad-artifacts/win32-x64/0.1.0+9e2e3cd709d0'
NODE=ASSETS/'profile/orcad-artifacts/win32-x64/runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe'
CLI=BUNDLE/'out/cli/index.js'
REC=TEST/'recovery-r1'
assert not REC.exists(),'Existing recovery: reconcile, never repeat'
assert psutil.virtual_memory().available>=4*1024**3
for p in psutil.process_iter(['pid','name','cmdline']):
    c=' '.join(p.info['cmdline'] or []).replace('\\','/').lower()
    if str(ROOT).replace('\\','/').lower() in c and p.info['name'].lower() in ('node.exe','codex.exe'):raise RuntimeError('Existing task process '+str(p.pid))
assert hashlib.sha256((TEST/'exec-start.json').read_bytes()).hexdigest()=='fecbdfbd5f2e416ecfe7409aa38870a99a481eb461c054bf01522d1cec801666'
assert hashlib.sha256((TEST/'result.json').read_bytes()).hexdigest()=='e7f6d74e01d441c9e31d20fc609aa1abcf5e25e93fda607db6aef914a9b7ffdc'
REC.mkdir()
profile=REC/'profile'
seed={'settings':{'workspaceDir':str(TEST/'worktrees'),'nestWorkspaces':True,'agentDefaultArgs':{'codex':'--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review -c service_tier=priority'},'agentDefaultEnv':{'codex':{}},'agentYoloDefaultsMigrated':True,'agentStatusHooksEnabled':False,'agentWorkspaceTrustEnabled':False,'experimentalNativeChat':False,'codexManagedAccounts':[],'activeCodexManagedAccountId':None,'activeCodexManagedAccountIdsByRuntime':{'host':None,'wsl':{}},'localWindowsRuntimeDefault':{'kind':'windows-host'},'terminalWindowsShell':'cmd.exe'}}
# The user authorized this exact isolated source task. Trust only its two roots,
# through an ephemeral CLI override; never persist global Codex trust.
trust_paths=[str(TEST/'fixture'),str(TEST/'worktrees/fixture/component')]
trust_table='{'+','.join("'"+p+"'={trust_level='trusted'}" for p in trust_paths)+'}'
seed['settings']['agentDefaultArgs']['codex']+=' -c "projects='+trust_table+'"'
data=profile/'profiles/local-default/orca-data.json'
data.parent.mkdir(parents=True)
data.write_text(json.dumps(seed),encoding='utf-8')

for name in ['scripts/run.py','tests/test_run_report_offline.py']:
    old=TEST/'worktrees/fixture/component'/name
    target=REC/'before'/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(old,target)
env=dict(os.environ,ORCA_USER_DATA=str(profile),ORCA_USER_DATA_PATH=str(profile),ORCA_VERSION='0.1.0+9e2e3cd709d0',ORCA_TELEMETRY_DISABLED='1',DO_NOT_TRACK='1')
result={'scope':'ORCA_TERMINAL_CODEX_EXEC_RESUME_T03_RECOVERY','started':time.time(),'checks':[]}
started=time.monotonic()
server=None
owned=[]
def command(args,cwd=TEST):
    r=subprocess.run([str(x) for x in args],cwd=cwd,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=25)
    if r.returncode: raise RuntimeError(str(args[:3])+': '+r.stdout[-2000:]+r.stderr[-2000:])
    return r.stdout
def cli(*args):
    out=command([NODE,CLI,*args,'--json'])
    obj=json.loads(out)
    if obj.get('ok') is False: raise RuntimeError(json.dumps(obj))
    return obj.get('result',obj)
try:
    with (REC/'server.stdout').open('w',encoding='utf-8') as stdout,(REC/'server.stderr').open('w',encoding='utf-8') as stderr:
        server=subprocess.Popen([str(NODE),str(BUNDLE/'orcad.js'),'--bind','127.0.0.1','--port','0','--no-pairing','--json'],env=env,cwd=TEST,stdout=stdout,stderr=stderr)
    deadline=time.monotonic()+60
    ready=False
    while time.monotonic()<deadline:
        if server.poll() is not None: raise RuntimeError('Server exited '+str(server.returncode))
        if 'orca_server_ready' in (REC/'server.stdout').read_text(encoding='utf-8'):
            ready=True; break
        time.sleep(.25)
    assert ready,'No ready payload within 60 seconds'
    result['checks'].append('OFFICIAL_STARTUP_IMPORT_READY')
    wt=json.loads((TEST/'result.json').read_text(encoding='utf-8'))['worktree']
    result['worktree']=wt
    source=ROOT/'dataset/source'
    result['registered_repo']=cli('repo','add','--path',str(TEST/'fixture'))
    result['worktree_selector']='path:'+wt['path']
    # Official noninteractive Codex: stdin contains UTF-8 request once; no paste or Enter replay.
    codex=pathlib.Path('C:/Users/A/AppData/Roaming/npm/node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe')
    assert command([codex,'--version']).strip()=='codex-cli 0.160.0'
    prompt='Resume only this exact unfinished T03. Previous controller stopped after 360s; no model remains. Existing tests/test_run_report_offline.py is retained and already fixes Windows path spelling and inherited temp directory creation. scripts/run.py is still original BAD. Complete the minimal report() zero-task guard for three rate fields (display -- for zero, retain nonzero percentages/spacing), run the existing five offline tests, fix only genuine local test issues, write DELIVERY.md with exact results, and finish. Do not spend time deleting old denied temp directories; leave them recorded. No ACL, global config, network changes, other tasks, model launches or credentials. Read only files needed in this worktree. Do not read parent recovery evidence or hidden checks.'
    prompt_file=REC/'prompt.txt';prompt_file.write_text(prompt,encoding='utf-8')
    result['prompt_sha256']=hashlib.sha256(prompt_file.read_bytes()).hexdigest()
    args=json.loads((TEST/'exec-start.json').read_text())['argv'][:-1]
    args[args.index('--output-last-message')+1]=str(REC/'last-message.txt')
    args+=['resume','01a140cc-584e-7c43-87a1-1f7ce24449c3','-']
    worker=REC/'exec-worker.py'
    worker_code="import os,json,pathlib,subprocess,time\n"+"base=pathlib.Path("+repr(str(REC))+")\n"+"args="+repr(args)+"\n"+"record={'handle':os.environ.get('ORCA_TERMINAL_HANDLE'),'cwd':os.getcwd(),'userprofile':os.environ.get('USERPROFILE'),'argv':args,'started':time.time()}\n"+"(base/'exec-start.json').write_text(json.dumps(record),encoding='utf-8')\n"+"with (base/'prompt.txt').open('rb') as inp,(base/'events.jsonl').open('wb') as out,(base/'exec.stderr').open('wb') as err:\n    p=subprocess.Popen(args,stdin=inp,stdout=out,stderr=err)\n    record['pid']=p.pid\n    (base/'exec-start.json').write_text(json.dumps(record),encoding='utf-8')\n    record['exit_code']=p.wait()\nrecord['ended']=time.time()\n(base/'exec-done.json').write_text(json.dumps(record),encoding='utf-8')\nprint('EXEC_PROCESS_ENDED',record['exit_code'])\n"
    worker.write_text(worker_code,encoding='utf-8')
    terminal=cli('terminal','create','--worktree','path:'+wt['path'],'--shell','cmd.exe','--title','T03 exec single task','--command','python -X utf8 "'+str(worker)+'"')['terminal']
    result['terminal']=terminal['handle']
    deadline=time.monotonic()+600
    while time.monotonic()<deadline and not (REC/'exec-done.json').exists():time.sleep(1)
    if not (REC/'exec-done.json').exists():raise RuntimeError('RESUME_TIMEOUT_600S_NO_REDISPATCH')
    result['exec']=json.loads((REC/'exec-done.json').read_text())
    assert result['exec']['handle']==terminal['handle'],'Orca terminal identity mismatch'
    assert pathlib.Path(result['exec']['cwd']).resolve()==pathlib.Path(wt['path']).resolve()
    result['terminal_output']=cli('terminal','read','--terminal',terminal['handle'])
    import importlib.util
    validator=ROOT/'tools/independent_check_CEO_FROZEN.py'
    assert hashlib.sha256(validator.read_bytes()).hexdigest()=='2d6f62b3205454ce5758c98c0160d7aa03b2820f7f05f9c1302a89651cb24979'
    qaspec=importlib.util.spec_from_file_location('qa',validator);qa=importlib.util.module_from_spec(qaspec);qaspec.loader.exec_module(qa)
    def selected(path):return [r for r in qa.check(path) if r['name'].startswith('T03_') or r['name']=='ALL_source_compile']
    result['bad_checks']=selected(source)
    result['candidate_checks']=selected(pathlib.Path(wt['path']))
    result['delivery_exists']=(pathlib.Path(wt['path'])/'DELIVERY.md').exists()
    result['git_diff']=command(['git','diff','--stat'],pathlib.Path(wt['path']))
    result['git_status']=command(['git','status','--porcelain'],pathlib.Path(wt['path']))
    result['passed']=result['exec']['exit_code']==0 and result['delivery_exists'] and len(result['candidate_checks'])==3 and all(x['passed'] for x in result['candidate_checks']) and any(not x['passed'] for x in result['bad_checks'])
    result['status']='T03_RECOVERY_QA_ACCEPTED_LIMITED_TERMINAL_ROUTE' if result['passed'] else 'T03_QA_REJECTED'
    result['terminal_close']=cli('terminal','close','--terminal',terminal['handle'])

except Exception as e:
    result['passed']=False;result['error']=str(e)
finally:
    if server and server.poll() is None:
        parent=psutil.Process(server.pid)
        owned=parent.children(recursive=True)
        # This test owns these processes by ancestry; never match/kill by process name.
        for proc in reversed(owned):
            try:proc.terminate()
            except psutil.NoSuchProcess:pass
        server.terminate()
        psutil.wait_procs(owned,timeout=5)
        server.wait(timeout=5)
    result['remaining_owned']=[p.pid for p in owned if p.is_running()]
    result['elapsed_ms']=1000*(time.monotonic()-started)
    (REC/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert json.loads((REC/'result.json').read_text(encoding='utf-8'))==json.loads(json.dumps(result))
    print(json.dumps(result))
