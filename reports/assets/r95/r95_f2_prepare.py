"""R95 F2: documented current-process affinity adaptation; retain F1 and probe evidence."""
from pathlib import Path
import json,hashlib,shutil,py_compile,time
R=Path(__file__).resolve().parent/"r95-four-core";F=R/"f2"
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
if F.exists():raise RuntimeError("Reconcile F2, do not recreate")
F.mkdir();shutil.copytree(R/"snapshot",F/"snapshot")
worker=F/"snapshot/scripts/archive_stream_worker.py";t=worker.read_text(encoding="utf-8")
old=' if pin:process.cpu_affinity(wanted)'
assert t.count(old)==1
t=t.replace(old,''' if pin:
  import ctypes
  from ctypes import wintypes as win
  kernel=ctypes.WinDLL("kernel32",use_last_error=True)
  kernel.GetCurrentProcess.argtypes=[];kernel.GetCurrentProcess.restype=win.HANDLE
  kernel.SetProcessAffinityMask.argtypes=[win.HANDLE,ctypes.c_size_t];kernel.SetProcessAffinityMask.restype=win.BOOL
  kernel.GetProcessAffinityMask.argtypes=[win.HANDLE,ctypes.POINTER(ctypes.c_size_t),ctypes.POINTER(ctypes.c_size_t)];kernel.GetProcessAffinityMask.restype=win.BOOL
  handle=kernel.GetCurrentProcess();actual_mask=ctypes.c_size_t();system_mask=ctypes.c_size_t()
  if not kernel.GetProcessAffinityMask(handle,ctypes.byref(actual_mask),ctypes.byref(system_mask)):raise ctypes.WinError(ctypes.get_last_error())
  mask=1 << wanted[0]
  assert mask & system_mask.value==mask
  if not kernel.SetProcessAffinityMask(handle,mask):raise ctypes.WinError(ctypes.get_last_error())
  if not kernel.GetProcessAffinityMask(handle,ctypes.byref(actual_mask),ctypes.byref(system_mask)):raise ctypes.WinError(ctypes.get_last_error())
  assert actual_mask.value==mask''')
worker.write_text(t,encoding="utf-8")
shutil.copy2(R/"launch_pi.py",F/"launch_pi.py")
t=(R/"benchmark.py").read_text(encoding="utf-8")
t=t.replace('B=Path(__file__).resolve().parent.parent;', 'B=Path(__file__).resolve().parent.parent.parent;')
t=t.replace('r95-four-core/run','r95-four-core/f2/run').replace('r95-four-core/snapshot','r95-four-core/f2/snapshot').replace('r95-four-core/launch_pi.py','r95-four-core/f2/launch_pi.py')
t=t.replace('"task_id":"R90-ENHANCED-CLI"','"task_id":"PI-R95-FOUR-CORE-20261110-F2"')
(F/"benchmark.py").write_text(t,encoding="utf-8")
for p in [worker,F/"benchmark.py"]:py_compile.compile(str(p),doraise=True)
files=[p for p in (F/"snapshot").rglob("*") if p.is_file() and "__pycache__" not in p.parts]+[F/"launch_pi.py",F/"benchmark.py"]
prior=json.loads((R/"EXPERIMENT-FREEZE.json").read_text(encoding="utf-8"))
freeze={**prior,"task_id":"PI-R95-FOUR-CORE-20261110-F2","created_ns":time.time_ns(),"parent_freeze":str(R/"EXPERIMENT-FREEZE.json"),"parent_sha256":sha(R/"EXPERIMENT-FREEZE.json"),
"failure_preserved":"F1 run/case-01-B failed before business: psutil OpenProcess AccessDenied; F1 A not ranked with F2",
"adaptation":"Microsoft GetCurrentProcess pseudohandle + SetProcessAffinityMask + GetProcessAffinityMask; original sandbox and ACL unchanged",
"probe":{"original_sandbox":"workspace-write","before_mask":15,"actual_masks":[1,2,4,8],"restored_mask":15,"exit_code":0},
"method_ref":"skills/artificial-single-page-extreme-time-engine/SANRENXING_V5.md","method_freeze":"SRX-V5-F001-20261020",
"snapshot_after":{str(p.relative_to(F)):sha(p) for p in files}}
(F/"EXPERIMENT-FREEZE.json").write_text(json.dumps(freeze,indent=2),encoding="utf-8")
print(json.dumps({"ready":True,"root":str(F),"sha256":sha(F/"EXPERIMENT-FREEZE.json")}))
