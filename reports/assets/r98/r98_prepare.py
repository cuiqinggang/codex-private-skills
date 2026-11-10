from pathlib import Path
import json,hashlib,shutil,ast,time
B=Path(__file__).resolve().parent;O=B/'r98-two-step';OLD=B/'r96-29s-reality';S=O/'snapshot'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not O.exists(),'Existing experiment: reconcile, do not duplicate'
freeze=json.loads((OLD/'EXPERIMENT-FREEZE.json').read_text())
assert all(sha(OLD/n)==h for n,h in freeze['snapshot_sha256'].items())
O.mkdir();shutil.copytree(OLD/'snapshot',S,ignore=shutil.ignore_patterns('__pycache__'))
def one(s,a,b):
 assert s.count(a)==1,(a,s.count(a))
 return s.replace(a,b)
delivery=(S/'scripts/deliver_archive_batch.py').read_text(encoding='utf-8')
start=delivery.index(' def verify_one(item):');end=delivery.index(' items=list(zip(',start)
verify=delivery[start:end]
# Reuse the existing verifier's receipt/manifest/source checks. Original archive already re-reads inputs, ZIP bytes and CRC.
verify=verify.replace('  assert tree(j/req["input_directory"])==expected\n','')
lo=verify.index('  with zipfile.ZipFile(');hi=verify.index('  assert json.loads((j/"manifest.json")',lo)
verify=verify[:lo]+verify[hi:]
verify=verify.replace(' def verify_one(item):','def verify_one(item):',1)
# Remove one nesting space from all lines except function declaration.
lines=verify.splitlines();verify='\n'.join([lines[0]]+[line[1:] if line.startswith(' ') else line for line in lines[1:]])+'\n'
helper='from pathlib import Path\nimport hashlib,json\ndef sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()\n'+verify
ast.parse(helper);(S/'scripts/accept_archive_item.py').write_text(helper,encoding='utf-8')
worker=(S/'scripts/archive_stream_worker.py').read_text(encoding='utf-8')
worker=one(worker,'def main():','from accept_archive_item import verify_one\ndef main():')
worker=one(worker,'match_s=None','match_s=None;item_acceptance=None')
worker=one(worker,'   assert sha(programme)==expected_source\n  except Exception','   assert sha(programme)==expected_source\n   item_acceptance=verify_one((cwd,req,{"exit_code":0,"cwd":str(cwd),"input_hashes":plan["input_hashes"],"source_hashes":plan["source_hashes"]}))\n  except Exception')
worker=one(worker,'"input_hashes":plan["input_hashes"] if plan else {}','"item_acceptance":item_acceptance,"input_hashes":plan["input_hashes"] if plan else {}')
ast.parse(worker);(S/'scripts/archive_stream_worker.py').write_text(worker,encoding='utf-8')
lo=delivery.index(' def verify_one(item):');hi=delivery.index(' final_qa_s=',lo)
delivery=delivery[:lo]+''' qa_started=time.perf_counter()
 verified=[]
 assert {x["index"] for x in execution["results"]}==set(range(len(jobs)))
 for j,ex in zip(jobs,execution["results"]):
  assert ex["exit_code"]==0 and Path(ex["cwd"]).resolve()==j
  item=ex["item_acceptance"]
  assert item and Path(item["workspace"]).resolve()==j and item["files"]>0
  verified.append(item)
'''+delivery[hi:]
delivery=delivery.replace('Original fixed QA plus independent paths, bytes, CRC, manifest, delivery fingerprints, unchanged input and unchanged source','Original per-item archive byte/CRC/input QA plus immediate existing manifest/source/output fingerprint verifier; batch completion checks IDs, failures and receipts only')
ast.parse(delivery);(S/'scripts/deliver_archive_batch.py').write_text(delivery,encoding='utf-8')
launch=(OLD/'launch_pi.py').read_text(encoding='utf-8');(O/'launch_pi.py').write_text(launch,encoding='utf-8')
bench=(B/'r97-four-simple/benchmark.py').read_text(encoding='utf-8')
bench=one(bench,'R=B/"r97-four-simple/run";L=B/"r96-29s-reality/snapshot"','R=B/"r98-two-step/run";L=B/"r98-two-step/snapshot"')
bench=one(bench,'ENTRY=B/"r96-29s-reality/launch_pi.py"','ENTRY=B/"r98-two-step/launch_pi.py"')
bench=bench.replace('PI-R97-FOUR-SIMPLE-20261111','PI-R98-TWO-STEP-20261111')
bench=one(bench,'L/"scripts/archive_stream_worker.py",','L/"scripts/archive_stream_worker.py",L/"scripts/accept_archive_item.py",')
bench=one(bench,'row={"case":case.name,','row={"production_s":cli_end-start,"production_with_fixture_s":cli_end-fixture_start,"batch_completion_check_s":json.loads(result["final_cli_receipt"])["final_qa_s"],"case":case.name,')
ast.parse(bench);(O/'benchmark.py').write_text(bench,encoding='utf-8')
# Guard the adaptation: original per-item archive and matcher are byte-identical.
for n in ['scripts/match_flow.py','scripts/batch_handoff.py','assets/ready-flows/pi-native/artifact_recipe.py']:
 assert sha(S/n)==sha(OLD/'snapshot'/n)
