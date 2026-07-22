# 运行时加固最终测试报告

- 技能正式名称：可回退并行探索与强制验收技能包 V1.0
- 技能 ID：`safe-parallel-exploration-and-acceptance`
- 日期：2026-07-12
- 最终状态：`FINAL_PASS`

## 三层复测

| 层级 | 静态检查 | 运行时正反例 | 原有三轮验收 |
|---|---:|---:|---:|
| 候选副本 | PASS | 15/15 PASS | 3/3 PASS |
| integration-candidate | PASS | 15/15 PASS | 3/3 PASS |
| 正式安装副本 | PASS | 15/15 PASS | 3/3 PASS |

运行时正反例覆盖：空 `.git`、非 Git 目录、普通 worktree、bare repository、合法 tree、Windows 非法路径阻断、普通 worktree 负例、隔离恢复预览、隔离恢复不改基线、`autocrlf` 精确字节正反例、只读沙箱注入、非 Git 安装副本验收。

## 测试推动的二次修复

1. 首次静态测试发现新 PowerShell 文件没有 UTF-8 BOM，Windows PowerShell 5.1 将中文误解码并报字符串未终止。已加 BOM，重新测试通过。
2. 首次运行测试发现 Git worktree 的进度输出污染 JSON 契约。把 native stderr 捕获后，PowerShell `ErrorRecord` 又在深层 JSON 序列化时造成长时间卡住。已把所有 native 输出先转换为纯字符串，并给 Python 测试命令增加 90 秒超时；从头重跑后通过。

## 安全结论

- 修改前关键文件哈希在安装前全部复核一致，没有覆盖并发改动。
- main/基线 ref 未改变；隔离恢复分支无父提交，自动合并关闭。
- 没有 push、没有自动 merge、没有初始化正式技能目录 Git。
- 没有写入 K 盘。
${REDACTED_SECRET}

## 外部证据目录

${REDACTED_SECRET}

其中包含候选、集成、正式安装三层的 static、runtime 和 three-round JSON 证据。

验收页视觉证据：`90_RUNTIME_HARDENING/acceptance-runtime-hardening.png`，已人工检查中文、状态、表格和链接区布局，无截断或乱码。
