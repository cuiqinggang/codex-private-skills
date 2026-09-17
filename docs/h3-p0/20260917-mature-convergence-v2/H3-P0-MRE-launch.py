#!/usr/bin/env python3
"""One-shot process guard for the frozen H3-P0 runner; no benchmark logic."""
import hashlib, json, os, socket, subprocess, sys, time, uuid
from pathlib import Path
import psutil

REPO = Path(r"C:\Users\A\Documents\Codex\codex-private-skills")
RUNNER = REPO / "docs/h3-p0/20260916-first-principles-v1/H3-P0-runner.py"
PYTHON = Path(r"C:\AI\MiniMax-H3\.venv\Scripts\python.exe")
COMFY = Path(r"C:\AI\MiniMax-H3\ComfyUI")
E = Path(r"C:\AI\H3-P0-Acceptance\mature-convergence-v2\20260917-mre-01")
PHASE = "MRE_REAL_STATE_01"
RUNNER_SHA = "EA3B3FB4FA70DFE05448B138E90FFDC6A22121033F936D764A8CD03A82B574E4"
CANONICAL = Path(r"C:\AI\MiniMax-H3\projects\H3-05-xuejing-dukou\06-WORKFLOWS\STATIC-PROBE\k3-fl2va-5f-20step-api.json")
CANONICAL_SHA = "89B6A40B13485A6633191F1350DB472556359CDB6407E5272C9ED109698FD0F5"
SAMPLERS = COMFY / "comfy/samplers.py"
MODELS = [
 COMFY / "models/diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors",
 COMFY / "models/text_encoders/qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors",
 COMFY / "models/vae/minimax_h3_video_vae_fp16.safetensors",
]

def sha(path):
 return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def save(name, value):
 target = E / name
 temp = E / (name + f".{os.getpid()}.{uuid.uuid4().hex}.tmp")
 temp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
 for attempt in range(20):
  try:
   os.replace(temp, target)
   return
  except PermissionError:
   if attempt == 19: raise
   time.sleep(.1)

def listening(port):
 with socket.socket() as sock:
  sock.settimeout(.25)
  return sock.connect_ex(("127.0.0.1", port)) == 0

def other_h3():
 for p in psutil.process_iter(["pid", "cmdline"]):
  try:
   cmd = " ".join(p.info["cmdline"] or []).lower()
   if p.pid != os.getpid() and ("h3-p0-runner.py" in cmd or ("minimax-h3" in cmd and "main.py" in cmd)):
    return True
  except (psutil.NoSuchProcess, psutil.AccessDenied):
   continue
 return False

def main():
 if E.exists(): raise RuntimeError("Evidence exists: inspect PID, 8194, results and restore proof; never blindly relaunch")
 if listening(8194) or listening(8195) or other_h3(): raise RuntimeError("Existing H3 instance or port listener")
 if sha(RUNNER) != RUNNER_SHA or sha(CANONICAL) != CANONICAL_SHA: raise RuntimeError("Frozen runner/workflow drift")
 samplers_before = sha(SAMPLERS)
 gpu = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.free,driver_version",
                       "--format=csv,noheader"], check=True, capture_output=True, text=True).stdout.strip()
 apps = subprocess.run(["nvidia-smi", "--query-compute-apps=pid,process_name,used_gpu_memory",
                        "--format=csv,noheader"], check=True, capture_output=True, text=True).stdout.strip()
 if any("python" in line.lower() for line in apps.splitlines()):
  raise RuntimeError("Another Python CUDA process is present")
 E.mkdir(parents=True)
 owner = psutil.Process()
 identity = {"launch_id":str(uuid.uuid4()), "controller_pid":owner.pid,
             "controller_start_time":owner.create_time(), "runner_pid":None,
             "runner_start_time":None, "phase":PHASE}
 lock = E / "controller.lock"
 with os.fdopen(os.open(lock, os.O_WRONLY|os.O_CREAT|os.O_EXCL, 0o600), "w", encoding="utf-8") as f:
  json.dump(identity, f)
 command = [str(PYTHON), str(RUNNER), "--evidence", str(E), "--phase", PHASE,
            "--reserve", "1.0", "--pinned", "disabled", "--runs", "3", "--cold"]
 save("preflight.json", {"time_epoch_s":time.time(), "8194_listener":False, "8195_listener":False,
      "no_other_h3_comfyui":True, "no_other_cuda_compute_workload":True,
      "cuda_workload_assessment":"Prelaunch process check: UI C+G processes only; no Python CUDA process",
      "gpu_snapshot":gpu, "nvidia_compute_apps_snapshot":apps, "python":sys.version,
      "torch":"2.9.1+cu130", "cuda":"13.0", "comfy_kitchen":"0.2.31", "comfy_aimdo":"0.4.15",
      "comfyui_commit":subprocess.run(["git","-C",str(COMFY),"rev-parse","HEAD"],
         check=True,capture_output=True,text=True).stdout.strip(),
      "runner_sha256":RUNNER_SHA, "canonical_workflow_sha256":CANONICAL_SHA,
      "samplers_sha256":samplers_before,
      "models":[{"path":str(p),"bytes":p.stat().st_size} for p in MODELS]})
 save("state.json", {"state":"STARTING", **identity})
 out, err = E/"runner.stdout.log", E/"runner.stderr.log"
 save("launch-intent.json", {"command":command,"stdout":str(out),"stderr":str(err),
      "launch_time_epoch_s":time.time(),**identity})
 proc = None
 try:
  with out.open("w",encoding="utf-8") as stdout, err.open("w",encoding="utf-8") as stderr:
   proc = subprocess.Popen(command,cwd=REPO,stdout=stdout,stderr=stderr,
                           creationflags=getattr(subprocess,"CREATE_NO_WINDOW",0))
   identity["runner_pid"] = proc.pid
   identity["runner_start_time"] = psutil.Process(proc.pid).create_time()
   save("pid.json",identity)
   save("controller.lock",identity)
   save("state.json",{"state":"RUNNING",**identity})
   while proc.poll() is None:
    save("heartbeat.json",{"time_epoch_s":time.time(),**identity})
    time.sleep(5)
  save("heartbeat.json",{"time_epoch_s":time.time(),"runner_exit_code":proc.returncode,**identity})
  summary = E/f"summary-{PHASE}.json"
  proof = E/"instrumentation-restore-proof.json"
  complete = proc.returncode == 0 and summary.is_file() and proof.is_file()
  if complete:
   s = json.loads(summary.read_text(encoding="utf-8"))
   p = json.loads(proof.read_text(encoding="utf-8"))
   complete = s.get("valid_warm_runs") == 3 and p.get("restored") is True and sha(SAMPLERS) == samplers_before
  save("state.json",{"state":"COMPLETE" if complete else "INCOMPLETE",
       "runner_exit_code":proc.returncode,**identity})
  if not complete: raise RuntimeError("Runner incomplete; lock retained for recovery")
  lock.unlink()
 except Exception:
  save("state.json",{"state":"RECOVERY_CHECK_REQUIRED",**identity})
  raise

if __name__ == "__main__":
 main()
