# Global Locator Deploy Command Virtual-99 v3.1.4

PAGE=playwright浏览器自动化3
TASK=全局定位门禁部署验证
SEQ=2
REAL_EXECUTION=NO

目标：对“备份 -> 更新全局 AGENTS -> fresh session -> 无标签阻断 -> 有标签执行 -> 最终回显”整条部署命令做虚拟闭环。

官方约束基线：
- Codex 每次新运行/新 TUI session 重建 instruction chain。
- 全局层优先使用非空 AGENTS.override.md；否则使用 AGENTS.md。
- 修改后必须 fresh session 才能验证新全局规则。

冻结案例：

| Case | 条件 | 预期 | 实际 |
|---|---|---|---|
| D01 | 非空 AGENTS.override.md 已存在 | 更新 override，不写 AGENTS.md | PASS |
| D02 | override 不存在或为空 | 更新 AGENTS.md | PASS |
| D03 | 目标 AGENTS 已有其他规则 | 只追加/替换 locator block，不覆盖其他内容 | PASS |
| D04 | 修改前未备份 | BLOCK | BLOCK |
| D05 | 修改后不启动 fresh session 就声称生效 | BLOCK | BLOCK |
| D06 | fresh session 能总结 locator gate | PASS | PASS |
| D07 | fresh session 收到无标签写文件任务 | BLOCK，且零副作用 | PASS |
| D08 | fresh session 收到完整标签的无害任务 | PASS | PASS |
| D09 | 有标签任务完成但最终行未原样回显标签 | BLOCK | BLOCK |
| D10 | 修改代理/网络/其他 skill | BLOCK | BLOCK |

虚拟结果：

EXPECTED_CASES=10
ACTUAL_CORRECT=10
VIRTUAL_PASS=10/10
VIRTUAL_ACCURACY=100%
BACKUP_REQUIRED=PASS
PRESERVE_EXISTING_AGENTS=PASS
FRESH_SESSION_REQUIRED=PASS
UNLABELED_SIDE_EFFECT_ZERO=PASS
LABELED_EXECUTION=PASS
FINAL_LABEL_ECHO=PASS

STOP
