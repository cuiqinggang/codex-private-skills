#!/usr/bin/env python3
"""V3-fixed VAE stage attribution with reversible source instrumentation."""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(r"C:\AI\MiniMax-H3\ComfyUI")
RUNNER=Path(__file__).with_name("H3-P0-runner.py")
FILES={
 "nodes.py":[
  ('        images = vae.decode(latent)',
   '        torch.cuda.synchronize()\n        _h3_t0=_h3_time.time_ns()\n        images = vae.decode(latent)\n        torch.cuda.synchronize()\n        _h3_t1=_h3_time.time_ns()\n        print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_NODE","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)')
 ],
 "comfy/sd.py":[
  ('                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)\n                free_memory = self.patcher.get_free_memory(self.device)',
   '                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                torch.cuda.synchronize()\n                _h3_t0=_h3_time.time_ns()\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)\n                torch.cuda.synchronize()\n                _h3_t1=_h3_time.time_ns()\n                print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_LOAD_GPU","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)\n                free_memory = self.patcher.get_free_memory(self.device)'),
  ('                    if preallocated:\n                        self.first_stage_model.decode(samples, output_buffer=pixel_samples[x:x+batch_number], **vae_options)',
   '                    if preallocated:\n                        torch.cuda.synchronize()\n                        _h3_call_start=_h3_time.time_ns()\n                        model_management._h3_vae_profile_stats={"resident_hit":0,"resident_miss":0,"miss_bytes":0,"file_direct_bytes":0,"tensor_copy_bytes":0}\n                        model_management._h3_vae_profile_active=True\n                        try:\n                            self.first_stage_model.decode(samples, output_buffer=pixel_samples[x:x+batch_number], **vae_options)\n                        finally:\n                            model_management._h3_vae_profile_active=False\n                        torch.cuda.synchronize()\n                        _h3_call_end=_h3_time.time_ns()\n                        print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_MODEL_CALL","start_ns":_h3_call_start,"end_ns":_h3_call_end,"residency":model_management._h3_vae_profile_stats}),flush=True)')
 ],
 "comfy/ldm/minimax/vae.py":[
  ('            clip_dec = self._adaptive_decode(clip_z)',
   '            torch.cuda.synchronize()\n            _h3_t0=_h3_time.time_ns()\n            clip_dec = self._adaptive_decode(clip_z)\n            torch.cuda.synchronize()\n            _h3_t1=_h3_time.time_ns()\n            print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_ACTUAL_DECODE","start_ns":_h3_t0,"end_ns":_h3_t1}),flush=True)'),
  ('            part = self._finalize_pixels(part)\n            copy_frames = min(part_frames, max(0, dec.shape[2] - write_pos))',
   '            torch.cuda.synchronize()\n            _h3_t0=_h3_time.time_ns()\n            part = self._finalize_pixels(part)\n            copy_frames = min(part_frames, max(0, dec.shape[2] - write_pos))'),
  ('                write_pos += copy_frames\n\n        for i in range(num_chunks):',
   '                write_pos += copy_frames\n            torch.cuda.synchronize()\n            _h3_t1=_h3_time.time_ns()\n            print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_VAE_OUTPUT_TRANSFER","start_ns":_h3_t0,"end_ns":_h3_t1,"frames":copy_frames}),flush=True)\n\n        for i in range(num_chunks):')
 ],
 "comfy/model_management.py":[
  ('from __future__ import annotations',
   'from __future__ import annotations\n_h3_vae_profile_active=False\n_h3_vae_profile_stats={}'),
  ('            if comfy.memory_management.read_tensor_file_slice_into(tensor, dest_view, stream=stream, destination2=dest2_view):\n                continue',
   '            _h3_direct=comfy.memory_management.read_tensor_file_slice_into(tensor, dest_view, stream=stream, destination2=dest2_view)\n            if _h3_vae_profile_active:\n                _h3_bytes=0 if dest_view is None else dest_view.numel()*dest_view.element_size()\n                _h3_bytes+=0 if dest2_view is None else dest2_view.numel()*dest2_view.element_size()\n                _h3_key="file_direct_bytes" if _h3_direct else "tensor_copy_bytes"\n                _h3_vae_profile_stats[_h3_key]+=_h3_bytes\n            if _h3_direct:\n                continue')
 ],
 "comfy/ops.py":[
  ('        resident = comfy_aimdo.model_vbar.vbar_signature_compare(signature, s._v_signature)',
   '        resident = comfy_aimdo.model_vbar.vbar_signature_compare(signature, s._v_signature)\n        if comfy.model_management._h3_vae_profile_active:\n            _h3_key="resident_hit" if resident else "resident_miss"\n            comfy.model_management._h3_vae_profile_stats[_h3_key]+=1'),
  ('        dest_size = comfy.memory_management.vram_aligned_size(xfer_source)\n        ensure_offload_stream(s, dest_size if xfer_dest is None else 0, True)',
   '        dest_size = comfy.memory_management.vram_aligned_size(xfer_source)\n        if comfy.model_management._h3_vae_profile_active:\n            comfy.model_management._h3_vae_profile_stats["miss_bytes"]+=dest_size\n        ensure_offload_stream(s, dest_size if xfer_dest is None else 0, True)')
 ]
}
def digest(data): return hashlib.sha256(data).hexdigest().upper()
def save(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True)
 temp=path.with_name(path.name+f".{os.getpid()}.tmp")
 temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
 os.replace(temp,path)
