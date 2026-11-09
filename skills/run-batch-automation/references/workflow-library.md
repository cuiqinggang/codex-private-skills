> V1.3补充：本页保留原分类和来源；最新范围、版本及导入条件以 R87-Catalog-Coverage.json 和 catalog-sources.json 为准，未配置项不代表本机可运行。

# 公共自动化流程分类速览

首批32个具体流程，8个已有条目的业务种类，5个平台；另有7个上游目录。只读索引，未启动这些外部流程。
每条的依赖、配置、原导入入口及证据界限用 `query.py --id <ID>` 取完整卡。没有下载地址时保留原模板入口。

## 分类目录

- 数据与表格：5条
- 文档与知识库：4条
- 邮件与客服：5条
- 内容与营销：4条
- 监测与运维：4条
- 文件与备份：5条
- 销售与CRM：2条
- 开发与部署：3条

## 数据与表格

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-694 | [Google表格追加、查找与更新 / Transform data in Google Sheets](https://n8n.io/workflows/694-transform-data-in-google-sheets/) | n8n | 把输入数据追加到表格，按值查找行、按键更新，再读取指定范围；可拆成单项表格流程。 |
| n8n-14205 | [Google表格逐批调用REST API并限流 / Enrich Google Sheets rows via any REST API in rate-limited batches](https://n8n.io/workflows/14205-enrich-google-sheets-rows-via-any-rest-api-in-rate-limited-batches/) | n8n | 读取整表后分批逐行调用REST API，把成功结果回填表格并记录错误。 |
| make-5893 | [Webhook数据写入Google表格 / Add webhook data to a Google Sheet](https://www.make.com/templates/5893-add-data-to-a-google-sheet-received-from-a-webhook) | Make | 接收入站Webhook，将数据作为新行写入Google Sheets。 |
| ap-55hreusuhp0srjtr3kgmn | [收据提取分类入表 / Expense Tracker](https://cloud.activepieces.com/templates/55hrEuSuHp0sRJTR3kgmn) | Activepieces | 收集收据，提取并分类费用，写入表格。 |
| dify-sentiment-analysis | [文本情感分析 / Sentiment Analysis](https://marketplace.dify.ai/template/langgenius/dd193c4c-622d-4b43-b0cc-0cda47e734d0) | Dify | 对文本做情感分析，按整体或多维模式返回分类及分数JSON。 |

### n8n-694

原流程：[Google表格追加、查找与更新 / Transform data in Google Sheets](https://n8n.io/workflows/694-transform-data-in-google-sheets/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-14205

原流程：[Google表格逐批调用REST API并限流 / Enrich Google Sheets rows via any REST API in rate-limited batches](https://n8n.io/workflows/14205-enrich-google-sheets-rows-via-any-rest-api-in-rate-limited-batches/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### make-5893

原流程：[Webhook数据写入Google表格 / Add webhook data to a Google Sheet](https://www.make.com/templates/5893-add-data-to-a-google-sheet-received-from-a-webhook)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### ap-55hreusuhp0srjtr3kgmn

原流程：[收据提取分类入表 / Expense Tracker](https://cloud.activepieces.com/templates/55hrEuSuHp0sRJTR3kgmn)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### dify-sentiment-analysis

原流程：[文本情感分析 / Sentiment Analysis](https://marketplace.dify.ai/template/langgenius/dd193c4c-622d-4b43-b0cc-0cda47e734d0)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 文档与知识库

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-9061 | [从Drive提取清理PDF数据 / 📁 Extract and clean PDF data from Google Drive](https://n8n.io/workflows/9061-extract-and-clean-pdf-data-from-google-drive/) | n8n | 从指定Google Drive文件夹查找并下载PDF，提取文本后用Code节点清洗成JSON。 |
| n8n-11049 | [以Claude技能生成文档并上传Drive / Generate professional documents with Claude AI skills🤹🤖 & upload to Google Drive](https://n8n.io/workflows/11049-generate-professional-documents-with-claude-ai-skills-and-upload-to-google-drive/) | n8n | 表单输入提示词和文件类型，调用Anthropic文档能力生成文件，再下载并上传Drive。 |
| dify-doc-extractor-summary | [文档提取与摘要 / Doc Extractor: AI Summarizer](https://marketplace.dify.ai/template/langgenius/008cedde-aa22-4d9b-8628-5ef272f5ecba) | Dify | 上传PDF、Word、TXT等文档，提取正文后交给LLM生成摘要。 |
| dify-multi-question-rag | [多问题知识库检索 / Multi-Question RAG Workflow](https://marketplace.dify.ai/template/langgenius/d2d2ae92-d95b-4d55-b343-be411c3147d3) | Dify | 从输入文本提取多个问题，逐问题检索知识库，生成带引用的回答并整理输出。 |

### n8n-9061

原流程：[从Drive提取清理PDF数据 / 📁 Extract and clean PDF data from Google Drive](https://n8n.io/workflows/9061-extract-and-clean-pdf-data-from-google-drive/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-11049

原流程：[以Claude技能生成文档并上传Drive / Generate professional documents with Claude AI skills🤹🤖 & upload to Google Drive](https://n8n.io/workflows/11049-generate-professional-documents-with-claude-ai-skills-and-upload-to-google-drive/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### dify-doc-extractor-summary

原流程：[文档提取与摘要 / Doc Extractor: AI Summarizer](https://marketplace.dify.ai/template/langgenius/008cedde-aa22-4d9b-8628-5ef272f5ecba)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### dify-multi-question-rag

原流程：[多问题知识库检索 / Multi-Question RAG Workflow](https://marketplace.dify.ai/template/langgenius/d2d2ae92-d95b-4d55-b343-be411c3147d3)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 邮件与客服

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-20297 | [Gmail回复与跟进草稿审批 / Draft and approve Gmail replies and follow-ups with OpenAI](https://n8n.io/workflows/20297-draft-and-approve-gmail-replies-and-follow-ups-with-openai/) | n8n | 识别新未读邮件，依据预置业务事实生成回复草稿，发送给负责人审批后才向客户回复。 |
| n8n-9414 | [Gmail知识库客户支持 / AI-powered Gmail customer support with OpenRouter & Pinecone knowledge base](https://n8n.io/workflows/9414-ai-powered-gmail-customer-support-with-openrouter-and-pinecone-knowledge-base/) | n8n | 把Gmail来信分类，针对客服邮件检索知识库生成并自动发送答复。 |
| make-5770 | [表格新增行触发Gmail邮件 / Send a Gmail email from a new Google Sheets row](https://www.make.com/templates/5770-send-a-gmail-email-from-a-new-google-sheets-row) | Make | 监视新增表格行，以收件地址、主题和正文列构建Gmail邮件。 |
| ap-n9cz9fltxz3z8zd8ixoeg | [邮件分类记录并分流 / Email Categorization](https://cloud.activepieces.com/templates/n9cZ9FlTxZ3z8Zd8IxOeg) | Activepieces | 接收邮件后AI分类，记录Excel并按类别转发。 |
| ap-xfhcpeyazf52mdzfwtb3l | [HubSpot工单分类通知 / Customer Support Ticketing](https://cloud.activepieces.com/templates/XFHCpEYazF52mDzfwTB3L) | Activepieces | 新工单经AI整理分类，通过路由发送Slack通知。 |

### n8n-20297

原流程：[Gmail回复与跟进草稿审批 / Draft and approve Gmail replies and follow-ups with OpenAI](https://n8n.io/workflows/20297-draft-and-approve-gmail-replies-and-follow-ups-with-openai/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-9414

原流程：[Gmail知识库客户支持 / AI-powered Gmail customer support with OpenRouter & Pinecone knowledge base](https://n8n.io/workflows/9414-ai-powered-gmail-customer-support-with-openrouter-and-pinecone-knowledge-base/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### make-5770

原流程：[表格新增行触发Gmail邮件 / Send a Gmail email from a new Google Sheets row](https://www.make.com/templates/5770-send-a-gmail-email-from-a-new-google-sheets-row)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### ap-n9cz9fltxz3z8zd8ixoeg

原流程：[邮件分类记录并分流 / Email Categorization](https://cloud.activepieces.com/templates/n9cZ9FlTxZ3z8Zd8IxOeg)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### ap-xfhcpeyazf52mdzfwtb3l

原流程：[HubSpot工单分类通知 / Customer Support Ticketing](https://cloud.activepieces.com/templates/XFHCpEYazF52mDzfwTB3L)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 内容与营销

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-19893 | [客户评论生成多渠道内容 / Turn customer reviews into multi-channel content with OpenAI, Gmail, and Google Sheets](https://n8n.io/workflows/19893-turn-customer-reviews-into-multi-channel-content-with-openai-gmail-and-google-sheets/) | n8n | 从表单收集客户评价并评分，把达标评价改写成多渠道文案包，以邮件交付并记表。 |
| n8n-8553 | [生成并发布社媒内容 / Auto-generate & post social media content with GPT-4, Notion & Instagram API](https://n8n.io/workflows/8553-auto-generate-and-post-social-media-content-with-gpt-4-notion-and-instagram-api/) | n8n | Webhook接收素材，在Notion集中保存，生成渠道文案和图片URL，并通过Instagram API发布。 |
| make-12103 | [监测网站内容并生成社媒文案 / Summarize website content and create social media posts with ChatGPT and Browse AI](https://www.make.com/templates/12103-summarize-content-with-chatgpt-from-a-monitored-site-using-browse-ai-and-create-a-social-media-posts) | Make | 使用Browse AI监测网站内容，由ChatGPT生成摘要和社交媒体文案。 |
| ap-j0phfpzhfpqueenj2hdvg | [RSS内容改写入库 / Content Repurposing](https://cloud.activepieces.com/templates/J0PHFpZHFPqUEenj2hDVg) | Activepieces | RSS内容经研究和改写，生成多种社媒草稿并存入Airtable。 |

### n8n-19893

原流程：[客户评论生成多渠道内容 / Turn customer reviews into multi-channel content with OpenAI, Gmail, and Google Sheets](https://n8n.io/workflows/19893-turn-customer-reviews-into-multi-channel-content-with-openai-gmail-and-google-sheets/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-8553

原流程：[生成并发布社媒内容 / Auto-generate & post social media content with GPT-4, Notion & Instagram API](https://n8n.io/workflows/8553-auto-generate-and-post-social-media-content-with-gpt-4-notion-and-instagram-api/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### make-12103

原流程：[监测网站内容并生成社媒文案 / Summarize website content and create social media posts with ChatGPT and Browse AI](https://www.make.com/templates/12103-summarize-content-with-chatgpt-from-a-monitored-site-using-browse-ai-and-create-a-social-media-posts)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### ap-j0phfpzhfpqueenj2hdvg

原流程：[RSS内容改写入库 / Content Repurposing](https://cloud.activepieces.com/templates/J0PHFpZHFPqUEenj2hDVg)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 监测与运维

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-19956 | [网站可用性与事件监测 / Monitor website uptime and incidents with Google Sheets, Slack and Gmail](https://n8n.io/workflows/19956-monitor-website-uptime-and-incidents-with-google-sheets-slack-and-gmail/) | n8n | 定时检查站点状态和时延，追踪连续失败及恢复，把事件写表并发送提醒和日报。 |
| n8n-3366 | [网页变化检测与提醒 / Webpage change detection & alerts with Google Suite and hash tracking](https://n8n.io/workflows/3366-webpage-change-detection-and-alerts-with-google-suite-and-hash-tracking/) | n8n | 定时抓取指定网页片段，对内容计算hash，只在遇到未见内容时归档、记表并通知。 |
| dify-website-health-guard | [网站健康检查 / Trigger: Website Health Guard](https://marketplace.dify.ai/template/langgenius/8d78751f-8469-446e-9bd6-c19b52e334dc) | Dify | 按计划向网站发起GET请求，发现HTTP错误时由LLM说明问题并输出健康报告。 |
| github-stale-maintenance | [Mark stale issues and pull requests](https://github.com/actions/starter-workflows/blob/main/automation/stale.yml) | GitHub Actions | 每天识别久未活动的Issue/PR，发布提示、加标签，并按action配置关闭。 |

### n8n-19956

原流程：[网站可用性与事件监测 / Monitor website uptime and incidents with Google Sheets, Slack and Gmail](https://n8n.io/workflows/19956-monitor-website-uptime-and-incidents-with-google-sheets-slack-and-gmail/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-3366

原流程：[网页变化检测与提醒 / Webpage change detection & alerts with Google Suite and hash tracking](https://n8n.io/workflows/3366-webpage-change-detection-and-alerts-with-google-suite-and-hash-tracking/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### dify-website-health-guard

原流程：[网站健康检查 / Trigger: Website Health Guard](https://marketplace.dify.ai/template/langgenius/8d78751f-8469-446e-9bd6-c19b52e334dc)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### github-stale-maintenance

原流程：[Mark stale issues and pull requests](https://github.com/actions/starter-workflows/blob/main/automation/stale.yml)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 文件与备份

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| n8n-6469 | [定时备份Google表格至Drive / Scheduled Google Sheets data backup to Google Drive](https://n8n.io/workflows/6469-scheduled-google-sheets-data-backup-to-google-drive/) | n8n | 按计划读取指定表页数据，以带日期文件名的CSV或XLSX保存到Drive备份文件夹。 |
| n8n-18512 | [导出工作流并备份GitHub / Back up workflows to GitHub with deterministic JSON exports](https://n8n.io/workflows/18512-back-up-workflows-to-github-with-deterministic-json-exports/) | n8n | 每天通过n8n API导出工作流，规范化JSON后与GitHub比较，仅在内容变化时提交备份。 |
| make-6030 | [Dropbox新文件转存Google Drive / Transfer files from Dropbox to Google Drive](https://www.make.com/templates/6030-transfer-files-from-dropbox-to-google-drive) | Make | 监视指定Dropbox目录的新上传文件，读取后上传到指定Drive目录。 |
| make-83 | [邮件附件原格式归档Drive / Save email attachments to Google Drive](https://www.make.com/templates/83-save-email-attachments-to-google-drive) | Make | 有附件的邮件到达后，将附件按原格式保存至指定Google Drive目录。 |
| n8n-4243 | [Gmail指定发件人附件备份Drive / Gmail attachment backup to Google Drive](https://n8n.io/workflows/4243-gmail-attachment-backup-to-google-drive/) | n8n | 轮询Gmail指定发件人的新邮件，将所有附件分别上传Drive并带时间标识。 |

### n8n-6469

原流程：[定时备份Google表格至Drive / Scheduled Google Sheets data backup to Google Drive](https://n8n.io/workflows/6469-scheduled-google-sheets-data-backup-to-google-drive/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-18512

原流程：[导出工作流并备份GitHub / Back up workflows to GitHub with deterministic JSON exports](https://n8n.io/workflows/18512-back-up-workflows-to-github-with-deterministic-json-exports/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### make-6030

原流程：[Dropbox新文件转存Google Drive / Transfer files from Dropbox to Google Drive](https://www.make.com/templates/6030-transfer-files-from-dropbox-to-google-drive)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### make-83

原流程：[邮件附件原格式归档Drive / Save email attachments to Google Drive](https://www.make.com/templates/83-save-email-attachments-to-google-drive)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### n8n-4243

原流程：[Gmail指定发件人附件备份Drive / Gmail attachment backup to Google Drive](https://n8n.io/workflows/4243-gmail-attachment-backup-to-google-drive/)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 销售与CRM

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| make-5972 | [HubSpot新交易通知Slack / Send a Slack message from a new HubSpot CRM deal](https://www.make.com/templates/5972-send-a-slack-message-from-a-new-hubspot-crm-deal) | Make | 新建HubSpot交易后，把交易信息发送给Slack频道或用户。 |
| ap-pjrmodiziwtcew41mmti9 | [定时线索培育邮件 / Lead Nurturing](https://cloud.activepieces.com/templates/pJRMODiZiwtCEw41MMTI9) | Activepieces | 定时选取表格线索与资源，生成个性化培育邮件。 |

### make-5972

原流程：[HubSpot新交易通知Slack / Send a Slack message from a new HubSpot CRM deal](https://www.make.com/templates/5972-send-a-slack-message-from-a-new-hubspot-crm-deal)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### ap-pjrmodiziwtcew41mmti9

原流程：[定时线索培育邮件 / Lead Nurturing](https://cloud.activepieces.com/templates/pJRMODiZiwtCEw41MMTI9)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 开发与部署

| 流程ID | 原流程 | 平台 | 用途 |
|---|---|---|---|
| github-nodejs-ci | [Node.js CI](https://github.com/actions/starter-workflows/blob/main/ci/node.js.yml) | GitHub Actions | 在push及pull_request时安装npm依赖、构建并跨Node版本运行测试。 |
| github-python-application | [Python application](https://github.com/actions/starter-workflows/blob/main/ci/python-app.yml) | GitHub Actions | 安装Python依赖，用flake8检查并运行pytest。 |
| github-static-pages | [Deploy static content to Pages](https://github.com/actions/starter-workflows/blob/main/pages/static.yml) | GitHub Actions | push或手动触发后，把仓库静态文件上传并部署至GitHub Pages。 |

### github-nodejs-ci

原流程：[Node.js CI](https://github.com/actions/starter-workflows/blob/main/ci/node.js.yml)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### github-python-application

原流程：[Python application](https://github.com/actions/starter-workflows/blob/main/ci/python-app.yml)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

### github-static-pages

原流程：[Deploy static content to Pages](https://github.com/actions/starter-workflows/blob/main/pages/static.yml)。
按ID取完整配置卡；当前为公开文档/源码核实，目标环境未配置运行。

## 其他分类与继续查找

“日程与通知”保留为稳定分类；本批相关通知是其他主分类流程的步骤，未另造重复卡。独立日程任务从上游目录继续检索。
上游七家入口及导入说明见 [catalog-sources.json](catalog-sources.json)。本地辅助批处理见 [existing-recipes.md](existing-recipes.md) 与 [official-recipes.md](official-recipes.md)。
