import os,json,hashlib,shutil,socket,subprocess,time,stat,sys
from pathlib import Path
out=Path('K:/Video-Storage-Audit-20261110')
w=json.loads((out/'action-plan.json').read_text(encoding='utf-8'));p=w['plan']
assert hashlib.sha256(json.dumps(p,sort_keys=True,separators=(',',':')).encode()).hexdigest()==w['sha256']==sys.argv[1]
assert p['host']==socket.gethostname() and time.time()-p['created']<86400
canonical={};events=out/'actions.jsonl'
def log(kind,**kw):
 r={'epoch':time.time(),'kind':kind,**kw}
 with events.open('a',encoding='utf-8') as f:f.write(json.dumps(r)+'\n')
 print(json.dumps(r),flush=True)
def info(path):
 with open(path,'rb') as f:return os.fstat(f.fileno())
def same(r):
 s=info(r['path'])
 return stat.S_ISREG(s.st_mode) and (s.st_size,s.st_mtime_ns,s.st_ino,s.st_dev)==(r['bytes'],r['mtime_ns'],r['inode'],r['device'])
def sha(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  while b:=f.read(8*1024**2):h.update(b)
 return h.hexdigest()
assert shutil.disk_usage('K:/').free>sum(r['bytes'] for t in p['trees'] for r in t['files'])+5*1024**3
for r in p['delete']:
 assert same(r),r['path']
log('preflight_pass',plan_hash=w['sha256'],delete_files=len(p['delete']),migrate_files=sum(len(t['files']) for t in p['trees']),C_free=shutil.disk_usage('C:/').free)
# Exact obsolete transfer paths only; shared hardlink bytes are counted by disk delta.
for r in p['delete']:
 assert same(r)
 os.unlink(r['path']);log('deleted',path=r['path'],logical_bytes=r['bytes'],reason=r['reason'],C_free=shutil.disk_usage('C:/').free)
for t in p['trees']:
 src=Path(t['source']);dst=Path(t['destination'])
 assert not src.is_symlink() and not src.is_junction()
 planned={os.path.normcase(os.path.abspath(r['path'])) for r in t['files']}
 actual={os.path.normcase(os.path.abspath(str(Path(dp)/n))) for dp,ds,fs in os.walk(src,followlinks=False) for n in fs}
 assert actual==planned,('tree_changed',str(src))
 assert all(same(r) for r in t['files'])
 for r in t['files']:
  source=Path(r['path']);target=dst/source.relative_to(src);target.parent.mkdir(parents=True,exist_ok=True)
  assert not target.exists(),str(target)
  key=(r['device'],r['inode'])
  if key in canonical:
   other,digest=canonical[key];os.link(other,target);assert info(target).st_ino==info(other).st_ino
   log('copied_hardlink',source=str(source),target=str(target),bytes=r['bytes'],sha256=digest)
  else:
   temp=target.with_name(target.name+'.copying-'+str(os.getpid()));h=hashlib.sha256()
   with source.open('rb') as inp,temp.open('xb') as output:
    while block:=inp.read(8*1024**2):output.write(block);h.update(block)
    output.flush();os.fsync(output.fileno())
   assert same(r),'source_changed'
   digest=h.hexdigest();assert sha(temp)==digest,'copy_hash_mismatch'
   shutil.copystat(source,temp);temp.rename(target);canonical[key]=(str(target),digest)
   log('copied_verified',source=str(source),target=str(target),bytes=r['bytes'],sha256=digest)
  r['destination']=str(target);r['sha256']=digest
 assert all(same(r) for r in t['files'])
 for r in t['files']:os.unlink(r['path'])
 for d in sorted(t['directories'],key=lambda v:len(Path(v).parts),reverse=True):os.rmdir(d)
 result=subprocess.run(['cmd.exe','/d','/c','mklink','/J',str(src),str(dst)],capture_output=True,text=True)
 if result.returncode:
  log('junction_failed',source=str(src),destination=str(dst),detail=result.stdout+result.stderr);raise RuntimeError('junction failure; verified copies safe on K')
 assert src.is_junction() and all(Path(r['path']).is_file() and info(r['path']).st_size==r['bytes'] for r in t['files'])
 log('tree_migrated_verified',source=str(src),destination=str(dst),C_free=shutil.disk_usage('C:/').free)
 (out/'migration-receipt.json').write_text(json.dumps(p,indent=2),encoding='utf-8')
log('complete',C_free=shutil.disk_usage('C:/').free,free_before=p['free_before'],net_free_gain=shutil.disk_usage('C:/').free-p['free_before'])
