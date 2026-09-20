# 冻结现实验证命令 — WIN1344-NARROW-SESSION-CWD-v1

【playwright浏览器自动化5｜1344唯一冻结方案现实验证｜1｜高智能虚拟成熟】

CURRENT_STEP=3

只执行已经由 GPT 完成 Virtual-99（虚拟99）并冻结的唯一方案。
Codex 不分析原因、不搜索方案、不修改冻结方案。

读取：
- 本目录 FROZEN-HARDENING-PLAN.json
- VIRTUAL-99-RESULT.json
- MINIMALITY-PROOF.json

唯一现实变化：
把一个**新的 Codex workspace-write 会话**的 session CWD（会话级工作目录）从：

C:\Users\A

改为：

C:\Users\A\playwright-browser-automation5-final-reality-competition-work

注意：必须改变新会话启动时的 CWD / workspace root；只给某条工具调用设置 workdir 不算执行方案。

如果目标目录不存在：
ACTION=STOP
只回 TARGET_PROJECT_MISSING
禁止创建替代目录。

保持全部其他 Reality 条件不变：
Codex 0.155.1；
windows.sandbox=unelevated；
approval_policy=on-request；
config/AGENTS/rules/skills/ACL/cap_sid/PATH/代理/网络全部不改。

在该窄项目目录中启动同版本 Codex workspace-write 会话。
执行完全相同的最小只读子进程探针 3 次，每次只输出：

H1_NARROW_CWD_OK

不得创建文件。
不得访问网络。
不得第4次测试。

每次记录：
SESSION_CWD
PROCESS_START_RESULT
STDOUT
STDERR
ERROR_API
ERROR_CODE

成功门禁：
3/3 PROCESS_START_RESULT=SUCCESS
3/3 STDOUT=H1_NARROW_CWD_OK
3/3 ERROR_CODE=NONE
1344_COUNT=0
REALITY_MUTATION_OUTSIDE_SESSION_CWD=0

如果出现任一 1344：
REAL_VERIFY=FAIL_1344
记录差异并 STOP。

如果 1344 消失但出现 1920 或任何其他新错误：
REAL_VERIFY=REALITY_DELTA_NEW_ERROR
记录新错误并 STOP。
禁止改 PATH、禁止换 shell、禁止自己继续修。

最终只回：
PLAN_ID=
SESSION_CWD=
RUN_1=
RUN_2=
RUN_3=
ERROR_1344_COUNT=
NEW_ERROR_CODES=
REALITY_MUTATION_OUTSIDE_SESSION_CWD=
REAL_VERIFY=
PREDICTION_MATCH=
ACTION=STOP

【playwright浏览器自动化5｜1344唯一冻结方案现实验证｜1｜高智能虚拟成熟】
