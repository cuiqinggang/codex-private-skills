import pathlib,json,time,uuid,subprocess,sys,asyncio,importlib.util,hashlib,traceback,shutil
import psutil,aiohttp,av,numpy as np
R=pathlib.Path(r'C:\AI\MiniMax-H3\projects\H3-MINIMAL-20261015')
ROOT=pathlib.Path(r'C:\AI\TenYears-Animatic-20261030')
BASE='http://127.0.0.1:8197'
SHOT=sys.argv[1]
CFG=json.loads((ROOT/'R9/config.json').read_text(encoding='utf-8'))[SHOT]
D=ROOT/'R9'/SHOT;D.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('mature_guard',ROOT/'R8/guard_ram95.py')
guardmod=importlib.util.module_from_spec(spec);spec.loader.exec_module(guardmod)
guardmod.D=D;guardmod.BASE=BASE
def save(n,v):guardmod.save(n,v)
PROMPTS={SHOT:CFG['prompt']}
async def run():
 assert psutil.virtual_memory().percent<90,'RAM_ADMISSION_90'
 q=guardmod.get('/queue');assert not q['queue_running'] and not q['queue_pending'],'BUSY_QUEUE'
 with (D/'submission.claim').open('x') as f:f.write(SHOT)
 w=json.loads(pathlib.Path(r'C:\Users\A\Desktop\H3_V4_5F_BATCH_20261017\A2\A2-workflow.json').read_text(encoding='utf-8-sig'))
 w['6']['inputs'].update(width=384,height=320,length=CFG['frames'],prompt=PROMPTS[SHOT])
 w['20']['inputs']['image']=CFG['first']

 w['22']={'class_type':'LoadImage','inputs':{'image':CFG['last']}}
 w['6']['inputs']['last_frame']=['22',0]
 parent='6'
 for j,(frame,tag) in enumerate(CFG.get('guides',[])):
  ni=str(40+j*2);ng=str(41+j*2)
  w[ni]={'class_type':'LoadImage','inputs':{'image':'HOTMEAL_R9_'+tag+'.jpg'}}
  w[ng]={'class_type':'MiniMaxH3AddGuide','inputs':{'positive':[parent,0],'latent':['6',1],'frame_idx':frame,'vae':['4',0],'image':[ni,0]}}
  parent=ng
 w['7']['inputs']['conditioning']=[parent,0]

 
 
 w['21']={'class_type':'CLIPLoader','inputs':{'clip_name':'qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors','type':'minimax','device':'default'}}
 w['10']['inputs']['noise_seed']=CFG['seed']
 w['5']={'class_type':'VAELoader','inputs':{'vae_name':'minimax_h3_audio_vae_fp32.safetensors'}}
 w['13']={'class_type':'VAEDecodeAudio','inputs':{'samples':['11',0],'vae':['5',0]}}
 w['14']={'class_type':'CreateVideo','inputs':{'images':['12',0],'audio':['13',0],'bit_depth':8,'fps':24}}
 w['15']={'class_type':'SaveVideo','inputs':{'video':['14',0],'filename_prefix':'HOTMEAL_R9_NATIVE_AV_'+SHOT+'_SHORT','format':'auto','codec':'auto'}}
 assert w['9']['inputs']['steps']==20 and w['30']['inputs']['threshold']==0.08
 save('workflow.json',w);save('contract.json',{'version':'HOTMEAL-R9-OPENING-PHONE','authorized_by':'user20261031','shot':SHOT,'input_sha256':hashlib.sha256((R/'input'/CFG['first']).read_bytes()).hexdigest(),'steps':20,'cache':'SAFE','dimensions':[384,320],'frames':w['6']['inputs']['length'],'fps':24,'guard':'task-scoped admission RAM90 and independent RAM95 guard; time budget from per-shot config','quality':'REVIEW_PENDING','native_audio':'generated Chinese exactness must review','source_workflow':'V4.1 A2 default, portrait/length/audio/output adapted','changes_not_certified_as_same_quality':True,'started_unix':time.time()})
 shutil.copyfile(ROOT/'service.json',D/'service.json')
 guardlog=(D/'guard.log').open('w')
 gp=subprocess.Popen([sys.executable,str(ROOT/'R8/guard_ram95.py'),'--guard',str(psutil.Process().pid),str(psutil.Process().create_time()),'--test-dir',str(D),'--test-base',BASE,'--phase-seconds',str(CFG.get('phase_seconds',900))],stdout=guardlog,stderr=subprocess.STDOUT)
 start=time.monotonic();pid=str(uuid.uuid4());cid='TENYEARS_'+SHOT
 save('active.json',{'active':True,'phase':SHOT,'prompt_id':pid,'started_monotonic':start})
 save('intent.json',{'prompt_id':pid,'time':time.time()})
 events=[];telemetry=[];history=None
 try:
  async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
   async with session.ws_connect(BASE+'/ws?clientId='+cid) as ws:
    async with session.post(BASE+'/prompt',json={'prompt':w,'client_id':cid,'prompt_id':pid}) as r:
     receipt=await r.json();save('receipt.json',receipt);assert r.status==200,receipt
    pid=receipt['prompt_id'];print('SUBMITTED',SHOT,pid,flush=True)
    nh=0;nt=0
    while time.monotonic()-start<CFG.get('phase_seconds',900)+30:
     assert gp.poll() is None,'GUARD_EXITED'
     assert not (D/'guard-stop.json').exists(),'GUARD_STOP'
     elapsed=time.monotonic()-start
     try:msg=await asyncio.wait_for(ws.receive(),timeout=1)
     except asyncio.TimeoutError:msg=None
     if msg is not None and msg.type==aiohttp.WSMsgType.TEXT:
      e=json.loads(msg.data);data=e.get('data',{})
      if data.get('prompt_id')==pid:
       events.append({'t':elapsed,**e});save('events.json',events)
       if e['type'] in ['executing','progress','execution_error','execution_success']:print(e['type'],data.get('node'),data.get('value'),data.get('max'),round(elapsed,2),flush=True)
     if elapsed>=nt:
      try:g=subprocess.check_output(['nvidia-smi','--query-gpu=memory.used,utilization.gpu','--format=csv,noheader,nounits'],text=True,timeout=3).strip()
      except Exception:g='UNAVAILABLE'
      telemetry.append({'t':elapsed,'ram':psutil.virtual_memory().percent,'gpu':g});save('gpu-telemetry.json',telemetry);nt=elapsed+5
     if elapsed>=nh:
      try:
       h=guardmod.get('/history/'+pid,timeout=5)
      except (OSError,TimeoutError) as connection_error:
       save('control-connection-warning.json',{'elapsed':elapsed,'error':repr(connection_error),'action':'keep independent guard alive and recheck same prompt; no resubmission'})
       nh=elapsed+3
       continue
      if pid in h:history=h[pid];break
      nh=elapsed+4
  assert history is not None,'NO_HISTORY'
  save('history.json',history)
  assert history['status']['status_str']=='success',history['status']
  out=history['outputs']['15'];save('outputs.json',out)
  candidates=list((R/'output').glob('HOTMEAL_R9_NATIVE_AV_'+SHOT+'_SHORT'+'*.mp4'))
  assert len(candidates)==1,candidates
  f=candidates[0];shutil.copyfile(f,D/'native.mp4')
  with av.open(str(f)) as c:frames=[z.to_image() for z in c.decode(video=0)]
  assert len(frames)==CFG['frames'] and frames[0].size==(384,320)
  af=0
  with av.open(str(f)) as c:
   for a in c.decode(audio=0):assert np.isfinite(a.to_ndarray()).all();af+=1
  from PIL import Image,ImageDraw
  sheet=Image.new('RGB',(576*4,1050*3),'white')
  for j in range(12):
   idx=round(j*(len(frames)-1)/11);sheet.paste(frames[idx],((j%4)*576,(j//4)*1050));ImageDraw.Draw(sheet).text(((j%4)*576+8,(j//4)*1050+1026),str(idx),fill='black')
  sheet.save(D/'contact.jpg',quality=90)
  result={'state':'GENERATED_REVIEW_PENDING','file':str(D/'native.mp4'),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'frames':len(frames),'audio_frames':af,'submission_through_decode_seconds':time.monotonic()-start,'T_VALID':None}
 except Exception as e:
  result={'state':'FAILED','error':repr(e),'traceback':traceback.format_exc(),'elapsed':time.monotonic()-start}
  try:
   q=guardmod.get('/queue')
   if any(x[1]==pid for x in q['queue_running']):guardmod.post('/interrupt',{'prompt_id':pid})
  except Exception:pass
 finally:
  save('active.json',{'active':False});save('batch-result.json',result)
  try:gp.wait(timeout=8)
  except subprocess.TimeoutExpired:gp.terminate()
  print(json.dumps(result,ensure_ascii=False),flush=True)
 return result
asyncio.run(run())
