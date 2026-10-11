import hashlib,json,os,subprocess,sys,tempfile,threading,unittest
from functools import partial
from http.server import HTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from PIL import Image

HERE=Path(__file__).parent
GUARD=HERE.parent/'scripts'/'quality'/'verify_comfy_provenance.py'
WF={
 "1":{"class_type":"UNETLoader","inputs":{"unet_name":"model.safetensors"}},
 "4":{"class_type":"CLIPTextEncode","inputs":{"clip":["2",0],"text":"kitchen"}},
 "2":{"class_type":"DualCLIPLoader","inputs":{"clip_name1":"clip_l.safetensors","clip_name2":"t5.safetensors","type":"flux"}},
 "5":{"class_type":"ConditioningZeroOut","inputs":{"conditioning":["4",0]}},
 "6":{"class_type":"EmptySD3LatentImage","inputs":{"width":512,"height":512,"batch_size":1}},
 "7":{"class_type":"KSampler","inputs":{"model":["1",0],"positive":["4",0],"negative":["5",0],"latent_image":["6",0],"seed":1,"steps":20,"cfg":1.0,"sampler_name":"euler","scheduler":"simple","denoise":1.0}},
 "3":{"class_type":"VAELoader","inputs":{"vae_name":"ae.safetensors"}},
 "8":{"class_type":"VAEDecode","inputs":{"samples":["7",0],"vae":["3",0]}},
 "9":{"class_type":"SaveImage","inputs":{"images":["8",0],"filename_prefix":"test"}}
}
PID='11111111-2222-3333-4444-555555555555'

class ServerHandler(BaseHTTPRequestHandler):
 def do_GET(self):
  if self.path=='/history/'+PID:
   dat=json.dumps({PID:self.server.record}).encode()
   self.send_response(200);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(dat)));self.end_headers();self.wfile.write(dat)
  else:self.send_error(404)
 def log_message(self,*args):pass

class GuardTest(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();root=Path(self.tmp.name);self.folder=root/'evidence';self.folder.mkdir();self.out=root/'out';self.out.mkdir()
  Image.new('RGB',(8,8),'orange').save(self.out/'new.png')
  (self.folder/'generated.png').write_bytes((self.out/'new.png').read_bytes())
  self.writewf(WF)
  (self.folder/'submit.json').write_text(json.dumps({'result':{'prompt_id':PID,'node_errors':{}}}))
  (self.folder/'output.sha256').write_text(hashlib.sha256((self.folder/'generated.png').read_bytes()).hexdigest()+' generated.png\n')
  self.record={'status':{'status_str':'success','completed':True},'prompt':[0,PID,WF], 'outputs':{'9':{'images':[{'filename':'new.png','subfolder':'','type':'output'}]}}}
  (self.folder/'history.json').write_text(json.dumps(self.record))
  self.server=HTTPServer(('127.0.0.1',0),ServerHandler);self.server.record=self.record
  self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
 def tearDown(self):
  self.server.shutdown();self.server.server_close();self.thread.join();self.tmp.cleanup()
 def writewf(self,w):
  p=self.folder/'workflow_api.json';p.write_text(json.dumps(w))
  (self.folder/'workflow.sha256').write_text(hashlib.sha256(p.read_bytes()).hexdigest()+'\n')
 def invoke(self,cert=True,mode='T2I_INDEPENDENT'):
  a=[sys.executable,str(GUARD),'--dir',str(self.folder),'--mode',mode]
  if cert:a+=['--api',f'http://127.0.0.1:{self.server.server_port}','--output-root',str(self.out)]
  return subprocess.run(a,text=True,capture_output=True)
 def test_real_history_and_png_agree_but_quality_remains_manual(self):
  r=self.invoke();self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('"G2": "PASS"',r.stdout);self.assertIn('NO_UNTIL_SOURCE_AND_QUALITY',r.stdout)
 def test_only_preflight_never_certifies_generation(self):
  r=self.invoke(False);self.assertEqual(r.returncode,0);self.assertIn('PREFLIGHT_ONLY',r.stdout);self.assertIn('UNVERIFIED',r.stdout)
 def test_chatgpt_gen_id_is_not_prompt_id(self):
  (self.folder/'submit.json').write_text(json.dumps({'gen_id':'sample-gen-id'}))
  r=self.invoke();self.assertEqual(r.returncode,2);self.assertIn('NO_NATIVE_COMFY_PROMPT_ID',r.stdout)
 def test_bad_independent_reference_path_rejected(self):
  w=json.loads(json.dumps(WF));w['6']={'class_type':'VAEEncode','inputs':{'pixels':['10',0],'vae':['3',0]}};w['10']={'class_type':'LoadImage','inputs':{'image':'reference.png'}};self.writewf(w)
  r=self.invoke(False);self.assertEqual(r.returncode,2);self.assertIn('UNAPPROVED_OR_IMAGE_INPUT_NODE',r.stdout)
 def test_history_workflow_mismatch(self):
  r=self.record.copy();r['status']={'status_str':'error','completed':True}
  (self.folder/'history.json').write_text(json.dumps(r))
  rr=self.invoke();self.assertEqual(rr.returncode,2);self.assertIn('SAVED_HISTORY_VS_LIVE_HISTORY_MISMATCH',rr.stdout)
 def test_png_replacement_rejected(self):
  Image.new('RGB',(8,8),'blue').save(self.folder/'generated.png')
  rr=self.invoke();self.assertEqual(rr.returncode,2);self.assertIn('HISTORY_OUTPUT_VS_EVIDENCE_PNG_MISMATCH',rr.stdout)
 def test_workflow_hash_mutation_rejected(self):
  self.writewf(WF);(self.folder/'workflow_api.json').write_text('edited')
  r=self.invoke(False);self.assertEqual(r.returncode,2);self.assertIn('WORKFLOW_SHA_MISMATCH',r.stdout)

if __name__=='__main__': unittest.main(verbosity=2)
