# 项目共同进度账

`SHARED_WORKSPACE_REPOSITORY=cuiqinggang/codex-private-skills`

| DATE | PREVIOUS_BEST | NEW_BEST | CHANGE | WHY | GAIN | EVIDENCE_PATH | GITHUB_COMMIT | SKILL_VERSION |
|---|---:|---:|---|---|---:|---|---|---|
| 2026-09-15 | — | 32.55975 ms | 冻结初始完整任务基线 | 为后续四列分析固定 CURRENT | — | `skills/absolute-time-fireworks-optimization/references/FOUR-COLUMN-P0-99.md` | `282a347818aa331d657c25ed00e6881dfffbbbc9` | pre-skill |
| 2026-09-15 | 32.55975 ms | 21.9215 ms | 删除 file-backed output / publish / reopen，改 memory/WebSocket | 磁盘结果链不是最终任务物理必需 | 10.63825 ms / 32.6730% | `skills/absolute-time-fireworks-optimization/references/FOUR-COLUMN-P0-99.md` | `282a347818aa331d657c25ed00e6881dfffbbbc9` | 1.0.0 |
| 2026-09-15 | 21.9215 ms | 12.6782 ms | 脱 history/double decode；固定 tensor 缓存 PNG；最终 40-run 认证 | 删除非必要同步与重复编码后再认证 | 9.2433 ms / 42.165454% | `workspaces/absolute-time-fireworks-optimization/P0-EXTREME-MINIMAL-FASTPATH/certification-20260915-193531/results.json` | `282a347818aa331d657c25ed00e6881dfffbbbc9` | 1.0.0 |
| 2026-09-15 | 12.6782 ms | 12.6782 ms | NEW_99_FREEZE：正式四列案例、完整工程、原始认证、失败索引和共享制度同步共同仓库 | 让 GPT、Codex 与其他智能体只靠共同仓库即可复刻和续作 | 0 ms；纯冻结收口 | `skills/absolute-time-fireworks-optimization/references/REMOTE-VALIDATION.md` | `c2adab036195dc011449dcf32c64769cde74d470` | 1.1.0 |
| 2026-09-15 | 12.6782 ms | 12.6782 ms | NEW_FAILURE：PowerShell `-File` 的多个 `string[]` 路径被合并 | 让 hot sync 以后直接按单文件调用，并以 `MISSING=0` 为门禁 | 0 ms；收口工具修复 | `skills/absolute-time-fireworks-optimization/references/FAILURE-INDEX.md#fi-12-powershell--file-的-string-参数被合并` | `8b14d5d2a4f892cee314e722e1ab5f712dcb96d9` | 1.1.0 |
| 2026-09-15 | 12.6782 ms | 12.6782 ms | METHOD_CHANGE + NEW_FAST_PATH：升级为通用99收敛引擎；结构涌现、去重甲核心化、默认入口极简，并加入 GPT/Codex/GitHub/浏览器闭环 | 将 P0 已验证方法推广为不预设节点或系统层级的通用执行引擎 | 0 ms；方法升级，不运行 benchmark | `skills/absolute-time-fireworks-optimization/SKILL.md`、`references/EXECUTION-BRIDGE.md`、`references/CASE-001-P0-COMFYUI-EXTREME-TIME.md` | `c4df94b` | 2.0.0 |
| 2026-09-15 | 12.6782 ms | 12.6782 ms | NEW_FAILURE：浏览器业务入口比预期多一层权威 Skill 路径 | 防止未来调用不存在的项目根脚本或复制第二套浏览器能力 | 0 ms；路径事实纠正 | `skills/absolute-time-fireworks-optimization/references/FAILURE-INDEX.md#fi-13-浏览器业务入口少了一层-skill-路径` | `c4df94b` | 2.0.0 |

## 追加规则

每次 `NEW_BEST（新的最好成绩）`、`NEW_FAILURE（新的失败经验）`、`NEW_FAST_PATH（新的成熟最短路径）`、`METHOD_CHANGE（方法变化）`、`ROOT_CAUSE_FOUND（找到根因）`、`99_REOPEN（99 重新开启）` 或 `NEW_99_FREEZE（新的 99 冻结）`，必须在阶段结束后追加一行并同步共同仓库。

不得改写历史行；事实修订用新行说明。
