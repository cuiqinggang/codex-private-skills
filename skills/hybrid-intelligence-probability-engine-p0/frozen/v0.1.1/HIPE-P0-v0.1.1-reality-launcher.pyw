import hashlib,json,os,subprocess,sys,time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox,simpledialog
from tkinter.scrolledtext import ScrolledText

VERSION='0.1.1'
RUNS=10
ROOT=Path(__file__).resolve().parent
RUNNER=ROOT/'HIPE-P0-v0.1.1-real-verify.py'
RESULT=ROOT/'HIPE-P0-REAL-RESULT-v0.1.1.json'
OUTER=ROOT/'HIPE-P0-OUTER-EVIDENCE-v0.1.1.json'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest().upper()

def iso_now():
 return datetime.now().astimezone().isoformat()

def run_reality():
 if not RUNNER.exists():
  messagebox.showerror('HIPE P0 v0.1.1','Frozen runner is missing.')
  return
 inherited=os.getenv('OPENROUTER_API_KEY','')
 key=inherited
 if not key:
  key=simpledialog.askstring('HIPE P0 v0.1.1','Enter OPENROUTER_API_KEY for this one run.\nIt will not be written to disk.',show='*',parent=root)
  if not key:return
 if not messagebox.askyesno('Reality Certification','This action will send paid OpenRouter requests using the frozen benchmark.\n\nRun the exact frozen Reality Certification now?',parent=root):
  return
 for p in (RESULT,OUTER):
  try:p.unlink(missing_ok=True)
  except Exception:pass
 env=os.environ.copy()
 env['OPENROUTER_API_KEY']=key
 start_ts=iso_now()
 t0=time.perf_counter_ns()
 try:
  cp=subprocess.run(
   [sys.executable,str(RUNNER),'--mode','live','--runs',str(RUNS),'--out',str(RESULT)],
   cwd=str(ROOT),env=env,capture_output=True,text=True,timeout=1800)
  exit_code=cp.returncode
  stdout=cp.stdout or ''
  stderr=cp.stderr or ''
 except subprocess.TimeoutExpired as e:
  exit_code=124
  stdout=e.stdout if isinstance(e.stdout,str) else ''
  stderr=(e.stderr if isinstance(e.stderr,str) else '')+'\nREALITY_DELTA=OUTER_TIMEOUT\nACTION=STOP\nRETURN_TO_GPT=YES'
 t1=time.perf_counter_ns()
 end_ts=iso_now()
 ms=round((t1-t0)/1_000_000,3)
 result_hash=sha256(RESULT) if RESULT.exists() else 'NOT_CREATED'
 evidence={
  'version':VERSION,
  'runs':RUNS,
  'outer_start_timestamp':start_ts,
  'outer_end_timestamp':end_ts,
  'outer_process_ms':ms,
  'child_exit_code':exit_code,
  'result_sha256':result_hash,
  'credential_source':'INHERITED_ENV' if inherited else 'ONE_RUN_GUI_INPUT',
  'credential_persisted':False
 }
 OUTER.write_text(json.dumps(evidence,indent=2),encoding='utf-8')
 text.delete('1.0',tk.END)
 text.insert(tk.END,stdout)
 if stderr.strip():
  text.insert(tk.END,'\n[stderr]\n'+stderr)
 text.insert(tk.END,f'\nOUTER_START_TIMESTAMP={start_ts}\nOUTER_END_TIMESTAMP={end_ts}\nOUTER_PROCESS_MS={ms}\nRESULT_SHA256={result_hash}\n')
 text.insert(tk.END,'\n【混合智能概率引擎｜冻结方案现实验证｜3｜实】\n')
 key=''
 env.pop('OPENROUTER_API_KEY',None)

root=tk.Tk()
root.title('HIPE P0 v0.1.1 Reality Certification')
root.geometry('900x650')
label=tk.Label(root,text='混合智能概率引擎 HIPE-P0 v0.1.1｜冻结方案现实验证｜实')
label.pack(pady=8)
btn=tk.Button(root,text='运行冻结 Reality Certification',command=run_reality)
btn.pack(pady=8)
text=ScrolledText(root,wrap=tk.WORD,font=('Consolas',10))
text.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
text.insert(tk.END,'This launcher does not modify the frozen benchmark or save the API key.\n')
root.mainloop()
