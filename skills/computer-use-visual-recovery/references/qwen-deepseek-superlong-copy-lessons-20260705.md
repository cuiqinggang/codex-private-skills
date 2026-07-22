# Qwen / DeepSeek 超屏复制普通人坐标截图法经验

创建日期：2026-07-05

适用技能：`computer-use-visual-recovery`

适用场景：

```text
Qwen 官方站长答案复制测试
DeepSeek 官方站长答案复制测试
普通人坐标截图法
一轮一截图
超屏答案复制
答案底部复制按钮定位
剪贴板验收
避免误复制 prompt / URL / 旧答案
```

## 价值判断

本材料为高价值可复用经验。

理由：

```text
1. 能减少 Codex 在官方 AI 网站测试中重复误点复制按钮。
2. 能形成 DeepSeek 后续可直接复用的 SOP。
3. 能把“看见回答”升级为“复制回本地并校验”的闭环验收。
4. 能防止 prompt、URL、旧答案、哨兵文本被误计为 PASS。
5. 用户明确要求沉淀到技能包和知识库，后续 DeepSeek 都要用上。
```

## 已验证成果

```text
Qwen 有边栏短版超屏复制：10/10 PASS
正式 PASS：
- R01
- R02b
- R03
- R04
- R05
- R06
- R07
- R08
- R09
- R10
```

Page3 新增 PASS：

```text
R03 Length=1159
R04 Length=1250
R05 Length=1297
R06 Length=1147
R07 Length=1230
R08 Length=1309
R09 Length=1378
R10 Length=1572
```

证据目录：

```text
${REDACTED_SECRET}
```

汇总报告：

```text
${REDACTED_SECRET}
```

## 必须遵守的 SOP

每一轮只跑一个 Rxx：

```text
1. 打开或归一化到目标官网干净聊天首页。
2. 截图确认目标站点、账号状态、边栏状态、输入框干净。
3. 粘贴本轮 prompt。
4. 截图确认 marker 在目标官网输入框内。
5. Enter 发送。
6. 等待回答完成。
7. 截图确认答案在左侧聊天窗口直接生成，没有右侧文章/正文/排版工作区。
8. 如果出现向下箭头，先点向下箭头到底部。
9. 裁答案底部按钮区。
10. 只定位最下方按钮行的第一枚复制图标。
11. 复制前先把剪贴板设为哨兵文本。
12. 点击复制按钮。
13. 读取剪贴板并保存文本。
14. 同时校验 Length、start marker、end marker、非 prompt、非哨兵、非 URL、非旧答案。
15. 只有全部通过才计 PASS。
```

## PASS 标准

```text
Length > 700
HasStart=True
HasEnd=True
LooksLikePrompt=False
StillSentinel=False
不是 URL
不是旧轮次答案
答案直接在左侧聊天窗口生成
没有右侧文章/正文/排版工作区
```

## 失败模式

不计 PASS 的情况：

```text
1. 剪贴板仍是哨兵文本。
2. 剪贴板是用户 prompt。
3. 剪贴板是 URL。
4. 剪贴板是旧轮次答案。
5. 只看见页面答案，但未复制回本地。
6. 复制到了用户 prompt 气泡的复制按钮。
7. 进入右侧文章/正文/排版工作区。
8. 未截图确认当前页面状态就套旧坐标。
```

## 按钮定位规则

Qwen 本次经验：

```text
复制按钮横坐标常在 x≈1017 附近。
y 坐标不是永久固定，必须绑定当前答案底部状态。
R03/R04/R06 成功点位约 y=1178。
R07 成功点位约 y=1205。
R08/R09/R10 出现向下箭头后，成功点位约 y=1221。
```

更重要的通用规则：

```text
不要记死坐标。
先截图，再看答案底部按钮行。
如果有向下箭头，先点到底部。
裁图时可能出现文字残影或上方小图标，必须选最下方按钮行。
复制按钮是答案底部按钮行的第一枚图标。
```

## DeepSeek 后续复用规则

DeepSeek 测试开始前必须复用本页规则：

```text
1. 不要一上来批量跑 20 轮。
2. 每个状态先做 1 轮冒烟。
3. 简单题、超屏复制、超复杂问题分开计数。
4. 有边栏和无边栏分开定坐标。
5. 复制按钮必须按 DeepSeek 当前截图重新定位。
6. 出现底部跳转/向下按钮时先点到底部。
7. 剪贴板必须设哨兵再复制。
8. 只有剪贴板完整回收 start/end marker 才算 PASS。
```

## 触发词

```text
Qwen 超屏复制
DeepSeek 超屏复制
普通人坐标截图法
答案复制按钮
向下箭头
哨兵剪贴板
复制 prompt 误判
复制 URL 误判
DeepSeek 后续测试
官方站长答案复制验收
```

## 失败复盘入口

失败时记录：

```text
TASK:
TARGET SITE:
ROUND:
PAGE STATE:
SIDEBAR STATE:
PROMPT MARKER:
WAIT SCREENSHOT:
DOWN ARROW PRESENT:
BUTTON CROP:
CLICK POINT:
CLIPBOARD LENGTH:
HAS_START:
HAS_END:
STILL_SENTINEL:
LOOKS_LIKE_PROMPT:
FAILURE MODE:
NEXT RECOVERY STEP:
```

## 最近使用记录

```text
2026-07-05: Qwen 有边栏短版超屏复制完成 10/10 PASS。R03-R10 在 Page3 补齐。DeepSeek 后续测试必须复用本规则。
```


## 2026-07-05 Additional PASS - Qwen No-Sidebar And DeepSeek Sidebar Matrix

```text
Run root:
${REDACTED_SECRET}

Final report:
${REDACTED_SECRET}

Official counted results:
Qwen no-sidebar simple copy: 10/10 PASS
Qwen no-sidebar superlong copy: 10/10 PASS
DeepSeek sidebar superlong copy: 10/10 PASS
DeepSeek no-sidebar superlong copy: 10/10 PASS
Total official counted rounds: 40/40 PASS

Validation rule reused:
sentinel before copy; clipboard after copy; non-sentinel; non-prompt; non-URL;
for superlong copy Length > 700 and both start/end markers present.

Coordinates from this run:
Qwen no-sidebar new chat x=73 y=151
Qwen no-sidebar homepage input x=1220 y=748
Qwen no-sidebar simple answer copy x=893 y=342
Qwen no-sidebar superlong answer copy x=893 y=1222
DeepSeek sidebar new chat x=132 y=211
DeepSeek sidebar homepage input x=1370 y=765
DeepSeek sidebar superlong answer copy x=1043 y=1202
DeepSeek no-sidebar new chat x=153 y=153
DeepSeek no-sidebar homepage input x=1370 y=765
DeepSeek no-sidebar superlong answer copy x=912 y=1202
```
