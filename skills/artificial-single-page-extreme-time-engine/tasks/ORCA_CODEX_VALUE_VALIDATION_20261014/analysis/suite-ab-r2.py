"""One isolated T01 business: official Orca dispatch + Codex exec/exact resume."""
import hashlib, json, os, pathlib, subprocess, sys, time, uuid, shutil, importlib.util
import psutil, threading, re

ROOT = pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
ARM = sys.argv[2] if len(sys.argv)>2 else 'B'
LABEL = sys.argv[3] if len(sys.argv)>3 else 'pilot'
assert ARM in ('A','B') and re.fullmatch(r'(pilot|p\d\d)',LABEL)
BATCH = ROOT / 'suite-ab-20261016-r2'
TEST = BATCH / (LABEL+'-'+ARM)
ASSETS = ROOT / 'CEO_assets'
BUNDLE = ASSETS / 'profile/orcad-artifacts/win32-x64/0.1.0+9e2e3cd709d0'
NODE = ASSETS / 'profile/orcad-artifacts/win32-x64/runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe'
CLI = BUNDLE / 'out/cli/index.js'
GOOD = ROOT / 'business-exec-20261015-r3/worktrees/fixture/component'
FILES = ['scripts/run.py', 'tests/test_run_report_offline.py', 'DELIVERY.md']
# Authoritative expectations come from independent hashes captured at entry, not worker output.
SPEC = '按顺序完成 requests/T01.md、T02.md、T03.md 三项真实修复，保持它们的全部 DONE_WHEN。只修改本工作树的 llm_verifier/fine_grained_reward.py、llm_verifier/benchmarks.py、llm_verifier/loaders.py、scripts/run.py；分别新增 tests/test_t01_offline.py、tests/test_t02_offline.py、tests/test_t03_offline.py，使用标准库 unittest，每个文件至少三项有意义测试，支持直接 python 文件名运行。离线 mock 禁止凭据加载、真实服务与网络。全部测试通过后写 DELIVERY.md，逐项写变更、命令、结果和未验证边界。保留原 AGENTS.md 和其余文件。不要读取父目录、隐藏验收器、旧答案、历史会话或外部资料；不得启动其它模型、子代理、安装依赖或修改全局配置。上级处理所有 Orca 生命周期与心跳，不要自行调用这些命令。完成后结束本轮。'
TARGETS={'llm_verifier/fine_grained_reward.py','llm_verifier/benchmarks.py','llm_verifier/loaders.py','scripts/run.py'}
SPEC += ' 已确认的 Windows Python 3.13 沙箱测试设施注意事项：不要使用 tempfile.TemporaryDirectory/mkdtemp，它们创建的0700目录可能无法访问或清理；改用工作树内 Path.mkdir() 正常继承现有权限，使用UUID避免冲突，仅清理自己本次创建的fixture，不改ACL、不提权。所有临时fixture结束后必须清理；存在不可访问残留则如实报告未完整验收。DELIVERY.md简明列出变更、命令和结果即可；原始命令和失败输出已由上级JSONL完整留存，不必把长日志重复粘贴进报告。'
TESTS={'tests/test_t01_offline.py','tests/test_t02_offline.py','tests/test_t03_offline.py'}
ALLOWED=TARGETS|TESTS|{'DELIVERY.md'}
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
    if ARM=='A':return {'handle':None,'pane':None,'native':True}
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
    return mod.check(path)

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
                assert psutil.virtual_memory().available>=4*1024**3,'RESOURCE_RESERVE_EXHAUSTED'
                if ARM=='B' and time.monotonic()>=heartbeat:
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
    record['usage']=[];record['errors']=[]
    for line in events.read_text(encoding='utf-8',errors='replace').splitlines():
        try:e=json.loads(line)
        except ValueError:continue
        if e.get('type')=='turn.completed':record['usage'].append(e.get('usage'))
        if e.get('type') in ('error','turn.failed'):record['errors'].append(e)
    write(label+'-done.json',record)
    if re.search(r'usage limit|quota exceeded|insufficient_quota',json.dumps(record['errors']),re.I):
        raise RuntimeError('MODEL_QUOTA_BLOCKED_NO_AUTOMATIC_RETRY')
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

def offline_tests(wt):
    records=[]
    for name in sorted(TESTS):
        assert (wt/name).is_file(),'Missing '+name
        r=subprocess.run([sys.executable,'-B','-X','utf8',str(wt/name)],cwd=wt,env=ENV,
            capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=remaining(deadline(),60))
        count=re.search(r'Ran (\d+) tests?',r.stderr+r.stdout)
        records.append({'path':name,'exit_code':r.returncode,'test_count':int(count[1]) if count else None,
            'stdout':r.stdout[-8000:],'stderr':r.stderr[-8000:]})
    return records

