# 2026 收费软件 → 免费/开源替代全景表
# Paid-to-Free / Open-Source Replacement Panorama

```ini
CATALOG_VERSION=2026-10-03-R1
ENTRY_COUNT=96
VERIFIED_AT=2026-10-03
DEFAULT_POLICY=FREE_AND_OSS_FIRST_WITH_VALID_GUARD
FREE_IS_NOT_OPEN_SOURCE=TRUE
AGENT_OPERABILITY_FIRST=YES
```

> 本表的“替代”是**任务级替代**，不是宣称像素级/功能表逐项 100% 克隆。真正迁移前必须把本任务 `DONE_WHEN`、文件格式、插件、协作、性能、安全和许可证做一次 Reality 验证。

## 等级

- **A直接**：常见核心工作流现在即可作为默认候选；不等于 100% 功能/格式逐项相同。
- **B强替代**：大部分目标可完成，但迁移、兼容或专业长尾有明显差异。
- **C组合/C局部**：需要组合多个项目，或只覆盖商业软件的一部分。
- **W重点观察**：AI 时代新路线/快速成熟中；暂不作为无条件生产默认。
- **A直接***：能力可直接替，但许可证不是严格开源，必须先过许可门。

## Agent 可操作等级

- **A**：已有 CLI / API / SDK / Headless / MCP 等直接控制面，优先给智能体。
- **A\***：正在形成明确的 Agent 控制面，当前版本与未来版需分开判断。
- **B**：可脚本化/插件化，或 GUI 自动化稳定可行。
- **C**：主要依赖人工 GUI，不应作为超级智能体首选。

## 全景表

