import pathlib,subprocess,sys,uuid
R=pathlib.Path(__file__).resolve().parent
goal=input('请输入需要Google规划的任务：').strip()
if not goal:raise SystemExit('任务不能为空')
folder=input('工作目录（回车使用原DSH-Workspace）：').strip().strip('"')
cwd=pathlib.Path(folder or r'C:\Users\A\Documents\DSH-Workspace').resolve(strict=True)
marker='GSB-GOOGLE-PLAN-'+uuid.uuid4().hex
task=('通过原正式shared_browser MCP与原Google Gemini登录身份，为下列任务取得Google规划。只在本任务新页提交一次标记'+marker+'，提交前先核对标记，UNKNOWN只读核账；不读凭据，不使用其他浏览器或GPT。按谷深强备成熟GOOGLE_BRAIN_PLAN_V1信封格式取得Google回答并原文保存GOOGLE_PLAN.md，回读校验后关闭自己的页、保留原页。本次只规划，不执行计划内业务或外部操作。用户任务：'+goal)
raise SystemExit(subprocess.call([sys.executable,str(R/'run_backup.py'),'--cwd',str(cwd),task]))
