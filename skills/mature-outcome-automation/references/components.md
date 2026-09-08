# 组件绑定清单

核查日期：2026-09-08。它是现成技能的调用清单，不是重新开发清单。

| 名称 | 精确识别信息 | 本轮证据状态 |
|---|---|---|
| AI 资源总调度 2.0 核心精简版 | 用户本轮指定；ai-resource-orchestrator 作为检索线索 | 用户确认已存在；当前云端未读取到目标机正文，具体入口/版本/内置门禁接法由本地首次绑定读取 |
| 专用 AI 浏览器成熟封装技能包 | 用户本轮指定；专用 AI 浏览器、Playwright 原生 AI 浏览器、封装/封袋/封存作为检索别名 | 用户确认已有路线；实际 name 和启动/重连/发送/读取入口本轮未读，不虚构英文包名，不换成另一浏览器技能 |
| find-skills | 当前可读技能 name=find-skills；原始来源 vercel-labs/skills 的 skills/find-skills | 本轮已读完整正文，官方目录和仓库已核对；本地是否可直接调用仍以运行环境为准 |
| command-pack-quality-gate | 当前已读技能，版本 1.1.2 | 命令编写端使用；原调度已有效调用时复用结果 |
| ECC | 当前已读识别名 ecc-four-role-loop-orchestration；正文标记2.1.0 | 用户提到的3.1不据此确认；按目标机实际安装版读取 |

首次只读目标机既有技能目录和索引，按 name、中文标题和别名找上表组件；保留实际路径、版本及相关接口。复用已有绑定记录；不要每轮全盘盘点。发现多个版本时使用用户指定的正式入口；不能仅取名字相似的历史包替换当前封装。

## find-skills：本流程的具体用途

原始来源：
- [官方技能页](https://skills.sh/vercel-labs/skills/find-skills)
- [原始技能正文](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md)
- [Skills CLI 原仓库](https://github.com/vercel-labs/skills)

它负责按任务发现专业技能。优先复用本地已安装版本；不为了搜索而重新安装。
原技能提供 npx skills find <任务关键词> 和 skills.sh 目录。按本包专用联网入口规则选择可用方式，不擅自改变网络环境。
安装数与来源可用于候选筛选，但不证明适用或实测通过；选择前读取原文及必要依赖。
用户已经要求自动推进：在授权范围内自动选择和调用必要技能，不每次列选项等待批准。若需要安装，沿目标环境已有技能安装流程，保留原成熟配置；范围外或真实权限仍遵从宿主约束。
其默认“没有技能就自行实现”的建议在本流程不采用；改查解决同一核心问题的成熟原项目或官方办法。

mature-capability-growth-radar（成熟能力增长雷达）是另一已存在技能，面向组合能力升级及收益验证；它不是本流程每个任务的搜索前置条件，当前使用轻量的 find-skills 即可。

## Reasonix 模型与资源控制（0.3.0新增）

用户截图已确认工具为Reasonix：模型菜单可见deepseek-v4-flash、deepseek-v4-pro等，力度菜单可见auto、disabled、low、high、max。它们是界面快照，不是本轮实际服务能力或调用成功证据。
绑定时新增记录：当前Reasonix版本、当前可用模型ID/供应商、每模型允许的力度、选定模型/力度的会话或请求入口、工具/技能作用域、智能体分派与回执入口。
当前界面的“询问／自动／Yolo”属于权限/操作模式，不与推理力度混用，不为本次资源测试切换该模式。
读取 [reasonix-resource-control.md](reasonix-resource-control.md) 落实具体能力，复用已有Reasonix适配器，不重建UI或模型路由服务。
