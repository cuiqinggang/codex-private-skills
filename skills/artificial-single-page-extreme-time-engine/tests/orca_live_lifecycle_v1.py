"""One-shot official Orca lifecycle validation. No model, no production scheduler."""
import hashlib, json, os, pathlib, subprocess, sys, time, uuid
import psutil

ROOT = pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
TEST = ROOT / 'lifecycle-v1-live-20261019-1945'
ASSETS = ROOT / 'CEO_assets'
BUNDLE = ASSETS / 'profile/orcad-artifacts/win32-x64/0.1.0+9e2e3cd709d0'
NODE = ASSETS / 'profile/orcad-artifacts/win32-x64/runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe'
CLI = BUNDLE / 'out/cli/index.js'
GOOD = ROOT / 'business-exec-20261015-r3/worktrees/fixture/component'
FILES = ['scripts/run.py', 'tests/test_run_report_offline.py', 'DELIVERY.md']
# Authoritative expectations come from independent hashes captured at entry, not worker output.
SPEC = 'Read only the three accepted T03 files named in input.json. Produce artifact-manifest.json with their SHA256 and byte sizes. Do not edit the source. Resume only unfinished hashing after the controlled child timeout; no model invocation.'
ROLE = sys.argv[1] if len(sys.argv) > 1 else 'main'
ENV = dict(os.environ, ORCA_USER_DATA=str(TEST/'profile'), ORCA_USER_DATA_PATH=str(TEST/'profile'), ORCA_VERSION='0.1.0+9e2e3cd709d0', ORCA_TELEMETRY_DISABLED='1', DO_NOT_TRACK='1')

def write(name, obj):
    p = TEST/name
    tmp = p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding='utf-8')
    os.replace(tmp, p)

def read(name):
    return json.loads((TEST/name).read_text(encoding='utf-8'))

def remaining(deadline, cap):
    left = deadline-time.monotonic()
    if left <= 0:
        raise TimeoutError('GLOBAL_BUDGET_EXHAUSTED')
    return min(cap, left)

def deadline():
    return read('input.json')['deadline_mono']

def cli(*args, cap=25):
    # Preserve the original request after any timeout; never retry here.
    r = subprocess.run([str(NODE),str(CLI),*map(str,args),'--json'], env=ENV,
        capture_output=True, text=True, encoding='utf-8', errors='replace',
        timeout=remaining(deadline(), cap))
    j = json.loads(r.stdout)
    if r.returncode or j.get('ok') is False:
        raise RuntimeError(json.dumps(j))
    return j.get('result',j)

def waitfile(name, cap):
    end = time.monotonic()+remaining(deadline(),cap)
    while time.monotonic() < end:
        if (TEST/name).exists(): return read(name)
        time.sleep(.1)
    raise TimeoutError('WAIT_FILE_UNKNOWN '+name)

def identity():
    handle = os.environ.get('ORCA_TERMINAL_HANDLE')
    pane = os.environ.get('ORCA_PANE_KEY')
    assert handle and pane, 'Missing own official terminal identity'
    return {'handle':handle, 'pane':pane}

def manifest():
    return [{'path':f,'sha256':hashlib.sha256((GOOD/f).read_bytes()).hexdigest(),
             'size':(GOOD/f).stat().st_size} for f in FILES]

def child():
    ident=identity()
    if sys.argv[2]=='first':
        row=manifest()[0]
        write('partial.json',{'identity':ident,'rows':[row]})
        print('PARTIAL_SAVED',flush=True)
        time.sleep(60)  # Deliberate isolated fault; parent enforces a 2 s timeout.
    else:
        partial=read('partial.json')
        assert partial['identity']==ident
        rows=manifest()
        assert partial['rows']==rows[:1]
        write('artifact-manifest.json',{'identity':ident,'files':rows,'preserved_partial':True})

