import hashlib,json,os,subprocess,sys,time
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import messagebox,simpledialog
from tkinter.scrolledtext import ScrolledText

VERSION='0.3.1';RUNS=30;WARMUPS=3
ROOT=Path(__file__).resolve().parent
RUNNER=ROOT/'HIPE-v0.3.1-real-verify.py'
RESULT=ROOT/'HIPE-v0.3.1-REAL-RESULT.json'
OUTER=ROOT/'HIPE-v0.3.1-OUTER-EVIDENCE.json'

def sha256(path):
 h=hashlib.sha256()
 with open(path,'rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
 return h.hexdigest().upper()

def iso_now():return datetime.now().astimezone().isoformat()

def run_reality():
 if not RUNNER.exists():messagebox.showerror('混合智能概率引擎 v0.3.1','冻结现实验证器不存在。');return
 inherited=os.getenv('OPENROUTER_API_KEY','').strip();key=inherited
 if not key:
  key=simpledialog.askstring('混合智能概率引擎 v0.3.1','请输入本次现实认证使用的 OPENROUTER_API_KEY。\n密钥只传给本次子进程，不写入磁盘。',show='*',parent=root)
  if not key:return
 if not messagebox.askyesno('确认现实认证','将执行冻结的真实 OpenRouter 请求，可能产生费用。\n\n固定：3 组预热 + 30 组 Full-GPT / Hybrid 交替 A/B。\n确认开始？',parent=root):return
 for p in (RESULT,OUTER):
  try:p.unlink(missing_ok=True)
  except Exception:pass
 env=os.environ.copy();env['OPENROUTER_API_KEY']=key
 start=iso_now();t0=time.perf_counter_ns()
 try:
  cp=subprocess.run([sys.executable,str(RUNNER),'--mode','live','--warmups',str(WARMUPS),'--runs',str(RUNS),'--out',str(RESULT),'--output-dir',str(ROOT/'reality-output-v0.3.1')],cwd=str(ROOT),env=env,capture_output=True,text=True,timeout=7200)
  code=cp.returncode;stdout=cp.stdout or '';stderr=cp.stderr or ''
 except subprocess.TimeoutExpired as e:
  code=124;stdout=e.stdout if isinstance(e.stdout,str) else '';stderr=(e.stderr if isinstance(e.stderr,str) else '')+'\n现实差异=外层超时'
 end=iso_now();ms=round((time.perf_counter_ns()-t0)/1e6,3);rh=sha256(RESULT) if RESULT.exists() else 'NOT_CREATED'
 evidence={'version':VERSION,'warmups':WARMUPS,'runs':RUNS,'outer_start_timestamp':start,'outer_end_timestamp':end,'outer_process_ms':ms,'child_exit_code':code,'result_sha256':rh,'credential_source':'INHERITED_ENV' if inherited else 'ONE_RUN_GUI_INPUT','credential_persisted':False}
 OUTER.write_text(json.dumps(evidence,ensure_ascii=False,indent=2),encoding='utf-8')
 text.delete('1.0',tk.END);text.insert(tk.END,stdout)
 if stderr.strip():text.insert(tk.END,'\n[错误输出]\n'+stderr)
 text.insert(tk.END,f'\n外层开始={start}\n外层结束={end}\n外层总时间毫秒={ms}\n结果SHA256={rh}\n')
 text.insert(tk.END,'\n【混合智能概率引擎｜完整任务现实认证｜3｜实】\n')
 key='';env.pop('OPENROUTER_API_KEY',None)

root=tk.Tk();root.title('混合智能概率引擎 v0.3.1｜完整任务现实认证');root.geometry('940x680')
tk.Label(root,text='混合智能概率引擎 v0.3.1｜完整任务现实认证｜实').pack(pady=8)
tk.Button(root,text='运行冻结现实认证',command=run_reality).pack(pady=8)
text=ScrolledText(root,wrap=tk.WORD,font=('Consolas',10));text.pack(fill=tk.BOTH,expand=True,padx=10,pady=10)
text.insert(tk.END,'本启动器不会修改冻结 benchmark，不保存 API Key。\n现实认证包含同任务、同验证器、交替顺序的 Full-GPT / Hybrid A/B。\n')
root.mainloop()
