# 通用 Playwright CLI 网页自动化技能包

## 目的

把 playwright-cli 变成一个通用网页自动化能力，供 Codex、Hermes 爱马仕、OpenClaw、小龙虾等 Agent 复用。

## 安装位置

通用技能包：

H:\AI\skills\universal-playwright-cli-browser-automation

Codex 适配目录：

%USERPROFILE%\.agents\skills\universal-playwright-cli-browser-automation

Hermes 适配说明：

H:\AI\skills\universal-playwright-cli-browser-automation\ADAPTER-HERMES.md

## 最小测试命令

playwright-cli open https://demo.playwright.dev/todomvc/ --headed
playwright-cli type "UNIVERSAL_PLAYWRIGHT_CLI_SMOKE_OK_20260529"
playwright-cli press Enter
playwright-cli snapshot --filename=.\evidence\snapshot-final.yml
playwright-cli screenshot --filename=.\evidence\screenshot-final.png
playwright-cli close

## 成功标准

最终 snapshot 中出现：

UNIVERSAL_PLAYWRIGHT_CLI_SMOKE_OK_20260529

并且最终截图文件存在。
