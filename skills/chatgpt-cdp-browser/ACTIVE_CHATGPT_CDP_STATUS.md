# ChatGPT CDP 当前活跃状态摘要

> 最后更新：2026-04-26  
> 版本：v1.1  
> 状态：链路已通，可使用  
> 搜索关键词：ChatGPT CDP 活跃状态、当前 WS、当前网关

---

## 链路状态

**整体状态：PASS**

| 步骤 | 状态 | 备注 |
|------|------|------|
| G01 调试 Chrome | PASS | Chrome/147.0.7727.102 |
| G02 9334 统一入口 | PASS | WIN_9333 + WIN_9334 + WSL_9334 全通 |
| G03 snapshot 读取 | PASS | 能看到 textbox |
| G04 英文发送 | PASS | TEST_OK 已验证 |
| G05 直接中文 | FAIL | 编码损坏 |
| G05-FIX UTF-8 中文 | PASS | 中文正常显示 |

---

## 关键入口（动态值，不可写死）

| 项目 | 当前值 | 获取方式 |
|------|--------|----------|
| Chrome 9333 | `127.0.0.1:9333` | 固定 |
| 统一入口 9334 | `0.0.0.0:9334 → 127.0.0.1:9333` | 固定（portproxy） |
| WSL 网关 | `192.168.128.1` | `ip route show default \| awk "{print \$3; exit}"` |
| Browser WS | `ws://192.168.128.1:9334/devtools/browser/1f1d7ca3-a0bc-445b-b3e7-ec5fe77cfc86` | `curl http://$GW:9334/json/version` |
${REDACTED_SECRET}

---

## 关键命令路径

```
agent-browser = /home/u123456/.npm-global/bin/agent-browser
hermes        = /home/u123456/.local/bin/hermes
PATH 必含     = $HOME/.npm-global/bin:$HOME/.local/bin:$PATH
```

---

## 关键规则提醒

1. **每次重开 Chrome 后** → 必须重新获取 Browser WS（读 `/json/version`）
2. **每次页面变化后** → 必须重新 snapshot 获取输入框 ref
3. **中文输入** → 必须用 UTF-8 文件方式（Python Unicode 转义写文件 → cat 文件 fill）
4. **一次只发一条** → 发完等回复，截图留证
5. **失败立即停** → 不要补丁式乱试

---

## 已验证截图

```
/tmp/hermes_g04_test_ok.png
/tmp/hermes_g05_fix_chinese_utf8.png
```

---

## 技能包位置

| 层 | 位置 |
|----|------|
| Hermes 技能 | `~/.hermes/skills/chatgpt-cdp-browser/SKILL.md` |
| 复盘文档 | `~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_BROWSER_AUTOMATION_RUNBOOK.md` |
| 本文件 | `~/.hermes/workspace/memory/03_projects/hermes/ACTIVE_CHATGPT_CDP_STATUS.md` |
| 命令索引 | `~/.hermes/workspace/memory/03_projects/hermes/CHATGPT_CDP_KNOWN_GOOD_COMMANDS.md` |
| H盘保存库 | `06_技能规则/chatgpt-cdp-browser/` |
