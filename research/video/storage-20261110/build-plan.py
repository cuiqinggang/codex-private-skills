import os,json,hashlib,shutil,time,socket
from pathlib import Path
out=Path('K:/Video-Storage-Audit-20261110')
roots=['C:/AI/MiniMax-H3/ComfyUI/models','C:/AI/MiniMax-H3/models','C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/models','C:/AI/MiniMax-H3-Star7-Repro-Manual/ComfyUI_windows_portable_nvidia/ComfyUI_windows_portable/ComfyUI/models','C:/AI/ComfyUI_Aaki_v3/ComfyUI/models','C:/AI/MuseTalk/models','C:/AI/Video-Recipe-Reproduction-20261110/S2V-15/model-downloads']
plan={'created':time.time(),'host':socket.gethostname(),'free_before':shutil.disk_usage('C:/').free,'destination_root':'K:/Video-Assets-20261110','trees':[],'delete':[]};seen={}
for root in roots:
 files=[];dirs=[]
 for dp,ds,fs in os.walk(root,followlinks=False):
  dirs.append(dp)
  for n in ds:
   p=Path(dp)/n
   if p.is_symlink() or p.is_junction():raise RuntimeError('REPARSE '+str(p))
  for n in fs:
   p=Path(dp)/n
   if p.is_symlink():raise RuntimeError('SYMLINK '+str(p))
   with p.open('rb') as f:s=os.fstat(f.fileno())
   files.append({'path':str(p),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'inode':s.st_ino,'device':s.st_dev,'links':s.st_nlink})
   seen[(s.st_dev,s.st_ino)]=s.st_size
 plan['trees'].append({'source':root,'destination':str(Path(plan['destination_root'])/Path(root).relative_to('C:/')),'files':files,'directories':dirs})
base=Path('C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/BLUE8-PAIRING-20261110/WAN-TRIAL-20261110')
paths=[(base/'models/checkpoints/sdpose_wholebody_fp16.safetensors.download','invalid length; verified final exists'),(base/'models/diffusion_models/Wan2.2-Animate-14B-Q5_K_S.gguf.download','abandoned partial; verified final exists'),(Path('C:/AI/Video-Recipe-Reproduction-20261110/S2V-15/mirror-download/wan2.2_s2v_14B_bf16.part'),'abandoned mirror; complete final exists')]
paths.extend((p,'abandoned attempt; current asset hash-verified') for p in (base/'downloads').rglob('*.incomplete'))
for p,why in paths:
 if not p.is_file():continue
 with p.open('rb') as f:s=os.fstat(f.fileno())
 plan['delete'].append({'path':str(p),'bytes':s.st_size,'mtime_ns':s.st_mtime_ns,'inode':s.st_ino,'device':s.st_dev,'reason':why})
payload=json.dumps(plan,sort_keys=True,separators=(',',':')).encode()
wrapper={'sha256':hashlib.sha256(payload).hexdigest(),'plan':plan}
(out/'action-plan.json').write_text(json.dumps(wrapper,indent=2),encoding='utf-8')
print(json.dumps({'plan_hash':wrapper['sha256'],'migrate_unique_bytes':sum(seen.values()),'trees':[{'source':t['source'],'files':len(t['files']),'logical_bytes':sum(r['bytes'] for r in t['files'])} for t in plan['trees']],'delete_paths':plan['delete'],'C_free':plan['free_before'],'K_free':shutil.disk_usage('K:/').free}),flush=True)