def workspace_inventory(wt):
    # Git status can silently omit empty or inaccessible directories.
    dirs={'llm_verifier','scripts','requests','tests'}
    errors=[];unexpected=[]
    for root,children,files in os.walk(wt,onerror=lambda e:errors.append(str(e)),followlinks=False):
        parent=pathlib.Path(root)
        for name in children:
            p=parent/name;relative=p.relative_to(wt).as_posix()
            if p.is_symlink() or (relative not in dirs and name!='__pycache__'):
                unexpected.append(relative)
    return {'accepted':not errors and not unexpected,'errors':errors,'unexpected_directories':unexpected}

def inspect(wt):
    checks=qa(wt)
    tests=offline_tests(wt) if all((wt/n).is_file() for n in TESTS) else []
    passed=(len(checks)==14 and all(x['passed'] for x in checks) and len(tests)==3
        and all(x['exit_code']==0 and (x['test_count'] or 0)>=3 for x in tests) and (wt/'DELIVERY.md').is_file())
    inventory=workspace_inventory(wt)
    return {'accepted':passed and inventory['accepted'],'qa':checks,'tests':tests,'delivery':(wt/'DELIVERY.md').is_file(),'inventory':inventory}

def worker():
    ident=identity();write('worker-identity.json',ident)
    task=ctx=None;before={}
    wt=pathlib.Path(read('worktree.json')['path'])
    prompt=SPEC
    if ARM=='B':
        envelope=waitfile('assignment.json',60);task=envelope['task'];ctx=envelope['dispatch']
        before=cli('orchestration','dispatch-show','--task',task)['dispatch']
        assert before['id']==ctx and before['assignee_handle']==ident['handle'] and before['assignee_pane_key']==ident['pane']
        prompt=(TEST/'official-preamble.txt').read_text(encoding='utf-8')+'\n\n'+SPEC
    first=run_model(wt,prompt,'initial',900,task,ctx);attempts=[first]
    inspection=inspect(wt);write('initial-inspection.json',inspection)
    if not inspection['accepted']:
        assert first['session'],'Unknown session: no redispatch'
        backup=TEST/'before-resume';backup.mkdir()
        for name in ALLOWED:
            if (wt/name).exists():
                target=backup/name;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(wt/name,target)
        failed=[x['name'] for x in inspection['qa'] if not x['passed']]
        prompt='继续本会话未完成部分，保留已有修复。外部验收未通过的检查名称：'+json.dumps(failed,ensure_ascii=False)+'。工作树残留核验：'+json.dumps(inspection.get('inventory'),ensure_ascii=False)+'。上次离线测试摘要：'+json.dumps(inspection['tests'],ensure_ascii=False)+'。补齐交付记录后结束。\n'+SPEC
        attempts.append(run_model(wt,prompt,'resume',600,task,ctx,first['session']))
    inspection=inspect(wt);write('business-inspection.json',inspection)
    context=effective_context(first['session']);write('effective-context.json',context)
    assert context['model']=='gpt-6.1-sol' and context['effort']=='ultra'
    assert context['approval_policy']=='on-request' and context['approvals_reviewer']=='auto_review'
    assert context['sandbox_policy']['type']=='workspace-write' and context['sandbox_policy'].get('network_access') is False
    assert pathlib.Path(context['cwd']).resolve()==wt.resolve()
    result={'identity':ident,'attempts':attempts,'accepted':inspection['accepted'],'resume_count':len(attempts)-1,'effective_context':context}
    if ARM=='B':
        after=cli('orchestration','dispatch-show','--task',task)['dispatch']
        assert all(before.get(k)==after.get(k) for k in ['id','assignee_handle','assignee_pane_key','process_incarnation'])
        request=str(uuid.uuid4());outcome='succeeded' if inspection['accepted'] else 'failed'
        args=['orchestration','send','--type','worker_done','--subject','T01-T03 '+outcome,
            '--body','Three-task suite complete; external checks and offline regression recorded for CEO review.',
            '--task-id',task,'--dispatch-id',ctx,'--outcome',outcome,'--retry-request',request]
        write('completion-request.json',{'request_id':request,'args':args,'identity':ident})
        receipt=cli(*args,cap=150)
        assert receipt.get('lifecycle',{}).get('action') in ('completed','failed','settled')
        result.update(same_dispatch_identity=True,request_id=request,message_id=receipt['message']['id'],lifecycle=receipt.get('lifecycle'))
    write('worker-done.json',result)

