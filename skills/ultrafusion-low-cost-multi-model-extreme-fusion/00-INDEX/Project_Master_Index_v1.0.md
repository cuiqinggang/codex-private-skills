# UltraFusion 主索引 v1.0

## 项目概要
- 名称：UltraFusion 低成本多模型极限融合
- 版本：v5.0.0
- 定位：自动化 A-B-C-D 多模型极限融合系统
- 原则：全自动化、V15 注入硬门、不手工、不缝合、不伪造

## 文件索引

### 10-SPEC（规范层）
| 文件 | 说明 |
|------|------|
| V15_Guard_Prefix_v1.0.md | V15 前置约束层（G 层） |
| V15_FULL_v1.0.md | V15 规范原文 |
| V15_FULL_WITH_GUARD_v1.0.md | V15+G 完整版本（仅供引用） |
| V15_CANONICAL_SOURCE.md | V7.0 canonical V15 source pointer and recovery evidence |
| SPEC_KIT_v1.1.md | 整体规范工具包 |
| Fusion_Spec_v1.0.md | 融合层规范 |

### 20-RUNBOOK（执行手册）
| 文件 | 说明 |
|------|------|
| Automated_Runbook_v1.0.md | 自动化执行总手册 |
| Hermes_Automated_Execution_v1.0.md | Hermes 编排执行 |
| Codex_Automated_Execution_v1.0.md | Codex 编排执行 |

### 30-TEMPLATES（模板层）
| 文件 | 说明 |
|------|------|
| 00_Router_Template_v1.0.md | 路由层模板 |
| 01_D_Lite_Template_v1.0.md | D-Lite 快速模板 |
| 10_A_Layer_Extreme_Draft_Template_v1.0.md | A 层极限稿模板 |
| 20_B_Layer_Cross_Enhancement_Template_v1.0.md | B 层交叉增强模板 |
| 30_C_Layer_Dense_Fusion_Extreme_Template_v4.0.md | C 层融合极限模板 |
| C_LAYER_OFFICIAL_FUSION_PROMPT_v20260706.md | V7.0 C 层官方复检陌生稿 + 稠密融合提示词 |
| 40_D_Layer_Final_Extreme_Report_Template_v3.0.md | D 层终审极限模板 |

### 35-MODEL-ROSTER（模型阵容）
| 文件 | 说明 |
|------|------|
| Model_Roster_v5.0.md | 模型阵容表 |
| Model_Selection_Rules_v5.0.md | 模型选择规则 |
| Qwen_Ablation_Test_Rules_v1.0.md | Qwen 消融测试规则 |
| Model_Failure_And_Skip_Rules_v1.0.md | 失败与空过规则 |
| Model_Update_Policy_v1.0.md | 模型更新策略 |
| Provider_Config_Template_v1.0.md | 提供商标识模板 |

### 36-PROVIDER-ADAPTERS（适配器）
| 文件 | 说明 |
|------|------|
| Provider_Adapter_Spec_v1.0.md | 适配器通用规范 |
| GPT_Official_Subscription_Automation_v1.0.md | GPT 套餐自动化 |
| DeepSeek_Official_API_Adapter_v1.0.md | 深度求索官方 API |
| MiniMax_Official_API_Adapter_v1.0.md | MiniMax 官方 API |
| Qwen_Official_API_Adapter_v1.0.md | 通义千问官方 API |
| Kimi_Official_API_Adapter_v1.0.md | Moonshot/Kimi 官方 API |
| Gemini_API_Adapter_v1.0.md | Google Gemini API |
| GLM_API_Adapter_v1.0.md | 智谱GLM API |
| ERNIE_API_Adapter_v1.0.md | 百度文心 API |
| Pangu_API_Adapter_v1.0.md | 华为盘古 API |
| Provider_Secrets_Template.example.yml | 密钥配置模板 |

### 37-SCORING（评分层）
| 文件 | 说明 |
|------|------|
| V15_Scoring_With_Deduction_v1.0.md | V15 评分加扣分体系 |
| Deduction_Rules_v1.0.md | 扣分细则 |
| Model_Contribution_Score_v1.0.md | 模型贡献度评分 |

### 38-PROMPT-ASSEMBLY（提示词拼装）
| 文件 | 说明 |
|------|------|
| Prompt_Assembly_Rules_v1.0.md | 总拼装规则 |
| V15_Injection_Hard_Gate_v1.0.md | V15 注入验收门 |
| A_Prompt_Assembly_Spec_v1.0.md | A 层拼装规范 |
| B_Prompt_Assembly_Spec_v1.0.md | B 层拼装规范 |
| C_Prompt_Assembly_Spec_v1.0.md | C 层拼装规范 |
| D_Prompt_Assembly_Spec_v1.0.md | D 层拼装规范 |
| RULE-PATCH-20260706-c-layer-official-prompt.md | V7.0 C 层官方提示词强制规则 |
| FAILURE-REVIEW-20260706-c-layer-simplified-prompt.md | C 层误用简化提示词失败复盘 |
