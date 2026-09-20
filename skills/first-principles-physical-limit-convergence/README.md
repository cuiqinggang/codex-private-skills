# 第一性原理极限短时间引擎 v3.1.7

## 唯一三个核心

```text
1. 极限短时间
2. 成熟方案集群
3. 高智能虚拟成熟
```

只有这三个核心拥有方法权。任何任务如果不能真实、唯一地映射到其中一个核心，就不能发布给执行器。

## 唯一流程

```text
极限短时间
-> 成熟方案集群
-> 高智能虚拟成熟
-> 执行器只验证/执行已冻结结果
```

现实执行不是第四核心。出现问题时也没有“Codex 修复路线”。

固定闭环：

```text
执行失败或发现差异
-> Codex 记录现实差异并停止
-> 返回 GPT 页面
-> GPT 重新判断三个核心中的归属
-> 必要时在“高智能虚拟成熟”中重新成熟并冻结
-> 再发新的执行命令
```

Codex / Reasonix / 本地执行器只能执行冻结命令，不能自行修复、重新设计、增加路线、修改模型/阈值/路由/fallback/验证合同。

## v3.1.5 四字段定位标签

原来的三个字段保留，只在最后增加一个中文核心归属：

```text
【实际页面名｜具体任务名｜序号｜核心归属】
```

第四字段只允许：

```text
极限短时间
成熟方案集群
高智能虚拟成熟
```

例如：

```text
【playwright浏览器自动化5｜现实环境全面检查｜1｜成熟方案集群】
【playwright浏览器自动化5｜冻结最终方案｜2｜高智能虚拟成熟】
【playwright浏览器自动化5｜执行冻结方案现实验证｜3｜高智能虚拟成熟】
```

第四字段禁止用英文别名、数字核心、STEP、修复、补丁、验收等其他分类替代。

如果一条命令同时跨多个核心，GPT 必须先拆分，不能把多个核心写进一个标签。

## 序号不再代表修复窗口

序号只是 GPT 正式命令计数。

```text
1..6 = 顺序号
不是修复阶段
```

v3.1.4 中“4..6 是修复窗口”的语义已取消。

执行器失败后必须停止；是否产生下一条命令，只能由 GPT 页面决定。

## 完成即交接

当 GPT 已经完成虚拟成熟并冻结可执行结果时，同一回复直接给执行器最短命令；详细规则只保留在正式文件/技能包中。

正式分支：

`codex/first-principles-physical-limit-convergence-v3.1.7`

## JEV Probability Engine P0 v0.4.0 现实认证

`jev-probability-engine-p0` 子组件已由 Reality Challenge V2 正式认证：

```text
STATUS=REAL_P0_CERTIFIED
PREVIOUS_T_P0_MS=840.6046999999962
T_REAL_STAR_MS=560.9819
T_P0_MS=560.9819
P50_MS=648.87
P95_MS=988.8238
MAX_MS=1285.2925
PASS_RUNS=30
FAIL_RUNS=0
COMMERCIAL_GATE_SERIES=PASS
EXPECTED_HTTP_REQUESTS=67
ACTUAL_HTTP_REQUESTS=67
REQUEST_COUNT_MATCH=PASS
```

认证入口：`components/jev-probability-engine-p0-extreme/certifications/v0.4.0/REALITY_CERTIFICATION.md`。旧 v0.3.0、V1/V2 和 840.6046999999962 ms 历史继续保留。


## v3.1.7 浏览器现实扩展

- 现实锚定技能：`reality-execution-environment-anchor@1.2.0`
- 中文：现实执行环境精确锚定与数字孪生基线
- 唯一数字孪生：`exact-reality-digital-twin@1.1.0`
- 中文：现实执行环境精确数字孪生唯一版
- R1/R2 Host Reality Fingerprint V3 保持：
  `9bdd4430596e306cf6f8061069659e2680d8a1b66bd69d7bb3e45fe4cfd63dd8`

v1.2.0 新增 Browser Reality R3，完整把 Browser/Profile/Context/Auth/DOM/actionability/Network/Service Worker/WebSocket/Runtime/Trace/CDP/Golden Task 纳入现实锚定。

当前状态：

```text
HOST_R2_REALITY_ANCHOR_COMPLETE=YES
BROWSER_R3_COLLECTOR_CONTRACT=FROZEN
BROWSER_R3_REAL_CAPTURE=NOT_YET
BROWSER_R3_FINGERPRINT=NOT_YET
BROWSER_TWIN_INPUT_READY=NO
ENVIRONMENT_99=NOT_YET
```

现实采集仍属于“成熟方案集群”；Twin 的重放、差异收敛、故障推演与 Virtual-99 仍属于“高智能虚拟成熟”。没有第四核心。