# Exercise the unchanged assertion bodies on real previously accepted artifacts, then corrupt copies.
import importlib.util
sp=importlib.util.spec_from_file_location('item_check',S/'scripts/accept_archive_item.py');m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
oldcase=B/'r97-four-simple/run/case-01-w4/work'
r=json.loads((oldcase/'EXECUTION.json').read_text())['results'][0]
req=json.loads((oldcase/'request-00.json').read_text())
j=O/'preflight-item';j.mkdir()
for n in ['delivery.zip','manifest.json','delivery.json']:shutil.copy2(Path(r['cwd'])/n,j/n)
ex={**r,'cwd':str(j)}
assert m.verify_one((j,req,ex))
receipt=(j/'delivery.json').read_bytes();manifest=(j/'manifest.json').read_bytes();zbytes=(j/'delivery.zip').read_bytes()
attacks=[]
for kind in ['manifest_mismatch','zip_corruption','false_qa','wrong_workspace']:
 try:
  if kind=='manifest_mismatch':(j/'manifest.json').write_text('{}')
  if kind=='zip_corruption':(j/'delivery.zip').write_bytes(zbytes+b'changed')
  if kind=='false_qa':
   data=json.loads(receipt);data['qa']['pass']=False;(j/'delivery.json').write_text(json.dumps(data))
  testex={**ex,'cwd':str(O)} if kind=='wrong_workspace' else ex
  m.verify_one((j,req,testex))
 except (AssertionError,ValueError):attacks.append(kind)
 finally:
  (j/'delivery.json').write_bytes(receipt);(j/'manifest.json').write_bytes(manifest);(j/'delivery.zip').write_bytes(zbytes)
assert len(attacks)==4
plan={'task_id':'PI-R98-TWO-STEP-20261111','created_epoch':time.time(),'virtual_mature':True,'order':[1,4,4,1],'partition':'128 same archive tasks; 4 contiguous groups of32 or one group128','pipeline':'select existing recipe and partition -> persistent lanes execute original archive with per-item full original QA and immediate receipt binding; only count/ID/failure/receipt aggregation at batch end','reuse':'R97 partition; original R96 archive/matcher/handoff; existing verify_one receipt/source/manifest/hash assertions copied without semantic change','removed_duplicates':['internal batch re-read of input tree','internal batch second ZIP byte and CRC pass'],'preserved':['original per-item input pre/during/post checks','original per-item ZIP full bytes CRC path and count','manifest equals matcher-admitted original input hashes','source before/after, output sha256 and receipt readback','sandbox bounds, unique workspaces, no process-per-item','test-only independent full audit still retained in total_s for both1 and4'],'clocks':{'production_s':'input-ready through per-item acceptance and lightweight batch completion receipt, includes entry/exit','production_with_fixture_s':'plus actual input provisioning','total_s':'production + same fixed4-thread independent full benchmark audit + RESULT write/readback','total_with_fixture_s':'full test acceptance including actual provisioning; primary comparison with R97 2.49x'},'test_contract':'all 128 tasks x48 files same unique markers, both modes same checks; keep slow/failed cases; stop on quality failure; exactly4 batches no fastest-sample reruns','preflight_attacks_rejected':attacks,'performance_claim':'NOT_MEASURED until Reality','historical_source_gap':'same known R94 delivery gap; R97/R98 use R96 reference, not claimed bit-identical R94','source_sha256':{str(p.relative_to(O)):sha(p) for p in O.rglob('*.py')},'prepare_sha256':sha(Path(__file__))}
(O/'FREEZE.json').write_text(json.dumps(plan,indent=2),encoding='utf-8')
print(json.dumps({'prepared':True,'preflight_rejected':attacks,'source_files':len(plan['source_sha256']),'freeze_sha256':sha(O/'FREEZE.json')}),flush=True)
