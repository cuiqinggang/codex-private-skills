import os,sys,json,time,subprocess,pathlib,uuid,hashlib
R=pathlib.Path("C:/AI/Orca-Codex-Validation-20261014")
AS=R/"CEO_assets/profile/orcad-artifacts/win32-x64"
BIN=AS/"0.1.0+9e2e3cd709d0"
NODE=AS/"runtimes/node-ba4e6d110e8c1592a1ecd390f6b05f3da124b13871a5be62b341a07a853c6c32/node.exe"
CLI=BIN/"out/cli/index.js"
W=R/"live-state-v1-20261019"
W.mkdir(exist_ok=True)
ENV=os.environ.copy()
ENV.update(ORCA_USER_DATA=str(W/"profile"),ORCA_USER_DATA_PATH=str(W/"profile"),ORCA_VERSION="0.1.0+9e2e3cd709d0",ORCA_TELEMETRY_DISABLED="1",DO_NOT_TRACK="1")
CP=W/"checkpoint.json"; LOG=W/"events.jsonl"
def save(d):
 p=CP.with_suffix(".tmp");p.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding="utf8");os.replace(p,CP)
def ev(m,**kw):
 with LOG.open("a",encoding="utf8") as f:f.write(json.dumps(dict(event=m,**kw),ensure_ascii=False)+"\n")
def cli(*args,timeout=25):
 if len(args)>1 and args[0]=='orchestration' and args[1] not in ('send',) and 's' in globals() and globals()['s'].get('coordinator'):
  args=(*args,'--from',globals()['s']['coordinator'])
 p=subprocess.run([str(NODE),str(CLI),*args,"--json"],env=ENV,capture_output=True,text=True,encoding="utf8",errors="replace",timeout=timeout)
 if p.returncode:raise RuntimeError("CLI "+str(args)+": "+p.stderr[-700:]+p.stdout[-700:])
 j=json.loads(p.stdout)
 if j.get("ok") is False:raise RuntimeError(str(j))
 return j.get("result",j)
