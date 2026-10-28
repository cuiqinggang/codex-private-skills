from pathlib import Path
import subprocess,os,json,time,urllib.request,webbrowser,sys,shutil,socket
root=Path(__file__).resolve().parent
source=root/'source'; app=source/'apps'/'web'; output=app/'.next'/'standalone'
env=os.environ.copy(); env['PM2_HOME']=str(root/'runtime'/'pm2-home')
pm2=root/'runtime'/'node_modules'/'pm2'/'bin'/'pm2'
def run(args,timeout=90):
 return subprocess.run(['node',str(pm2)]+args,cwd=root,env=env,timeout=timeout)
def healthy():
 try:
  with urllib.request.urlopen('http://localhost:4399/api/health',timeout=2) as response:
   return response.status==200 and json.load(response).get('status')=='healthy'
 except OSError: return False
def ready():
 print('READY http://localhost:4399',flush=True)
 if '--no-browser' not in sys.argv: webbrowser.open('http://localhost:4399/dashboard')
 raise SystemExit(0)
if '--stop' in sys.argv: raise SystemExit(run(['stop','rental-n001']).returncode)
if not (output/'apps'/'web'/'server.js').is_file(): raise SystemExit('Production build is missing')
if not (output/'apps'/'web'/'public').exists(): shutil.copytree(app/'public',output/'apps'/'web'/'public')
if not (output/'apps'/'web'/'.next'/'static').exists(): shutil.copytree(app/'.next'/'static',output/'apps'/'web'/'.next'/'static')
r=subprocess.run(['node',str(pm2),'jlist'],cwd=root,env=env,capture_output=True,text=True,timeout=30)
data=[]
for offset,char in enumerate(r.stdout):
 if char=='[':
  try:
   candidate=json.loads(r.stdout[offset:])
   if isinstance(candidate,list): data=candidate;break
  except ValueError: pass
known=any(x.get('name')=='rental-n001' for x in data)
if known and healthy(): ready()
if not known:
 with socket.socket() as probe:
  if probe.connect_ex(('127.0.0.1',4399))==0: raise SystemExit('Port4399 is owned by another process')
r=run(['restart','rental-n001','--update-env'] if known else ['start',str(root/'ecosystem.config.cjs')])
if r.returncode: raise SystemExit(r.returncode)
run(['save'])
for _ in range(120):
 if healthy(): ready()
 time.sleep(0.5)
raise SystemExit('Startup health check failed; inspect runtime/pm2-home/logs')
