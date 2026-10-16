import pathlib,json,sys,time,subprocess,hashlib,uuid,shutil,urllib.request,os
import psutil
R=pathlib.Path(__file__).parent;D=R/'V2R2_MIN_20261016';BASE='http://127.0.0.1:8196'
def save(n,v):
 p=D/n;t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def get(p,timeout=3):return json.load(urllib.request.urlopen(BASE+p,timeout=timeout))
def post(p,v,timeout=3):
 req=urllib.request.Request(BASE+p,data=json.dumps(v).encode(),headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=timeout) as q:
  body=q.read()
  return json.loads(body) if body else {'http_status':q.status,'body':''}
def stop_owned(info):
 p=psutil.Process(info['pid'])
 assert p.cmdline()[1:]==info['command'][1:],'SERVICE_OWNER_CHANGED'
 children=p.children(recursive=True)
 for c in reversed(children):
  assert c.cmdline()[1:]==info['command'][1:]
  c.terminate()
 for c in children:
  try:c.wait(timeout=5)
  except psutil.TimeoutExpired:c.kill();c.wait(timeout=3)
 try:p.wait(timeout=5)
 except psutil.TimeoutExpired:p.terminate();p.wait(timeout=3)
 return not p.is_running() and all(not c.is_running() for c in children)
def guard(parent,created):
 info=json.loads((D/'service.json').read_text());samples=[];trigger=None
 while psutil.pid_exists(parent) and psutil.Process(parent).create_time()==created:
  if (D/'batch-result.json').exists() and not json.loads((D/'active.json').read_text()).get('active'):break
  if not (D/'active.json').exists():time.sleep(1);continue
  try:act=json.loads((D/'active.json').read_text())
  except Exception:time.sleep(1);continue
  if not act.get('active'):time.sleep(1);continue
  m=psutil.virtual_memory();elapsed=time.monotonic()-act['started_monotonic']
  s={'phase':act['phase'],'elapsed':elapsed,'ram_percent':m.percent,'ram_available':m.available}
  procs=[]
  try:
   sp=psutil.Process(info['pid'])
   for p in [sp]+sp.children(recursive=True):
    mi=p.memory_info();procs.append({'pid':p.pid,'rss':mi.rss,'private':getattr(mi,'private',None)})
  except psutil.Error:pass
  s['processes']=procs;samples.append(s);save('telemetry.json',samples)
  reason='RAM90' if m.percent>=90 else ('PHASE_900S' if elapsed>=900 else None)
  if reason:
   result={'reason':reason,'at':elapsed,'phase':act['phase'],'prompt_id':act['prompt_id']}
   try:result['interrupt']=post('/interrupt',{'prompt_id':act['prompt_id']})
   except Exception as e:result['interrupt_error']=repr(e)
   # Resource threshold triggers bounded cleanup even if interrupt cannot stop allocation.
   try:result['terminated_owned_service']=stop_owned(info)
   except Exception as e:result['cleanup_error']=repr(e)
   save('guard-stop.json',result);return
  time.sleep(1)
 if (D/'active.json').exists() and json.loads((D/'active.json').read_text()).get('active'):
  try:save('guard-orphan-cleanup.json',{'terminated_owned_service':stop_owned(info)})
  except Exception as e:save('guard-orphan-cleanup.json',{'error':repr(e)})
 save('guard-finished.json',{'samples':len(samples),'stopped':False})
def selftest():
 p=subprocess.Popen([sys.executable,'-c','import time;time.sleep(30)'])
 assert p.poll() is None;p.terminate();p.wait(timeout=5);assert p.poll() is not None
 print('BOUNDED_OWN_CHILD_TERMINATION_PASS',flush=True)
