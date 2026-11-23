# UltraFusion 低成本多模型极限融合 v5.0

> **自动化多模型极限融合系统** — 不是手工流程，不是提示词合集，不是答案拼接器。

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

## 核心规则

| 规则 | 说明 |
|------|------|
| 🚫 禁止手工 | 所有执行必须通过自动化编排器 |
| 🔒 V15 注入 | A/B/C/D 四层全部必须注入 V15 |
| 🔚 D_Final 最终 | 无 E 层，D_Final 即最终报告 |
| ⚡ C_Fusion 极限 | C 层不是普通合并，是 V15 驱动的极限融合 |
| ⚡ D_Final 极限 | D 层不是审核，是 V15 驱动的最终稳定极限稿 |

## 模型阵容

**默认 Core-3（生产模式）：**
- **M0 GPT** — 质量锚点，官方套餐自动化，A→D 全程参与
- **M1 DeepSeek-V4-Pro** — 主力推理引擎
- **M2 MiniMax-M2.7** — 多样性与交叉验证

**观察位 Qwen3.5-Flash：** 不自动进入主融合，需通过消融测试证明独立贡献后才可升级。

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