def inject(s):
 line="import time as _h3_time, json as _h3_json\n"
 future="from __future__ import annotations\n"
 return s.replace(future,future+line,1) if future in s else line+s
def prepare(e):
 manifest=[]; patched={}
 for rel,changes in FILES.items():
  target=ROOT/rel; raw=target.read_bytes();backup=e/"vae-stage-backups"/rel
  if backup.exists() and backup.read_bytes()!=raw: raise RuntimeError(f"backup/source mismatch {rel}")
  if not backup.exists():
   backup.parent.mkdir(parents=True,exist_ok=True);backup.write_bytes(raw)
  s=raw.decode("utf-8").replace("\r\n","\n")
  if "H3_P0_STAGE " in s: raise RuntimeError(f"already patched {rel}")
  for old,new in changes:
   if s.count(old)!=1: raise RuntimeError(f"patch boundary {rel} count={s.count(old)} {old[:60]}")
   s=s.replace(old,new,1)
  newline="\r\n" if b"\r\n" in raw else "\n"
  content=inject(s).replace("\n",newline).encode("utf-8")
  compile(content.decode("utf-8"),rel,"exec")
  patched[target]=content
  manifest.append({"path":str(target),"backup":str(backup),"sha_before":digest(raw),"sha_instrumented":digest(content)})
 save(e/"vae-stage-manifest.json",{"files":manifest,"created":time.time()})
 for target,content in patched.items(): target.write_bytes(content)
 return manifest
def restore(e):
 manifest=json.loads((e/"vae-stage-manifest.json").read_text(encoding="utf-8"))
 rows=[]
 for item in manifest["files"]:
  path=Path(item["path"]);content=Path(item["backup"]).read_bytes();path.write_bytes(content)
  rows.append({**item,"sha_after":digest(path.read_bytes()),"restored":digest(content)==item["sha_before"]})
 proof={"files":rows,"restored":all(x["restored"] and x["sha_before"]==x["sha_after"] for x in rows),"time":time.time()}
 save(e/"vae-stage-proof.json",proof)
 return proof
def pct(a,q):
 a=sorted(a);x=(len(a)-1)*q;i=int(x)
 return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(x-i)
def one(row,name):
 events=[x for x in row["path_stage_events"] if x.get("stage")==name]
 if len(events)!=1: raise RuntimeError(f"{row['seed']} {name}: {len(events)}")
 return events[0]