def worker():
    ident=identity(); write('worker-identity.json',ident)
    envelope=waitfile('assignment.json',60)
    task,ctx,run=envelope['task'],envelope['dispatch'],envelope['run']
    before=cli('orchestration','dispatch-show','--task',task)['dispatch']
    assert before['id']==ctx and before['assignee_handle']==ident['handle']
    assert before['assignee_pane_key']==ident['pane']
    # Trigger a real CLI timeout (1 ms) in the control plane; do not mutate/re-send heartbeat.
    try:
        cli('orchestration','dispatch-show','--task',task,cap=0.001)
        control_fault='FAST_READ_SUCCEEDED'
    except subprocess.TimeoutExpired:
        control_fault='REAL_CLI_READ_TIMEOUT'
    write('control-fault.json',{'outcome':control_fault,'task':task,'dispatch':ctx,
                              'identity':ident,'business_interrupted':False})
    # Fresh independent official read reconciles the SAME dispatch/terminal.
    recovered=cli('orchestration','dispatch-show','--task',task,cap=25)['dispatch']
    assert recovered['id']==ctx and recovered['assignee_handle']==ident['handle']
    assert recovered['assignee_pane_key']==ident['pane']
    write('control-recovered.json',{'same_dispatch':True,'identity':ident,'task':task,
                                     'dispatch':ctx,'fault':control_fault})
    # Do not send another ambiguous control mutation. Continue child work on same identity.
    # Only the disposable child is stopped. The official terminal and parent remain alive.
    timed_out=False
    with (TEST/'child-first.log').open('wb') as log:
        p=subprocess.Popen([sys.executable,'-X','utf8',__file__,'child','first'],env=os.environ,stdout=log,stderr=log)
        first_pid=p.pid
        try:p.wait(timeout=remaining(deadline(),2))
        except subprocess.TimeoutExpired:
            timed_out=True;p.terminate();p.wait(timeout=5)
    assert timed_out and p.poll() is not None
    first_code=p.returncode
    partial=read('partial.json'); assert partial['identity']==ident
    # Exactly one resumption of the deterministic test child, not a Codex resume claim.
    r=subprocess.run([sys.executable,'-X','utf8',__file__,'child','resume'],env=os.environ,
        capture_output=True,text=True,encoding='utf-8',timeout=remaining(deadline(),25))
    assert r.returncode==0,r.stderr
    after=cli('orchestration','dispatch-show','--task',task)['dispatch']
    for key in ['id','assignee_handle','assignee_pane_key','process_incarnation']:
        assert before.get(key)==after.get(key),key
    assert read('artifact-manifest.json')['files']==read('input.json')['expected']
    request=str(uuid.uuid4())
    args=['orchestration','send','--type','worker_done','--subject','Artifact manifest ready',
          '--body','Hashed three accepted artifacts. Partial work survived the controlled child timeout. Source files are unchanged and ready for independent verification.',
          '--task-id',task,'--dispatch-id',ctx,'--outcome','succeeded','--retry-request',request]
    write('completion-request.json',{'request_id':request,'args':args,'identity':ident})
    receipt=cli(*args,cap=150)
    # Intentional idempotence verification: exact same request, not a second completion.
    replay=cli(*args,cap=150)
    assert receipt['message']['id']==replay['message']['id']
    assert receipt.get('lifecycle',{}).get('action') in ('completed','settled')
    write('worker-done.json',{'identity':ident,'first_child_pid':first_pid,'first_exit':first_code,
        'controlled_timeout':timed_out,'resume_count':1,'same_dispatch_identity':True,
        'process_incarnation':after.get('process_incarnation'),'request_id':request,
        'message_id':receipt['message']['id'],'replay_message_id':replay['message']['id'],
        'lifecycle':receipt.get('lifecycle'),'artifact_sha256':hashlib.sha256((TEST/'artifact-manifest.json').read_bytes()).hexdigest()})

