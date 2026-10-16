"""One isolated T01 business: official Orca dispatch + Codex exec/exact resume."""
import hashlib, json, os, pathlib, subprocess, sys, time, uuid, shutil, importlib.util
import psutil

ROOT = pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
TEST = ROOT / 'combined-business-20261016-r1'
ASSETS = ROOT / 'CEO_assets'
BUNDLE = ASSETS / 'profile/orcad-artifacts/win32-x64/0.1.0+9e2e3cd709d0'
NODE = ASSETS / 'profile/orcad-artifacts/win32-x64/runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe'
CLI = BUNDLE / 'out/cli/index.js'
GOOD = ROOT / 'business-exec-20261015-r3/worktrees/fixture/component'
FILES = ['scripts/run.py', 'tests/test_run_report_offline.py', 'DELIVERY.md']
# Authoritative expectations come from independent hashes captured at entry, not worker output.
SPEC = 'Complete requests/T01.md only in this new isolated worktree. Fix response parsing in llm_verifier/fine_grained_reward.py, add offline regression tests in tests/test_t01_offline.py, run them, and write DELIVERY.md. Do not implement T02/T03, read parent directories, hidden checks, previous solutions, credentials, or use network or additional models. Preserve unrelated files. Parent executor handles all Orca heartbeat and worker_done commands; do not issue those commands yourself.'
CODEX = pathlib.Path('C:/Users/A/AppData/Roaming/npm/node_modules/@openai/codex/node_modules/@openai/codex-win32-x64/vendor/x86_64-pc-windows-msvc/bin/codex.exe')
VALIDATOR = ROOT/'tools/independent_check_CEO_FROZEN.py'
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

def qa(path):
    assert hashlib.sha256(VALIDATOR.read_bytes()).hexdigest()=='2d6f62b3205454ce5758c98c0160d7aa03b2820f7f05f9c1302a89651cb24979'
    spec=importlib.util.spec_from_file_location('external_qa',VALIDATOR)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return [x for x in mod.check(path) if x['name'].startswith('T01_') or x['name']=='ALL_source_compile']

def session_id(event_file):
    for line in event_file.read_text(encoding='utf-8',errors='replace').splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        if e.get('type')=='thread.started':return e.get('thread_id')
    return None

def run_model(wt, prompt, label, budget, task, ctx, session=None):
    trust='{'+','.join("'"+str(p)+"'={trust_level='trusted'}" for p in [TEST/'fixture',wt])+'}'
    args=[str(CODEX),'exec','--sandbox','workspace-write','-c','approval_policy="on-request"',
        '-c','approvals_reviewer="auto_review"','-c','service_tier="priority"','-c','model_reasoning_effort="ultra"',
        '-c','projects='+trust,'--model','gpt-6.1-sol','--cd',str(wt),'--json','--color','never',
        '--output-last-message',str(TEST/(label+'-last.txt'))]
    args += ['resume',session,'-'] if session else ['-']
    prompt_path=TEST/(label+'-prompt.txt');prompt_path.write_text(prompt,encoding='utf-8')
    events=TEST/(label+'-events.jsonl');t=time.monotonic();end=min(deadline()-180,t+budget)
    assert end>t,'Insufficient budget for completion and QA'
    record={'identity':identity(),'argv':args,'started_mono':t,'budget_seconds':budget,'resume_session':session,
        'prompt_sha256':hashlib.sha256(prompt_path.read_bytes()).hexdigest()}
    with prompt_path.open('rb') as inp,events.open('wb') as out,(TEST/(label+'-stderr.log')).open('wb') as err:
        p=subprocess.Popen(args,cwd=wt,env=os.environ,stdin=inp,stdout=out,stderr=err)
        record['pid']=p.pid;write(label+'-start.json',record)
        heartbeat=t+300
        try:
            while p.poll() is None and time.monotonic()<end:
                if time.monotonic()>=heartbeat:
                    cli('orchestration','send','--type','heartbeat','--subject','Codex active',
                        '--task-id',task,'--dispatch-id',ctx,'--phase','implementing')
                    heartbeat=time.monotonic()+300
                time.sleep(.5)
            record['timed_out']=p.poll() is None
        finally:
            if p.poll() is None:
                owned=psutil.Process(p.pid).children(recursive=True)
                for child in reversed(owned):
                    try:child.terminate()
                    except psutil.NoSuchProcess:pass
                p.terminate();p.wait(timeout=5)
                _,alive=psutil.wait_procs(owned,timeout=5)
                for child in alive:
                    try:child.kill()
                    except psutil.NoSuchProcess:pass
                _,alive=psutil.wait_procs(alive,timeout=5)
                assert not alive,'Owned model child remains; do not resume'
    record.update(exit_code=p.returncode,elapsed_ms=(time.monotonic()-t)*1000,session=session_id(events))
    write(label+'-done.json',record)
    return record