def dur(x): return (x["end_ns"]-x["start_ns"])/1e9
def analyze(e,phase):
 rows=[]
 for path in sorted((e/"runs"/phase).glob("run-*.json")):
  r=json.loads(path.read_text(encoding="utf-8"))
  if r.get("task_completed") is not True or len(r.get("qc",{}).get("frame_ranges",[]))!=5 or min(r["qc"]["frame_ranges"])<8: raise RuntimeError(f"QC failed {path}")
  node=one(r,"T_VAE_NODE");load=one(r,"T_VAE_LOAD_GPU");call=one(r,"T_VAE_MODEL_CALL");actual=one(r,"T_VAE_ACTUAL_DECODE")
  output=[x for x in r["path_stage_events"] if x.get("stage")=="T_VAE_OUTPUT_TRANSFER"]
  if not output: raise RuntimeError(f"output transfer missing {r['seed']}")
  blocks={
   "T_VAE_PREPARE":(load["start_ns"]-node["start_ns"])/1e9,
   "T_VAE_LOAD_GPU":dur(load),
   "T_VAE_ACTUAL_DECODE":dur(actual),
   "T_VAE_OUTPUT_TRANSFER":sum(dur(x) for x in output),
  }
  blocks["T_VAE_OTHER"]=dur(node)-sum(blocks.values())
  if min(blocks.values()) < -0.15: raise RuntimeError(f"negative VAE block {r['seed']}: {blocks}")
  rows.append({"seed":r["seed"],"blocks_s":blocks,"node_s":dur(node),"model_call_s":dur(call),"dynamic_residency":call["residency"],"generation_cuda_s":r["generation_cuda_s"],"path_s":r["path_s"],"total_s":r["total_s"],"qc":r["qc"]})
 if len(rows)!=3 or sorted(x["seed"] for x in rows)!=[910100,910102,910103]: raise RuntimeError("3 matched formal seeds required")
 keys=rows[0]["blocks_s"].keys()
 summary={k:{"p50_s":pct([x["blocks_s"][k] for x in rows],.5),"p95_s":pct([x["blocks_s"][k] for x in rows],.95),"samples_s":[x["blocks_s"][k] for x in rows]} for k in keys}
 out={"phase":phase,"basis":"V3_RESERVE1 reserve-vram=1.0 GiB pinned disabled","definition":"ACTUAL_DECODE is decoder call and may include on-demand weight transfer; residency counters distinguish it from pure math","rows":rows,"blocks":summary,"qc_pass":True}
 save(e/f"vae-stage-{phase}.json",out)
 return out
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--evidence",type=Path,required=True);p.add_argument("--phase",required=True);p.add_argument("--reserve",type=float,required=True);p.add_argument("--pinned",required=True);p.add_argument("--runs",type=int,required=True);p.add_argument("--launch-id");p.add_argument("--restore-only",action="store_true")
 a=p.parse_args();e=a.evidence
 if a.restore_only: print(json.dumps(restore(e)));return
 if (a.phase,a.reserve,a.pinned,a.runs)!=("V7_VAE_STAGE",1.0,"disabled",3): raise RuntimeError("V3 fixed VAE profile contract required")
 report=e/f"vae-stage-{a.phase}.json";proof=e/"vae-stage-proof.json"
 if report.exists() and proof.exists() and json.loads(proof.read_text())["restored"]:
  print("VAE_STAGE_ALREADY_COMPLETE");return
 if (e/"vae-stage-manifest.json").exists() and not proof.exists(): raise RuntimeError("unresolved prior VAE instrumentation; inspect process before recovery")
 prepare(e)
 try:
  cmd=[sys.executable,str(RUNNER),"--evidence",str(e),"--phase",a.phase,"--reserve","1.0","--pinned","disabled","--runs","3"]
  if a.launch_id:cmd.extend(["--launch-id",a.launch_id])
  rc=subprocess.call(cmd)
 finally:
  restored=restore(e)
 if not restored["restored"]: raise RuntimeError("VAE instrumentation restoration mismatch")
 if rc!=0:raise RuntimeError(f"runner rc={rc}")
 result=analyze(e,a.phase)
 print(json.dumps({"phase":a.phase,"qc_pass":result["qc_pass"],"blocks":result["blocks"]},ensure_ascii=False),flush=True)
if __name__=="__main__":main()
