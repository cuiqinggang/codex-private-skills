# 不打开GPT时如何使用
版本V1.6，2026-10-28。

## 日常
双击新增桌面“谷深强备-V1.6.cmd”，按提示输入本次任务和本机已授权工作目录。也可把完整任务保存成UTF-8文本，用：
```text
python "<本包>\\scripts\\run_backup.py" --task-file "<任务.txt>" --cwd "<工作目录>"
```
该入口通过既有launch.py调用DSH，显式要求原生加载强备技能和V4.2依赖。无需GPT、Codex或Gemini CLI；需要网络访问DeepSeek与已有账户。断网离线推理不在本合同内。
更长任务宜用--task-file；网页任务可用--mode browser，难题--mode deep。普通目标保留auto由现有成熟入口选路。
不要在目标里粘贴密钥；原DSH使用本机已有官方认证。本包不复制凭据、不安装第二套运行时。

## 接续
先读该任务已有回执，找到session-id与原cwd；调用：
```text
python "<本包>\\scripts\\run_backup.py" --task-file "<接续目标.txt>" --cwd "<原工作目录>" --session-id "<原session-id>"
```
这只复用官方会话延续，不等于崩溃后自动唤醒。外部提交不明时只读对账，不能再交一个相似任务。
原入口、旧任务和计划任务保留。新入口不可用时使用旧入口，先核账，不重复提交。

## Gemini按需协作
需要Gemini时打开其官方网页，把本包GEMINI-HANDOFF.md中相应提示词和必要脱敏任务/证据交给它；再将冻结方案或审核结论作为原任务输入交给同一DSH会话。
当前新入口验收不认证Gemini自动网页派发；人工交接必须如实标记，不能称无人值守。不要把整库资料、秘密或无关个人文件发送给Gemini。
