#!/usr/bin/env python3
"""Reversible H3-P0 PATH instrumentation on the V3 reserve baseline."""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(r"C:\AI\MiniMax-H3\ComfyUI")
SELF=Path(__file__)
RUNNER=SELF.with_name("H3-P0-runner.py")
FILES={
 "comfy/sampler_helpers.py": [
 ('    comfy.model_management.load_models_gpu([model] + models, memory_required=memory_required, minimum_memory_required=minimum_memory_required, force_full_load=force_full_load)',
  '    torch.cuda.synchronize()\n    _h3_t0=_h3_time.time_ns()\n    comfy.model_management.load_models_gpu([model] + models, memory_required=memory_required, minimum_memory_required=minimum_memory_required, force_full_load=force_full_load)\n    torch.cuda.synchronize()\n    _h3_t1=_h3_time.time_ns()\n    print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_H3_LOAD_OR_TRANSFER","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)')
 ],
 "comfy/model_management.py": [
 ('        if memory_to_free > 0 and current_loaded_models[i].model_unload(memory_to_free):\n            logging.debug(f"Unloading {current_loaded_models[i].model.model.__class__.__name__}")\n            unloaded_model.append(i)',
  '        if memory_to_free > 0:\n            _h3_class=current_loaded_models[i].model.model.__class__.__name__\n            torch.cuda.synchronize()\n            _h3_t0=_h3_time.time_ns()\n            _h3_unloaded=current_loaded_models[i].model_unload(memory_to_free)\n            torch.cuda.synchronize()\n            _h3_t1=_h3_time.time_ns()\n            print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_MODEL_OFFLOAD","model_class":_h3_class,"start_ns":_h3_t0,"end_ns":_h3_t1,"fully_unloaded":_h3_unloaded}),flush=True)\n            if _h3_unloaded:\n                logging.debug(f"Unloading {_h3_class}")\n                unloaded_model.append(i)')
 ],
 "comfy/sd.py": [
 ('                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)\n                free_memory = self.patcher.get_free_memory(self.device)',
  '                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                torch.cuda.synchronize()\n                _h3_t0=_h3_time.time_ns()\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)\n                torch.cuda.synchronize()\n                _h3_t1=_h3_time.time_ns()\n                print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_LOAD","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)\n                free_memory = self.patcher.get_free_memory(self.device)')
 ],
 "nodes.py": [
 ('        images = vae.decode(latent)',
  '        torch.cuda.synchronize()\n        _h3_t0=_h3_time.time_ns()\n        images = vae.decode(latent)\n        torch.cuda.synchronize()\n        _h3_t1=_h3_time.time_ns()\n        print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_NODE","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)')
 ],
 "comfy_extras/nodes_video.py": [
 ('        video.save_to(\n            os.path.join(full_output_folder, file),\n            format=Types.VideoContainer(format_name),\n            codec=Types.VideoCodec(codec_name),\n            metadata=saved_metadata,\n            crf=encoding.get("crf"),\n        )',
  '        torch.cuda.synchronize()\n        _h3_t0=_h3_time.time_ns()\n        video.save_to(\n            os.path.join(full_output_folder, file),\n            format=Types.VideoContainer(format_name),\n            codec=Types.VideoCodec(codec_name),\n            metadata=saved_metadata,\n            crf=encoding.get("crf"),\n        )\n        torch.cuda.synchronize()\n        _h3_t1=_h3_time.time_ns()\n        print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VIDEO_SAVE","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)'),
 ('        if bit_depth == "auto":\n            bit_depth = 10 if color_space in ("HDR", "HDR PQ") else 8\n        return io.NodeOutput(',
  '        if bit_depth == "auto":\n            bit_depth = 10 if color_space in ("HDR", "HDR PQ") else 8\n        _h3_t0=_h3_time.time_ns()\n        _h3_result=io.NodeOutput('),
 ('                color_space=color_space,\n            )\n        )\n\nclass GetVideoComponents',
  '                color_space=color_space,\n            )\n        )\n        _h3_t1=_h3_time.time_ns()\n        print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VIDEO_CREATE","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)\n        return _h3_result\n\nclass GetVideoComponents')
 ]
}
def digest(data): return hashlib.sha256(data).hexdigest().upper()
def atomic(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_name(path.name+f".{os.getpid()}.tmp")
 temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
 os.replace(temp,path)
def inject_imports(s):
 import_line="import time as _h3_time, json as _h3_json\n"
 future="from __future__ import annotations\n"
 return s.replace(future,future+import_line,1) if future in s else import_line+s

def instrument(e):
 manifest=[]
 for rel,changes in FILES.items():
  target=ROOT/rel; raw=target.read_bytes(); newline="\r\n" if b"\r\n" in raw else "\n"
  backup=e/"profile-backups"/rel
  if backup.exists() and backup.read_bytes()!=raw: raise RuntimeError(f"backup mismatch {rel}")
  if not backup.exists():
   backup.parent.mkdir(parents=True,exist_ok=True); backup.write_bytes(raw)
  s=raw.decode("utf-8").replace("\r\n","\n")
  if "H3_P0_STAGE " in s: raise RuntimeError(f"already patched {rel}")
  for old,new in changes:
   if s.count(old)!=1: raise RuntimeError(f"patch boundary {rel}: {s.count(old)} {old[:60]}")
   s=s.replace(old,new,1)
  s=inject_imports(s)
  patched=s.replace("\n",newline).encode("utf-8")
  manifest.append({"path":str(target),"backup":str(backup),"sha_before":digest(raw),"sha_instrumented":digest(patched)})
 atomic(e/"profile-instrumentation-manifest.json",{"files":manifest,"created":time.time()})
 # Write calculated bytes only after all patch boundaries and backups validate.
 for rel,changes in FILES.items():
  target=ROOT/rel; raw=(e/"profile-backups"/rel).read_bytes(); newline="\r\n" if b"\r\n" in raw else "\n"
  s=raw.decode("utf-8").replace("\r\n","\n")
  for old,new in changes: s=s.replace(old,new,1)
  target.write_bytes(inject_imports(s).replace("\n",newline).encode("utf-8"))
 return manifest
def restore(e):
 manifest=json.loads((e/"profile-instrumentation-manifest.json").read_text(encoding="utf-8"))
 proof=[]
 for item in manifest["files"]:
  target=Path(item["path"]); backup=Path(item["backup"])
  before=backup.read_bytes(); target.write_bytes(before)
  after=target.read_bytes()
  proof.append({**item,"sha_after":digest(after),"restored":digest(after)==item["sha_before"]})
 result={"files":proof,"restored":all(x["restored"] for x in proof),"time":time.time()}
 atomic(e/"profile-instrumentation-proof.json",result)
 return result
def event(row,name):
 found=[x for x in row["path_stage_events"] if x.get("stage")==name]
 if len(found)!=1: raise RuntimeError(f"{row['seed']} {name} count {len(found)}")
 return found[0]
def duration(x): return (x["end_ns"]-x["start_ns"])/1e9
def pct(a,q):
 a=sorted(a);x=(len(a)-1)*q;i=int(x)
 return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
def analyze(e,phase):
 rows=[]
 for f in sorted((e/"runs"/phase).glob("run-*.json")):
  row=json.loads(f.read_text(encoding="utf-8"))
  if not row.get("task_completed"): raise RuntimeError(f"incomplete {f}")
  load=event(row,"T_H3_LOAD_OR_TRANSFER"); vae=event(row,"T_VAE_LOAD"); node=event(row,"T_VAE_NODE")
  create=event(row,"T_VIDEO_CREATE");save=event(row,"T_VIDEO_SAVE")
  unload=[x for x in row["path_stage_events"] if x.get("stage")=="T_MODEL_OFFLOAD" and vae["start_ns"]<=x["start_ns"]<=x["end_ns"]<=vae["end_ns"]]
  offload=sum(duration(x) for x in unload)
  raw={
   "T_PRE_GENERATION":(row["generation_start_epoch_ns"]-row["submit_epoch_ns"])/1e9,
   "T_H3_LOAD_OR_TRANSFER":duration(load),
   "T_H3_OFFLOAD":offload,
   "T_VAE_LOAD":duration(vae),
   "T_VAE_DECODE":duration(node)-duration(vae),
   "T_VIDEO_CREATE":duration(create),
   "T_VIDEO_SAVE":duration(save),
   "T_RESULT_READY":(row["ready_epoch_ns"]-save["end_ns"])/1e9,
  }
  exclusive={**raw,"T_PRE_GENERATION":raw["T_PRE_GENERATION"]-raw["T_H3_LOAD_OR_TRANSFER"],"T_VAE_LOAD":raw["T_VAE_LOAD"]-offload}
  exclusive["T_OTHER_PATH"]=row["path_s"]-sum(exclusive.values())
  if min(exclusive.values()) < -0.15: raise RuntimeError(f"negative exclusive segment {row['seed']}: {exclusive}")
  rows.append({"seed":row["seed"],"raw_s":raw,"exclusive_s":exclusive,"offloaded_models":unload,"path_s":row["path_s"],"generation_cuda_s":row["generation_cuda_s"],"total_s":row["total_s"]})
 if len(rows)!=3 or sorted(x["seed"] for x in rows)!=[910100,910102,910103]: raise RuntimeError("three matched formal seeds required")
 keys=list(rows[0]["exclusive_s"])
 summary={key:{"p50_s":pct([r["exclusive_s"][key] for r in rows],.5),"p95_s":pct([r["exclusive_s"][key] for r in rows],.95),"samples_s":[r["exclusive_s"][key] for r in rows]} for key in keys}
 out={"phase":phase,"basis":"V3_RESERVE1 reserve-vram=1.0 GiB pinned disabled","measurement":"CUDA Event core unchanged; UTC epoch stage boundaries; exclusive blocks avoid nesting","rows":rows,"blocks":summary,"qc_pass":True}
 atomic(e/f"path-profile-{phase}.json",out)
 return out
def main():
 p=argparse.ArgumentParser();p.add_argument("--evidence",type=Path,required=True);p.add_argument("--phase",required=True);p.add_argument("--reserve",type=float,required=True);p.add_argument("--pinned",required=True);p.add_argument("--runs",type=int,default=3);p.add_argument("--restore-only",action="store_true");p.add_argument("--launch-id",default=None)
 a=p.parse_args();e=a.evidence
 if a.restore_only:
  print(json.dumps(restore(e)));return
 if a.reserve!=1.0 or a.pinned!="disabled" or a.runs!=3 or a.phase!="V6_PATH_PROFILE": raise RuntimeError("V3 fixed diagnostic contract required")
 proof=e/"profile-instrumentation-proof.json"; report=e/f"path-profile-{a.phase}.json"
 if report.exists() and proof.exists() and json.loads(proof.read_text())["restored"]:
  print("PROFILE_ALREADY_COMPLETE");return
 if (e/"profile-instrumentation-manifest.json").exists() and not proof.exists(): raise RuntimeError("prior profile instrumentation unresolved; inspect process and restore safely")
 instrument(e)
 try:
  cmd=[sys.executable,str(RUNNER),"--evidence",str(e),"--phase",a.phase,"--reserve","1.0","--pinned","disabled","--runs","3"]
  if a.launch_id: cmd.extend(["--launch-id",a.launch_id])
  rc=subprocess.call(cmd)
 finally:
  restoration=restore(e)
 if not restoration["restored"]: raise RuntimeError("profile restoration hash mismatch")
 if rc!=0: raise RuntimeError(f"benchmark runner failed rc={rc}")
 out=analyze(e,a.phase)
 print(json.dumps({"phase":a.phase,"qc_pass":out["qc_pass"],"blocks":out["blocks"]},ensure_ascii=False),flush=True)
if __name__=="__main__": main()
