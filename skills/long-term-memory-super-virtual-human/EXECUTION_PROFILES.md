# 长期记忆超级虚拟人｜执行能力档位 v0.1

## 原则

不新建一个永久常驻“巨型工作站”。

现有成熟能力按任务作为执行档位按需激活。

## P0｜Direct Fast Path

适合：
- 搜索；
- 文件查询；
- 邮件/日历/Drive；
- 简单 Windows 操作；
- 轻量分析；
- 图像等原生工具任务。

```text
GPT → 原生 Tool/Connector → Reality → FINAL_VALID
```

默认先竞争此路。

## P1｜Engineering Executor

适合：
- 多文件编码；
- 仓库修改；
- build/test；
- 工程化脚本；
- 明显需要开发工具链的任务。

候选：
- GPT 直接本地工程工具；
- Codex；
- Reasonix。

按完整 T_VALID 竞争，不固定 Codex 必经。

## P2｜Long-Flow ECC

适合：
- 复杂长任务；
- 跨会话恢复；
- 多角色；
- Gate → Repair → Re-Gate；
- checkpoint/handoff；
- lease/fencing；
- 故障注入、耐力与恢复验证。

成熟基线：
```text
ECC v3.1.1 四角色长流程闭环编排系统
```

默认复用，不重造第二套长流程体系。

## P3｜Mature AI Coding SuperTool Ecosystem Station

本机已有成熟资产：
```text
C:\AI\DeerFlow-SuperEmployee-Station
```

包括：
- 成熟规则；
- Skill/Tool Registry；
- 重资料库；
- Gate Review；
- Repair Loop；
- checkpoint/resume/handoff；
- 多智能体合同；
- 模型路由；
- 验证与回滚；
- Reasonix 迁移资产。

定位：
```text
复杂度足够高时按需唤醒的生产生态工作站
```

不是 GPT 每次启动都加载的永久中间层。

当前资产存在；本机 127.0.0.1:2026 服务可按需启动，平时允许 Dormant。

## P4｜Independent Continuity

GPT 本身不可用时启用。

目标是用低相关模型/执行器读取同一权威任务合同、Checkpoint 和持久资产继续业务。

此档未完成完整 Reality 认证前不得宣称生产就绪。

## 路由

```text
先 P0
→ 如果不 VALID 或完整 T_VALID 更差，再升 P1
→ 长流程特征触发 P2
→ 多工具/多智能体/重资料复杂工程触发 P3
→ GPT 故障触发 P4
```

不是按任务“大不大”机械升级，而是由 Reality 和预期返工/恢复成本决定。
