"""Finite acceptance fixtures/observer. Never implements the agent's repair."""
from pathlib import Path
import hashlib,json,sys,subprocess
from PIL import Image,ImageDraw
R=Path(__file__).resolve().parent
H=Path('C:/Users/A/.hermes')
PYTHON=H/'hermes-agent/venv/Scripts/python.exe'
CS=H/'skills/hermes-long-task-continuity/scripts'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,s): p.write_text(s,encoding='utf-8')
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def jd(p,v): put(p,json.dumps(v,ensure_ascii=False,indent=2))
REQUIREMENTS='''Implement total_paid_cents(rows) in invoice.py. Return an exact Python int.
Include only rows whose status is exactly "paid". Ignore all other statuses.
For a paid row, cents must be int but not bool; otherwise raise ValueError.
Missing status means ignored. Missing cents on a paid row raises ValueError.
Allow negative integers and arbitrary-size integers. Empty input returns 0.
Do not change this contract or the tests. Do not install any dependencies.
'''
TESTS='''import unittest
from invoice import total_paid_cents
class InvoiceTests(unittest.TestCase):
 def test_empty(self): self.assertEqual(total_paid_cents([]),0)
 def test_statuses(self): self.assertEqual(total_paid_cents([{'status':'paid','cents':120},{'status':'pending','cents':50},{'status':'cancelled','cents':70}]),120)
 def test_negative(self): self.assertEqual(total_paid_cents([{'status':'paid','cents':-7},{'status':'paid','cents':20}]),13)
 def test_large(self): self.assertEqual(total_paid_cents([{'status':'paid','cents':10**30},{'status':'paid','cents':1}]),10**30+1)
 def test_missing_status(self): self.assertEqual(total_paid_cents([{}, {'cents':12}]),0)
 def test_missing_cents(self):
  with self.assertRaises(ValueError): total_paid_cents([{'status':'paid'}])
 def test_invalid_paid(self):
  for v in [True,False,1.2,'20',None]:
   with self.subTest(v=v),self.assertRaises(ValueError): total_paid_cents([{'status':'paid','cents':v}])
 def test_ignore_invalid_unpaid(self): self.assertEqual(total_paid_cents([{'status':'pending','cents':None}]),0)
if __name__=='__main__': unittest.main()
'''
def setup():
 frozen={'task':'HERMES-ECO-20261014','suite':'F001','cases':[]}
 for n in range(1,6):
  d=R/f'R{n:02d}'; d.mkdir(exist_ok=False); tid=f'hermes-eco-20261014-r{n:02d}'
  put(d/'requirements.md',REQUIREMENTS);put(d/'test_invoice.py',TESTS)
  put(d/'invoice.py','def total_paid_cents(rows):\n    return sum(row["cents"] for row in rows)\n')
  im=Image.new('RGB',(600,220),'white');draw=ImageDraw.Draw(im)
  draw.rectangle((35,70,150,160),fill='blue');draw.ellipse((250,60,360,170),fill='red');draw.polygon([(490,55),(430,170),(550,170)],fill='green');im.save(d/'visual.png')
  run=f'@echo off\r\n"{PYTHON}" -m unittest discover -s "%~dp0" -p "test_invoice.py" -v\r\nexit /b %errorlevel%\r\n'; put(d/'run-tests.cmd',run)
  common=f' --root "{d/"continuity"}"'
  cmds=[f'"{PYTHON}" "{CS/"new-task.py"}" {tid} 2 "Hermes acceptance"'+common,
        f'"{PYTHON}" "{CS/"save-checkpoint.py"}" {tid} 1 DONE "Code review and vision completed" --required-file "{d/"invoice.py"}" --required-file "{d/"gate.json"}" --required-file "{d/"vision.json"}"'+common,
        f'"{PYTHON}" "{CS/"write-handoff.py"}" {tid}'+common]
  put(d/'save-handoff.cmd','@echo off\r\n'+'\r\nif errorlevel 1 exit /b 1\r\n'.join(cmds)+'\r\nexit /b %errorlevel%\r\n')
  cmds=[f'"{PYTHON}" "{CS/"resume-task.py"}" {tid}'+common,
        f'call "{d/"run-tests.cmd"}"',
        f'"{PYTHON}" "{CS/"save-checkpoint.py"}" {tid} 2 DONE "New session resumed and independently retested" --required-file "{d/"invoice.py"}"'+common,
        f'"{PYTHON}" "{CS/"close-task.py"}" {tid} PASS "Acceptance case closed"'+common]
  put(d/'resume-close.cmd','@echo off\r\n'+'\r\nif errorlevel 1 exit /b 1\r\n'.join(cmds)+'\r\nexit /b %errorlevel%\r\n')
  p=f'''这是一次获准的隔离真实验收，不是要你写方案。唯一可写工作区：{d}。只读允许本工作区、下述已有skills和Python官方文档。禁止读取凭据、私人会话、其他项目；禁止安装组件、变更配置、代理、账户、定时任务或打开浏览器。Windows环境，不用bash heredoc。
请依次实际完成：
1. 用skill_view加载hermes-repair-loop-adapter；用todo_list记录本任务步骤。读取requirements.md、invoice.py和test_invoice.py。实际使用terminal执行 cmd /c "{d/'run-tests.cmd'}" 确认既有缺陷；这是预期注入失败，保留根因。
2. 只修复invoice.py满足契约，不能改测试、要求、cmd或图片。再次运行同一测试。写repair.json，字段root_cause、before_exit_code（非零）、after_exit_code（零），如实际失败不得写成功。
3. 必须实际用web_extract或web_search读取 https://docs.python.org/3/library/functions.html#sum 并写research.json，包含source_url和一条来自该来源的发现。不得以常识假装已检索。
4. 必须实际用vision_analyze分析 {d/'visual.png'}，不得用代码读取像素或从文件生成脚本找答案。写vision.json，格式{{"objects":[{{"color":"英文小写颜色","shape":"rectangle或circle或triangle"}}]}}，依图片从左到右排列。
5. 真正用原生delegate_task批量派发两个独立只读子任务：A审查invoice.py是否满足requirements.md；B检查test_invoice.py的边界覆盖并复核修复。告知子任务精确路径和只读边界，要求读真实文件并返回审查结论，不得仅扮演角色。委派后按原生机制接收两个真实完成回执，不轮询其他任务。将两份审查写gate.json，字段verdict(PASS/FAIL)、reviews(两项)。存在问题时按Repair最小修复并复验；超过三次同类失败停止报告。
6. 全部通过后用terminal实际执行 cmd /c "{d/'save-handoff.cmd'}"。此cmd只复用已部署连续性脚本创建两步任务、保存已完成第1步和handoff。禁止手造continuity状态；此时不执行resume-close.cmd。
最终回复HANDOFF_READY；任何未完成项明确BLOCKED及原因，禁止伪造完成。
'''
  put(d/'prompt-1.txt',p)
  put(d/'prompt-2.txt',f'''这是接收旧任务交接的新会话。唯一写入范围{d}。原任务ID={tid}，交接包位于{d/'continuity/tasks'/tid/'handoff.json'}。禁止读取私人会话、凭据或其他任务，禁止改invoice.py/测试/图片/cmd。实际读取该交接包，确认completed_steps=[1]、next_step=2；然后用terminal执行 cmd /c "{d/'resume-close.cmd'}"。该入口复用原有resume、unittest、checkpoint第2步和close，不能重复第1步。真实成功才回复RESUME_CLOSE_PASS；失败报告原错误，不手写任务状态。''')
  frozen['cases'].append({'round':n,'task_id':tid,'files':{f.name:sha(f) for f in d.iterdir() if f.is_file()},'immutable':['requirements.md','test_invoice.py','visual.png','run-tests.cmd','save-handoff.cmd','resume-close.cmd']})
 jd(R/'FIXTURE-MANIFEST.json',frozen)
 print(json.dumps({'prepared':5,'manifest_sha256':sha(R/'FIXTURE-MANIFEST.json')}))
