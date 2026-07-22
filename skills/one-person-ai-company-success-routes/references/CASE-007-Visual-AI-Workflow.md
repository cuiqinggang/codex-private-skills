# CASE-007 - Visual AI Workflow: n8n / Dify / Flowise / LangFlow / Activepieces

## 项目定位

这一组代表“可视化工作流 + AI 节点”路线。它们不是一人 AI 公司操作系统本身，但提供了控制台、节点画布、AI Agent node、工具/API 节点、credential 管理、历史、导入导出、人类回退等关键经验。

## 证据

- n8n README：`sources\web\n8n-README.md`，关键位置 `:5`, `:11-15`, `:38-39`, `:48-58`。
- Dify README：`sources\web\Dify-README.md`，关键位置 `:63`, `:94-108`, `:220-222`。
- Flowise README：`sources\web\Flowise-README.md`，关键位置 `:20-22`, `:90`, `:171`, `:239-241`。
- LangFlow README：`sources\web\Langflow-README.md`，关键位置 `:16`, `:23-24`。
- Activepieces README：`sources\web\Activepieces-README.md`，关键位置 `:51`, `:71`, `:77-79`, `:101`, `:113-115`。
- 本轮验证方式：raw README + 官方文档检索，不部署服务、不导入 workflow、不设置凭据。

## 关键比较

| 项目 | 可吸收机制 | 注意事项 |
|---|---|---|
| n8n | 节点画布、400+集成、AI/LangChain 工作流、模板市场、自托管 | fair-code/Sustainable Use License；真实集成涉及 credentials |
| Dify | AI workflow、RAG、Agent、模型管理、observability integrations、可视化调试 | Dify Open Source License 带附加条件；模型和工具需 key |
| Flowise | Build AI Agents visually、Agentflow、第三方节点组件、环境变量配置 | Node/服务部署重；适合 UI 原型参考 |
| LangFlow | Visual authoring、API/MCP server、multi-agent orchestration、JSON export | 更适合作为“流程可导出/可调用工具”的参考 |
| Activepieces | AI-first automation、type-safe pieces、human approval、人类输入界面、200+集成 | 真实连接器涉及账号/凭据；企业特性有商业许可 |

## 对 Polsia 控制台的参考价值

1. 可视化画布应该用于“理解和审批”，不应让用户以为拖线就等于安全生产。
2. 每个节点必须显示：输入、输出、执行体、权限、凭据需求、审批状态、历史运行。
3. Credential 管理必须只显示状态，不显示明文 secret。
4. Workflow import/export 应成为技能包/route 的迁移格式，但导入后必须先进入 mock/replay。
5. Human fallback 应是一等节点或节点属性，不能作为失败后的临时聊天。
6. Workflow history 应映射到昨日重现法：每次更新保留来源、判断、吸收/暂缓/放弃理由。

## 可吸收机制

| 机制 | 吸收到本地体系 |
|---|---|
| Visual canvas | AICompany Dashboard 控制台原型 |
| Agent/tool/API node | HiveWard Blueprint / Polsia task workflow 节点模型 |
| Credential status | 只读凭据状态，不打印密钥 |
| Import/export | 技能包 route card / workflow JSON/YAML |
| Human approval/fallback | 审批门和 Level 3 stop gate |
| Workflow history | run history、periodic update、case study evidence |
| Template marketplace | WATCHLIST + ROUTE-MATRIX 的外部路线库 |

## 风险

- 可视化工具容易诱导“安装一堆平台”，与用户硬规则冲突。
- 多数真实 workflow 需要账号/API key/付费连接器，本轮不运行。
- UI 借鉴必须避免复制品牌、布局和私有工作流。

## 是否进入技能包

进入。把这组作为 CASE-007，吸收 UI/流程/凭据/历史/导入导出/人类回退机制；下一阶段建议只做 Polsia/AICompany Dashboard 控制台原型，不做真实接入。