| # | 类别 | 原收费/商业产品 | 免费/开源替代 | 替代等级 | 许可证类别 | 许可证 | Agent | 平台 | 关键判断 |
|---:|---|---|---|---|---|---|---|---|---|
| 1 | 视频/媒体 | 剪映 / CapCut | OpenCut | W重点观察 | OSS | MIT | A* | Web/Windows/macOS/Linux/移动规划 | 当前 Classic 可用；重写版规划 Editor API、MCP、Headless、脚本，AI Agent 潜力极高。 |
| 2 | 视频/媒体 | Adobe Premiere Pro | Kdenlive | A直接 | OSS | GPL | B | Windows/macOS/Linux | 成熟多轨、代理、字幕、语音转文字、嵌套时间线；常规剪辑可直接替换。 |
| 3 | 视频/媒体 | Adobe Premiere Pro | Shotcut | A直接 | OSS | GPL | B | Windows/macOS/Linux | 成熟跨平台编辑器，适合常规剪辑与转码工作流。 |
| 4 | 视频/媒体 | Premiere / Final Cut 常规剪辑 | OpenShot | B强替代 | OSS | GPLv3 | B | Windows/macOS/Linux | 易用；复杂大型工程能力弱于 Premiere。 |
| 5 | 视频/媒体 | 商业无损切割器 | LosslessCut | A直接 | OSS | GPL | A | Windows/macOS/Linux | 基于 FFmpeg 的快速无重编码剪切/合并，适合自动化。 |
| 6 | 视频/媒体 | Adobe Media Encoder | HandBrake | A直接 | OSS | GPLv2 | A | Windows/macOS/Linux | GUI + CLI，批量编码成熟。 |
| 7 | 视频/媒体 | Adobe Media Encoder / 商业转码器 | FFmpeg | A直接 | OSS | LGPL/GPL | A | 跨平台 | 媒体处理基础设施；CLI/API 生态极成熟。 |
| 8 | 视频/媒体 | Camtasia 录屏 | OBS Studio | A直接 | OSS | GPLv2 | B | Windows/macOS/Linux | 录屏/直播可直接替；后期编辑与 Kdenlive 等组合。 |
| 9 | 视频/媒体 | Snagit | ShareX | A直接 | OSS | GPLv3 | A | Windows | 截图、录屏、OCR/上传工作流，命令/自动化友好。 |
| 10 | 视频/媒体 | After Effects 合成 | Natron | C局部 | OSS | GPLv2 | B | Windows/macOS/Linux | 节点合成可替部分 AE/Nuke 工作流；动态图形生态不等价。 |
| 11 | 视频/媒体 | After Effects / 3D Motion | Blender | B强替代 | OSS | GPLv3 | A | Windows/macOS/Linux | 3D、合成、动画、VSE；Python API 适合 Agent。 |
| 12 | 图片/设计 | Adobe Photoshop | GIMP | A直接 | OSS | GPLv3+ | A | Windows/macOS/Linux | 通用位图编辑成熟；部分 PSD/Adobe 专属工作流需 Reality 验证。 |
| 13 | 图片/设计 | Photoshop 插画/绘画 | Krita | A直接 | OSS | GPLv3 | B | Windows/macOS/Linux | 绘画、笔刷、动画成熟。 |
| 14 | 图片/设计 | Adobe Illustrator | Inkscape | A直接 | OSS | GPLv2+ | A | Windows/macOS/Linux | SVG 原生；CLI 可自动导出/转换。 |
| 15 | 图片/设计 | Adobe Lightroom | darktable | A直接 | OSS | GPLv3+ | A | Windows/macOS/Linux | 成熟非破坏 RAW 工作流。 |
| 16 | 图片/设计 | Adobe Lightroom | RawTherapee | A直接 | OSS | GPLv3 | B | Windows/macOS/Linux | 成熟 RAW 显影，质量优先。 |
| 17 | 图片/设计 | Adobe Lightroom | RapidRAW | W重点观察 | OSS | AGPLv3 | A | Windows/macOS/Linux/Android | GPU、AI Mask、生成式编辑、Headless CLI；仍处快速开发期。 |
| 18 | 图片/设计 | Adobe InDesign | Scribus | B强替代 | OSS | GPL | B | Windows/macOS/Linux | 桌面排版成熟；Adobe 复杂兼容需验证。 |
| 19 | 图片/设计 | Figma | Penpot | A直接 | OSS | MPLv2 | A/B | Web/自托管 | 设计、原型、协作、自托管；适合作为开放设计系统。 |
| 20 | 图片/设计 | Miro | Excalidraw | A直接 | OSS | MIT | A/B | Web/自托管 | 白板/示意图简单高效，文件格式开放。 |
| 21 | 图片/设计 | Canva 常规设计 | Penpot + Inkscape + Scribus | C组合 | 多 OSS | MPL/GPL | B | 跨平台 | 组合覆盖 UI/矢量/排版；模板素材生态不等价。 |
| 22 | 办公/PDF/知识 | Microsoft Office | LibreOffice | A直接 | OSS | MPLv2 | B | Windows/macOS/Linux | Writer/Calc/Impress 成熟；复杂宏与极端格式兼容需测试。 |
| 23 | 办公/PDF/知识 | Microsoft Office | ONLYOFFICE Desktop Editors | A直接 | OSS | AGPLv3 | B | Windows/macOS/Linux | Office OOXML 兼容强，含 PDF 能力。 |
| 24 | 办公/PDF/知识 | Adobe Acrobat 页面操作 | PDF Arranger | A直接 | OSS | GPLv3 | B | Windows/Linux | 合并、拆分、旋转、重排等基础 PDF 工作。 |
| 25 | 办公/PDF/知识 | ABBYY FineReader / Acrobat OCR | OCRmyPDF | A直接 | OSS | MPLv2 | A | 跨平台/Windows 常用 WSL/Docker | 批量 OCR PDF，CLI 极适合 Agent。 |
| 26 | 办公/PDF/知识 | 商业 OCR 引擎 | Tesseract OCR | B强替代 | OSS | Apache-2.0 | A | 跨平台 | 通用 OCR 基础引擎；版面/手写等场景需专项模型。 |
| 27 | 办公/PDF/知识 | Notion | AppFlowy | A直接 | OSS | AGPLv3 | A/B | Windows/macOS/Linux/移动 | 文档、数据库、看板、自托管；开放替代路线成熟。 |
| 28 | 办公/PDF/知识 | Notion + Miro | AFFiNE Community Edition | B强替代 | OSS | MIT | B | 桌面/Web/自托管 | 文档+白板；生态成熟度继续观察。 |
| 29 | 办公/PDF/知识 | Confluence / Notion Wiki | Docmost | A直接 | 开源核心 | AGPLv3 core | A/B | Web/自托管 | 协作文档/Wiki；企业附加能力单独授权。 |
| 30 | 办公/PDF/知识 | Evernote / OneNote | Joplin | A直接 | OSS | AGPLv3 | A/B | 桌面/移动 | Markdown、同步、插件生态成熟。 |
| 31 | 办公/PDF/知识 | Confluence | BookStack | A直接 | OSS | MIT | A/B | Web/自托管 | 结构化知识库，部署简单。 |
| 32 | 办公/PDF/知识 | Confluence | Wiki.js | A直接 | OSS | AGPLv3 | A/B | Web/自托管 | 现代 Wiki，自托管成熟。 |
| 33 | 办公/PDF/知识 | EndNote / Mendeley | Zotero | A直接 | OSS | AGPLv3 | A | Windows/macOS/Linux | 文献管理成熟；Connector/API 可自动化。 |
| 34 | 办公/PDF/知识 | Grammarly | LanguageTool | B强替代 | 开源核心 | LGPL core | A | 跨平台/自托管 | 语法检查可自托管；高级商业模型功能不等价。 |
| 35 | 办公/PDF/知识 | DeepL / Google Translate 私有部署需求 | LibreTranslate | B强替代 | OSS | AGPLv3 | A | Web/自托管 | REST API 友好；翻译质量依语言对而异。 |
| 36 | 项目/协作 | Jira | OpenProject Community | A直接 | OSS/开放核心 | GPLv3 core | A | Web/自托管 | 项目/工单/路线图；社区版免费且有 API。 |
| 37 | 项目/协作 | Linear / Jira | Plane | B强替代 | OSS/开放核心 | AGPLv3 core | A | Web/自托管 | 现代 issue/project UX；企业能力需区分。 |
| 38 | 项目/协作 | Asana / Todoist / Trello | Vikunja | A直接 | OSS | AGPLv3+ | A | Web/自托管 | 任务、项目、看板，API 友好。 |
| 39 | 项目/协作 | Trello | Wekan | A直接 | OSS | MIT | A/B | Web/自托管 | Kanban 自托管成熟。 |
| 40 | 项目/协作 | Slack | Zulip | A直接 | OSS | Apache-2.0 | A | Web/桌面/移动/自托管 | 主题式聊天，API/机器人能力强。 |
| 41 | 项目/协作 | Slack / Teams | Mattermost Team Edition | B强替代 | 开放核心 | MIT Team Edition | A | Web/桌面/移动/自托管 | Team Edition 开源；企业模块另算。 |
| 42 | 项目/协作 | Zoom / Google Meet | Jitsi Meet | A直接 | OSS | Apache-2.0 | A | Web/自托管 | 视频会议、自托管与 API/嵌入能力成熟。 |
| 43 | 项目/协作 | Slack / Teams 部分工作流 | Matrix + Element | A直接 | OSS/开放核心 | 多开源许可证 | A | 跨平台/自托管 | 开放协议、联邦、自托管；选服务器实现时复核许可证。 |
| 44 | 项目/协作 | Calendly | Cal.diy | W重点观察 | OSS | MIT | A | Web/自托管 | 100% MIT 社区版；官方明确建议个人/非生产优先，生产需自行承担运维风险。 |
| 45 | 项目/协作 | Loom 异步视频 | OBS + PeerTube | C组合 | OSS | GPL/AGPL | A/B | 跨平台/自托管 | 录制+自托管视频发布组合，协作 UX 与 Loom 不完全相同。 |
| 46 | 存储/安全/远程 | Dropbox / Google Drive | Nextcloud | A直接 | OSS/开放核心 | AGPLv3 core | A | Web/桌面/移动/自托管 | 文件、日历、协作生态；API/WebDAV 丰富。 |
| 47 | 存储/安全/远程 | Dropbox 纯同步 | Syncthing | A直接 | OSS | MPLv2 | A | 跨平台 | P2P 文件同步，无中心云订阅。 |
| 48 | 存储/安全/远程 | Google Photos / iCloud Photos | Immich | A直接 | OSS | AGPLv3 | A | Web/移动/自托管 | 照片备份、搜索、相册；活跃项目。 |
| 49 | 存储/安全/远程 | 1Password / LastPass | Bitwarden 开源核心 | A直接 | 开放核心 | GPL/AGPL core | A | 跨平台/自托管 | 核心客户端/服务端开放；企业模块另授权。 |
| 50 | 存储/安全/远程 | 1Password / LastPass 自托管 | Vaultwarden | A直接 | OSS | AGPLv3 | A | 自托管 | 轻量 Bitwarden-compatible server；资源占用低。 |
| 51 | 存储/安全/远程 | TeamViewer / AnyDesk | RustDesk | A直接 | OSS/开放核心 | AGPLv3 core | B | Windows/macOS/Linux/移动 | 远程桌面、自建服务器；适合 Agent 辅助控制。 |
| 52 | 存储/安全/远程 | MobaXterm / Termius | Tabby | A直接 | OSS | MIT | B | Windows/macOS/Linux | SSH/Serial/终端，插件化。 |
| 53 | 存储/安全/远程 | WeTransfer | Pingvin Share X | B强替代 | OSS（部署前复核） | 项目 LICENSE | A | Web/自托管 | 原 Pingvin Share 已归档；官方指向活跃 fork Pingvin Share X，部署前检查最新安全公告。 |
| 54 | 自动化/开发/数据 | Zapier / Make | Activepieces Community | A直接 | 开放核心 | MIT core | A | Web/自托管 | 自动化工作流，AI/Connector 友好。 |
| 55 | 自动化/开发/数据 | Zapier / Make / 内部任务平台 | Windmill 源码构建 | A直接 | OSS/开放核心 | AGPLv3 + Apache-2.0 | A | Web/自托管 | 源码构建核心可开源使用；官方 Community binary 含专有部分，需按使用方式核对。 |
| 56 | 自动化/开发/数据 | Zapier / Make | n8n | A直接* | 源码可见 | Sustainable Use License | A | Web/自托管 | 非常强但不是严格 OSI 开源；内部使用通常可行，商业托管/嵌入先核许可证。 |
| 57 | 自动化/开发/数据 | Retool | Appsmith Community | A直接 | 开放核心 | Apache-2.0 core | A/B | Web/自托管 | 内部工具低代码构建。 |
| 58 | 自动化/开发/数据 | Retool | ToolJet Community | A直接 | 开放核心 | AGPLv3 core | A/B | Web/自托管 | 内部工具/数据库 UI。 |
| 59 | 自动化/开发/数据 | Airtable | Baserow Open Source Edition | A直接 | 开放核心 | MIT core | A | Web/自托管 | 表格数据库；premium/enterprise 目录另授权。 |
| 60 | 自动化/开发/数据 | Airtable | NocoDB | A直接* | 源码可见 | Sustainable Use License | A | Web/自托管 | 2026 已由 AGPL 转 SUL；不能再作为严格 OSS 宣传。 |
| 61 | 自动化/开发/数据 | Typeform / SurveyMonkey | Formbricks | A直接 | OSS/开放核心 | AGPLv3 core | A | Web/自托管 | 调查/体验管理，自托管与 API 友好。 |
| 62 | 自动化/开发/数据 | Intercom / Zendesk | Chatwoot | A直接 | 开放核心 | MIT core | A | Web/自托管 | 客服/全渠道收件箱，API 丰富。 |
| 63 | 自动化/开发/数据 | Google Analytics | Matomo | A直接 | OSS/开放核心 | GPLv3 core | A | Web/自托管 | 成熟分析平台，数据自主。 |
| 64 | 自动化/开发/数据 | Google Analytics | Plausible Community Edition | A直接 | OSS | AGPLv3 | A | Web/自托管 | 轻量隐私分析。 |
| 65 | 自动化/开发/数据 | Postman | Bruno | A直接 | OSS | MIT | A | Windows/macOS/Linux | Git-native API Client，CLI/集合适合 Agent。 |
| 66 | 自动化/开发/数据 | Postman | Hoppscotch | A直接 | OSS | MIT | A | Web/桌面/自托管 | REST/GraphQL/WebSocket 等。 |
| 67 | 自动化/开发/数据 | DataGrip / TablePlus | DBeaver Community | A直接 | OSS | Apache-2.0 | A/B | Windows/macOS/Linux | 数据库客户端成熟。 |
| 68 | 自动化/开发/数据 | Firebase | Supabase | A直接 | OSS/开放核心 | Apache-2.0 core | A | 云/自托管 | Postgres、Auth、Storage、Realtime；API-first。 |
| 69 | 自动化/开发/数据 | Firebase | Appwrite | A直接 | OSS | BSD-3-Clause | A | 云/自托管 | Auth/DB/Storage/Functions，SDK/API 完整。 |
| 70 | 自动化/开发/数据 | Auth0 / Okta | Keycloak | A直接 | OSS | Apache-2.0 | A | Web/自托管 | IAM/SSO/OIDC/SAML 成熟。 |
| 71 | 自动化/开发/数据 | Auth0 / Okta | authentik | A直接 | 开放核心 | 开源核心 | A | Web/自托管 | IAM/SSO，自托管友好；企业能力另算。 |
| 72 | 自动化/开发/数据 | Heroku / Render / Railway | Coolify | A直接 | OSS | Apache-2.0 | A | 自托管 | PaaS、自建部署/数据库/服务管理。 |
| 73 | 自动化/开发/数据 | Shopify Headless / 商业电商后端 | Medusa Core | B强替代 | 开放核心 | MIT core | A | 自托管/云 | Headless commerce；生态/支付/运营插件需按项目评估。 |
| 74 | 自动化/开发/数据 | Webflow | Webstudio | W重点观察 | OSS/混合 | AGPLv3+ core | B | Web/自托管 | 开放 Webflow 路线；个别可选包为专有，部署前核对。 |
| 75 | 自动化/开发/数据 | Mailchimp 基础 Newsletter | listmonk | A直接 | OSS | AGPLv3 | A | Web/自托管 | 高性能邮件列表/Newsletter；CLI/API 友好。 |
| 76 | 自动化/开发/数据 | Bitly / Rebrandly | Shlink | A直接 | OSS | MIT | A | Web/自托管 | 短链、统计、REST API。 |
| 77 | CAD/3D/科学 | AutoCAD 2D | LibreCAD | A直接 | OSS | GPLv2 | B | Windows/macOS/Linux | 2D CAD 成熟。 |
| 78 | CAD/3D/科学 | AutoCAD / SolidWorks 部分 3D | FreeCAD | B强替代 | OSS | LGPLv2+ | A/B | Windows/macOS/Linux | 参数化 3D CAD；行业插件与复杂装配需验证。 |
| 79 | CAD/3D/科学 | Maya / 3ds Max / Cinema 4D / ZBrush 多数工作流 | Blender | A直接 | OSS | GPLv3 | A | Windows/macOS/Linux | 建模、雕刻、渲染、动画、合成；Python API 强。 |
| 80 | CAD/3D/科学 | Unity | Godot | A直接 | OSS | MIT | A | Windows/macOS/Linux/Web/移动 | 2D/3D 游戏引擎，无版税，脚本/CLI 友好。 |
| 81 | CAD/3D/科学 | ArcGIS | QGIS | A直接 | OSS | GPLv2+ | A | Windows/macOS/Linux | GIS 专业能力成熟，Python/Processing 自动化强。 |
| 82 | CAD/3D/科学 | MATLAB | GNU Octave | A直接 | OSS | GPL | A | Windows/macOS/Linux | 数值计算/MATLAB 兼容路线成熟。 |
| 83 | CAD/3D/科学 | Mathematica / Maple | SageMath | A直接 | OSS | GPL | A | 跨平台/Web | 数学系统整合大量成熟开源库，脚本化强。 |
| 84 | CAD/3D/科学 | SPSS | GNU PSPP | A直接 | OSS | GPL | A | Windows/macOS/Linux | 经典统计分析免费替代。 |
| 85 | CAD/3D/科学 | SPSS / Stata 常用 GUI 统计 | jamovi | A直接 | OSS | 开源 | A/B | Windows/macOS/Linux | R 驱动、GUI 友好。 |
| 86 | CAD/3D/科学 | Tableau / Power BI 自托管 BI | Apache Superset | B强替代 | OSS | Apache-2.0 | A | Web/自托管 | BI/可视化，SQL/API/部署自动化强。 |
| 87 | CAD/3D/科学 | Tableau / Power BI 轻量 BI | Metabase OSS | B强替代 | 开放核心 | AGPL core | A | Web/自托管 | 低门槛分析/仪表板；企业功能另算。 |
| 88 | 音频 | Adobe Audition | Audacity | A直接 | OSS | GPL | B | Windows/macOS/Linux | 波形编辑/降噪/插件成熟。 |
| 89 | 音频 | Pro Tools | Ardour | A直接 | OSS | GPL | B | Windows/macOS/Linux | 录音、编辑、混音完整 DAW。 |
| 90 | 音频 | FL Studio | LMMS | B强替代 | OSS | GPLv2+ | B | Windows/macOS/Linux | 编曲、MIDI、合成器；商业插件生态不同。 |
| 91 | 音频 | Serato DJ / Traktor | Mixxx | A直接 | OSS | GPL | B | Windows/macOS/Linux | DJ、控制器、BPM/同步成熟。 |
| 92 | 系统工具 | WinRAR / WinZip | 7-Zip | A直接 | OSS | LGPL/BSD | A | Windows | 压缩/解压成熟，CLI 极适合 Agent。 |
| 93 | 系统工具 | WinZip / PowerArchiver | PeaZip | A直接 | OSS | LGPLv3 | A/B | Windows/Linux | 图形化归档管理，多格式。 |
| 94 | 系统工具 | CCleaner | BleachBit | A直接 | OSS | GPLv3 | A | Windows/Linux | 清理缓存/临时文件，CLI 可自动化。 |
| 95 | 系统工具 | Acronis / Macrium 部分磁盘镜像 | Clonezilla | B强替代 | OSS | GPL | B | Live Linux | 块级克隆/备份成熟；交互体验偏工程化。 |
| 96 | 系统工具 | Acronis / Macrium 恢复镜像 | Rescuezilla | A直接 | OSS | GPLv3 | B | Live Linux | Clonezilla 兼容的易用恢复 GUI。 |

