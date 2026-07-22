# UltraFusion 低成本多模型极限融合 6.1B

## Alias / 记忆名

This skill can also be called:

- `UltraFusion 6.1B`
- `官网三模型`
- `两档路由`
- `GPT直答`
- `GPT DeepSeek 千问`
- `多智能体极限低成本回答6.1B`

Meaning: this is the current official UltraFusion route. Normal questions stay with GPT. High-value or extreme-answer questions escalate to GPT + DeepSeek + Qwen official sites.

Alias skill entry:

${REDACTED_SECRET}

> **两档路由的官网三模型极限答案工作台** — 普通问题不复杂化，高价值问题才升级。

## UltraFusion 6.1B 当前模型路线

当前固定两档路由：

```text
第一档：普通问题 -> GPT / ChatGPT 官网直接回答
第二档：高价值 / 极限答案问题 -> GPT 官网 + DeepSeek 官网 + 千问/Qwen 官网
```

核心原则：

- 追求极限高质量与低成本，不追求模型数量越多越好。
- 普通问题不复杂化；GPT 已足够时不调用 DeepSeek、千问/Qwen、V15、A/B/C/D。
- 高价值问题才使用多模型互审、V15 或融合流程。
- 优先使用普通用户可见的官方网站界面，不默认 API。

当前固定模型入口：

- **GPT / ChatGPT 官网**：`https://chatgpt.com/`
- **DeepSeek Chat 官网**：`https://chat.deepseek.com/`
- **千问/Qwen 官网优先**：`https://www.qianwen.com/`
- **Qwen 备用**：`https://chat.qwen.ai/`

当前角色：

- **GPT 官网版**：默认入口、普通问题直答、初始框架、最终融合、最终验收。
- **DeepSeek 官网版**：低成本深度分析、反方审稿、高价值问题补深度。
- **千问/Qwen 官网版**：第三视角、中文资料补充、搜索/综合视角、多样性审稿。

旧路线：

```text
GPT + Kimi + GLM = deprecated / old route / not current official route
```

## Quick Start

**官网测试默认执行方式：**
- 截图
- 可见坐标定位
- 一个小动作
- 再截图验证
- 按普通用户公开界面低频操作

**不作为默认方式：**
- 调试接口
- DOM / CDP / Playwright 网页内部控制
- 浏览器控制插件
- 反检测、隐藏自动化、绕过官网限制
- 用户正在使用电脑时抢占真实鼠标、键盘或前台焦点

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


## 旧路线状态

**GPT + Kimi + GLM 是旧路线，不作为 UltraFusion 6.1B 当前测试标准。**

本轮测试必须写成：

```text
当前 UltraFusion 6.1B 正式路线是两档路由：
普通问题 GPT 直答；
高价值 / 极限答案问题使用 GPT + DeepSeek + 千问/Qwen 官网三模型。
```

## 核心规则

| 规则 | 说明 |
|------|------|
| 🧭 两档路由 | 普通问题 GPT 直答；高价值问题才进入三模型 |
| 🖱 官网坐标法 | 官网测试默认截图 + 可见坐标 + 一步一验证 |
| 🔒 V15 注入 | A/B/C/D 四层全部必须注入 V15 |
| 🔚 D_Final 最终 | 无 E 层，D_Final 即最终报告 |
| ⚡ C_Fusion 极限 | C 层不是普通合并，是 V15 驱动的极限融合 |
| ⚡ D_Final 极限 | D 层不是审核，是 V15 驱动的最终稳定极限稿 |

## UltraFusion 6.1B 模型阵容

**默认 Core-3（正式路线）：**
- **M0 GPT 官网版** — 总控、最终融合、最高质量判断、最终表达、最终验收
- **M1 DeepSeek 官网版** — 深度分析、反方审稿、推理补强
- **M2 千问/Qwen 官网版** — 第三视角、中文资料补充、综合搜索视角

**旧路线位：** Kimi、GLM 不作为 6.1B 当前答案主链。

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
