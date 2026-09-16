#!/usr/bin/env python3
"""V10 V3-fixed generation attribution; reversible source instrumentation."""
import argparse, hashlib, importlib.util, json, os, sys, time
from pathlib import Path

ROOT=Path(r"C:\AI\MiniMax-H3\ComfyUI")
BASE=Path(__file__).with_name("H3-P0-runner.py")
MODEL=ROOT/"comfy/ldm/minimax/model.py"
OPS=ROOT/"comfy/ops.py"
PHASE="V10_GENERATION_PROFILE"
MODEL_HEADER='''
_h3_gen_profile_records=[]
def _h3_gen_profile_flush(seed):
    records=_h3_gen_profile_records[:]
    _h3_gen_profile_records.clear()
    names=["T_GEN_PREPARE","T_GEN_EMBED","T_DIT_01_10","T_DIT_11_20","T_DIT_21_30","T_DIT_31_40","T_DIT_41_50","T_GEN_FINAL","T_GEN_OUTPUT"]
    sums={name:0.0 for name in names}
    totals={"resident_hit":0,"resident_miss":0,"miss_bytes":0}
    for events,stats in records:
        if len(events)!=len(names)+1:
            raise RuntimeError("generation event boundary mismatch")
        for i,name in enumerate(names):
            sums[name]+=events[i].elapsed_time(events[i+1])
        for key in totals:
            totals[key]+=stats[key]
    print("H3_P0_STAGE "+_h3_json.dumps({"stage":"T_GENERATION_PROFILE","seed":seed,"forward_calls":len(records),"segments_ms":sums,"residency":totals}),flush=True)
'''
CHANGES={
 "comfy/ldm/minimax/model.py":[
  ('import math\n', 'import math\nimport json as _h3_json\n'+MODEL_HEADER+'\n'),
  ('    def _forward(self, x, timestep, context, transformer_options={}, minimax_payload=None, denoise_mask=None, audio_denoise_mask=None, **kwargs):\n        video_x, audio_x = x[0], x[1]',
   '    def _forward(self, x, timestep, context, transformer_options={}, minimax_payload=None, denoise_mask=None, audio_denoise_mask=None, **kwargs):\n        _h3_events=[]\n        _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n        comfy.ops._h3_gen_profile_active=True\n        comfy.ops._h3_gen_profile_stats={"resident_hit":0,"resident_miss":0,"miss_bytes":0}\n        video_x, audio_x = x[0], x[1]'),
  ('        # embed\n', '        _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n        # embed\n'),
  ('        # blocks\n', '        _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n        # blocks\n'),
  ('                h = block(h, t_emb, mod_segments, rope_freqs, transformer_options=transformer_options)\n        if prefetch_queue is not None:',
   '                h = block(h, t_emb, mod_segments, rope_freqs, transformer_options=transformer_options)\n            if (i+1)%10==0:\n                _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n        if prefetch_queue is not None:'),
  ('        v, a = self.final_layer(h, t_emb, video_seg, audio_seg, sigma_v, transformer_options.get("sample_sigmas"), (shift_v, shift_a))\n\n        video_out',
   '        v, a = self.final_layer(h, t_emb, video_seg, audio_seg, sigma_v, transformer_options.get("sample_sigmas"), (shift_v, shift_a))\n        _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n\n        video_out'),
  ('        return [-video_out.to(video_x.dtype), -audio_out.to(audio_x.dtype)]',
   '        _h3_event=torch.cuda.Event(enable_timing=True); _h3_event.record(); _h3_events.append(_h3_event)\n        comfy.ops._h3_gen_profile_active=False\n        _h3_gen_profile_records.append((_h3_events,dict(comfy.ops._h3_gen_profile_stats)))\n        return [-video_out.to(video_x.dtype), -audio_out.to(audio_x.dtype)]')
 ],
 "comfy/ops.py":[
  ('import torch\n', 'import torch\n_h3_gen_profile_active=False\n_h3_gen_profile_stats={}\n'),
  ('        resident = comfy_aimdo.model_vbar.vbar_signature_compare(signature, s._v_signature)',
   '        resident = comfy_aimdo.model_vbar.vbar_signature_compare(signature, s._v_signature)\n        if _h3_gen_profile_active:\n            _h3_gen_profile_stats["resident_hit" if resident else "resident_miss"]+=1'),
  ('        dest_size = comfy.memory_management.vram_aligned_size(xfer_source)\n        ensure_offload_stream(s, dest_size if xfer_dest is None else 0, True)',
   '        dest_size = comfy.memory_management.vram_aligned_size(xfer_source)\n        if _h3_gen_profile_active:\n            _h3_gen_profile_stats["miss_bytes"]+=dest_size\n        ensure_offload_stream(s, dest_size if xfer_dest is None else 0, True)')
 ]
}
def sha(b): return hashlib.sha256(b).hexdigest().upper()
def save(p,obj):
    p.parent.mkdir(parents=True,exist_ok=True)
    temp=p.with_name(p.name+"."+str(os.getpid())+".tmp")
    temp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8")
    os.replace(temp,p)