def effective_context(session):
    assert session and str(uuid.UUID(session))==session
    paths=list((pathlib.Path.home()/'.codex/sessions').glob('**/*'+session+'*.jsonl'))
    contexts=[]
    for path in paths:
        for line in path.read_text(encoding='utf-8',errors='replace').splitlines():
            try:e=json.loads(line)
            except ValueError:continue
            if e.get('type')=='turn_context':
                p=e.get('payload',{})
                contexts.append({k:p.get(k) for k in ['cwd','model','effort','approval_policy','approvals_reviewer','sandbox_policy','service_tier']})
    assert contexts,'No effective policy evidence for exact session'
    return contexts[-1]

def worker():
    ident=identity(); write('worker-identity.json',ident)
    envelope=waitfile('assignment.json',60)
    task,ctx,run=envelope['task'],envelope['dispatch'],envelope['run']
    before=cli('orchestration','dispatch-show','--task',task)['dispatch']
    assert before['id']==ctx and before['assignee_handle']==ident['handle']
    assert before['assignee_pane_key']==ident['pane']
    cli('orchestration','send','--type','heartbeat','--subject','T01 starting',
        '--task-id',task,'--dispatch-id',ctx,'--phase','implementing')
    wt=pathlib.Path(read('worktree.json')['path'])
    prompt=(TEST/'official-preamble.txt').read_text(encoding='utf-8')+'\n\n'+SPEC+'\nUse Python standard library offline tests. Parent handles Orca lifecycle; after DELIVERY.md finish your turn.'
    first=run_model(wt,prompt,'initial',360,task,ctx)
    attempts=[first];resume_count=0
    initial_qa=qa(wt);write('initial-qa.json',initial_qa)
    accepted=len(initial_qa)==10 and all(x['passed'] for x in initial_qa) and (wt/'DELIVERY.md').exists()
    if not accepted and first['timed_out']:
        assert first['session'],'Unknown session: no blind redispatch'
        before_dir=TEST/'before-resume';before_dir.mkdir()
        for name in ['llm_verifier/fine_grained_reward.py','tests/test_t01_offline.py','DELIVERY.md']:
            if (wt/name).exists():
                dest=before_dir/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(wt/name,dest)
        resume=run_model(wt,'Continue only the unfinished T01 in the same worktree. Preserve existing work, run tests/test_t01_offline.py, finish DELIVERY.md, then exit. '+SPEC,'resume',600,task,ctx,first['session'])
        attempts.append(resume);resume_count=1
    final_qa=qa(wt);write('business-qa.json',final_qa)
    accepted=len(final_qa)==10 and all(x['passed'] for x in final_qa) and (wt/'DELIVERY.md').exists()
    context=effective_context(first['session']);write('effective-context.json',context)
    assert context['model']=='gpt-6.1-sol' and context['effort']=='ultra'
    assert context['approval_policy']=='on-request' and context['approvals_reviewer']=='auto_review'
    assert context['sandbox_policy']['type']=='workspace-write' and context['sandbox_policy'].get('network_access') is False
    assert pathlib.Path(context['cwd']).resolve()==wt.resolve()
    after=cli('orchestration','dispatch-show','--task',task)['dispatch']
    for key in ['id','assignee_handle','assignee_pane_key','process_incarnation']:
        assert before.get(key)==after.get(key),key
    request=str(uuid.uuid4())
    outcome='succeeded' if accepted else 'failed'
    args=['orchestration','send','--type','worker_done','--subject','T01 '+outcome,
          '--body','Codex executed T01 in the assigned worktree. External checks passed '+str(sum(x['passed'] for x in final_qa))+'/10. CEO will independently review the source diff and delivery.',
          '--task-id',task,'--dispatch-id',ctx,'--outcome',outcome,'--retry-request',request]
    write('completion-request.json',{'request_id':request,'args':args,'identity':ident})
    receipt=cli(*args,cap=150)
    assert receipt.get('lifecycle',{}).get('action') in ('completed','failed','settled')
    write('worker-done.json',{'identity':ident,'attempts':attempts,'accepted':accepted,
        'resume_count':resume_count,'same_dispatch_identity':True,'effective_context':context,
        'process_incarnation':after.get('process_incarnation'),'request_id':request,
        'message_id':receipt['message']['id'],'lifecycle':receipt.get('lifecycle')})

