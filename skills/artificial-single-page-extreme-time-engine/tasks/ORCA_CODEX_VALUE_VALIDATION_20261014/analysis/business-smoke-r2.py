"""One bounded isolated Orca component test; no model dispatch, no credentials."""
import hashlib, json, os, pathlib, sqlite3, subprocess, time, shutil
import psutil
ROOT=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
TEST=ROOT/'business-smoke-20261015-r2'
ASSETS=ROOT/'CEO_assets'
BUNDLE=ASSETS/'profile/orcad-artifacts/win32-x64/0.1.0+9e2e3cd709d0'
NODE=ASSETS/'profile/orcad-artifacts/win32-x64/runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe'
CLI=BUNDLE/'out/cli/index.js'
assert not TEST.exists(), 'Existing attempt: reconcile; never replay'
assert psutil.virtual_memory().available>=4*1024**3, '4 GiB reserve'
for p,expected in [(NODE,'ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32'),(BUNDLE/'orcad-server.js','bea1e0ce0f5cd40a046a40c04ef5e66c9e38ce110387f35d5b54abccf65cb8ba')]:
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected, str(p)
TEST.mkdir()
profile=TEST/'profile'
seed={'settings':{'workspaceDir':str(TEST/'worktrees'),'nestWorkspaces':True,'agentDefaultArgs':{'codex':'--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review -c service_tier=priority'},'agentDefaultEnv':{'codex':{}},'agentYoloDefaultsMigrated':True,'agentStatusHooksEnabled':False,'agentWorkspaceTrustEnabled':False,'experimentalNativeChat':False,'codexManagedAccounts':[],'activeCodexManagedAccountId':None,'activeCodexManagedAccountIdsByRuntime':{'host':None,'wsl':{}},'localWindowsRuntimeDefault':{'kind':'windows-host'},'terminalWindowsShell':'cmd.exe'}}
# The user authorized this exact isolated source task. Trust only its two roots,
# through an ephemeral CLI override; never persist global Codex trust.
trust_paths=[str(TEST/'fixture'),str(TEST/'worktrees/fixture/component')]
trust_table='{'+','.join("'"+p+"'={trust_level='trusted'}" for p in trust_paths)+'}'
seed['settings']['agentDefaultArgs']['codex']+=' -c "projects='+trust_table+'"'
data=profile/'profiles/local-default/orca-data.json'
data.parent.mkdir(parents=True)
data.write_text(json.dumps(seed),encoding='utf-8')
env=dict(os.environ,ORCA_USER_DATA=str(profile),ORCA_USER_DATA_PATH=str(profile),ORCA_VERSION='0.1.0+9e2e3cd709d0',ORCA_TELEMETRY_DISABLED='1',DO_NOT_TRACK='1')
result={'scope':'SINGLE_T03_SMOKE_NOT_FULL_REALITY','started':time.time(),'checks':[]}
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
    with (TEST/'server.stdout').open('w',encoding='utf-8') as stdout,(TEST/'server.stderr').open('w',encoding='utf-8') as stderr:
        server=subprocess.Popen([str(NODE),str(BUNDLE/'orcad.js'),'--bind','127.0.0.1','--port','0','--no-pairing','--json'],env=env,cwd=TEST,stdout=stdout,stderr=stderr)
    deadline=time.monotonic()+60
    ready=False
    while time.monotonic()<deadline:
        if server.poll() is not None: raise RuntimeError('Server exited '+str(server.returncode))
        if 'orca_server_ready' in (TEST/'server.stdout').read_text(encoding='utf-8'):
            ready=True; break
        time.sleep(.25)
    assert ready,'No ready payload within 60 seconds'
    result['checks'].append('OFFICIAL_STARTUP_IMPORT_READY')
    db=profile/'profiles/local-default/profile-state.db'
    con=sqlite3.connect(db.as_uri()+'?mode=ro',uri=True)
    tables=con.execute("SELECT name,sql FROM sqlite_master WHERE type='table'").fetchall()
    settings=json.loads(con.execute("SELECT payload FROM profile_state_documents WHERE domain='settings'").fetchone()[0])
    for key,value in seed['settings'].items():
        if key not in ('agentDefaultArgs','agentDefaultEnv'): assert settings[key]==value,key
    assert settings['agentDefaultArgs']['codex']==seed['settings']['agentDefaultArgs']['codex']
    result['effective_settings_verified']=True
    con.close()
    manifest=json.loads((ROOT/'DATASET_MANIFEST.json').read_text(encoding='utf-8-sig'))
    source=ROOT/'dataset/source'
    repo=TEST/'fixture';repo.mkdir()
    for entry in manifest['input_files']:
        path=entry['path']; original=source/path
        assert hashlib.sha256(original.read_bytes()).hexdigest()==entry['sha256'],path
        target=repo/path;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,target)
    (repo/'AGENTS.md').write_text('Only perform requests/T03.md. Do not perform T01 or T02. Modify only scripts/run.py, your offline tests and DELIVERY.md in this worktree. Do not read parent directories, credentials, historical solutions or hidden tests. Do not use network, other models, elevated permissions or alter global configuration. Run offline standard-library tests; no real verifier API. Write DELIVERY.md only after finishing, including commands and results.',encoding='utf-8')
    for args in [['init','-b','main'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','add','.'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','commit','-m','fixture']]:
        command(['git',*args],repo)
    registered=cli('repo','add','--path',str(repo))['repo']
    wt=cli('worktree','create','--repo','id:'+registered['id'],'--name','component','--setup','skip','--no-parent')['worktree']
    result['worktree']=wt
    assert pathlib.Path(wt['path']).is_relative_to(TEST)
    request=(repo/'requests/T03.md').read_text(encoding='utf-8')
    objective='One isolated T03 BAD replay; no other task; no production changes.'
    spec=request+'\nOnly this new worktree. Follow AGENTS.md. Finish offline tests then write DELIVERY.md.'
    launch=TEST/'dispatch.json'
    coordinator=TEST/'coordinator.cjs'
    code="const fs=require('node:fs'),cp=require('node:child_process');const cli="+json.dumps(str(CLI))+";const file="+json.dumps(str(launch))+";function call(a){const r=cp.spawnSync(process.execPath,[cli,...a,'--json'],{encoding:'utf8',timeout:70000,env:process.env});let j;try{j=JSON.parse(r.stdout)}catch(e){throw new Error('CLI exit '+r.status+' '+r.stderr)};if(!j.ok)throw new Error(JSON.stringify(j));return j.result;}try{const run=call(['orchestration','run-create','--objective',"+json.dumps(objective)+"]);fs.writeFileSync(file,JSON.stringify({stage:'RUN_CREATED',run,terminal:process.env.ORCA_TERMINAL_HANDLE}));const worker=call(['orchestration','worker-start','--run',run.run.id,'--spec',"+json.dumps(spec)+",'--worktree','current','--agent','codex','--model','gpt-6.1-sol','--effort','ultra','--timeout-ms','45000']);fs.writeFileSync(file,JSON.stringify({stage:'DISPATCH_RETURNED',run,worker,terminal:process.env.ORCA_TERMINAL_HANDLE}));}catch(e){fs.writeFileSync(file,JSON.stringify({stage:'ERROR',error:String(e),terminal:process.env.ORCA_TERMINAL_HANDLE}));}"
    coordinator.write_text(code,encoding='utf-8')
    terminal=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','T03 coordinator','--command','"'+str(NODE)+'" "'+str(coordinator)+'"')['terminal']
    result['coordinator']=terminal['handle']
    deadline=time.monotonic()+85
    while time.monotonic()<deadline:
        if launch.exists():
            dispatch=json.loads(launch.read_text())
            if dispatch['stage']!='RUN_CREATED':break
        time.sleep(.5)
    else:raise RuntimeError('Coordinator outcome unknown: reconcile exact run; do not redispatch')
    result['dispatch']=dispatch
    assert dispatch['terminal']==terminal['handle'],'Coordinator identity mismatch'
    assert dispatch['stage']=='DISPATCH_RETURNED',dispatch
    processes=[]
    for p in psutil.Process(server.pid).children(recursive=True):
        try:
            if p.name().lower()=='codex.exe':processes.append({'pid':p.pid,'exe':p.exe(),'argv':p.cmdline()})
        except psutil.NoSuchProcess:pass
    result['codex_processes']=processes
    assert dispatch['worker'].get('state')=='ready',dispatch['worker']
    (TEST/'launch-result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    deadline=time.monotonic()+180
    while time.monotonic()<deadline and not (pathlib.Path(wt['path'])/'DELIVERY.md').exists():time.sleep(1)
    result['delivery_exists']=(pathlib.Path(wt['path'])/'DELIVERY.md').exists()
    result['terminals']=cli('terminal','list','--worktree',wt['id'])
    result['passed']=False
    result['status']='READY_FOR_INDEPENDENT_QA' if result['delivery_exists'] else 'BOUNDED_WAIT_ENDED_REVIEW_TERMINALS'
    for item in result['terminals'].get('terminals',[]):
        handle=item.get('handle')
        if handle:result.setdefault('terminal_outputs',[]).append(cli('terminal','read','--terminal',handle))

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
    (TEST/'result.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    assert json.loads((TEST/'result.json').read_text(encoding='utf-8'))==json.loads(json.dumps(result))
    print(json.dumps(result))
