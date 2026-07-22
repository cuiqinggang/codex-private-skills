# 千问 Qwen 普通人坐标截图法数据页

中文归属技能：**普通人坐标截图法**

用途：记录千问 / Qwen 网页在不同可见状态下的轻量坐标数据。这里不建立单独大状态机，只保存经过截图验证的坐标、键盘等价动作、成功率、失败修正和证据路径。

## 通用操作法

```text
截图
识别当前页面状态
定位目标控件
记录当前状态下坐标
执行普通人动作
截图验收
成功则累计成功次数
失败则归一化状态并更新失败修正
```

## 坐标数据表

| 日期 | 网站 | 页面状态 | 动作 | 坐标 | 键盘等价动作 | 成功次数 | 失败修正 | 证据路径 |
|---|---|---|---|---|---|---:|---|---|
| 待测 | Qwen / 千问 | 待测 | 打开/确认页面 | 待测 | 无 | 0 | 待测 | 待测 |
| 待测 | Qwen / 千问 | 待测 | 新对话 | 待测 | 无 | 0 | 待测 | 待测 |
| 待测 | Qwen / 千问 | 待测 | 输入框 | 待测 | Ctrl+V | 0 | 待测 | 待测 |
| 待测 | Qwen / 千问 | 待测 | 发送 | 待测 | Enter 优先 | 0 | 待测 | 待测 |
| 待测 | Qwen / 千问 | 待测 | 结果验收 | 截图区域待测 | 无 | 0 | 待测 | 待测 |

## 明日验收计划

```text
1. 打开 Qwen 官网。
2. 截图确认登录和可输入状态。
3. 记录输入框坐标。
4. 粘贴简单题并截图确认。
5. Enter 或点击可见发送按钮。
6. 截图确认回答。
7. 简单题 10 轮。
8. 复杂短答 10 轮。
9. 写入成功率、失败修正、证据路径。
```

## PASS 标准

```text
简单题：10/10 截图看到正确回答。
复杂短答：10/10 截图看到唯一 marker。
成熟坐标：同一页面状态下坐标稳定；状态变化通过截图重新定位。
```
## 2026-07-04 交接补丁：Qwen 已验证样本，但未达到 10/10 成熟

本页原有内容如果在某些终端里显示乱码，以本节中文补丁为准。

### 已验证页面状态

```text
网站：Qwen / 千问
网址：https://www.qianwen.com/
状态：左侧边栏打开，首页干净 composer
窗口：Chrome 可见窗口，约 2560 x 1440
输入框坐标样本：x=1052 y=745 附近
新对话坐标样本：x=100 y=198 附近
发送方式：优先 Enter
```

### 已验证成功样本

```text
What is the capital of France? Answer briefly. -> Paris.
What is 2 plus 2? Answer briefly. -> 4.
```

这些只证明 Qwen 有边栏状态下的输入/发送通道可用，不等于正式 10/10 验收。

### 不能计入通过的原因

```text
1. 有一批问题误发到了 ChatGPT，不是 Qwen。
2. 有一批操作被 Cursor / Kilo 抢走前台焦点。
3. 有一批循环没有做到一步一截图。
4. 有一批重复同一个简单题，不能算正式多题 10/10。
5. 无边栏状态未单独定坐标。
6. 复杂长题和复制答案流程未完成。
```

### 下一次必须分开验收

```text
Qwen 有边栏：简单 10 轮 + 复杂 10 轮 + 超复杂复制答案
Qwen 无边栏：简单 10 轮 + 复杂 10 轮 + 超复杂复制答案
```

证据目录：

```text
${REDACTED_SECRET}
```

## 2026-07-04 补丁：中间主屏有边栏冒烟 PASS

### 固定屏幕状态

```text
必须先把 Chrome / Qwen 移到中间主屏 DISPLAY2。
DISPLAY2: x=0 y=0 width=2560 height=1440。
不要在左侧 DISPLAY1 负坐标窗口里继续测试；左屏坐标会导致位置体系对不上。
Chrome 最大化后窗口矩形可能显示为 left=-8 top=-8 right=2568 bottom=1408，这是 Windows 最大化边框外延，仍属于中间主屏状态。
```

### 本轮有效页面状态

```text
网站：Qwen / 千问
网址：https://www.qianwen.com/
状态：左侧边栏打开，首页干净 composer
窗口：Chrome 位于中间主屏 DISPLAY2，最大化
```

### 新增有效坐标

