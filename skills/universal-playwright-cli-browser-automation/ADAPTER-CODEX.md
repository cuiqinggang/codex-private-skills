# Codex 适配说明

## 使用方式

重启 Codex 桌面版后，输入：

/skills

或者输入：

$

应该能看到：

universal-playwright-cli-browser-automation

## Codex 测试提示词

请使用 $universal-playwright-cli-browser-automation 技能，打开 https://demo.playwright.dev/todomvc/ ，添加一条 todo：

CODEX_ADAPTER_OK

然后保存 snapshot 和 screenshot，最后报告 PASS / FAIL 和证据路径。

## 注意

Codex 只是这个通用能力包的一个适配端。
底层能力仍然是 playwright-cli。
不要把这个能力理解成 Codex 专用插件。