def prepare(e):
    manifest=[]; planned={}
    for rel,changes in CHANGES.items():
        path=ROOT/rel; raw=path.read_bytes()
        backup=e/"generation-profile-backups"/rel
        if backup.exists() and backup.read_bytes()!=raw: raise RuntimeError("backup/source mismatch "+rel)
        if not backup.exists():
            backup.parent.mkdir(parents=True,exist_ok=True); backup.write_bytes(raw)
        s=raw.decode("utf-8").replace("\r\n","\n")
        if "_h3_gen_profile_records" in s: raise RuntimeError("already patched "+rel)
        for old,new in changes:
            count=s.count(old)
            if count!=1: raise RuntimeError("patch boundary "+rel+" count="+str(count)+" "+old[:80])
            s=s.replace(old,new,1)
        newline="\r\n" if b"\r\n" in raw else "\n"
        content=s.replace("\n",newline).encode("utf-8")
        compile(content.decode("utf-8"),rel,"exec")
        planned[path]=content
        manifest.append({"path":str(path),"backup":str(backup),"sha_before":sha(raw),"sha_instrumented":sha(content)})
    save(e/"generation-profile-manifest.json",{"files":manifest,"created":time.time()})
    for path,content in planned.items(): path.write_bytes(content)
    return manifest
def restore(e):
    manifest=json.loads((e/"generation-profile-manifest.json").read_text(encoding="utf-8"))
    rows=[]
    for item in manifest["files"]:
        path=Path(item["path"]); original=Path(item["backup"]).read_bytes()
        path.write_bytes(original)
        rows.append({**item,"sha_after":sha(path.read_bytes()),"restored":sha(original)==item["sha_before"]})
    proof={"files":rows,"restored":all(x["restored"] and x["sha_before"]==x["sha_after"] for x in rows),"time":time.time()}
    save(e/"generation-profile-proof.json",proof)
    return proof
def pct(a,q):
    a=sorted(a);pos=(len(a)-1)*q;i=int(pos)
    return a[i]+(a[min(i+1,len(a)-1)]-a[i])*(pos-i)
