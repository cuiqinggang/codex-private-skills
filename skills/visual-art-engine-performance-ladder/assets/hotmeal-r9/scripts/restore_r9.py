from pathlib import Path
import json,subprocess,shutil,time,uuid,urllib.request,psutil,av,hashlib,sys,traceback
R=Path('C:/AI/TenYears-Animatic-20261030');P=Path('C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015');BASE='http://127.0.0.1:8197'
def req(path,data=None):
 q=urllib.request.Request(BASE+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(q,timeout=10) as f:
  body=f.read()
  return json.loads(body) if body else {}
def save(d,n,v): (d/n).write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8')
gate=json.loads((R/'R9/upstream-disposition.json').read_text(encoding='utf-8'));assert gate['allow_restoration_for_human_review'] is True
sources={'A':R/'R9/A/native.mp4','P':R/'R9/P/native.mp4','B_AV':R/'R8/B_AV/native.mp4','C':R/'R8/C/native.mp4'};counts={'A':73,'P':39,'B_AV':73,'C':175}
assert not any(req('/queue').values());req('/free',{'unload_models':True,'free_memory':True})
results=[]
for label,source in sources.items():
 D=R/'R9/RESTORE'/label;D.mkdir(exist_ok=True);assert not any(req('/queue').values());assert psutil.virtual_memory().percent<90
 with(D/'submission.claim').open('x') as f:f.write('SR only; no motion regeneration')
 shutil.copyfile(source,P/'input'/f'HOTMEAL_R9_RESTORE_INPUT_{label}.mp4')
 w={'1':{'class_type':'LoadVideo','inputs':{'file':f'HOTMEAL_R9_RESTORE_INPUT_{label}.mp4'}},'2':{'class_type':'GetVideoComponents','inputs':{'video':['1',0]}},'3':{'class_type':'UpscaleModelLoader','inputs':{'model_name':'RealESRGAN_x2plus.pth'}},'4':{'class_type':'ImageUpscaleWithModel','inputs':{'upscale_model':['3',0],'image':['2',0]}},'5':{'class_type':'CreateVideo','inputs':{'images':['4',0],'audio':['2',1],'fps':24,'bit_depth':8}},'6':{'class_type':'SaveVideo','inputs':{'video':['5',0],'filename_prefix':f'HOTMEAL_R9_RESTORE_{label}','format':'auto','codec':'auto'}}}
 save(D,'workflow.json',w);shutil.copyfile(R/'service.json',D/'service.json')
 inf=json.loads((D/'service.json').read_text(encoding='utf-8'));assert psutil.Process(inf['pid']).cmdline()[1:]==inf['command'][1:]
 pid=str(uuid.uuid4());start=time.monotonic();save(D,'active.json',{'active':True,'phase':'SR_'+label,'prompt_id':pid,'started_monotonic':start})
 gl=(D/'guard.log').open('w');g=subprocess.Popen([sys.executable,str(R/'R8/guard_ram95.py'),'--guard',str(psutil.Process().pid),str(psutil.Process().create_time()),'--test-dir',str(D),'--test-base',BASE,'--phase-seconds','900'],stdout=gl,stderr=subprocess.STDOUT)
 try:
  receipt=req('/prompt',{'prompt':w,'client_id':'HOTMEAL_R9_RESTORE','prompt_id':pid});save(D,'receipt.json',receipt);assert 'prompt_id' in receipt,receipt
  pid=receipt['prompt_id'];print('SR_SUBMITTED',label,pid,flush=True);history=None;errors=[]
  while time.monotonic()-start<900:
   assert g.poll() is None,'GUARD_DIED';assert not(D/'guard-stop.json').exists(),'GUARD_STOP'
   try:h=req('/history/'+pid)
   except Exception as e:errors.append(type(e).__name__);time.sleep(2);continue
   if pid in h:history=h[pid];break
   time.sleep(2)
  assert history is not None,'HISTORY_TIMEOUT';save(D,'history.json',history);assert history['status']['status_str']=='success',history['status']
  files=list((P/'output').glob(f'HOTMEAL_R9_RESTORE_{label}*.mp4'));assert len(files)==1,files
  out=D/'restored.mp4';shutil.copyfile(files[0],out)
  with av.open(str(out)) as v:
   fs=0
   for f in v.decode(video=0):assert (f.width,f.height)==(768,640);fs+=1
  assert fs==counts[label],(label,fs)
  with av.open(str(out)) as v:assert sum(1 for f in v.decode(audio=0))>0
  result={'state':'RESTORED_REVIEW_PENDING','frames':fs,'dimensions':[768,640],'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'seconds':time.monotonic()-start,'transient_history_errors':errors,'motion_regenerated':False,'human_approval':False}
  save(D,'result.json',result);results.append(result);print('SR_DONE',label,json.dumps(result),flush=True)
 except Exception as e:
  result={'state':'FAILED','error':repr(e),'traceback':traceback.format_exc()};save(D,'result.json',result);print(json.dumps(result),flush=True);raise
 finally:
  save(D,'active.json',{'active':False});save(D,'batch-result.json',result)
  try:g.wait(timeout=8)
  except subprocess.TimeoutExpired:g.terminate();g.wait(timeout=5)
  gl.close()
assert not any(req('/queue').values());req('/free',{'unload_models':True,'free_memory':True})
save(R/'R9/RESTORE','batch-result.json',{'state':'FOUR_SHOTS_RESTORED_REVIEW_PENDING','results':results,'human_approval':False});print('SR_BATCH_COMPLETED',flush=True)
