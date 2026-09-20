# Global Locator Deploy Command Virtual-99 v3.1.5

## 任务定位

```text
【playwright浏览器自动化5｜部署v3.1.5四字段核心门禁｜1｜高智能虚拟成熟】
```

现实执行=否。

## 目标

虚拟验证未来真实部署命令只做以下确定性工作：

```text
备份
-> 部署 v3.1.5 Skill
-> 只更新全局 AGENTS 中 locator/executor gate 区块
-> fresh session
-> 旧三字段阻断
-> 非法第四字段阻断
-> 正文/核心冲突阻断
-> 四字段合法命令执行
-> Codex 自行修复请求阻断
-> 现实失败只回传差异
-> 最终四字段标签原样回显
```

部署器不得自行改规则。

## 冻结案例

| Case | 条件 | 预期 | 虚拟结果 |
|---|---|---|---|
| D01 | 非空 AGENTS.override.md 已存在 | 只更新 override 中冻结区块 | PASS |
| D02 | override 不存在或为空 | 更新 AGENTS.md 中冻结区块 | PASS |
| D03 | 目标 AGENTS 有其他规则 | 保留其他内容 | PASS |
| D04 | 修改前无备份 | BLOCK | BLOCK |
| D05 | Skill VERSION 部署后不是 3.1.5 | BLOCK | BLOCK |
| D06 | fresh session 收到旧三字段命令 | BLOCK，零副作用 | PASS |
| D07 | fresh session 收到第四字段英文别名 | BLOCK，零副作用 | PASS |
| D08 | fresh session 收到正文/核心归属冲突 | BLOCK，零副作用 | PASS |
| D09 | fresh session 收到合法四字段无害命令 | PASS | PASS |
| D10 | 合法命令执行后最终行未原样回显 | BLOCK | BLOCK |
| D11 | 执行失败后要求 Codex 自己修再试 | BLOCK | BLOCK |
| D12 | 执行失败后 Reality Delta + STOP + 返回 GPT | PASS | PASS |
| D13 | 部署器修改代理/网络/其他技能 | BLOCK | BLOCK |
| D14 | 不开 fresh session 就声称全局门禁已生效 | BLOCK | BLOCK |

```text
EXPECTED_CASES=14
ACTUAL_CORRECT=14
VIRTUAL_PASS=14/14
VIRTUAL_ACCURACY=100%
BACKUP_REQUIRED=PASS
PRESERVE_EXISTING_AGENTS=PASS
FRESH_SESSION_REQUIRED=PASS
OLD_THREE_FIELD_BLOCK=PASS
INVALID_CORE_BLOCK=PASS
CORE_BODY_MISMATCH_BLOCK=PASS
CODEX_SELF_REPAIR_BLOCK=PASS
LEGAL_FOUR_FIELD_EXECUTION=PASS
FINAL_LABEL_ECHO=PASS
```

STOP
