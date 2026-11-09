import argparse,os,sys,pathlib,json,subprocess,yaml
R=pathlib.Path(__file__).resolve().parent
OLD=pathlib.Path(r"C:\Users\A\Documents\DSH-Workspace\pi-comparison-20261028")
p=argparse.ArgumentParser(description="Pi mature commercial delivery entry")
p.add_argument("--mode",choices=["core","docs","browser","code","recipes"],default="core")
p.add_argument("--cwd",default=str(R/"workspace"))
p.add_argument("--session-id")
p.add_argument("--network-discovery",action="store_true")
p.add_argument("--fast-official-brief",action="store_true")
p.add_argument("--fast-orders-input")
p.add_argument("--fast-archive-input")
p.add_argument("--fast-office-file",action="append")
p.add_argument("--fast-orders-out",default="output")
p.add_argument("--fast-orders-title",default="订单经营日报")
p.add_argument("--json",action="store_true")
p.add_argument("--print",dest="one_shot",action="store_true")
p.add_argument("task",nargs="*")
a=p.parse_args();cwd=pathlib.Path(a.cwd).resolve(strict=True)
if not cwd.is_dir():p.error("--cwd must be a directory")
if sum(bool(x) for x in [a.fast_official_brief,a.fast_orders_input,a.fast_archive_input,a.fast_office_file])>1:p.error("Choose exactly one explicit recipe")
if a.fast_orders_input and a.fast_orders_title!="订单经营日报":p.error("Custom title is outside the accepted fixed order contract")
if a.fast_archive_input or a.fast_office_file:
 if a.task or a.mode!="core" or a.json or a.one_shot:p.error("Explicit native recipe only; do not combine with Pi prompt options")
 native_kind="archive" if a.fast_archive_input else "ingest"
 native_args=["--input",a.fast_archive_input] if a.fast_archive_input else ["--files-json",json.dumps(a.fast_office_file)]
 runner=r"C:\AI\DeepSeek-Harness-Trial\dsh-0.2.1-rc.2-isolated\node_modules\@deepseek-ai\dsh-sandbox-windows-acl\lib\runner.js"
 temp=r"C:\Users\A\Documents\DSH-Workspace\pi-comparison-20261028\temp"
 sys.exit(subprocess.call([r"C:\Program Files\nodejs\node.exe",runner,"--workspace",str(cwd),"--temp",temp,"--mode","workspace-write","--",sys.executable,str(R/"artifact_recipe.py"),native_kind,"--cwd",str(cwd),*native_args],cwd=cwd,stdin=subprocess.DEVNULL))
if a.fast_official_brief:
 if a.fast_orders_input or a.task or a.mode!="core" or a.json or a.one_shot:p.error("Official brief is an explicit fixed business recipe")
 sys.exit(subprocess.call([sys.executable,str(R/"accept_official_brief.py"),"--cwd",str(cwd)],cwd=cwd))
if a.fast_orders_input:
 if a.task or a.mode!="core" or a.json or a.one_shot:p.error("Fast orders is an explicit structured task, not a Pi prompt or browser operation")
 sys.exit(subprocess.call([sys.executable,str(R/"fast_order_route.py"),"--cwd",str(cwd),"--input",a.fast_orders_input,"--out",a.fast_orders_out,"--title",a.fast_orders_title],cwd=cwd))
runtime=R/("runtime-"+("core" if a.mode in ("code","recipes") else a.mode))
key=yaml.safe_load(pathlib.Path(r"C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent\.credentials.yaml").read_text(encoding="utf-8"))["refs"]["DEEPSEEK_API_KEY"]
env={**os.environ,"DEEPSEEK_API_KEY":key,"PI_CODING_AGENT_DIR":str(runtime),"PI_OFFLINE":"1","PYTHONIOENCODING":"utf-8"}
cmd=[r"C:\Program Files\nodejs\node.exe",r"C:\Users\A\AppData\Roaming\npm\node_modules\@earendil-works\pi-coding-agent\dist\bundle\cli.js","--offline","--extension",str(OLD/"windows_sandbox.mjs"),"--extension",str(R/"capabilities.mjs"),"--provider","deepseek","--model","deepseek-flash","--thinking","high","--no-skills","--no-context-files","--no-prompt-templates","--no-themes","--no-approve","--tools","read,powershell,edit,write,codemode,tool_search,capability_search,mature_web_search,mature_web_fetch,mature_order_report,mature_official_brief,mature_archive,mature_office_ingest","--append-system-prompt",str(R/"INSTRUCTIONS.md"),"--session-dir",str(cwd/".pi-sessions")]
if a.mode!="recipes":
 for i,value in enumerate(cmd):
  if value==str(R/"capabilities.mjs"):cmd[i]=str(R/"coding-baseline"/"capabilities.mjs")
  elif value==str(R/"INSTRUCTIONS.md"):cmd[i]=str(R/"coding-baseline"/"INSTRUCTIONS.md")
 cmd[cmd.index("--tools")+1]='read,powershell,edit,write,codemode,tool_search,capability_search,mature_web_search,mature_web_fetch,mature_order_report'
H=pathlib.Path(r"C:\AI\DeepSeek-Harness-Trial\dsh-home-mature-agent\skills")
for name in ["ai-organization-v4-2","reuse-experience-brain","local-capability-index","dsh-mature-capabilities","mature-systematic-debugging","mature-verification-before-completion","mature-agent-memory","reasonix-continuity"]:
 f=H/name/"SKILL.md"
 if f.is_file():cmd+=["--skill",str(f)]
network_skill=R/"skills"/"network-mature-route"/"SKILL.md"
if a.network_discovery and network_skill.is_file():cmd+=["--skill",str(network_skill)]
if a.mode in ("core","code","recipes"):cmd+=["--no-mcp"]
if a.mode=="browser":
 for f in [H/"dsh-shared-browser-and-aiorg-v3"/"SKILL.md",pathlib.Path(r"C:\AI\Playwright-Native-AI-Browser\skills\playwright-native-ai-browser\SKILL.md")]:
  if f.is_file():cmd+=["--skill",str(f)]
if a.session_id:cmd+=["--session-id",a.session_id]
if a.json:cmd+=["--mode","json"]
if a.one_shot:cmd+=["--print"]
if a.task:cmd+=[" ".join(a.task)]
sys.exit(subprocess.call(cmd,cwd=cwd,env=env,stdin=subprocess.DEVNULL if a.one_shot and a.task else None))
