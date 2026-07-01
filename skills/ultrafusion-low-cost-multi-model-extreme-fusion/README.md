# UltraFusion 低成本多模型极限融合 vNext-2026-07-01-night

> **自动化多模型极限融合系统** — 不是手工流程，不是提示词合集，不是答案拼接器。

## vNext 模型路线

本版本的正式核心路线调整为：

```text
GPT 官网版 + Kimi 官网会员版 + GLM-5.2 / GLM Coding Plan
```

核心原则：

- 追求极限高质量与低成本，不追求模型数量越多越好。
- 优先使用官方网站、官方客户端、官方 Coding Plan、官方 Agent 产品。
- API 只作为自动化、批处理、备用路线，不作为极限答案主路线。

正式核心三智能体：

- **GPT 官网版**：总控、最终融合、最高质量判断、最终表达、最终验收。
- **Kimi 官网会员版**：Agent Swarm、Deep Research、多智能体分群、多角色并行审查、大规模资料探索、复杂方案分支推演、极限答案增益测试。
- **GLM-5.2 / GLM Coding Plan**：Coding Agent、技能包制作、PPT、文档结构化生成、长程任务执行、工程化落地、自动化任务。

备用模型：

- **Qwen / 通义千问**：低成本综合联网备用；如果 Kimi 测试增益不足，则可替代 Kimi 进入核心。
- **DeepSeek**：免费测试、纯推理、低成本反向审稿备用；不再作为正式核心。
- **MiniMax**：音视频、创意、多模态备用；不进入核心回答链。

## Quick Start

**正式执行方式（自动化）：**
- Hermes Agent 自动化编排
- Codex CLI 自动化编排
- Provider Adapter 自动化 API 调用
- GPT 官网套餐 + 浏览器自动化

**已废弃执行方式（禁止使用）：**
- ~~用户手工打开多个网页复制粘贴 A/B/C/D 答案~~
- ~~用户在多个模型间手动切换拼接~~
- ~~手工评分~~

### 默认输出
```
D_Final_Ultra_Answer_Final.md
```

D_Final 既包含最终答案，也包含：
- 关键事实与证据等级
- 反例测试结果
- 推理链闭合检查
- 模型贡献与扣分记录
- 残留不确定性


## V15+G Search Gate v1.1

用于处理未知实体、最新版本、当前状态、价格、政策、模型名称等易变事实。
不是让系统无限搜索，而是用小搜索预算建立事实池，避免 A/B/C/D 在错误前提上继续优化。

| 规则 | 说明 |
|------|------|
| 不认识就搜 | 专有名词/产品/版本/项目名 |
| 会变就搜 | 职位/价格/政策/法律/接口 |
| 不变的不用搜 | 数学定理/语法/历史事实/常识 |
| 搜索预算 | 1/3/5 次 |
| 事实池共享 | Search_Fact_Pool 供 A/B/C/D 共用 |


## v5.0 Core-2 Bootstrap Mode（历史基线）

**历史可用模型：GPT + DeepSeek-V4-Pro。vNext 中 DeepSeek 已降级为备用，不再作为正式核心。**

- ✅ 是否允许启动 Core-2：**是**
- ❌ 是否需要立刻接入 MiniMax/Qwen：否
- 📋 后续建议第三模型：MiniMax-M2.7 官方 API 或 Kimi
- 🔬 Qwen3.5-Flash 继续作为观察位，不进入默认主融合

## 核心规则

| 规则 | 说明 |
|------|------|
| 🚫 禁止手工 | 所有执行必须通过自动化编排器 |
| 🔒 V15 注入 | A/B/C/D 四层全部必须注入 V15 |
| 🔚 D_Final 最终 | 无 E 层，D_Final 即最终报告 |
| ⚡ C_Fusion 极限 | C 层不是普通合并，是 V15 驱动的极限融合 |
| ⚡ D_Final 极限 | D 层不是审核，是 V15 驱动的最终稳定极限稿 |

## vNext 模型阵容

**默认 Core-3（正式路线）：**
- **M0 GPT 官网版** — 总控、最终融合、最高质量判断、最终表达、最终验收
- **M1 Kimi 官网会员版** — 复杂任务位、Agent Swarm、Deep Research、多角色审查、大规模资料探索
- **M2 GLM-5.2 / GLM Coding Plan** — Coding Agent、技能包制作、文档结构化、长程任务执行、工程化落地

**备用位：** Qwen、DeepSeek、MiniMax。Qwen 可在 Kimi 增益不足时替代 Kimi；DeepSeek 仅作为测试/纯推理/反向审稿备用。

## 四层链路

```
用户问题
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ A 层 — 首轮独立极限稿                                  │
│ V15 + A_Template + Question → A_<model>_Extreme.md     │
├─────────────────────────────────────────────────────┤
│ B 层 — 第二轮交叉增强极限稿                              │
│ V15 + B_Template + Question + All A_Drafts            │
│ → B_<model>_Extreme.md                                │
├─────────────────────────────────────────────────────┤
│ C 层 — V15 驱动融合极限稿 (C_Fusion)                    │
│ V15 + C_Template + Question + All B_Drafts            │
│ → C_Fusion_Extreme.md                                 │
├─────────────────────────────────────────────────────┤
│ D 层 — V15 驱动最终稳定极限稿 (D_Final)                  │
│ V15 + D_Template + Question + C_Fusion                │
│ → D_Final_Ultra_Answer_Final.md                       │
└─────────────────────────────────────────────────────┘
```

## 安装

```bash
# 安装到 Hermes skills
cp -r ultrafusion-low-cost-multi-model-extreme-fusion ~/.hermes/skills/

# 安装到 Codex skills（如果使用 Codex 作为执行器）
cp -r ultrafusion-low-cost-multi-model-extreme-fusion ~/.codex/skills/

# H 盘备份
cp -r ultrafusion-low-cost-multi-model-extreme-fusion H:\AI\skills\
```

## 文件结构

```
ultrafusion-low-cost-multi-model-extreme-fusion/
├── SKILL.md                    # 技能包主文件
├── README.md                   # 本文件
├── 00-INDEX/                   # 索引与变更日志
├── 10-SPEC/                    # V15 规范与融合规范
├── 20-RUNBOOK/                 # 自动化执行手册
├── 30-TEMPLATES/               # A/B/C/D 极限模板
├── 35-MODEL-ROSTER/            # 模型阵容与选择规则
├── 36-PROVIDER-ADAPTERS/       # 多模型 API 适配器
├── 37-SCORING/                 # 扣分原则与评分规则
├── 38-PROMPT-ASSEMBLY/         # 提示词拼装规则 + V15 注入硬门
├── 40-WORKFLOWS/               # 自动化执行工作流
├── 45-RUNTIME/                 # 运行时状态与命名规范
├── 50-TESTS/                   # 测试样例与答案
├── 60-KB/                      # 知识库
├── 70-NOTES/                   # 模型行为笔记
├── 80-SERVICE-ROADMAP/         # 服务化路线
├── 90-ARCHIVE/                 # 历史归档
└── reports/                    # 安装与验证报告
```