def coordinator():
    ident=identity()
    run=cli('orchestration','run-create','--objective','Validate exact terminal lifecycle after child timeout, with real artifact manifest.')['run']['id']
    task=cli('orchestration','task-create','--run',run,'--spec',SPEC,'--task-title','Accepted artifacts manifest')['task']
    assert task['status']=='ready',task
    wt=read('worktree.json')
    term=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','Lifecycle worker',
        '--command','python -X utf8 "'+str(pathlib.Path(__file__).resolve())+'" worker')['terminal']['handle']
    write('worker-terminal.json',{'handle':term})
    wi=waitfile('worker-identity.json',30); assert wi['handle']==term
    dispatch=cli('orchestration','dispatch','--task',task['id'],'--run',run,'--to',term,'--return-preamble')
    assert dispatch.get('injected') is False
    assert SPEC in dispatch['preamble']
    ctx=dispatch['dispatch']['id']
    write('assignment.json',{'run':run,'task':task['id'],'dispatch':ctx,
        'preamble_sha256':hashlib.sha256(dispatch['preamble'].encode()).hexdigest(),'coordinator':ident})
    done=waitfile('worker-done.json',400)
    tasks=cli('orchestration','task-list','--run',run)['tasks']
    found=[t for t in tasks if t['id']==task['id']]
    final=cli('orchestration','dispatch-show','--task',task['id'])['dispatch']
    assert len(found)==1 and found[0]['status']=='completed'
    assert final['id']==ctx and final['status']=='completed'
    result=json.loads(found[0]['result'])
    assert result['provenance']=='worker_report' and result['messageId']==done['message_id']
    write('coordinator-done.json',{'run':run,'task':task['id'],'dispatch':ctx,
        'task_status':found[0]['status'],'dispatch_status':final['status'],'worker_result':result})