```text
新建窗口归零：打开新的 Chrome 窗口到 https://www.qianwen.com/，再移动到 DISPLAY2 并最大化。
输入框焦点探针坐标：x=1113 y=759 附近，先输入 x 验证焦点。
输入框已验证旧样本：x=1053 y=745 附近，能落在输入框区域，但焦点视觉不明显。
发送：当前主屏状态下 Enter 成功；发送箭头 x=1764 y=801 点击未触发发送，先不作为优先路线。
```

### 有效冒烟样本

```text
SMOKE-QWEN-MAIN-SIDEBAR-20260704-01:
What is 6 plus 7? Answer briefly.
结果截图显示：6 plus 7 is 13.
```

证据目录：

```text
${REDACTED_SECRET}
```

关键证据：

```text
qwen-main-display-06-new-window-qwen.png
qwen-main-display-12-after-type-x-probe.png
qwen-main-display-13-after-clear-and-paste-smoke.png
qwen-main-display-17-after-enter-send-smoke.png
```

### 本轮新增失败修正

```text
1. Chrome 在左侧 DISPLAY1 时会出现负坐标，必须移动到中间 DISPLAY2 后再测。
2. 标签页污染会把地址栏归零发到抖音等错误标签页；截图发现错误页后，不能继续输入，必须重新打开 Qwen 窗口。
3. 新建对话按钮在旧会话中两次点击未变化，不能假设成功；需要截图验收，失败则用新窗口 / 地址栏归零。
4. 输入框焦点不明显时，必须先输入 x 做焦点探针，截图确认后 Ctrl+A / Backspace 清空，再粘贴正式题。
5. 当前发送箭头点击未触发发送；Enter 在焦点明确时成功，主屏有边栏状态暂时优先 Enter。
```

### 坐标稳定性的正确解释

```text
坐标不是随机变化。普通人坐标法的前提是“同一可见状态内坐标固定”。

必须单独区分：
1. 中间主屏 DISPLAY2 / 左侧 DISPLAY1 / 右侧 DISPLAY3。
2. Chrome 最大化 / 非最大化。
3. 浏览器边框、标签栏、书签栏是否存在。
4. Qwen 左侧边栏打开 / 边栏收起。
5. 首页干净 composer / 回答后底部 composer。
6. 页面缩放比例。

如果这些状态一致，坐标应当基本固定；如果其中一项改变，就不能说坐标失效，而是进入另一条坐标样本。
本次中间主屏 + 最大化 + 有边栏 + 首页 composer 状态下，输入框 x≈1053 y≈745 / x≈1113 y≈759 已验证可用。
```

### 简单 10 轮验收结果

```text
状态：Qwen + 中间主屏 DISPLAY2 + Chrome 最大化 + 左侧边栏打开 + 首页 composer 归零
坐标：输入框 x≈1113 y≈759
发送：焦点明确后 Enter
结果：10/10 PASS（R01b + R02-R10）
失败样本：原 R01 只看到题目留在输入框，未出现答案；不计入通过，已用 R01b 复跑替换。
```

证据：

```text
${REDACTED_SECRET}
```

通过轮次：

```text
R01b: grass -> Green.
R02: 9 minus 4 -> 5
R03: animal says meow -> Cat
R04: opposite of hot -> Cold
R05: Red Planet -> Mars
R06: 12 divided by 3 -> 4
R07: bees make -> Honey
R08: days in a week -> 7
R09: frozen water -> Ice
R10: gas humans breathe -> Oxygen
```

### 复杂短答 10 轮验收结果

```text
状态：Qwen + 中间主屏 DISPLAY2 + Chrome 最大化 + 左侧边栏打开 + 首页 composer 归零
坐标：输入框 x≈1113 y≈759
发送：焦点明确后 Enter
结果：10/10 PASS（R01-R10）
验收：每轮答案截图均出现对应 QWEN-COMPLEX10-xx-20260704 marker 和短答内容。
```

证据：

```text
${REDACTED_SECRET}
```

### 超复杂长题复制回来进行中

```text
状态：Qwen + 中间主屏 DISPLAY2 + Chrome 最大化 + 左侧边栏打开
marker：QWEN-SUPERLONG-COPY-20260704-01
结束 marker：END-QWEN-SUPERLONG-COPY-20260704-01
当前进度：长题已发送，long-04-after-wait-70s.png 已看到长中文答案生成。
未完成：尚未跳到底部、未点击复制按钮、未把答案复制到本地文件。
```

证据：

```text
${REDACTED_SECRET}
```

下一步规则：

