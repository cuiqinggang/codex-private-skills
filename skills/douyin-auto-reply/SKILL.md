---
name: douyin-auto-reply
description: Use when Codex must visually locate and reply to one specific Douyin web comment on a multi-monitor Windows desktop by the ordinary coordinate screenshot method. Requires coarse-to-fine grids, per-monitor DPI-aware negative coordinates, one action followed by one screenshot that is visibly embedded in chat, exact reply-context verification, duplicate prevention, and explicit confirmation before public sending. Do not use for bulk, unattended, API-cracking, spam, or rule-evasion workflows.
---

# 抖音单条评论坐标截图回复

将它作为 `computer-use-visual-recovery` 的抖音数据页与受控执行层。优先使用普通人坐标截图法；不要因首次误点就切换到 DOM、CDP、逆向接口或批量自动化。

## 强制证据规则

每一步必须遵循：

```text
截图 → 直接以 Markdown 图片发到当前对话 → 说明看到的状态 → 执行一个动作 → 再截图并发图
```

- 仅保存文件、仅调用图像查看器、仅由代理内部查看，全部视为无效证据。
- 图片必须用绝对路径嵌入对话：`![步骤说明](C:/absolute/path.png)`。
- 用户看不到图时立即停止，先修复图片发送方式。

## 坐标定位

1. 截取整个虚拟桌面，识别目标屏幕、窗口和评论栏。
2. 裁出评论栏，先用 50px 粗网格找目标区域。
3. 对“回复”等小按钮再次裁剪，改用 20–25px 细网格：红色竖线、绿色横线、每 100px 主刻度、黄色目标圆圈或十字。
4. 让“回”和“复”尽量分别落在一个小格内，点击两字组合的中心，不点图标边缘。
5. 使用当前截图重新计算坐标，不复用滚动、缩放、窗口移动前的旧坐标。

物理坐标换算：

```text
screen_x = monitor_physical_left + crop_left + target_x
screen_y = monitor_physical_top  + crop_top  + target_y
```

在多屏负坐标环境，必须先启用 Per-Monitor DPI Awareness：`SetProcessDpiAwareness(2)`；然后用 Win32 `SetCursorPos` / `SendInput`。不要依赖 pyautogui 的负坐标行为。

## 受控回复状态机

1. **重复拦截**：截图检查目标评论下是否已有本账号回复；评论数增加或相同回复已存在时停止。
2. **目标定位**：发出细网格图，明确目标用户名、原评论和“回复”按钮所在小格。
3. **单次点击**：仅点击“回复”。
4. **上下文门禁**：截图并发图；必须看到右下角大输入框以及 `回复@目标用户名：原评论`。看不到就禁止粘贴。
5. **输入门禁**：点击空白输入区，直接粘贴；不要默认使用 `Ctrl+A`，以免破坏回复上下文。
6. **文本门禁**：截图并发图，核对目标用户名、全文、发送控件和无重复内容。
7. **发送门禁**：公开评论属于对外代表性沟通，发送前取得当下确认；脚本要求显式 `--confirm-send SEND_PUBLIC_REPLY`。
8. **最终验收**：发送后截图并发图；新内容必须显示为目标评论下的嵌套回复，而不是独立评论。评论计数、回复者、目标用户名和文本至少匹配三项。

## 禁止继续的状态

- 登录、验证码、账号安全、权限或平台风控提示。
- 目标用户名或原评论不一致。
- 回复上下文未出现或在粘贴后消失。
- 已有相同回复，可能造成重复发送。
- 页面滚动、缩放、窗口或屏幕布局改变后仍使用旧坐标。
- 批量回复、无人值守循环、绕过平台规则、破解接口或规避封禁。

## 脚本

使用 `scripts/douyin_reply_template.py`：

```powershell
# 安全默认：只截图并生成 25px 细网格
python scripts/douyin_reply_template.py grid --screen-bbox=-3840,-189,0,1971 --crop=2800,400,900,800 --grid-step=25 --output-dir <task-output-dir>

# 点击必须显式给出当前截图换算后的坐标
python scripts/douyin_reply_template.py click --x -789 --y 595 --confirm-click CLICK_REPLY

# 只设置剪贴板并粘贴，不发送
python scripts/douyin_reply_template.py paste --text-file <reply.txt> --confirm-context "Samous的游戏工坊"

# 仅在发送前截图已由用户确认后执行
python scripts/douyin_reply_template.py send --confirm-send SEND_PUBLIC_REPLY
```

脚本输出 `CHAT_IMAGE_REQUIRED=<absolute path>` 时，必须先把该图片发到对话正文，然后才能进入下一步。

## 验收与复盘

- 首次失败与修复：读 `references/exploration-log-20260710.md`。
- 最近使用与下一次入口：读 `references/recent-use.md`。
- 可视验收页：打开 `acceptance/index.html`。
- 状态只能是 `PASS`、`PARTIAL` 或 `BLOCKED`。没有嵌套回复截图时不得写 `PASS`。