def events(d,phase):
 out=[]
 for line in (d/f'events-{phase}.sse').read_text(encoding='utf-8-sig').splitlines():
  if line.startswith('data: '):
   try: out.append(json.loads(line[6:]))
   except ValueError: pass
 return out

def grade(d,phase):
 n=int(d.name[1:]); manifest=read(R/'FIXTURE-MANIFEST.json')['cases'][n-1]; checks={}
 checks['immutable_inputs']=all(sha(d/f)==manifest['files'][f] for f in manifest['immutable'])
 test=subprocess.run([str(PYTHON),'-m','unittest','discover','-s',str(d),'-p','test_invoice.py','-v'],capture_output=True,text=True,timeout=45)
 put(d/f'independent-tests-{phase}.txt',test.stdout+test.stderr);checks['independent_tests']=test.returncode==0
 e=events(d,phase);completed=[v for v in e if v.get('event')=='tool.completed'];tools={v.get('tool') for v in completed}
 if phase==1:
  checks['actual_tool_calls']={'skill_view','terminal','vision_analyze','delegate_task','todo_list'}<=tools and bool({'web_extract','web_search'}&tools)
  children=[v for v in e if v.get('event')=='subagent.complete'];ids={v.get('child_session_id') for v in children if v.get('child_session_id')}
  checks['real_independent_children']=len(ids)>=2 and all(v.get('status') not in ('failed','error','cancelled','stalled') for v in children)
  checks['no_unexpected_tool_errors']=not any(v.get('error') and v.get('tool')!='terminal' for v in completed)
  checks['vision_result']=read(d/'vision.json')['objects']==[{'color':'blue','shape':'rectangle'},{'color':'red','shape':'circle'},{'color':'green','shape':'triangle'}]
  repair=read(d/'repair.json');checks['repair_receipt']=repair['before_exit_code']!=0 and repair['after_exit_code']==0 and bool(repair['root_cause'])
  gate=read(d/'gate.json');checks['gate_review']=gate['verdict']=='PASS' and len(gate['reviews'])>=2
  research=read(d/'research.json');checks['research_source']=str(research['source_url']).startswith('https://docs.python.org/')
  hand=read(d/'continuity/tasks'/manifest['task_id']/'handoff.json');checks['handoff']=hand['completed_steps']==[1] and hand['next_step']==2
  jd(d/'phase1-code-hash.json',{'sha256':sha(d/'invoice.py')})
 else:
  checks['resume_tool_call']='terminal' in tools
  checks['no_code_rework']=sha(d/'invoice.py')==read(d/'phase1-code-hash.json')['sha256']
  td=d/'continuity/tasks'/manifest['task_id'];state=read(td/'task-state.json');close=read(td/'closeout.json')
  checks['closed_after_resume']=state['status']=='CLOSED_PASS' and state['completed_steps']==[1,2] and state['next_step'] is None and close['verdict']=='PASS'
  sys.path.insert(0,str(H/'skills/hermes-long-task-continuity/lib'));from continuity import checkpoint_hash,canonical_hash
  chain=[read(f) for f in sorted((td/'checkpoints').glob('checkpoint-*.json'))]
  checks['checkpoint_hash_chain']=len(chain)==2 and all(checkpoint_hash(c)==c['checkpoint_sha256'] for c in chain) and chain[1]['previous_checkpoint_sha256']==chain[0]['checkpoint_sha256']
  hand=read(td/'handoff.json');hs=hand.pop('handoff_sha256');checks['handoff_hash']=canonical_hash(hand)==hs
  log=[json.loads(s) for s in (td/'events.jsonl').read_text(encoding='utf-8').splitlines()];checks['resume_event']=any(v['event']=='TASK_RESUMED' for v in log)
 result={'phase':phase,'pass':all(checks.values()),'checks':checks,'actual_tools':sorted(t for t in tools if t)}
 jd(d/f'grade-{phase}.json',result);print(json.dumps(result,ensure_ascii=False));return result['pass']
if __name__=='__main__':
 if sys.argv[1]=='setup': setup()
 elif sys.argv[1]=='grade':
  try: ok=grade(Path(sys.argv[2]),int(sys.argv[3]))
  except Exception as ex:
   print(json.dumps({'pass':False,'error':type(ex).__name__,'detail':str(ex)}));ok=False
  sys.exit(0 if ok else 2)
