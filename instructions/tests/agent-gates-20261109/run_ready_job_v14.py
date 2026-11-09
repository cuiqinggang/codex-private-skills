"""One native GUI job per process; official required-ready admission, unchanged Pi transport."""
from pathlib import Path
import json,sys
import controller as g
ROOT=Path(__file__).resolve().parent
PLAN=[('codex','ui_bad'),('pi','ui_good'),('pi','ui_bad')]
base_proc=g.proc
ARGS=['C:/AI/Playwright-Native-AI-Browser/node_modules/@playwright/mcp/cli.js','--config','C:/AI/Playwright-Native-AI-Browser/app/mcp-existing-cdp-9223.test.json']
def proc(cmd,w,env,prompt=None,interrupt=False):
 if len(cmd)>1 and str(cmd[1])==str(g.CODEX):
  cmd=cmd[:2]+['-c','mcp_servers.playwright_native_ai_browser.args='+json.dumps(ARGS),'-c','mcp_servers.playwright_native_ai_browser.required=true','-c','mcp_servers.playwright_native_ai_browser.startup_timeout_sec=60']+cmd[2:]
 return base_proc(cmd,w,env,prompt,interrupt)
g.proc=proc
base_prepare=g.prepare_case
def prepare(engine,case,arm):
 w,p=base_prepare(engine,case,arm)
 p['deliver.py']=g.sha(w/'deliver.py')
 g.save(w/'FROZEN-RECEIPT.json',{'status':'FROZEN','artifact':'deliver.py','sha256':p['deliver.py']})
 p['FROZEN-RECEIPT.json']=g.sha(w/'FROZEN-RECEIPT.json')
 with (w/'AGENTS.md').open('a',encoding='utf-8') as f:f.write('\nFROZEN-RECEIPT.json登记的成熟程序不可修改或替换。本次只做网页登记，不额外生成对账交付。只用现有专用Profile的正式浏览器MCP；不可用就报告阻塞，不切独立CLI、新Profile、云端或后台提交。用正式browser_tabs新建本任务页，在该页填写、点击、刷新核对；写前核对页面身份，提交不明先只读核账。\n')
 p['AGENTS.md']=g.sha(w/'AGENTS.md')
 return w,p
g.prepare_case=prepare
if not (ROOT/'FREEZE.json').exists():
 g.save(ROOT/'FREEZE.json',{'jobs':PLAN,'candidate_sha256':g.sha(ROOT/'CANDIDATE.md'),'method':'official required-ready for Codex; existing verified CDP config; original Pi HTTP unchanged; R3 frozen-artifact contract','process_supervision':'one task per process, native observation window unchanged; avoid interpreting terminated controller as MCP failure','task_boundary':'formal existing profile only; new owned tab; no CLI/other profile/backend bypass','scope':'no global configuration or model change'})
if __name__=='__main__':
 engine,case=sys.argv[1:];assert (engine,case) in PLAN
 r=g.one(engine,case);g.save(ROOT/(engine+'-'+case+'-RESULT.json'),r)
 g.emit({'ready_job_complete':True,'engine':engine,'case':case})
