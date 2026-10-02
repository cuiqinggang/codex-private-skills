# 长期记忆超级虚拟人｜按需工具索引 v0.1

原则：**能力全、入口轻、按需加载。**

| 任务类型 | 首选能力 | 备选 / 专项 |
|---|---|---|
| 公共互联网信息 | GPT Web / Search | 专用 Browser |
| 网页交互 | 成熟 Browser / Computer Use（可用时） | Playwright / 既有浏览器技能 |
| Windows 文件/命令 | Desktop Commander Remote | GitHub Windows runner |
| 大型编码/仓库工程 | Codex | Reasonix / 其他代码执行器 |
| GitHub | GitHub Connector / gh | Windows runner |
| 邮件/日历/云文档 | 对应 Connector | 浏览器 |
| 图像 | 图像生成/编辑工具 | 专项视觉模型 |
| 视频 | 专项视频工具 | 本地/云端成熟流水线 |
| 长任务恢复 | Checkpoint + 项目权威状态 | 独立强备份路线 |
| GPT 不可用 | 独立强备份 | 待 Reality 认证 |

## 路由规则

1. 原生直达优先；
2. 不因为已经安装某工具就默认调用；
3. 工程任务才引入工程执行器；
4. 并行只有能降低完整 T_VALID 才启用；
5. 工具失败优先换成熟等价路径，不先膨胀架构；
6. 两条现实通道都失败时，保存 Checkpoint 并明确 BLOCKED。