s=json.loads(CP.read_text(encoding="utf-8-sig")) if CP.exists() else {"stage":"INIT","mutations":0}
server=None
try:
 if s["stage"]=="DONE":print(json.dumps(s));sys.exit(0)
 if s["stage"]=="INIT":
  (W/"profile/profiles/local-default").mkdir(parents=True,exist_ok=True)
  seed={"settings":{"workspaceDir":str(W/"worktrees"),"nestWorkspaces":True,"agentDefaultArgs":{"codex":"--sandbox workspace-write --ask-for-approval on-request"},"agentDefaultEnv":{"codex":{}},"agentYoloDefaultsMigrated":True,"agentStatusHooksEnabled":False,"agentWorkspaceTrustEnabled":False,"experimentalNativeChat":False,"codexManagedAccounts":[],"activeCodexManagedAccountId":None,"activeCodexManagedAccountIdsByRuntime":{"host":None,"wsl":{}},"localWindowsRuntimeDefault":{"kind":"windows-host"},"terminalWindowsShell":"cmd.exe"}}
  (W/"profile/profiles/local-default/orca-data.json").write_text(json.dumps(seed),encoding="utf8")
  (W/"fixture").mkdir(exist_ok=True)
  subprocess.run(["git","init","-b","main"],cwd=W/"fixture",capture_output=True,check=True)
  (W/"fixture"/"README.md").write_text("Live Orca lifecycle identity and control interruption acceptance\n",encoding="utf8")
  subprocess.run(["git","add","."],cwd=W/"fixture",check=True,capture_output=True)
  subprocess.run(["git","-c","user.name=Orca Test","-c","user.email=test@example.invalid","commit","-m","fixture"],cwd=W/"fixture",check=True,capture_output=True)
  s["stage"]="READY";save(s)
 with (W/"server.stdout").open("w") as out,(W/"server.stderr").open("w") as err:
  server=subprocess.Popen([str(NODE),str(BIN/"orcad.js"),"--bind","127.0.0.1","--port","0","--no-pairing","--json"],env=ENV,stdout=out,stderr=err)
 s["server_pid"]=server.pid;save(s)
 for i in range(150):
  if server.poll() is not None:raise RuntimeError("server exited "+str(server.returncode))
  if "orca_server_ready" in (W/"server.stdout").read_text(errors="replace"):break
  time.sleep(.2)
 else:raise RuntimeError("server not ready")
 ev("ORCA_REAL_SERVER_READY",pid=server.pid)
 if s["stage"]=="READY":
  if 'worktree' not in s:
   repo=cli("repo","add","--path",str(W/"fixture"))["repo"]
   wt=cli("worktree","create","--repo","id:"+repo["id"],"--name","accept","--setup","skip","--no-parent")["worktree"]
   s["worktree"]=wt;save(s)
  wt=s['worktree']
  if 'coordinator' not in s:
   s['coordinator']=cli('terminal','create','--worktree',wt['id'],'--title','V1 coordinator')['terminal']['handle'];save(s)
  run=cli("orchestration","run-create","--objective","Complete real local business with Orca identity recovery")["run"]["id"]
  task=cli("orchestration","task-create","--run",run,"--spec","Create deterministic SHA256 manifest from README and verify it","--task-title","V1 live identity recovery")["task"]["id"]
  s.update(run=run,task=task,stage="TASK_CREATED");save(s);ev("TASK_CREATED",run=run,task=task)
 if s["stage"]=="TASK_CREATED":
  wt=s["worktree"];worker=pathlib.Path(wt["path"])
  cmd='python -c "import hashlib,pathlib; p=pathlib.Path(\'README.md\');pathlib.Path(\'OUTPUT.sha256\').write_text(hashlib.sha256(p.read_bytes()).hexdigest())"'
  term=cli("terminal","create","--worktree",wt["id"],"--shell","cmd.exe","--title","V1 identity worker","--command",cmd)["terminal"]["handle"]
  s["terminal"]=term;save(s)
  dispatch=cli("orchestration","dispatch","--task",s["task"],"--run",s["run"],"--to",term,"--return-preamble")["dispatch"]
  s.update(dispatch=dispatch["id"],stage="DISPATCHED",mutations=s["mutations"]+1);save(s);ev("DISPATCHED",dispatch=s["dispatch"],terminal=term)
 if s["stage"]=="DISPATCHED":
  # An actual interrupted official CLI control client: process termination mid read.
  cl=subprocess.Popen([str(NODE),str(CLI),"orchestration","task-list","--run",s["run"],"--json"],env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  time.sleep(.02)
  was_running=cl.poll() is None
  if was_running:cl.kill()
  cl.communicate(timeout=10)
  ev("CONTROL_CLIENT_INTERRUPTED",client_pid=cl.pid,killed_inflight=was_running,exit=cl.returncode)
  s["control_client_interrupted"]=was_running;s["stage"]="CONTROL_UNKNOWN";save(s)
 if s["stage"]=="CONTROL_UNKNOWN":
  tasklist=cli("orchestration","task-list","--run",s["run"])["tasks"]
  disp=cli("orchestration","dispatch-show","--task",s["task"])["dispatch"]
  assert disp["id"]==s["dispatch"] and disp["assignee_handle"]==s["terminal"]
  assert len([x for x in tasklist if x["id"]==s["task"]])==1
  s["stage"]="RECONCILED";save(s);ev("RECONNECTED_IDENTITY_CONFIRMED",task=s["task"],dispatch=s["dispatch"])
 if s["stage"]=="RECONCILED":
  out=pathlib.Path(s["worktree"]["path"])/"OUTPUT.sha256"
  for i in range(100):
   if out.exists():break
   time.sleep(.1)
  else:raise RuntimeError("business output missing")
  orig=pathlib.Path(s["worktree"]["path"])/"README.md"
  assert out.read_text().strip()==hashlib.sha256(orig.read_bytes()).hexdigest()
  s["stage"]="QA_PASS";save(s);ev("INDEPENDENT_BUSINESS_QA_PASS")
 if s["stage"]=="QA_PASS":
  req=str(uuid.uuid4())
  s["receipt_request"]=req;s["stage"]="RECEIPT_UNKNOWN";save(s)
  try:
   reply=cli("orchestration","send","--type","worker_done","--subject","Verified business DONE","--body","Official Orca lifecycle recovered and output SHA validated","--task-id",s["task"],"--dispatch-id",s["dispatch"],"--outcome","succeeded","--from",s["terminal"],"--retry-request",req,timeout=30)
   ev("WORKER_DONE_SENT",reply=str(reply)[:1000])
  except Exception as ex:ev("WORKER_DONE_UNKNOWN",error=str(ex))
 if s["stage"]=="RECEIPT_UNKNOWN":
  tasks=cli("orchestration","task-list","--run",s["run"])["tasks"]
  task=next(x for x in tasks if x["id"]==s["task"])
  disp=cli("orchestration","dispatch-show","--task",s["task"])["dispatch"]
  s.update(task_status=task["status"],dispatch_status=disp["status"])
  assert task["status"]=="completed" and disp["status"]=="completed",str(s)
  s["stage"]="DONE";save(s);ev("FINAL_RECEIPT_RECONCILED")
 print(json.dumps(s,ensure_ascii=False,indent=2))
finally:
 if server is not None and server.poll() is None:
  server.terminate()
  try:server.wait(timeout=8)
  except subprocess.TimeoutExpired:server.kill();server.wait()
 ev("EXIT_ORCA_OWNED_SERVICE_ONLY")
