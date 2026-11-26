# Google AI 权益串联单任务交接模板

> 整单只用一个 `TASK_ID`。普通任务只填主线字段；未触发的支路写 `N/A`，未测指标写 `NOT_MEASURED`。

```markdown
## 任务单回执｜<TASK_ID>

- **任务名称**：
- **当前档位**：`PRO_20` / `ULTRA_5X`
- **日期（北京时间）**：YYYY-MM-DD HH:mm
- **规格版本与冻结路径**：Drive 链接或路径（含版本号）
- **Git 仓库与提交号**：`<repo> @ <commit_sha>`
- **交付产物链接 / 路径**：

### 1. 各环节执行与证据
- **Gemini 调研 / NotebookLM 溯源**：已用 / N/A｜来源链接与关键结论路径
- **Antigravity 本地开发与复核**：使用模型（如 Gemini 4 Neon / Claude）｜修改文件｜测试命令与结果
- **AI Studio 长材料 / 审片支路**：已用 / N/A｜带时间戳或原文引文的问题清单路径
- **Colab GPU 算力支路**：已用 / N/A
  - 触发原因：本机 2080 Ti 显存不足 / 本机被占用 / 批量任务更省时
  - GPU 型号与 CU 消耗：
  - 分段计时（分:秒:毫秒）：上传 + 排队启动 + 运行 + 下载校验 = 总耗时
  - 本机 2080 Ti 对照耗时：`分:秒:毫秒` 或 `NOT_MEASURED`
  - 回收核销：`colab stop` 后 `colab sessions` 确认已清空（PASS / FAIL）
- **Gemini API / Cloud 赠金支路**：已用 / N/A｜调用次数｜计费/赠金抵扣状态

### 2. 端到端验收与升级信号观察
- **最终验收状态**：`PASS` / `PARTIAL` / `FAIL` / `BLOCKED`
- **完整 `T_VALID_E2E`（含等待、传输、重试、回读）**：`分:秒:毫秒`
- **本单是否触发 Pro 瓶颈**：
  - [ ] Antigravity / Gemini 触发额度封顶并拖慢交付
  - [ ] 当月 Colab 消耗逼近 200 CU
  - [ ] 当月 Gemini API 消耗超过 $10 赠金
- **后续动作 / 遗留未决项**：
```
