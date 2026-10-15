"""One bounded isolated Orca component test; no model dispatch, no credentials."""
import hashlib, json, os, pathlib, sqlite3, subprocess, time
import psutil
ROOT=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
TEST=ROOT/'component-check-20261015-r1'
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
data=profile/'profiles/local-default/orca-data.json'
data.parent.mkdir(parents=True)
data.write_text(json.dumps(seed),encoding='utf-8')
env=dict(os.environ,ORCA_USER_DATA=str(profile),ORCA_USER_DATA_PATH=str(profile),ORCA_VERSION='0.1.0+9e2e3cd709d0',ORCA_TELEMETRY_DISABLED='1',DO_NOT_TRACK='1')
result={'scope':'COMPONENT_ONLY_NO_MODEL_NO_BUSINESS','started':time.time(),'checks':[]}
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
    result['database_schema']=tables
    con.close()
    repo=TEST/'fixture'; repo.mkdir(); (repo/'README.md').write_text('# Isolated terminal fixture\n',encoding='utf-8')
    for args in [['init','-b','main'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','add','.'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','commit','-m','fixture']]:
        command(['git',*args],repo)
    registered=cli('repo','add','--path',str(repo))['repo']
    wt=cli('worktree','create','--repo','id:'+registered['id'],'--name','component','--setup','skip','--no-parent')['worktree']
    result['worktree']=wt
    probe=TEST/'terminal-probe.cjs'
    receipt=TEST/'terminal-receipt.json'
    probe.write_text("const fs=require('node:fs'),os=require('node:os');fs.writeFileSync("+json.dumps(str(receipt))+",JSON.stringify({home:os.homedir(),cwd:process.cwd(),terminal:process.env.ORCA_TERMINAL_HANDLE||null,codexHomePresent:!!process.env.CODEX_HOME,orcaCodexHomePresent:!!process.env.ORCA_CODEX_HOME}));console.log('ORCA_COMPONENT_RECEIPT_WRITTEN');",encoding='utf-8')
    terminal=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','component-check','--command','"'+str(NODE)+'" "'+str(probe)+'"')['terminal']
    result['terminal_handle']=terminal['handle']
    deadline=time.monotonic()+30
    while time.monotonic()<deadline and not receipt.exists():time.sleep(.25)
    assert receipt.exists(),'Terminal did not create receipt'
    observed=json.loads(receipt.read_text(encoding='utf-8'))
    assert pathlib.Path(observed['cwd']).is_relative_to(TEST),'Worktree escaped task root'
    assert observed['home']==str(pathlib.Path.home()),'Home changed'
    assert observed['terminal'],'No real terminal identity'
    result['terminal_environment']=observed
    result['checks'].append('TERMINAL_ENVIRONMENT_RECEIPT')
    result['terminal_output']=cli('terminal','read','--terminal',terminal['handle'])
    cli('terminal','close','--terminal',terminal['handle'])
    result['passed']=True
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
    assert json.loads((TEST/'result.json').read_text(encoding='utf-8'))==result
    print(json.dumps(result))