def main():
    started=time.monotonic(); utc=time.time(); end=started+1200
    assert not TEST.exists(),'Existing node: reconcile, never rerun'
    assert psutil.virtual_memory().available>=4*1024**3,'4 GiB reserve'
    for p in psutil.process_iter(['pid','name','cmdline']):
        cmd=' '.join(p.info['cmdline'] or []).replace('\\','/').lower()
        if p.info['name'].lower() in ('node.exe','codex.exe') and str(ROOT).replace('\\','/').lower() in cmd:
            raise RuntimeError('Existing task-owned process requires reconciliation '+str(p.pid))
    for p,h in [(NODE,'ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32'),
                (BUNDLE/'orcad-server.js','bea1e0ce0f5cd40a046a40c04ef5e66c9e38ce110387f35d5b54abccf65cb8ba')]:
        assert hashlib.sha256(p.read_bytes()).hexdigest()==h
    expected=manifest()
    known=['320f2bf3825bf000bd501309e44ce39f36ce507005e0e694a07fe950777d2314',
           '00cce6d3fd3ff845f165634f51c16f2ab0bb3cf542ab82c3db80c381d644c619',
           '5a711c8b52b7627bac9a5470e56eedc05ed253336ecdbcd3b4aeb804992e2d10']
    assert [x['sha256'] for x in expected]==known,'Accepted artifact changed'
    TEST.mkdir()
    write('input.json',{'started_mono':started,'started_utc':utc,'deadline_mono':end,
        'expected':expected,'budget_seconds':1200,'scope':'DETERMINISTIC_LIFECYCLE_NOT_CODEX_BUSINESS'})
    seed={'settings':{'workspaceDir':str(TEST/'worktrees'),'nestWorkspaces':True,
        'agentDefaultArgs':{'codex':'--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review'},
        'agentDefaultEnv':{'codex':{}},'agentYoloDefaultsMigrated':True,'agentStatusHooksEnabled':False,
        'agentWorkspaceTrustEnabled':False,'experimentalNativeChat':False,'codexManagedAccounts':[],
        'activeCodexManagedAccountId':None,'activeCodexManagedAccountIdsByRuntime':{'host':None,'wsl':{}},
        'localWindowsRuntimeDefault':{'kind':'windows-host'},'terminalWindowsShell':'cmd.exe'}}
    data=TEST/'profile/profiles/local-default/orca-data.json';data.parent.mkdir(parents=True)
    data.write_text(json.dumps(seed),encoding='utf-8')
    result={'scope':'DETERMINISTIC_LIFECYCLE_NOT_CODEX_BUSINESS','passed':False};server=None;owned=[]
    try:
        with (TEST/'server.stdout').open('w') as out,(TEST/'server.stderr').open('w') as err:
            server=subprocess.Popen([str(NODE),str(BUNDLE/'orcad.js'),'--bind','127.0.0.1','--port','0','--no-pairing','--json'],env=ENV,stdout=out,stderr=err)
        ready_end=time.monotonic()+remaining(end,60)
        while time.monotonic()<ready_end:
            assert server.poll() is None,'Runtime exited'
            if 'orca_server_ready' in (TEST/'server.stdout').read_text():break
            time.sleep(.2)
        else:raise TimeoutError('Runtime not ready')
        repo=TEST/'fixture';repo.mkdir();(repo/'TASK.md').write_text(SPEC,encoding='utf-8')
        for a in [['init','-b','main'],['add','.'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','commit','-m','fixture']]:
            subprocess.run(['git',*a],cwd=repo,env=ENV,capture_output=True,check=True,timeout=remaining(end,25))
        registered=cli('repo','add','--path',repo)['repo']
        wt=cli('worktree','create','--repo','id:'+registered['id'],'--name','lifecycle','--setup','skip','--no-parent')['worktree']
        write('worktree.json',wt)
        term=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','Lifecycle coordinator',
            '--command','python -X utf8 "'+str(pathlib.Path(__file__).resolve())+'" coordinator')['terminal']['handle']
        write('coordinator-terminal.json',{'handle':term})
        outcome_end=time.monotonic()+remaining(end,500)
        while time.monotonic()<outcome_end:
            errors=list(TEST.glob('*-error.json'))
            if errors:raise RuntimeError(errors[0].read_text())
            if (TEST/'coordinator-done.json').exists():break
            time.sleep(.2)
        else:raise TimeoutError('Coordinator outcome UNKNOWN; no redispatch')
        result['coordinator']=read('coordinator-done.json');result['worker']=read('worker-done.json')
        artifact=read('artifact-manifest.json')
        assert artifact['files']==expected==manifest(),'Independent artifact QA'
        result['independent_qa']='3_OF_3_HASHES_AND_SIZES_UNCHANGED'
        result['closes']=[]
        for name in ['worker-terminal.json','coordinator-terminal.json']:
            result['closes'].append(cli('terminal','close','--terminal',read(name)['handle']))
        result['passed']=True
    except Exception as exc:
        result['error']=str(exc)
    finally:
        if server and server.poll() is None:
            owned=psutil.Process(server.pid).children(recursive=True)
            for p in reversed(owned):
                try:p.terminate()
                except psutil.NoSuchProcess:pass
            server.terminate();_,alive=psutil.wait_procs(owned,timeout=5)
            for p in alive:
                try:p.kill()
                except psutil.NoSuchProcess:pass
            psutil.wait_procs(alive,timeout=5);server.wait(timeout=5)
        result['remaining_owned']=[p.pid for p in owned if p.is_running()]
        result['passed']=result['passed'] and not result['remaining_owned']
        write('result.json',result);assert read('result.json')==result
        # Endpoint AFTER QA, owned cleanup, evidence write and local readback.
        write('local-acceptance.json',{'accepted':result['passed'],'scope':result['scope'],
            'local_valid_ms':(time.monotonic()-started)*1000,'started_utc':utc,'accepted_utc':time.time(),
            'excludes':'cloud delivery before script entry and later GitHub archive/readback; see final acceptance',
            'result_sha256':hashlib.sha256((TEST/'result.json').read_bytes()).hexdigest()})
        print(json.dumps(result),flush=True)

if __name__=='__main__':
    try:
        {'main':main,'coordinator':coordinator,'worker':worker,'child':child}[ROLE]()
    except Exception as exc:
        if TEST.exists():write(ROLE+'-error.json',{'role':ROLE,'error':str(exc)})
        raise