```text
不要手动乱滚到底。
Qwen 长答案页面中间偏上有“向下箭头”，表示答案完成/可跳到底部。
点击向下箭头后，应到达答案最底部。
答案最下面一排按钮里，左边那个是复制按钮。
点击复制按钮后，必须读取剪贴板并保存本地文本。
本地文本必须同时包含 QWEN-SUPERLONG-COPY-20260704-01 和 END-QWEN-SUPERLONG-COPY-20260704-01，才算超复杂复制 PASS。
DeepSeek 类似，但向下箭头在答案框上方偏右。
```
## 2026-07-04 补丁：Qwen 有边栏超复杂复制回来 PASS

```text
状态：Qwen + 中间主屏 DISPLAY2 + Chrome 最大化 + 左侧边栏打开
会话：测试截图坐标浏览器流程可靠性
marker：QWEN-SUPERLONG-COPY-20260704-01
结束 marker：END-QWEN-SUPERLONG-COPY-20260704-01
动作：
1. 从 Qwen 标签恢复到 qianwen.com/chat 长答案页。
2. 截图确认页面已在答案底部，且可见开头 marker 与结束 marker。
3. 点击答案底部按钮区最左侧复制按钮，约 x=1018 y=1222。
4. 读取剪贴板并保存到本地文本。
验收：
剪贴板长度：1348
HAS_START=True
HAS_END=True
结果：Qwen 有边栏超复杂复制回来 PASS。
证据：
${REDACTED_SECRET}
${REDACTED_SECRET}
${REDACTED_SECRET}
```
## 2026-07-05 补充纠偏：Qwen 超屏复制不要触发右侧文章工作区

本轮用户现场纠偏：Qwen 在提示词包含“不少于 3000 字、详细操作手册、12 个章节、生成全文”等写作型指令时，会触发右侧大纲 / 正文 / 排版工作区。该模式虽然内容很多，但复制验收变麻烦，不适合作为普通人坐标截图法的成熟测试路径。

新的 Qwen 超屏复制标准：

```text
1. 目标只是“回答明显超过当前聊天页面一屏”，不追求 2500/3000 字。
2. 提示词必须明确要求：只在左侧聊天窗口直接回复，不要生成大纲，不要创建文章，不要打开右侧正文/排版/编辑工作区。
3. 推荐长度：6 段，每段 120 到 180 字；以视觉上需要滚动或超过一屏为准。
4. 仍然必须包含唯一 start marker 和 end marker。
5. 复制回本地后必须同时包含 start/end marker。
6. 如果进入右侧文章工作区，本轮不算正式 PASS，记录为“Qwen 写作工作区分支”，回到新对话重跑短版超屏 prompt。
```

推荐模板：

```text
请只在左侧聊天窗口直接回复，不要生成大纲，不要创建文章，不要打开右侧正文/排版/编辑工作区。
请写一段中文连续回答，长度只需要明显超过当前聊天页面一屏即可，不要太长。
开头必须原样包含：
QWEN-SUPERLONG-COPY-20260704-Rxx
内容主题：普通人坐标截图法为什么适合做浏览器稳定性测试。请分 6 段，每段 120 到 180 字。
最后一行必须原样输出：
END-QWEN-SUPERLONG-COPY-20260704-Rxx
```

判定更新：

```text
旧阈值：剪贴板文本至少 >2500 字符。
新阈值：视觉证据显示回答超过一屏或需要滚动；剪贴板文本通常约 900 到 1600 中文字符即可；核心仍是 start/end marker 完整回收。
```

## 2026-07-06 补丁：Qwen externalH5 参数页焦点异常分支

本轮 V8.0 官方网页测试发现一个新分支：

```text
网址形态：https://www.qianwen.com/?bizPassParams=...externalH5
屏幕状态：中间主屏 DISPLAY2，Chrome 最大化，左侧边栏打开，首页 composer 可见。
现象：旧成熟坐标 x≈1113 y≈759、占位文字区、输入框中心点均未激活可粘贴编辑焦点。
结果：短探针和长提示均未进入输入框。
判定：这不是 Qwen 普通人坐标法整体失败，而是 externalH5 参数页的新焦点分支。
```

修复建议：

```text
1. 不要把 externalH5 参数页计入旧“Qwen 有边栏首页 composer”成熟坐标。
2. 先通过地址栏完整归一到标准入口 https://www.qianwen.com/，注意必须清空原 URL，不能把新 URL 追加到旧 URL 后面。
3. 如果标准入口仍保留 externalH5 状态，本轮标记 QWEN_EXTERNAL_H5_FOCUS_BRANCH，不硬算失败。
4. 下一次需要单独建立 externalH5 坐标数据页：输入焦点、发送、复制各 3/3 小预检。
```
