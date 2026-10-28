from pathlib import Path
import subprocess,os,json,time
root=Path(__file__).resolve().parent/'source'
env=os.environ.copy()
for line in (root/'.env.local').read_text(encoding='utf-8').splitlines():
 if '=' in line:
  key,value=line.split('=',1);env[key]=json.loads(value)
env['MIGRATIONS_FOLDER']=str(root/'packages'/'db'/'src'/'migrations')
env['NEXT_TELEMETRY_DISABLED']='1'
commands=[['--filter=@louez/voice','build'],['--filter=@louez/web','type-check'],['--filter=@louez/web','build']]
results=[]
for args in commands:
 start=time.time(); print('BUILD_STEP '+args[-1],flush=True)
 p=subprocess.run(['cmd.exe','/d','/c',r'C:\Users\A\AppData\Roaming\npm\pnpm.cmd']+args,cwd=root,env=env,timeout=1200)
 results.append({'args':args,'exit_code':p.returncode,'seconds':round(time.time()-start,3)})
 (root.parent/'build-results.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
 if p.returncode: raise SystemExit(p.returncode)
print('BUILD_ALL_PASS',flush=True)
