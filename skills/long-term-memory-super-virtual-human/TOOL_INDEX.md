# 长期记忆超级虚拟人｜按需工具索引 v0.1

原则：**能力全、入口轻、按需加载。**

## 当前能力索引

| 任务类型 | 首选能力 | 已有备选 / 专项 |
|---|---|---|
| 公共互联网信息 | GPT Web / Search | 专用 Browser |
| 网页交互 | Browser / DOM / Playwright | `screenshot-recognize-operate-browser` |
| 高可靠截图式浏览器操作 | Playwright / DOM 不可靠时启用 | `screenshot-browser-100-percent-route v2.0.0`（历史 9/9 最终成功） |
| 虚拟鼠标/键盘 | `virtual-mouse-keyboard-demo` | Playwright 虚拟浏览器 / Selenium 隔离 Chrome / 经授权真实 Windows 输入 |
| Windows 文件/命令 | Desktop Commander Remote | GitHub Windows runner |
| 大型编码/仓库工程 | Codex | Reasonix / 其他代码执行器 |
| GitHub | GitHub Connector / gh | Windows runner |
| 邮件/日历/云文档 | 对应 Connector | 浏览器 |
| 图像 | 图像生成/编辑工具 | 专项视觉模型 |
| 视频 | 专项视频工具 | 本地/云端成熟流水线 |
| 极低延迟概率/路径类专项 | 任务匹配时调用 | `jev-probability-engine-p0` 等既有专项技能 |
| 长任务恢复 | TASK_CONTRACT + Checkpoint + 项目权威状态 | 独立强备份路线 |
| GPT 不可用 | 独立强备份 | 待 Reality 认证 |

## 轻入口规则

启动时只需要知道：

```text
任务是什么？
需要观察哪个现实域？
需要哪类能力？
```

随后只读取对应索引项和必要 Skill。

**不要：**
- 把所有 Skill 全文塞进一个上下文；
- 因为工具“已经有”就默认全部启动；
- 把浏览器、Windows、Codex、Reasonix、图像、视频等同时挂到每个任务。

**要：**

```text
轻入口
→ 任务分类
→ 查索引
→ 加载最小必要 Skill / 工具
→ 执行
→ 结果回主脑
```

## 路由规则

1. 原生直达优先；
2. 高层 API / Connector 优先于低层鼠标键盘；
3. 浏览器 DOM/Playwright 优先于截图点击；DOM 不可靠再启用截图识别；
4. Windows 文件/进程优先 Remote；Remote 不可用再走 GitHub runner；
5. 工程任务才引入 Codex / Reasonix；
6. 并行只有能降低完整 T_VALID 才启用；
7. 工具失败优先换成熟等价路径，不先膨胀架构；
8. 两条现实通道都失败时，保存 Checkpoint 并明确 BLOCKED。

## GUI / 鼠标键盘说明

当前 Desktop Commander Remote 在本项目中主要承担：
- 文件；
- 目录；
- 进程；
- 命令；
- 本地数据处理。

它不是唯一 GUI 控制入口。

需要窗口、鼠标、键盘时，优先从现有成熟能力中按任务选择：
1. 浏览器原生/DOM/Playwright；
2. `virtual-mouse-keyboard-demo` 的虚拟浏览器；
3. Selenium 隔离 Chrome；
4. 截图识别 + 单步验证；
5. 只有确实需要且已授权时，使用真实 Windows 输入。

这样避免把 GUI 控制能力是否存在绑定到单一工具。
