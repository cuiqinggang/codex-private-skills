# 《爱马仕完整体建设规范：能力自检 + 核心补齐 + Skills 增强》

## 0. 总目标
建设一个**强大、稳定、可复现、低成本的完整体**。
默认路线：
```
先自检 → 再补齐 → 再安装必要 skills → 最后生成能力报告
```
禁止一开始就乱装、乱改、乱试。

---

## 1. 核心原则

### 第一原则：先检测，不先修复
先回答清楚：
- 我现在能控制什么？
- 我现在不能控制什么？
- 缺的是权限、工具、配置、还是浏览器连接？
- 哪些能力已经可用？
- 哪些能力只是理论支持但未验证？

没有检测证据，不准说"已具备"。

### 第二原则：完整授权不等于乱用 root
正确理解：具备完整执行能力、完整检测能力、完整操作入口。
系统级操作需要时明确说明：需要管理员 PowerShell / 普通 PowerShell / WSL / 浏览器 CDP / Docker / 用户手动登录。

### 第三原则：浏览器操作按人类极简法
调用 ChatGPT 网页版时：
```
粘贴问题 → 发送 → 等待回答完成 → 点击复制 → 读取剪贴板 → 返回答案
```
截图只用于异常排障，不用于正常提取答案。

### 第四原则：skills 按昨日重现法安装
只优先安装：官方支持的、Hub 里能查到的、社区常用的、能力提升明显的、与当前系统目标相关的。

---

## 2. 第一阶段：能力自检

### G01｜基础身份与版本自检
检测内容：Hermes 版本、安装路径、Python/uv/Node 环境、配置文件路径、当前模型、当前 provider、API 网关是否启动、Open WebUI 是否连通。

输出格式：
```
G01 基础状态：
- Hermes 版本：
- 安装路径：
- 配置路径：
- 当前模型：
- API 网关：
- Open WebUI：
- 结论：PASS / FAIL / PARTIAL
```

### G02｜本地电脑控制能力自检
检测内容：终端执行、文件读写、文件搜索、文件修改、进程启停、Windows 桌面路径访问、WSL 调 PowerShell、Docker、端口检测。

重点验证：WSL 文件读写、Windows 文件读写、PowerShell 桥接、Docker Desktop 状态、本机端口访问。

输出格式：
```
G02 本地控制能力：
- terminal/process：
- read_file/write_file/patch/search：
- WSL → Windows PowerShell：
- Windows 桌面读写：
- Docker：
- 端口检测：
- 结论：PASS / FAIL / PARTIAL
```

### G03｜网络能力自检
检测内容：公网访问、GitHub 访问、Hermes 官方文档访问、ChatGPT 访问、OpenRouter 访问、本机 127.0.0.1:3000/8642 访问、Windows host.docker.internal 访问。

输出格式：
```
G03 网络能力：
- 公网：
- GitHub：
- ChatGPT：
- OpenRouter：
- Open WebUI 3000：
- Hermes API 8642：
- Docker host.docker.internal：
- 结论：PASS / FAIL / PARTIAL
```

### G04｜浏览器能力自检
检测内容：Chrome CDP 连接、browser_navigate、browser_snapshot、browser_click、browser_type、browser_press、console 读取、dialog 处理、ChatGPT 页面操作。

特别要求：优先检测本地 Chrome CDP；不要优先使用截图/云浏览器/复杂 DOM 解析。

输出格式：
```
G04 浏览器能力：
- Chrome CDP：
- browser_navigate：
- browser_click：
- browser_type：
- browser_press：
- ChatGPT 输入框：
- ChatGPT 发送：
- ChatGPT 复制按钮：
- 剪贴板读取：
- 结论：PASS / FAIL / PARTIAL
```

### G04B｜鼠标键盘控制能力判断
核心判断：鼠标和键盘对人类是主要输入手段，但对爱马仕不是默认主路径。

优先使用顺序：
```
API / 工具调用 → 文件操作 → 终端命令 → 浏览器 CDP → browser_click/type/press → 系统级鼠标键盘（仅备用）
```

浏览器内鼠标键盘（必须具备）：
- browser_snapshot 识别页面元素
- browser_click 点击按钮
- browser_type 输入文本
- browser_press 按 Enter/Tab/Escape
- ChatGPT 输入框定位、粘贴、发送、复制按钮点击

系统级鼠标键盘（作为备用能力检测）：
- 适用：Windows 原生软件、安装器窗口、权限弹窗、无 DOM 元素界面、远程桌面
- 不适用：ChatGPT 网页、普通网页点击、复制 GPT 答案、网页表单、网页导航
- 暂不作为 A 类核心 Skill（易干扰用户、坐标点击脆弱、对 ChatGPT 调用无必要）

启用系统级鼠标键盘的前提条件（满足之一）：
1. browser_click 找不到目标按钮
2. 页面元素无法通过 ref ID 点击
3. 必须操作 Windows 原生窗口
4. 必须处理安装器或授权弹窗
5. 用户明确要求操作某个桌面软件
6. CDP / 浏览器工具全部失败

启用前必须说明：为什么不能用浏览器工具？是否影响用户操作？失败会不会点错窗口？

