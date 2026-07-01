# Source Snapshot

本文件记录本轮调研使用的主要来源和本地证据路径。

## 本地克隆

- HiveWard: `H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\HiveWard`, HEAD `6f4524b483a1be8cef72baed8843c881d6c4901f`.
- MetaGPT: `H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\MetaGPT`, HEAD `11cdf466d042aece04fc6cfd13b28e1a70341b1f`.
- ChatDev: `H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\ChatDev`, HEAD `a6a5cda5560053136897aa44301eacc6c48d8168`.
- AgileCoder: `H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\AgileCoder`, partial clone only, HEAD `f9924185bcc8db9ba504e588e1a425920d4dd9db`.

## Raw README 快照

- CrewAI: `sources\web\CrewAI-README.md`, raw URL `https://raw.githubusercontent.com/crewAIInc/crewAI/main/README.md`.
- AutoGen: `sources\web\AutoGen-README.md`, raw URL `https://raw.githubusercontent.com/microsoft/autogen/main/README.md`.
- LangGraph: `sources\web\LangGraph-README.md`, raw URL `https://raw.githubusercontent.com/langchain-ai/langgraph/main/README.md`.
- AG2: `sources\web\AG2-README.md`.
- Agency Swarm: `sources\web\AgencySwarm-README.md`.
- n8n: `sources\web\n8n-README.md`.
- Dify: `sources\web\Dify-README.md`.
- Flowise: `sources\web\Flowise-README.md`.
- Langflow: `sources\web\Langflow-README.md`.
- Activepieces: `sources\web\Activepieces-README.md`.
- OpenHands: `sources\web\OpenHands-README.md`.
- Aider: `sources\web\Aider-README.md`.
- Codex: `sources\web\Codex-README.md`.
- AgentOps: `sources\web\AgentOps-README.md`.
- Langfuse: `sources\web\Langfuse-README.md`.
- Phoenix: `sources\web\Phoenix-README.md`.
- Opik: `sources\web\Opik-README.md`.
- OpenPolsia: `sources\web\OpenPolsia-README.md`.

## 元数据和日志

- GitHub 搜索结果：`sources\metadata\github-search-results.json`.
- GitHub 执行/观察查询：`sources\metadata\github-search-execution-observability.json`.
- Repo API 限流记录：`sources\metadata\github-repo-metadata.json`.
- Raw README 下载记录：`sources\metadata\raw-readme-downloads.json`.
- 克隆日志：`logs\clone-*.log`.
- 执行日志：`logs\execution.log`.

## Polsia / POSA 2026-05-28 追加证据

- CASE-008：`references\CASE-008-Polsia-Zero-Employee-Company.md`.
- Intake 报告：`reports\periodic-updates\20260528-posa-polsia-intake.md`.
- 官网快照：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\polsia-posa-20260528\polsia_com.html`.
- 前端 JS 快照：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\polsia-posa-20260528\assets_index_DGRm7ehX_js`.
- 提取的关键 API：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\polsia-posa-20260528\extracted-api-endpoints-interesting.txt`.
- 公开 live dashboard summary：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\polsia-posa-20260528\public-live-dashboard-summary.json`.
- 登录边界探测：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\web\polsia-posa-20260528\read-only-api-probe-results.json`.
- 用户截图证据：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\screenshots\polsia-posa-20260528\source-screenshot-1.jpg` 到 `source-screenshot-3.jpg`.

## Sahil Lavingia / Minimalist Entrepreneur 10 Skills 2026-05-30 追加证据

- CASE-009：`references\CASE-009-Sahil-Lavingia-Minimalist-Entrepreneur-10-Skills.md`.
- Intake 报告：`reports\periodic-updates\20260530-sahil-lavingia-10-skills-intake.md`.
- 独立技能包：`H:\AI\skills\minimalist-entrepreneur-10-skills`.
- 可复制发布页：`PUBLISH-MINIMALIST-ENTREPRENEUR-10-SKILLS-20260530.md`.
- GitHub 仓库：`https://github.com/slavingia/skills`.
- 本地浅克隆：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\sources\repos\slavingia-skills`, HEAD `eb9f57fba03ddb0382ed3bfe6654d3d7df128c70`.
- 视频抽帧：`H:\AI\_explore\one-person-ai-company-success-routes-20260528\screenshots\sahil-lavingia-10-skills-20260530\contact-sheet.jpg`.
- 用户视频：`F:\000\xwechat_files\wxid_bq3n41o6t4o721_699b\msg\video\2026-05\7d88e97ac92dba18f29b33b5277cff48.mp4`.
- 用户截图：`F:\000\xwechat_files\wxid_bq3n41o6t4o721_699b\temp\RWTemp\2026-05\0af7c60bf5b2c143d160ba3441fcefa7\d6486782a550402d20bbf024342e6ccd.jpg`.

## 安全说明

- 未读取任何真实 `.env`、用户 token、生产配置或凭据文件。
- 只读取 `.env.example` 和公共 README/docs，以确认 mock 模式和配置边界。
- 未执行任何真实发送、账号登录、微信/飞书/Telegram/邮件/API 调用。
