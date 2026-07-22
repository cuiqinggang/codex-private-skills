# Hermes / 爱马仕适配说明

## 定位

Hermes / 爱马仕也可以使用这个能力，因为底层是命令行工具 playwright-cli。

只要 Hermes 能执行 PowerShell、shell 或 WSL 命令，就可以复用这个技能包。

## Windows 路径

H:\AI\skills\universal-playwright-cli-browser-automation

## WSL 路径通常是

/mnt/h/AI/skills/universal-playwright-cli-browser-automation

## 推荐给 Hermes 的任务提示词

请使用以下技能包：

H:\AI\skills\universal-playwright-cli-browser-automation

先读取：

1. SKILL.md
2. RUNBOOK.md
3. SAFETY.md
4. ADAPTER-HERMES.md

然后使用 playwright-cli 操作浏览器网页。

要求：

1. 优先使用 snapshot 和元素 ref；
2. 不要优先坐标点击；
3. 每一步保存日志；
4. 最后保存 screenshot；
5. 最后保存 snapshot；
6. 最后保存 final-report.md；
7. 不登录真实账号；
8. 不发布；
9. 不发送；
10. 不删除；
11. 不购买；
12. 不付款；
13. 不做验证码绕过；
14. 不做反检测。

## Hermes smoke test

playwright-cli open https://demo.playwright.dev/todomvc/ --headed
playwright-cli type "HERMES_ADAPTER_PLAYWRIGHT_OK"
playwright-cli press Enter
playwright-cli snapshot --filename=H:\AI\workspaces\HERMES-PLAYWRIGHT-SMOKE\evidence\snapshot-final.yml
playwright-cli screenshot --filename=H:\AI\workspaces\HERMES-PLAYWRIGHT-SMOKE\evidence\screenshot-final.png
playwright-cli close