MOUSE_KEYBOARD_POLICY_PASS 标准：
1. 网页任务优先使用 browser tools
2. ChatGPT 网页调用不使用真实鼠标键盘作为默认路径
3. 系统级鼠标键盘只作为备用能力
4. 只有桌面软件/安装器/弹窗/无法识别元素时才启用
5. 不安装来源不明的鼠标键盘 Skill
6. 先检测，再决定是否安装

### G05｜ChatGPT 网页极简链路自检
只做最小测试：
1. 打开 ChatGPT 网页
2. 粘贴一个短问题
3. 发送
4. 等待回答完成
5. 点击最新回答复制按钮
6. 读取剪贴板
7. 确认复制到的是 GPT 回答

禁止：截图识别正文、OCR、复杂 DOM 解析、提前读取半截回答、要求 GPT 输出机器协议。

输出格式：
```
G05 ChatGPT 网页链路：
- 已粘贴：
- 已发送：
- 回答是否完成：
- 复制按钮是否出现：
- 是否点击复制：
- 剪贴板内容是否为最新回答：
- 结论：PASS / FAIL / PARTIAL
```

### G06｜skills 系统自检
检测内容：skills list、skills browse、skills search、skill_view、skill_manage、skills 目录、已安装数量、重复/冲突。

输出格式：
```
G06 Skills 系统：
- skills list：
- skills browse：
- skills search：
- skill_view：
- skill_manage：
- skills 目录：
- 已安装数量：
- 重复/冲突：
- 结论：PASS / FAIL / PARTIAL
```

---

## 3. 第二阶段：核心能力补齐

只有自检完成后，才允许补齐能力。

### 第一优先级：本地电脑控制
终端执行、文件读写、文件搜索、进程管理、端口检测、PowerShell 桥接、Docker 检测、WSL 检测。

### 第二优先级：浏览器控制
Chrome CDP 连接、网页打开、点击、输入、按键、等待、复制按钮点击、剪贴板读取。

### 第三优先级：网络控制
公网访问、GitHub 访问、官方文档访问、本机服务访问、OpenRouter 访问、ChatGPT 访问。

### 第四优先级：skills 管理
列出、搜索、浏览官方 Hub、安装、查看内容、删除/停用不合适 skills。

---

## 4. 第三阶段：推荐安装的 skills 类型

### A 类：必须优先安装 / 保留
hermes-agent、plan、writing-plans、systematic-debugging、requesting-code-review、test-driven-development、subagent-driven-development、native-mcp、github-auth、github-repo-management、github-issues、github-code-review、github-pr-workflow

### B 类：建议安装，按需启用
google-workspace、maps、notion、obsidian、nano-pdf、himalaya、webhook-subscriptions、jupyter-live-kernel、llm-wiki、arxiv、research-paper-writing

注意：需要账号/OAuth/API key 的标注"已安装/已配置/已验证"三种状态。

### C 类：创作增强，可选安装
architecture-diagram、excalidraw、popular-web-designs、p5js、manim-video、baoyu-infographic、songwriting-and-ai-music、pixel-art

### D 类：暂缓安装或按需安装
大型 MLOps 模型 skills、训练类 skills、游戏类 skills、智能家居类 skills、社交媒体发布类 skills、需要复杂外部账号的 skills

判断标准：用户近期不用就不先装，装了也标注"未验证"。

---

## 5. skills 安装规则

### 安装前
列出现有 skills → 搜索官方 Hub → 确认 skill 来源 → 确认是否重复 → 确认是否需要额外依赖

### 安装中
只允许优先安装：official/*、Hermes 官方仓库内置/可浏览 skills、明确来源可信的 skills。不要从未知网页复制陌生脚本直接执行。

### 安装后
必须验证：skills list 能看到 → skill_view 能打开 → 新 session 中能加载 → 必要依赖是否存在

### 状态必须分三级
- **已安装**：文件存在，skills list 能看到
- **已配置**：需要的配置/API/OAuth 已处理
- **已验证**：实际跑过一个最小任务并成功

---

## 6. 禁止行为

- 一次性安装几百个 skills
- 安装来源不明的 skills
- 重复创建相同功能 skills
- 没有自检就修复
- 没有备份就大改配置
- 为了证明能力大量截图
- 把 ChatGPT 网页调用做成复杂机器协议
- 用截图/OCR 代替复制按钮
- 把所有任务都转成 root 执行

---

## 7. 最终输出报告格式

```
《爱马仕完整体能力报告》
一、基础状态
二、本地电脑能力
三、网络能力
四、浏览器能力
五、skills 能力
六、缺口清单
七、下一步
```

---

## 8. 最小成功标准（COMPLETE_BODY_PASS）

1. 已完成本地电脑能力自检
2. 已完成网络能力自检
3. 已完成浏览器能力自检
4. 已完成 ChatGPT 网页极简链路自检
5. 已完成 skills 系统自检
6. 已列出推荐安装 skills
7. 已区分：已安装 / 已配置 / 已验证
8. 已明确哪些能力缺失、为什么缺失、如何补齐
9. 没有乱装来源不明 skills
10. 没有把简单网页操作复杂化
