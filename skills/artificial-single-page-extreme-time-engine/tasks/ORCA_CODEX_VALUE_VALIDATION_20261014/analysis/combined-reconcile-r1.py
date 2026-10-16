import runpy,json,pathlib,hashlib,subprocess,sys,time,psutil
R=pathlib.Path('C:/AI/Orca-Codex-Validation-20261014')
P=R/'combined-business-r1.py'
assert hashlib.sha256(P.read_bytes()).hexdigest()=='fca83d88fc75c62640251aa52dc6f69f88edca1db266017bad83a83a74d9dc77'
m=runpy.run_path(str(P),run_name='reconciliation_only')
T=m['TEST'];read=m['read'];W=pathlib.Path(read('worktree.json')['path'])
original=read('result.json');assert original['error']=='AGENTS.md' and not original['passed']
assert original['coordinator']['task_status']==original['coordinator']['dispatch_status']=='completed'
assert original['worker']['accepted'] and original['worker']['same_dispatch_identity']
assert len(original['qa'])==10 and all(x['passed'] for x in original['qa'])
assert (W/'AGENTS.md').read_bytes()==m['SPEC'].encode('utf-8')
head=subprocess.run(['git','show','HEAD:AGENTS.md'],cwd=W,capture_output=True,check=True,timeout=20).stdout
assert head==(W/'AGENTS.md').read_bytes()
dataset=json.loads((R/'DATASET_MANIFEST.json').read_text(encoding='utf-8-sig'))
unchanged=[]
for e in dataset['input_files']:
    if e['path'] in ('AGENTS.md','llm_verifier/fine_grained_reward.py'):continue
    assert hashlib.sha256((W/e['path']).read_bytes()).hexdigest()==e['sha256'],e['path']
    unchanged.append(e['path'])
assert m['manifest']()==read('input.json')['expected']
test=subprocess.run([sys.executable,'-X','utf8',str(W/'tests/test_t01_offline.py')],cwd=W,capture_output=True,text=True,encoding='utf-8',timeout=45)
assert test.returncode==0,test.stderr
status=subprocess.run(['git','status','--porcelain','--untracked-files=all'],cwd=W,capture_output=True,text=True,check=True,timeout=20).stdout
allowed={'llm_verifier/fine_grained_reward.py','tests/test_t01_offline.py','DELIVERY.md'}
for line in status.splitlines():
    assert line[3:] in allowed or '__pycache__/' in line[3:],line
diff=subprocess.run(['git','diff','--','llm_verifier/fine_grained_reward.py'],cwd=W,capture_output=True,text=True,encoding='utf-8',check=True,timeout=20).stdout
outputs=[{'path':n,'sha256':hashlib.sha256((W/n).read_bytes()).hexdigest(),'size':(W/n).stat().st_size,'text':(W/n).read_text(encoding='utf-8')} for n in sorted(allowed)]
owned=[]
for p in psutil.process_iter(['pid','name','cmdline']):
    cmd=' '.join(p.info['cmdline'] or []).replace('\\','/').lower()
    if p.info['name'].lower() in ('node.exe','codex.exe') and str(T).replace('\\','/').lower() in cmd:owned.append(p.info['pid'])
assert not owned,owned
result={'accepted':True,'scope':'ORCA_CODEX_T01_COMBINED_BUSINESS_RECOVERED','original':original,
'original_local_acceptance':read('local-acceptance.json'),
'correction':'Harness compared intentionally injected AGENTS.md to original dataset. Verified exact frozen SPEC bytes and committed HEAD; no business/model/runtime rerun.',
'agents_sha256':hashlib.sha256((W/'AGENTS.md').read_bytes()).hexdigest(),'unchanged_inputs':unchanged,
'previous_T03_unchanged':True,'offline_tests':{'returncode':test.returncode,'stdout':test.stdout,'stderr':test.stderr},
'git_status':status,'diff':diff,'outputs':outputs,'remaining_task_node_codex':owned,
'cleanup_note':'Original finally terminated runtime descendants; explicit terminal-close step was not reached. Runtime not restarted to cosmetically close persisted panes.',
'input':read('input.json')}
out=T/'reconciled-acceptance.json';assert not out.exists()
out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
assert json.loads(out.read_text(encoding='utf-8'))==result
timing={'accepted':True,'entry_through_reconciled_readback_ms':(time.monotonic()-result['input']['started_mono'])*1000,'includes':'initial timeout, exact resume, Orca settlement, harness failure, diagnosis, independent reconciliation and local readback','excludes':'prior analysis/deployment and later remote archival/readback'}
(T/'reconciled-time.json').write_text(json.dumps(timing,indent=2),encoding='utf-8')
print(json.dumps({'accepted':True,'tests':test.stderr,'outputs':[{k:v for k,v in e.items() if k!='text'} for e in outputs],'timing':timing,'diff':diff},ensure_ascii=False))
