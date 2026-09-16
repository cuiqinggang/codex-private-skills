#!/usr/bin/env python3
"""Reversible VAE full residency candidate on the single 22 GB GPU."""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path
ROOT=Path(r"C:\AI\MiniMax-H3\ComfyUI")
TARGET=ROOT/"comfy/sd.py"
RUNNER=Path(__file__).with_name("H3-P0-runner.py")
OLD='                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=self.disable_offload)\n                free_memory = self.patcher.get_free_memory(self.device)'
NEW='                memory_used = self.memory_used_decode(samples_in.shape, self.vae_dtype)\n                model_management.load_models_gpu([self.patcher], memory_required=memory_used, force_full_load=(self.disable_offload or self.first_stage_model.__class__.__name__ == "MiniMaxH3VideoVAE"))\n                free_memory = self.patcher.get_free_memory(self.device)'
def digest(b):return hashlib.sha256(b).hexdigest().upper()
def save(p,obj):
 p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_name(p.name+f".{os.getpid()}.tmp")
 tmp.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding="utf-8");os.replace(tmp,p)
def patch(e):
 before=TARGET.read_bytes();backup=e/"v8-sd.py.before"
 if backup.exists() and backup.read_bytes()!=before:raise RuntimeError("V8 backup/source mismatch")
 if not backup.exists():backup.write_bytes(before)
 newline="\r\n" if b"\r\n" in before else "\n"
 s=before.decode("utf-8").replace("\r\n","\n")
 if s.count(OLD)!=1:raise RuntimeError(f"V8 patch boundary count={s.count(OLD)}")
 modified=s.replace(OLD,NEW,1).replace("\n",newline).encode("utf-8")
 compile(modified.decode("utf-8"),str(TARGET),"exec")
 identity={"target":str(TARGET),"backup":str(backup),"sha_before":digest(before),"sha_patched":digest(modified),"time":time.time()}
 save(e/"v8-candidate-manifest.json",identity)
 TARGET.write_bytes(modified)
 return identity
def restore(e):
 identity=json.loads((e/"v8-candidate-manifest.json").read_text(encoding="utf-8"))
 original=Path(identity["backup"]).read_bytes();TARGET.write_bytes(original)
 proof={**identity,"sha_after":digest(TARGET.read_bytes()),"restored":digest(original)==identity["sha_before"],"time_restored":time.time()}
 save(e/"v8-candidate-proof.json",proof)
 return proof
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--evidence",type=Path,required=True);p.add_argument("--phase",required=True);p.add_argument("--reserve",type=float,required=True);p.add_argument("--pinned",required=True);p.add_argument("--runs",type=int,required=True);p.add_argument("--launch-id");p.add_argument("--restore-only",action="store_true")
 a=p.parse_args();e=a.evidence
 if a.restore_only:print(json.dumps(restore(e)));return
 if (a.phase,a.reserve,a.pinned,a.runs)!=("V8_VAE_FULL_SINGLE",1.0,"disabled",3):raise RuntimeError("V3 single-GPU candidate contract required")
 report=e/f"summary-{a.phase}.json";proof=e/"v8-candidate-proof.json"
 if report.exists() and proof.exists() and json.loads(proof.read_text())["restored"]:
  print("V8_ALREADY_COMPLETE");return
 if (e/"v8-candidate-manifest.json").exists() and not proof.exists():raise RuntimeError("prior V8 patch unresolved; inspect process before recovery")
 patch(e)
 try:
  cmd=[sys.executable,str(RUNNER),"--evidence",str(e),"--phase",a.phase,"--reserve","1.0","--pinned","disabled","--runs","3"]
  if a.launch_id:cmd.extend(["--launch-id",a.launch_id])
  rc=subprocess.call(cmd)
 finally:
  restored=restore(e)
 if not restored["restored"]:raise RuntimeError("V8 source restoration mismatch")
 log=e/f"server-{a.phase}.log"
 data=log.read_text(encoding="utf-8",errors="replace") if log.exists() else ""
 save(e/"v8-mechanism-observation.json",{"loaded_completely_events":data.count("loaded completely;"),"loaded_partially_events":data.count("loaded partially;"),"vae_requests":data.count("Requested to load MiniMaxH3VideoVAE"),"runner_rc":rc,"time":time.time()})
 if rc!=0:raise RuntimeError(f"V8 runner rc={rc}")
 print(json.dumps({"phase":a.phase,"runner_rc":rc,"restored":True}),flush=True)
if __name__=="__main__":main()