def child_command(role):
    return 'python -X utf8 "'+str(pathlib.Path(__file__).resolve())+'" '+role+' '+ARM+' '+LABEL

def coordinator():
    ident=identity()
    run=cli('orchestration','run-create','--objective','Complete and independently verify the T01-T03 real business suite.')['run']['id']
    task=cli('orchestration','task-create','--run',run,'--spec',SPEC,'--task-title','T01-T03 business suite')['task']
    assert task['status']=='ready'
    wt=read('worktree.json')
    term=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','Suite worker','--command',child_command('worker'))['terminal']['handle']
    write('worker-terminal.json',{'handle':term})
    wi=waitfile('worker-identity.json',30);assert wi['handle']==term
    dispatch=cli('orchestration','dispatch','--task',task['id'],'--run',run,'--to',term,'--return-preamble')
    assert dispatch.get('injected') is False and SPEC in dispatch['preamble']
    ctx=dispatch['dispatch']['id'];(TEST/'official-preamble.txt').write_text(dispatch['preamble'],encoding='utf-8')
    write('assignment.json',{'run':run,'task':task['id'],'dispatch':ctx,'coordinator':ident,
        'preamble_sha256':hashlib.sha256(dispatch['preamble'].encode()).hexdigest()})
    done=waitfile('worker-done.json',1700)
    tasks=cli('orchestration','task-list','--run',run)['tasks'];found=[x for x in tasks if x['id']==task['id']]
    final=cli('orchestration','dispatch-show','--task',task['id'])['dispatch']
    expected='completed' if done['accepted'] else 'failed'
    assert len(found)==1 and found[0]['status']==expected and final['id']==ctx and final['status']==expected
    report=json.loads(found[0]['result']);assert report['provenance']=='worker_report' and report['messageId']==done['message_id']
    write('coordinator-done.json',{'run':run,'task':task['id'],'dispatch':ctx,'task_status':expected,'dispatch_status':expected,'worker_result':report})

def process_snapshot(root):
    found=[]
    for p in psutil.process_iter(['pid','name','cmdline']):
        cmd=' '.join(p.info['cmdline'] or []).replace('\\','/').lower()
        if p.info['name'].lower() in ('node.exe','codex.exe') and str(root).replace('\\','/').lower() in cmd:found.append(p.info['pid'])
    return found

def stop_tree(p):
    if p is None or p.poll() is not None:return []
    children=psutil.Process(p.pid).children(recursive=True)
    for item in reversed(children):
        try:item.terminate()
        except psutil.NoSuchProcess:pass
    p.terminate();p.wait(timeout=10)
    _,alive=psutil.wait_procs(children,timeout=5)
    for item in alive:
        try:item.kill()
        except psutil.NoSuchProcess:pass
    _,alive=psutil.wait_procs(alive,timeout=5)
    return [x.pid for x in alive]

def sampler(stop):
    base=time.monotonic();index=0
    with (TEST/'resources.jsonl').open('w',encoding='utf-8') as out:
        while not stop.is_set():
            try:
                ps=[psutil.Process()]+psutil.Process().children(recursive=True)
                rss=cpu=0
                for p in ps:
                    try:rss+=p.memory_info().rss;c=p.cpu_times();cpu+=c.user+c.system
                    except (psutil.NoSuchProcess,psutil.AccessDenied):pass
                out.write(json.dumps({'mono':time.monotonic(),'rss_bytes':rss,'cpu_seconds':cpu,'available_bytes':psutil.virtual_memory().available,'system_cpu_percent':psutil.cpu_percent()})+'\n');out.flush()
            except Exception as e:out.write(json.dumps({'mono':time.monotonic(),'error':str(e)})+'\n');out.flush()
            index+=1;stop.wait(max(0,base+index-time.monotonic()))