def coordinator():
    ident=identity()
    run=cli('orchestration','run-create','--objective','Deliver real T01 parsing repair through Orca and Codex, with independent acceptance.')['run']['id']
    task=cli('orchestration','task-create','--run',run,'--spec',SPEC,'--task-title','T01 response parsing repair')['task']
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
    (TEST/'official-preamble.txt').write_text(dispatch['preamble'],encoding='utf-8')
    write('assignment.json',{'run':run,'task':task['id'],'dispatch':ctx,
        'preamble_sha256':hashlib.sha256(dispatch['preamble'].encode()).hexdigest(),'coordinator':ident})
    done=waitfile('worker-done.json',1100)
    tasks=cli('orchestration','task-list','--run',run)['tasks']
    found=[t for t in tasks if t['id']==task['id']]
    final=cli('orchestration','dispatch-show','--task',task['id'])['dispatch']
    expected_status='completed' if done['accepted'] else 'failed'
    assert len(found)==1 and found[0]['status']==expected_status
    assert final['id']==ctx and final['status']==expected_status
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
    version=subprocess.run([str(CODEX),'--version'],capture_output=True,text=True,timeout=25,check=True).stdout.strip()
    assert version=='codex-cli 0.160.0',version
    dataset=json.loads((ROOT/'DATASET_MANIFEST.json').read_text(encoding='utf-8-sig'))
    for entry in dataset['input_files']:
        assert hashlib.sha256((ROOT/'dataset/source'/entry['path']).read_bytes()).hexdigest()==entry['sha256']
    TEST.mkdir()
    write('input.json',{'started_mono':started,'started_utc':utc,'deadline_mono':end,
        'expected':expected,'dataset_manifest_sha256':hashlib.sha256((ROOT/'DATASET_MANIFEST.json').read_bytes()).hexdigest(),
        'budget_seconds':1200,'scope':'ORCA_CODEX_T01_COMBINED_BUSINESS'})
    seed={'settings':{'workspaceDir':str(TEST/'worktrees'),'nestWorkspaces':True,
        'agentDefaultArgs':{'codex':'--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review'},
        'agentDefaultEnv':{'codex':{}},'agentYoloDefaultsMigrated':True,'agentStatusHooksEnabled':False,
        'agentWorkspaceTrustEnabled':False,'experimentalNativeChat':False,'codexManagedAccounts':[],
        'activeCodexManagedAccountId':None,'activeCodexManagedAccountIdsByRuntime':{'host':None,'wsl':{}},
        'localWindowsRuntimeDefault':{'kind':'windows-host'},'terminalWindowsShell':'cmd.exe'}}
    data=TEST/'profile/profiles/local-default/orca-data.json';data.parent.mkdir(parents=True)
    data.write_text(json.dumps(seed),encoding='utf-8')
    result={'scope':'ORCA_CODEX_T01_COMBINED_BUSINESS','passed':False};server=None;owned=[]
    try:
        with (TEST/'server.stdout').open('w') as out,(TEST/'server.stderr').open('w') as err:
            server=subprocess.Popen([str(NODE),str(BUNDLE/'orcad.js'),'--bind','127.0.0.1','--port','0','--no-pairing','--json'],env=ENV,stdout=out,stderr=err)
        ready_end=time.monotonic()+remaining(end,60)
        while time.monotonic()<ready_end:
            assert server.poll() is None,'Runtime exited'
            if 'orca_server_ready' in (TEST/'server.stdout').read_text():break
            time.sleep(.2)
        else:raise TimeoutError('Runtime not ready')
        repo=TEST/'fixture';repo.mkdir()
        for entry in dataset['input_files']:
            dst=repo/entry['path'];dst.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/'dataset/source'/entry['path'],dst)
        (repo/'AGENTS.md').write_text(SPEC,encoding='utf-8')
        for a in [['init','-b','main'],['config','core.autocrlf','false'],['add','.'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','commit','-m','fixture']]:
            subprocess.run(['git',*a],cwd=repo,env=ENV,capture_output=True,check=True,timeout=remaining(end,25))
        registered=cli('repo','add','--path',repo)['repo']
        wt=cli('worktree','create','--repo','id:'+registered['id'],'--name','lifecycle','--setup','skip','--no-parent')['worktree']
        write('worktree.json',wt)
        bad=qa(pathlib.Path(wt['path']));write('original-bad-qa.json',bad)
        assert len(bad)==10 and any(not x['passed'] for x in bad),'Original BAD must be detected'
        term=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','Lifecycle coordinator',
            '--command','python -X utf8 "'+str(pathlib.Path(__file__).resolve())+'" coordinator')['terminal']['handle']
        write('coordinator-terminal.json',{'handle':term})
        outcome_end=time.monotonic()+remaining(end,1150)
        while time.monotonic()<outcome_end:
            errors=list(TEST.glob('*-error.json'))
            if errors:raise RuntimeError(errors[0].read_text())
            if (TEST/'coordinator-done.json').exists():break
            time.sleep(.2)
        else:raise TimeoutError('Coordinator outcome UNKNOWN; no redispatch')
        result['coordinator']=read('coordinator-done.json');result['worker']=read('worker-done.json')
        work=pathlib.Path(wt['path']);result['qa']=qa(work);result['bad_qa']=bad
        assert expected==manifest(),'Prior accepted T03 changed'
        assert result['worker']['accepted'] and all(x['passed'] for x in result['qa']) and len(result['qa'])==10
        unchanged=[]
        for entry in dataset['input_files']:
            if entry['path']=='llm_verifier/fine_grained_reward.py':continue
            assert hashlib.sha256((work/entry['path']).read_bytes()).hexdigest()==entry['sha256'],entry['path']
            unchanged.append(entry['path'])
        tests=work/'tests/test_t01_offline.py';assert tests.exists(),'Missing offline tests'
        test_run=subprocess.run([sys.executable,'-X','utf8',str(tests)],cwd=work,env=ENV,
            capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=remaining(end,45))
        result['offline_tests']={'exit_code':test_run.returncode,'stdout':test_run.stdout[-6000:],'stderr':test_run.stderr[-6000:]}
        assert test_run.returncode==0,'Offline regression failed'
        result['diff']=subprocess.run(['git','diff','--','llm_verifier/fine_grained_reward.py'],cwd=work,capture_output=True,text=True,encoding='utf-8',timeout=remaining(end,25),check=True).stdout
        status=subprocess.run(['git','status','--porcelain','--untracked-files=all'],cwd=work,capture_output=True,text=True,encoding='utf-8',timeout=remaining(end,25),check=True).stdout
        result['git_status']=status
        allowed={'llm_verifier/fine_grained_reward.py','tests/test_t01_offline.py','DELIVERY.md'}
        for line in status.splitlines():
            path=line[3:]
            assert path in allowed or '__pycache__/' in path,'Unexpected changed file '+path
        outputs=[]
        for name in sorted(allowed):
            f=work/name;assert f.exists()
            outputs.append({'path':name,'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size':f.stat().st_size})
        result['outputs']=outputs;result['unchanged_inputs']=unchanged
        write('artifact-manifest.json',outputs)
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
        {'main':main,'coordinator':coordinator,'worker':worker}[ROLE]()
    except Exception as exc:
        if TEST.exists():write(ROLE+'-error.json',{'role':ROLE,'error':str(exc)})
        raise
