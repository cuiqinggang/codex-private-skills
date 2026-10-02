# 长期记忆超级虚拟人｜按需工具索引 v0.1.1

原则：**能力全、入口轻、按需加载。**

## 当前能力索引

| 任务类型 | 首选能力 | 已有备选 / 专项 |
|---|---|---|
| 公共互联网信息 | GPT Web / Search | 专用 Browser |
| 网页交互 | Browser / DOM / Playwright | `screenshot-recognize-operate-browser` / Computer-use 类执行面（可用时） |
| 高可靠截图式浏览器操作 | Playwright / DOM 不可靠时启用 | `screenshot-browser-100-percent-route v2.0.0` |
| 虚拟鼠标/键盘 | `virtual-mouse-keyboard-demo` | Selenium 隔离 Chrome / pywinauto / 经授权真实 Windows 输入 |
| Windows 文件/命令 | Desktop Commander Remote | GitHub Windows self-hosted runner |
| 大型编码/仓库工程 | GPT 直达或 Codex（按 T_VALID） | Reasonix / 其他代码执行器 |
| 复杂长流程 | TASK_CONTRACT + GPT | ECC v3.1.1 / Reasonix 集成路线 |
| 多工具重工程/生态执行 | 最小必要工具组合 | `C:\AI\DeerFlow-SuperEmployee-Station` 成熟生态站按需唤醒 |
| 成熟 Skill 发现 | 本地/私库技能索引 + 按需搜索 | 公共成熟 Skill / 官方方案 / 网络资料 |
| GitHub | GitHub Connector / gh | Windows runner |
| 邮件/日历/云文档 | 对应 Connector | 浏览器 |
| 图像 | 图像生成/编辑工具 | 专项视觉模型 |
| 视频 | 专项视频工具 | 本地/云端成熟流水线 |
| 极低延迟概率/路径类专项 | 任务匹配时调用 | `jev-probability-engine-p0` 等既有专项技能 |
| 长任务恢复 | TASK_CONTRACT + Checkpoint + 项目权威状态 | ECC v3.1.1 / 独立强备份 |
| GPT 不可用 | 独立强备份 | Reasonix / DeepSeek；页面租约继续保留，主脑恢复后再 reconcile |

## 轻入口规则

启动时只需要知道：

```text
任务是什么？
需要观察哪个现实域？
需要哪类能力？
```

随后只读取对应索引项和必要 Skill。

**不要：**
- 把数百个 Skill 全文塞进一个上下文；
- 因为工具“已经有”就默认全部启动；
- 把浏览器、Windows、Codex、Reasonix、图像、视频、ECC、生态站同时挂到每个任务；
- 默认认为私有 Skill 一定优于外部成熟方案。

**要：**

```text
轻入口
→ 任务分类
→ 查索引/发现成熟能力
→ 比较现有 Skill、官方成熟方案和必要最小实现
→ 加载最小必要 Skill / 工具
→ 执行
→ Reality 验证
```

## 路由规则

1. 原生直达优先；
2. 高层 API / Connector 优先于低层鼠标键盘；
3. GUI 只是执行面，不是固定最后一级；
4. Windows 文件/进程优先 Remote；Remote 不可用立即切 GitHub runner；
5. 工程任务由 GPT 直达、Codex、Reasonix按完整 T_VALID 竞争；
6. 长流程优先复用 ECC v3.1.1，不重新开发第二套 checkpoint/fencing/Gate/Repair 体系；
7. 多工具重工程才按需唤醒成熟生态站；
8. 并行只有能降低完整 T_VALID 才启用；
9. 关键能力必须满足 `RESILIENCE_REDUNDANCY.md` 的双路低相关冗余；
10. 工具失败先切成熟备路恢复业务，再修故障源。

## GUI / 鼠标键盘说明

当前 Desktop Commander Remote 主要承担文件、目录、进程、命令和本地数据处理。

需要窗口、鼠标、键盘时，按任务和 Reality 在以下成熟执行面中选择：
- 原生 API / Connector；
- Browser DOM / Playwright；
- Computer-use 类成熟能力（当前环境可用时）；
- `virtual-mouse-keyboard-demo`；
- Selenium / pywinauto；
- 截图识别 + 单步验证；
- 经授权真实 Windows 输入。

不是“走到最后才允许自动化”，而是从一开始就选**能够自动完成且完整 T_VALID 最短**的执行面。人工只保留用户本人不可替代动作。