async def execute(label,workflow):
 import aiohttp,asyncio
 q=get('/queue');assert not q['queue_running'] and not q['queue_pending'],'QUEUE_NOT_EMPTY'
 assert psutil.virtual_memory().percent<80,'RAM_ADMISSION_80'
 for node in workflow.values():assert node['class_type'] not in ['SaveVideo','CreateVideo','VAEDecodeAudio']
 pid=str(uuid.uuid4());cid='V2_MIN_'+label
 with (D/(label+'-submission.claim')).open('x') as f:f.write(pid)
 save(label+'-workflow.json',workflow);save(label+'-intent.json',{'prompt_id':pid,'utc':time.time()})
 events=[];spans=[];last=None;last_t=0;start=time.monotonic()
 save('active.json',{'active':True,'phase':label,'prompt_id':pid,'started_monotonic':start})
 async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
  async with session.ws_connect(BASE+'/ws?clientId='+cid) as ws:
   async with session.post(BASE+'/prompt',json={'prompt':workflow,'client_id':cid,'prompt_id':pid}) as r:
    receipt=await r.json();save(label+'-receipt.json',receipt);assert r.status==200,receipt
   pid=receipt['prompt_id'];print('SUBMITTED '+label+' '+pid,flush=True)
   terminal=False;history=None;next_hist=0.
   while time.monotonic()-start<930:
    if (D/'guard-stop.json').exists():raise RuntimeError('GUARD_STOP')
    try:msg=await asyncio.wait_for(ws.receive(),timeout=1)
    except asyncio.TimeoutError:msg=None
    t=time.monotonic()-start
    if msg is not None and msg.type==aiohttp.WSMsgType.TEXT:
     e=json.loads(msg.data);data=e.get('data',{});typ=e.get('type')
     if data.get('prompt_id')==pid:
      events.append({'t':t,'type':typ,'data':data});save(label+'-events.json',events)
      if typ=='executing':
       if last is not None:spans.append({'node':last,'seconds':t-last_t})
       last=data.get('node');last_t=t
       print('NODE '+label+' '+str(last)+' '+str(round(t,2)),flush=True)
      if typ=='progress':print('PROGRESS '+label+' '+str(data.get('value'))+'/'+str(data.get('max')),flush=True)
      if typ in ['execution_error','execution_interrupted','execution_success']:terminal=True;next_hist=0
    if t>=next_hist:
     try:h=get('/history/'+pid)
     except Exception:
      if (D/'guard-stop.json').exists():raise RuntimeError('GUARD_STOP')
      h={}
     if pid in h:history=h[pid];break
     next_hist=t+3
    if terminal and t-last_t>20:raise RuntimeError('TERMINAL_HISTORY_TIMEOUT')
   assert history is not None,'HISTORY_TIMEOUT'
   save(label+'-history.json',history);save(label+'-spans.json',spans)
   assert history['status']['status_str']=='success',history['status']
   outputs=history['outputs']['15']['images'];assert len(outputs)==5,outputs
   from PIL import Image
   imgs=[];files=[]
   for j,item in enumerate(outputs):
    path=R/'output'/item.get('subfolder','')/item['filename']
    assert path.suffix.lower()=='.png' and path.is_file()
    with Image.open(path) as im:
     assert im.size==(1024,576);im.load();imgs.append(im.convert('RGB'))
    files.append({'file':str(path),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    if label=='A':shutil.copyfile(path,R/'input'/('V2_A_FRAME_'+str(j)+'.png'))
   sheet=Image.new('RGB',(1024*5,576))
   for j,im in enumerate(imgs):sheet.paste(im,(1024*j,0))
   sheet.save(D/(label+'-contact.png'))
   result={'status':'success','images':files,'frames':5,'size':[1024,576],'submission_through_image_validation_seconds':time.monotonic()-start,'spans':spans,'quality_review':'PENDING'}
   save(label+'-result.json',result)
   save('active.json',{'active':False,'phase':label})
   return result
async def batch():
 import asyncio
 D.mkdir(exist_ok=True)
 with (D/'batch.claim').open('x') as f:f.write('V2_MIN_AB')
 start=time.monotonic();result={'status':'RUNNING','method':'SANRENXING_V2_C002','bridge':'V7_C','A':None,'comparison':'single complete R2 candidate; B/LMS not executed'}
 try:
  manifest=json.loads((D/'freeze.json').read_text())
  for name,h in manifest['file_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==h,name
  assert manifest['frames']==5 and manifest['video_output']==False
  assert get('/queue')=={'queue_running':[],'queue_pending':[]}
  assert json.loads((R/'GPU-BASELINE-LOCK.json').read_text()).get('authorized_test')=='V2R2_MIN_20261016'
  p=psutil.Process()
  guard_log=(D/'guard.log').open('w')
  g=subprocess.Popen([sys.executable,str(pathlib.Path(__file__)),'--guard',str(p.pid),str(p.create_time())],stdout=guard_log,stderr=subprocess.STDOUT)
  save('guard-process.json',{'pid':g.pid});assert g.poll() is None
  result['A']=await execute('A',json.loads((R/'V2R2_MIN_20261016/workflow.json').read_text(encoding='utf-8')))
  result['status']='IMAGE_BATCH_COMPLETED_REVIEW_PENDING'
 except Exception as e:
  result['status']='STOPPED';result['error']=repr(e)
  if (D/'active.json').exists() and json.loads((D/'active.json').read_text()).get('active') and not (D/'guard-stop.json').exists():
   try:
    q=get('/queue')
    if q['queue_running'] or q['queue_pending']:
     try:post('/interrupt',{})
     except Exception:pass
     result['error_cleanup']=stop_owned(json.loads((D/'service.json').read_text()))
   except Exception as ce:result['error_cleanup_error']=repr(ce)
  save('active.json',{'active':False,'ended_with_error':True})
 finally:
  result['batch_wall_seconds']=time.monotonic()-start
  if (D/'guard-stop.json').exists():result['guard_stop']=json.loads((D/'guard-stop.json').read_text())
  result['T_VALID']=None;result['physical_limit']='UNKNOWN';save('batch-result.json',result)
  print(json.dumps(result,ensure_ascii=False),flush=True)
if __name__=='__main__':
 if '--selftest' in sys.argv:selftest()
 elif '--guard' in sys.argv:guard(int(sys.argv[2]),float(sys.argv[3]))
 else:
  import asyncio
  asyncio.run(batch())