def main():
    started=time.monotonic();utc=time.time();end=started+1900
    assert not TEST.exists(),'Existing attempt: reconcile, never replay'
    TEST.mkdir(parents=True);result={'scope':'THREE_TASK_SUITE','arm':ARM,'label':LABEL,'passed':False}
    server=None;stop=threading.Event();sampling=None
    write('input.json',{'started_mono':started,'started_utc':utc,'deadline_mono':end,'budget_seconds':1900,
        'script_sha256':hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),'business_spec_sha256':hashlib.sha256(SPEC.encode()).hexdigest()})
    try:
        assert psutil.virtual_memory().available>=4*1024**3,'4 GiB reserve'
        assert not process_snapshot(ROOT),'Existing task process requires reconciliation'
        assert sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())<20*1024**3,'20 GiB task cap'
        for p,h in [(NODE,'ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32'),(BUNDLE/'orcad-server.js','bea1e0ce0f5cd40a046a40c04ef5e66c9e38ce110387f35d5b54abccf65cb8ba')]:assert hashlib.sha256(p.read_bytes()).hexdigest()==h
        assert subprocess.run([str(CODEX),'--version'],capture_output=True,text=True,check=True,timeout=25).stdout.strip()=='codex-cli 0.160.0'
        expected=manifest();write('prior-good.json',expected)
        prior_t01=ROOT/'combined-business-20261016-r1/worktrees/fixture/lifecycle'
        prior_hashes={'DELIVERY.md':'74cfa788cb081b8f02efb24208202920a6451d093a058adeb851ee85db7dacc3','llm_verifier/fine_grained_reward.py':'33f4881138c2a3d57df2077198ee56021edbfaf1b6ade898043a7b2053f7b712','tests/test_t01_offline.py':'962c2df7bafe98c7fcad1a99c5d58ad108525ae3bd40774912000ba355654651'}
        assert all(hashlib.sha256((prior_t01/n).read_bytes()).hexdigest()==h for n,h in prior_hashes.items())
        assert [x['sha256'] for x in expected]==['320f2bf3825bf000bd501309e44ce39f36ce507005e0e694a07fe950777d2314','00cce6d3fd3ff845f165634f51c16f2ab0bb3cf542ab82c3db80c381d644c619','5a711c8b52b7627bac9a5470e56eedc05ed253336ecdbcd3b4aeb804992e2d10']
        assert hashlib.sha256((ROOT/'DATASET_MANIFEST.json').read_bytes()).hexdigest()=='56ab2c16bfb3c618a5c893f47ae13e91e7fd07fee4cd50c073ae72c63a05e8a8'
        dataset=json.loads((ROOT/'DATASET_MANIFEST.json').read_text(encoding='utf-8-sig'))
        sampling=threading.Thread(target=sampler,args=(stop,),daemon=True);sampling.start()
        repo=TEST/'fixture';repo.mkdir()
        for entry in dataset['input_files']:
            source=ROOT/'dataset/source'/entry['path'];assert hashlib.sha256(source.read_bytes()).hexdigest()==entry['sha256']
            target=repo/entry['path'];target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
        # Preserve original AGENTS bytes. Business additions are only in equal A/B stdin.
        for a in [['init','-b','main'],['config','core.autocrlf','false'],['add','.'],['-c','user.name=Orca Test','-c','user.email=test@example.invalid','commit','-m','fixture']]:
            subprocess.run(['git',*a],cwd=repo,env=ENV,capture_output=True,check=True,timeout=remaining(end,25))
        if ARM=='B':
            seed={'settings':{'workspaceDir':str(TEST/'worktrees'),'nestWorkspaces':True,'agentDefaultArgs':{'codex':'--sandbox workspace-write --ask-for-approval on-request -c approvals_reviewer=auto_review'},'agentDefaultEnv':{'codex':{}},'agentYoloDefaultsMigrated':True,'agentStatusHooksEnabled':False,'agentWorkspaceTrustEnabled':False,'experimentalNativeChat':False,'codexManagedAccounts':[],'activeCodexManagedAccountId':None,'activeCodexManagedAccountIdsByRuntime':{'host':None,'wsl':{}},'localWindowsRuntimeDefault':{'kind':'windows-host'},'terminalWindowsShell':'cmd.exe'}}
            p=TEST/'profile/profiles/local-default/orca-data.json';p.parent.mkdir(parents=True);p.write_text(json.dumps(seed),encoding='utf-8')
            with (TEST/'server.stdout').open('w') as out,(TEST/'server.stderr').open('w') as err:
                server=subprocess.Popen([str(NODE),str(BUNDLE/'orcad.js'),'--bind','127.0.0.1','--port','0','--no-pairing','--json'],env=ENV,stdout=out,stderr=err)
            write('runtime-pid.json',{'pid':server.pid})
            ready_end=time.monotonic()+remaining(end,60)
            while time.monotonic()<ready_end:
                assert server.poll() is None,'Runtime exited'
                if 'orca_server_ready' in (TEST/'server.stdout').read_text():break
                time.sleep(.2)
            else:raise TimeoutError('Runtime not ready')
            registered=cli('repo','add','--path',repo)['repo']
            wt=cli('worktree','create','--repo','id:'+registered['id'],'--name','suite','--setup','skip','--no-parent')['worktree']
        else:
            work=TEST/'worktrees/fixture/suite';work.parent.mkdir(parents=True)
            subprocess.run(['git','worktree','add','-b','suite',str(work)],cwd=repo,capture_output=True,check=True,timeout=remaining(end,25))
            wt={'path':str(work),'id':None}
        write('worktree.json',wt);work=pathlib.Path(wt['path']);assert work.resolve().is_relative_to(TEST.resolve())
        result['bad_qa']=qa(work);assert len(result['bad_qa'])==14 and sum(x['passed'] for x in result['bad_qa'])==5
        if ARM=='B':
            term=cli('terminal','create','--worktree',wt['id'],'--shell','cmd.exe','--title','Suite coordinator','--command',child_command('coordinator'))['terminal']['handle']
            write('coordinator-terminal.json',{'handle':term})
            until=time.monotonic()+remaining(end,1750)
            while time.monotonic()<until:
                errors=list(TEST.glob('*-error.json'))
                if errors:raise RuntimeError(errors[0].read_text(encoding='utf-8'))
                if (TEST/'coordinator-done.json').exists():break
                time.sleep(.5)
            else:raise TimeoutError('Coordinator outcome UNKNOWN; no redispatch')
            result['coordinator']=read('coordinator-done.json')
        else:worker()
        result['worker']=read('worker-done.json');result['inspection']=inspect(work)
        assert result['worker']['accepted'] and result['inspection']['accepted'],'Business QA rejected'
        assert expected==manifest(),'Prior accepted T03 changed'
        assert all(hashlib.sha256((prior_t01/n).read_bytes()).hexdigest()==h for n,h in prior_hashes.items()),'Prior accepted T01 changed'
        for e in dataset['input_files']:
            if e['path'] not in TARGETS:assert hashlib.sha256((work/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
        result['git_status']=subprocess.run(['git','status','--porcelain','--untracked-files=all'],cwd=work,capture_output=True,text=True,check=True,timeout=25).stdout
        for line in result['git_status'].splitlines():assert line[3:] in ALLOWED or '__pycache__/' in line[3:],'Unexpected file '+line
        result['diff']=subprocess.run(['git','diff','--',*sorted(TARGETS)],cwd=work,capture_output=True,text=True,encoding='utf-8',check=True,timeout=25).stdout
        result['outputs']=[{'path':n,'sha256':hashlib.sha256((work/n).read_bytes()).hexdigest(),'size':(work/n).stat().st_size,'text':(work/n).read_text(encoding='utf-8')} for n in sorted(ALLOWED)]
        write('artifact-manifest.json',[{k:v for k,v in x.items() if k!='text'} for x in result['outputs']])
        result['passed']=True
    except Exception as exc:result['error']=type(exc).__name__+': '+str(exc)
    finally:
        result['terminal_closes']=[]
        if ARM=='B' and server and server.poll() is None:
            for name in ['worker-terminal.json','coordinator-terminal.json']:
                if (TEST/name).exists():
                    try:result['terminal_closes'].append(cli('terminal','close','--terminal',read(name)['handle']))
                    except Exception as exc:result['terminal_closes'].append({'error':str(exc)});result['passed']=False
        result['remaining_cleanup']=stop_tree(server)
        stop.set()
        if sampling:sampling.join(timeout=5)
        result['remaining_task_processes']=process_snapshot(TEST)
        result['passed']=result['passed'] and not result['remaining_cleanup'] and not result['remaining_task_processes']
        result['resource_samples_sha256']=hashlib.sha256((TEST/'resources.jsonl').read_bytes()).hexdigest() if (TEST/'resources.jsonl').exists() else None
        write('result.json',result);assert read('result.json')==result
        write('local-acceptance.json',{'accepted':result['passed'],'local_wall_ms':(time.monotonic()-started)*1000,
            'started_mono':started,'started_utc':utc,'accepted_utc':time.time(),'result_sha256':hashlib.sha256((TEST/'result.json').read_bytes()).hexdigest(),
            'scope':'input entry through final independent QA, cleanup, evidence write/readback; excludes later cloud CEO archive/readback'})
        print(json.dumps({'arm':ARM,'label':LABEL,'accepted':result['passed'],'error':result.get('error'),'local':read('local-acceptance.json')},ensure_ascii=False),flush=True)

if __name__=='__main__':
    try:{'main':main,'coordinator':coordinator,'worker':worker}[ROLE]()
    except Exception as exc:
        if TEST.exists():write(ROLE+'-error.json',{'role':ROLE,'error':str(exc)})
        raise