def analyze(e):
    rows=[]
    for path in sorted((e/"runs"/PHASE).glob("run-*.json")):
        r=json.loads(path.read_text(encoding="utf-8"))
        if not r.get("task_completed") or len(r["qc"]["frame_ranges"])!=5 or min(r["qc"]["frame_ranges"])<8:
            raise RuntimeError("QC failed "+str(path))
        ev=[x for x in r["path_stage_events"] if x.get("stage")=="T_GENERATION_PROFILE" and x.get("seed")==r["seed"]]
        if len(ev)!=1 or ev[0]["forward_calls"]<1: raise RuntimeError("missing generation profile "+str(path))
        item=ev[0]
        segments={k:v/1000 for k,v in item["segments_ms"].items()}
        residual=r["generation_cuda_s"]-sum(segments.values())
        rows.append({"seed":r["seed"],"segments_s":segments,"generation_residual_s":residual,"forward_calls":item["forward_calls"],"residency":item["residency"],"generation_cuda_s":r["generation_cuda_s"],"path_s":r["path_s"],"total_s":r["total_s"],"qc":r["qc"]})
    if len(rows)!=3 or sorted(x["seed"] for x in rows)!=[910100,910102,910103]: raise RuntimeError("three fixed formal seeds required")
    keys=rows[0]["segments_s"]
    blocks={k:{"p50_s":pct([r["segments_s"][k] for r in rows],.5),"p95_s":pct([r["segments_s"][k] for r in rows],.95),"samples_s":[r["segments_s"][k] for r in rows]} for k in keys}
    blocks["T_GEN_OTHER"]={"p50_s":pct([r["generation_residual_s"] for r in rows],.5),"p95_s":pct([r["generation_residual_s"] for r in rows],.95),"samples_s":[r["generation_residual_s"] for r in rows]}
    report={"phase":PHASE,"basis":"V3_RESERVE1 reserve-vram=1.0 GiB pinned disabled","definition":"CUDA events within H3 forward; residency counts and bytes do not directly measure transfer time","rows":rows,"blocks":blocks,"qc_pass":True}
    save(e/f"generation-profile-{PHASE}.json",report)
    return report
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--evidence",type=Path,required=True); ap.add_argument("--phase",required=True)
    ap.add_argument("--reserve",type=float,required=True); ap.add_argument("--pinned",required=True)
    ap.add_argument("--runs",type=int,required=True); ap.add_argument("--launch-id")
    ap.add_argument("--restore-only",action="store_true")
    a=ap.parse_args(); e=a.evidence
    if a.restore_only: print(json.dumps(restore(e))); return
    if (a.phase,a.reserve,a.pinned,a.runs)!=(PHASE,1.0,"disabled",3): raise RuntimeError("V3 fixed generation profile contract required")
    report=e/f"generation-profile-{PHASE}.json"; proof=e/"generation-profile-proof.json"
    if report.exists() and proof.exists() and json.loads(proof.read_text(encoding="utf-8"))["restored"]:
        print("GENERATION_PROFILE_ALREADY_COMPLETE"); return
    if (e/"generation-profile-manifest.json").exists() and not proof.exists(): raise RuntimeError("unresolved prior instrumentation; inspect process")
    prepare(e)
    try:
        spec=importlib.util.spec_from_file_location("h3_p0_base_runner",BASE)
        base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
        needle=b' b"        _p0_end.synchronize()",'
        extra=b' b"        _p0_end.synchronize()",\n b"        import comfy.ldm.minimax.model as _h3_model",\n b"        _h3_model._h3_gen_profile_flush(extra_args.get(\'seed\'))",'
        source=BASE.read_bytes()
        if source.count(needle)!=1: raise RuntimeError("base timer patch boundary drift")
        base.PATCH=base.PATCH.replace(b"        _p0_end.synchronize()",b"        _p0_end.synchronize()\n        import comfy.ldm.minimax.model as _h3_model\n        _h3_model._h3_gen_profile_flush(extra_args.get('seed'))",1)
        sys.argv=[str(BASE),"--evidence",str(e),"--phase",PHASE,"--reserve","1.0","--pinned","disabled","--runs","3"]
        if a.launch_id: sys.argv.extend(["--launch-id",a.launch_id])
        base.main()
    finally:
        proof=restore(e)
    if not proof["restored"]: raise RuntimeError("generation profile SHA restoration mismatch")
    result=analyze(e)
    print(json.dumps({"phase":PHASE,"qc_pass":result["qc_pass"],"blocks":result["blocks"]}),flush=True)
if __name__=="__main__": main()