## 强制边界：免费 ≠ 开源

以下项目很有价值，但不能混写成“严格开源”：

| 项目 | 当前分类 | 使用规则 |
|---|---|---|
| Photon Studio | 免费软件 / 未验证为严格 OSS | 当前可确认个人与商业使用免费；未找到足够证据证明源码按开源许可证发布，因此只进入“免费替代观察池”，不标 OSS。 |
| n8n | Source-available / Fair-code | Sustainable Use License；内部自动化很强，但商业托管、嵌入、代客户持有凭据等先过许可证门。 |
| NocoDB | Source-available | 2026 已迁移到 Sustainable Use License；不再标成严格 OSS。 |
| Stirling PDF | 混合许可 / 开放核心边界需逐版本核对 | 不能把整个产品笼统写成 MIT/严格 OSS；生产采用前读当前 LICENSE 与 restricted/enterprise 部分。 |
| Cal.com 主产品 | 商业/开放边界已变化 | 若要完全 MIT 社区路线，检查 Cal.diy；Cal.diy 当前官方又明确提示优先个人/非生产。 |
| Obsidian | 免费可用但闭源 | 可作为免费工具，但不进入严格 OSS 默认池。 |
| Pingvin Share（原项目） | 已归档 | 不再作为默认；候选迁移到 Pingvin Share X，并检查其最新安全公告。 |

