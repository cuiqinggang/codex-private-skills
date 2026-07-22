---
name: wechat-screenshot-capture
description: "【纯截图法】微信用户信息截取→保存到桌面文件。一步一截图，不用任何复杂工具(pywinauto/Ctrl+C/Codex)，只靠全屏截图+视觉识别+坐标点击。"
---

# 微信截图法：截取用户信息 → 保存到桌面文件

## 核心理念

> **用最简单的方法：全屏截图 + 视觉识别 + 坐标点击。**
>
> 不用 pywinauto 读控件（Qt 自绘无节点）、不用 Ctrl+C（复制乱码）、不用 Codex（UAC 拦截）。
> 就三步：①截全屏 → ②找坐标 → ③点击+验证。一步一截图，错了就调，丢了重来。

## 为什么这是唯一可靠的方法

| 尝试过的方法 | 失败原因 |
|-------------|---------|
| pywinauto UIA 树 | Qt 窗口无文本节点，读不到任何内容 |
| Ctrl+A + Ctrl+C | 复制出二进制乱码/进程内存 dump |
| Codex exec | UAC 拦截、SendKeys 乱码 |
| 视觉坐标直接点击 | 偏差 30-100px，点不中 |
| 批量循环点击 | 点击太快，最后一次覆盖前面选中 |

## 完整流程

```
① 确认微信窗口在哪个显示器
② 全屏截图（monitors[0] = 所有显示器合并）
③ 视觉分析确认当前状态
④ 像素扫描 / 二分探索 → 找到目标
⑤ 点击 → 截图验证
⑥ 错误就调整坐标重试
⑦ 成功 → 截图保存到桌面
⑧ 用视觉模型"逐字抄出"内容
⑨ 保存为 .txt 文件到桌面
```

---

## 步骤详解

### 步骤1：确认微信窗口位置

```python
from pywinauto import Desktop

for w in Desktop(backend='win32').windows(visible_only=True):
    if '微信' in w.window_text():
        r = w.rectangle()
        print(f"微信窗口: ({r.left},{r.top})~({r.right},{r.bottom})")
        break
```

**此电脑已知位置：**
- 浮动窗口：(1705,16)~(2551,1391)，在显示器2（2560x1440）
- 最大化：2576×1416

### 步骤2：全屏截图

```python
import mss
from PIL import Image
from datetime import datetime

with mss.mss() as sct:
    raw = sct.grab(sct.monitors[0])  # 所有显示器合并
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
${REDACTED_SECRET}
    Image.frombytes('RGB', raw.size, raw.rgb).save(path)
```

### 步骤3：在联系人列表中找到目标（二分探索法）

**实战经验：找"硅基文明"（5次尝试才成功）**

```python
# 第1次失败：视觉模型说 Y≈420 → 点到了"东方通讯"（偏差50px）
# 第2次：粗扫上范围 y=340~540 步长20 → 锁定上界 y=540
# 第3次：粗扫下范围 y=540~690 步长15 → 锁定下界 y=690
# 第4次失败：批量循环点击 y=545~690 步长5 → 太快，没选中任何人
# 第5次成功：一次一点一截图

import pyautogui, time

for y in [570, 585, 600]:
    pyautogui.click(175, y)
    time.sleep(0.5)
    # 截图 → 视觉确认当前选中的是谁
    # y=600 → "硅基文明" ✅
```

**铁律：不能批量循环！必须一次一点一截图一验证！**

**已知联系人坐标（浮动窗口）：**
| 联系人 | 坐标 |
|--------|------|
| 文件传输助手 | (175, 100) |
| 李炳章 | (175, 540) |
| 硅基文明 | (175, 600) |
| 物流托运 | (175, 690) |

X=175 是左侧面板中心，固定不变。Y 取决于联系人排序。

### 步骤4：截取聊天内容区域

```python
# 点击联系人后，聊天内容显示在右侧面板
# 对整个微信窗口截图，裁剪右侧内容区域
with mss.mss() as sct:
    raw = sct.grab(sct.monitors[0])
    img = Image.frombytes('RGB', raw.size, raw.rgb)

# 微信内容区大致位置（浮动窗口下）
# 右面板 X≈1950~2520, Y≈75~1330
content = img.crop((1950, 75, 2520, 1330))
${REDACTED_SECRET}
```

### 步骤5：视觉模型"逐字抄出"内容

