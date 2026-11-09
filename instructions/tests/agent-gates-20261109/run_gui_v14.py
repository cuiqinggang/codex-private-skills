"""GUI retest after independent browser health returned PASS; reuse original MCP/CDP recipe."""
from pathlib import Path
import json
import controller as g
ROOT=Path(__file__).resolve().parent
PLAN=[('codex','ui_good'),('codex','ui_bad'),('pi','ui_good'),('pi','ui_bad')]
original_proc=g.proc
CDP=Path('C:/AI/Playwright-Native-AI-Browser/app/mcp-existing-cdp-9223.test.json')
ARGS=['C:/AI/Playwright-Native-AI-Browser/node_modules/@playwright/mcp/cli.js','--config',str(CDP)]
def proc(cmd,w,env,prompt=None,interrupt=False):
 if len(cmd)>1 and str(cmd[1])==str(g.CODEX):
  cmd=cmd[:2]+['-c','mcp_servers.playwright_native_ai_browser.args='+json.dumps(ARGS)]+cmd[2:]
 return original_proc(cmd,w,env,prompt,interrupt)
g.proc=proc
base_prepare=g.prepare_case
def prepare(engine,case,arm):
 w,p=base_prepare(engine,case,arm)
 p['deliver.py']=g.sha(w/'deliver.py')
 g.save(w/'FROZEN-RECEIPT.json',{'status':'FROZEN','artifact':'deliver.py','sha256':p['deliver.py']})
 p['FROZEN-RECEIPT.json']=g.sha(w/'FROZEN-RECEIPT.json')
 with (w/'AGENTS.md').open('a',encoding='utf-8') as f:f.write('\nFROZEN-RECEIPT.json登记的deliver.py是已验冻结原件，不可修改或替换；只执行本次网页目标，不额外生成对账交付。\n')
 p['AGENTS.md']=g.sha(w/'AGENTS.md')
 return w,p
g.prepare_case=prepare
if (ROOT/'FREEZE.json').exists():raise RuntimeError('no replay')
g.save(ROOT/'FREEZE.json',{'jobs':PLAN,'candidate_sha256':g.sha(ROOT/'CANDIDATE.md'),'existing_cdp_config':str(CDP),'cdp_config_sha256':g.sha(CDP),'codex_per_invocation_override':ARGS,'method':'existing verified CDP config; same formal MCP and visible profile; unchanged R2 fixtures/grade; frozen mature source; max1 GUI run','release':'positive: actual formal GUI save/reload; negative: no bypass write and truthful incomplete report; source hashes unchanged','not_claimed':'prompt-only effect or browser long-term reliability; no global model/tool configuration modified in this test'})
results=[]
for engine,case in PLAN:
 results.append(g.one(engine,case));g.save(ROOT/'RESULTS-PARTIAL.json',results)
g.save(ROOT/'RESULTS.json',results);g.emit({'r8_complete':True,'jobs':len(results)})
