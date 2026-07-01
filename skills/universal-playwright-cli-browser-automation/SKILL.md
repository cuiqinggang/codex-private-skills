---
name: universal-playwright-cli-browser-automation
description: 通用 Playwright CLI 网页自动化技能包。适用于 Codex、Hermes 爱马仕、OpenClaw、小龙虾、Claude Code、Cursor、GitHub Copilot，以及其他能执行命令行的 AI Agent。用于浏览器网页打开、元素级定位、snapshot、ref 点击、表单填写、截图证据、网页测试、数据抓取。禁止用于验证码绕过、反检测、群发、私域骚扰、未授权发布、付款、购买、删除、Windows 原生桌面软件控制。
---

# 通用 Playwright CLI 网页自动化技能包

## 一句话定位

这是一个“通用网页自动化能力包”，不是 Codex 专用插件。

它可以被以下工具复用：

- GPT Codex 桌面版
- Codex CLI
- Hermes / 爱马仕数字助手
- OpenClaw / 小龙虾
- Claude Code
- Cursor
- GitHub Copilot
- 其他能执行 PowerShell / shell / WSL 命令的 AI Agent

## 核心思想

网页自动化不要优先靠截图猜坐标，而要优先使用：

1. playwright-cli 打开网页；
2. playwright-cli snapshot 获取页面结构；
3. 从 snapshot 中找元素 ref；
4. 用 ref 或稳定选择器点击、填写、输入；
5. 每一步保存日志；
6. 最后保存 screenshot 和 snapshot 作为证据。

## 标准流程

1. 打开网页：

playwright-cli open <url> --headed

2. 获取页面快照：

playwright-cli snapshot --filename=<快照文件路径>

3. 根据 snapshot 找元素 ref。

4. 操作页面：

playwright-cli click <ref>
playwright-cli type "文本"
playwright-cli fill <ref> "文本"
playwright-cli press Enter

5. 保存最终截图：

playwright-cli screenshot --filename=<截图文件路径>

6. 输出 final-report.md。

## 适合场景

- 网页 UI 测试
- 控制台首页测试
- 后台管理页面操作
- 表单填写
- 网页数据抓取
- Review Queue 审核页
- 草稿准备
- 自动截图取证
- AI 公司控制台测试

## 不适合场景

- Windows 原生软件
- 微信桌面客户端
- 游戏
- Canvas 纯画布页面
- 验证码页面
- 需要反检测的页面
- 私域群发
- 未授权自动发布
- 付款、购买、退款、删除等高风险动作

## 发布/发送安全规则

官方 API + 自有公开账号 + 明确授权：
可以自动发布。

微信私聊、微信群、私域消息：
只允许自动准备草稿，最后必须人工确认。

验证码绕过、反检测、批量骚扰、群控：
禁止。

## 证据要求

每一个正式任务必须保存：

- 命令日志；
- 初始 snapshot；
- 最终 snapshot；
- 最终 screenshot；
- final-report.md；
- PASS / FAIL 状态码。