将截图送给视觉模型，要求它逐字抄出聊天内容：

```
用 `vision_analyze` 工具，prompt:
"把截图中微信聊天区域的文字内容逐字抄出来，不要遗漏任何内容。
包括：用户名、时间、每条消息的完整文字。"
```

### 步骤6：保存到桌面文件

```python
# 将视觉模型返回的文字内容保存到桌面 .txt 文件
content = "视觉模型返回的文字内容"
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
${REDACTED_SECRET}

with open(save_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"✅ 已保存到: {save_path}")
```

---

## 微信窗口特征速查

| 属性 | 值 |
|------|-----|
| 进程名 | Weixin.exe |
| 窗口标题 | "微信" |
| 窗口类名 | Qt51514QWindowIcon |
| 渲染引擎 | Qt 自绘（MMUIRenderSubWindowHW） |
| 控件可读性 | pywinauto 无文本节点 |

### 浮动窗口状态

| 元素 | 坐标 |
|------|------|
| 窗口位置 | (1705,16)~(2551,1391) |
| 最大化按钮 | (2477, 54) — 窗口左沿+宽-68, 上沿+35 |
| 左面板中心 X | 175 |
| 右面板内容区 X | 1950~2520 |

---

## ⚠️ 关键陷阱

### 陷阱1：视觉模型坐标不准

视觉模型给的"坐标"只能当方向参考，误差 30-100px。不能直接点击！

正确做法：视觉模型给大致范围 → 像素扫描/逐行点击精确定位 → 截图验证。

### 陷阱2：批量点击失效

```python
# ❌ 错误：循环太快
for y in range(545, 690, 5):
    pyautogui.click(175, y)  # 最后一次覆盖前面，最终停在空白区

# ✅ 正确：一次一点一截图
pyautogui.click(175, 570)
time.sleep(0.5)
screenshot()  # 看选中的是谁
# 不是目标 → 调整y → 再点
```

### 陷阱3：GPU 截图空白

Chrome/微信 GPU 加速可能导致截图白屏。检测方法：

```python
from PIL import Image
img = Image.open(screenshot_path)
w, h = img.size
non_white = sum(1 for x in range(0,w,100) for y in range(0,h,100) 
                if img.getpixel((x,y))[0] < 240)
if non_white < 10:
    print('⚠️ 截图几乎全白！改用 Win+Shift+S 或 WGC')
```

### 陷阱4：状态丢失不救

如果窗口关了/切走了/不知道选了什么：
- **不要试图救回来** — 退回第①步重新开始
- 走通的路第二次只需一半时间

---

## 一键脚本模板

```python
# wechat_capture_to_desktop.py
${REDACTED_SECRET}

import time, pyautogui, mss
from PIL import Image
from pywinauto import Desktop
from datetime import datetime

def find_wechat():
    for w in Desktop(backend='win32').windows(visible_only=True):
        if '微信' in w.window_text():
            return w
    return None

def full_screenshot():
    with mss.mss() as sct:
        raw = sct.grab(sct.monitors[0])
        ts = datetime.now().strftime('%Y%m%d_%H%M%S')
${REDACTED_SECRET}
        Image.frombytes('RGB', raw.size, raw.rgb).save(path)
        return path

def click_contact(x=175, y=600):
    """点击联系人，默认坐标(175,600)=硅基文明"""
    pyautogui.click(x, y)
    time.sleep(0.5)
    return full_screenshot()

# ===== 执行 =====
wechat = find_wechat()
if not wechat:
    print("❌ 微信未运行")
    exit(1)

wechat.set_focus()
time.sleep(1)

# 全屏截图确认状态
screenshot_path = full_screenshot()
print(f"✅ 截图已保存: {screenshot_path}")

# 点击联系人
result_path = click_contact(175, 600)
print(f"✅ 点击后截图: {result_path}")

# 此时把截图送给视觉模型，让它"逐字抄出"聊天内容
# 然后把内容保存到 .txt 文件
```

---

## 与其他技能的关系

| 技能 | 关系 |
|------|------|
| `one-step-one-screenshot` | 本技能的核心方法论来源（像素分析、二分探索） |
| `desktop-content-to-cloud-document` | 如需上传到 Google Docs 而非只保存桌面，用这个 |
| `remote-desktop-automation` | 如需更复杂的桌面自动化框架 |

本技能是**最简版本**：纯截图法，只保存到桌面文件，不上传云端。
