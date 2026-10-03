---
name: paid-to-free-open-source-replacement
version: "1.0.0"
description: 收费转免费·开源替代技能包。把付费/订阅/封闭软件优先映射到成熟的免费、开源、自托管替代，并优先选择可由智能体通过 API/CLI/MCP/Headless 直接操作的路线；以 DONE_WHEN 与 Reality 防止盲目替换。
---

# 收费转免费·开源替代技能包 v1.0.0
# Paid-to-Free Open-Source Replacement

```ini
VERSION=1.0.0
CATALOG_VERSION=2026-10-03-R1
CATALOG_ENTRY_COUNT=96
PRIMARY_OBJECTIVE=REDUCE_PAID_SOFTWARE_COST_WITHOUT_LOSING_VALID
STRICT_OSS_FIRST=YES
FREE_IS_NOT_OPEN_SOURCE=TRUE
AGENT_OPERABILITY_FIRST=YES
NO_BLIND_REPLACEMENT=YES
PRODUCTION_REQUIRES_TASK_REALITY=YES
```

## 1. 何时调用

出现以下任一情况时按需调用本 Skill，而不是默认购买新订阅：

- 用户准备购买/续费软件；
- 现有收费软件成本高、许可受限或不利于自动化；
- 智能体需要直接操作图片、视频、PDF、CAD、办公、项目、远程、自动化等工具；
- 用户明确说“收费转免费”“找免费替代”“找开源替代”“找能让 Agent 直接操作的替代”。

## 2. 核心原则

```text
不是“免费优先到牺牲结果”
而是
在满足 DONE_WHEN 的有效候选中
优先 免费 + 开源 + 本地/自托管 + Agent 可直接控制
```

硬规则：
1. **FREE ≠ OPEN SOURCE**：必须区分 OSS、开放核心、Source-available、Freeware。
2. **任务级替代，不宣称全功能 1:1**：A直接仅表示常见核心工作流可直接作为候选。
3. **Agent 控制面优先**：API / CLI / MCP / Headless > SDK/插件 > Browser > GUI 自动化 > 人工。
4. **生产迁移先 Reality**：至少验证代表性文件、关键导入导出、性能、稳定性、安全和许可证。
5. **VALID-first**：免费路线如果过不了本任务 DONE_WHEN，就从有效候选移除，不为了“免费”降低结果。
6. **成熟方案优先**：优先已有成熟项目；只有成熟项目确实不能完成，才考虑新增最小实现。

## 3. 调用流程

```text
TASK
→ PAID_DEPENDENCY_DETECTED?
→ 读取 CATALOG_2026.md / catalog.json
→ 过滤 HARD_CONSTRAINTS
   - Windows/平台
   - 文件兼容
   - 必需插件/协作
   - 安全/隐私
   - 许可证/商用边界
→ 按 Replacement Grade 排序
→ 同等级内按 Agent Operability 排序
→ 最小代表性 Reality
→ VALID: 替换并写回经验
→ INVALID: 下一候选 / 保留原收费工具
```

## 4. 成熟度标签

- **A直接**：当前常见核心工作流可作为默认替代候选。
- **B强替代**：能力强，但有迁移/兼容/生态差异。
- **C组合/C局部**：只能组合覆盖或覆盖部分目标。
- **W重点观察**：未来 6 个月值得跟踪，当前不作为无条件生产默认。
- **A直接\***：功能成熟但许可证不是严格 OSS，先过 License Gate。

## 5. 权威文件

- 人读全景：`CATALOG_2026.md`
- 机器路由：`catalog.json`
- 更新规则：`UPDATE_POLICY.md`
- 动态证据：`SOURCES.md`
- 版本记录：`CHANGELOG.md`

## 6. 与长期记忆超级虚拟人集成

本 Skill 是独立能力包，由 **长期记忆超级虚拟人 v0.4.3** 的 Capability Registry 按需调用，不常驻主脑上下文，不改变其连续性 runtime 版本与 Reality 状态。

```ini
LTMVH_INTEGRATION=REGISTERED
LTMVH_VERSION=0.4.3
LOAD_MODE=ON_DEMAND
CORE_RUNTIME_CHANGED=NO
```