## “未来半年最值得盯”的 AI 原生替代

1. **OpenCut**：核心价值不是“又一个剪辑器”，而是正在把 Editor API、MCP Server、Headless、脚本放进同一 Rust 核心；一旦重写版稳定，最适合超级智能体直接剪视频。
2. **RapidRAW**：已经出现 Headless CLI 批处理，叠加 GPU、AI Mask、生成式编辑；Agent 操作比传统 Lightroom GUI 更自然，但项目自己仍声明处于快速开发期。
3. **Webstudio**：开放 Webflow 路线，适合设计到网站的自动化，但许可/可选专有包与生态成熟度需持续跟踪。
4. **Cal.diy**：完整 MIT 社区路线很有价值，但当前生产运维风险提示明确，先观察稳定性。
5. **Photon Studio**：作为“免费 Photoshop 类”观察对象很有价值，但在许可证可验证前不进入严格 OSS 生产默认。

## 默认选择逻辑

```text
识别正在付费/准备购买的软件
→ 定义本任务 DONE_WHEN
→ 查本表
→ 先过滤许可证与平台硬约束
→ 优先 A直接 + Agent=A
→ 再看 B强替代
→ W重点观察不得直接替生产关键链路
→ 做最小代表性 Reality
→ PASS 才迁移
→ FAIL 则保留原收费工具或换下一成熟候选
```

