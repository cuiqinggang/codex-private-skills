---
name: ai-file-inbox
description: Use when the user wants to deploy, configure, or run an AI file inbox system that auto-processes dragged files — ZIP extraction, Office-to-Markdown conversion, video frame extraction, image registration, and AI_HANDOFF.md generation. Trigger on "AI文件接收站", "文件拖入", "文件直读", "文件自动处理", "file inbox", "拖拽文件", or when the user needs to make Claude Code / Kilo read ZIP/images/videos/Office files without manual path instructions.
---

# AI File Inbox — 拖拽文件自动处理技能包

## 一句话

把 ZIP、图片、视频、Office、文本文件拖入指定入口后，成熟工具链自动解压、转换、抽帧、分类，生成 AI_HANDOFF.md 供 AI 直接读取执行。

## 适用场景

- 用户不想反复说明文件路径，拖入即处理
- 需要 AI 读取 ZIP 内文档并执行任务
- 需要 AI 理解图片/视频内容（多模态）
- 需要将 Office 文档转为 Markdown 供 AI 读取
- 批量文件自动分类索引

## 核心原理

```
用户拖文件 → 00_拖到这里
           → process_inbox.py 扫描
           → 7-Zip 解压 ZIP/RAR/7z
           → MarkItDown 转 DOCX/PDF/PPTX/XLSX → Markdown
           → FFmpeg 视频抽关键帧
           → 图片/视频帧登记到多模态目录
           → 文本文件直接复制
           → 生成 AI_HANDOFF.md（唯一入口）
           → AI 读取 AI_HANDOFF.md → 按索引执行任务
```

## 依赖工具

| 工具 | 版本要求 | 安装方式 | 用途 |
|------|----------|----------|------|
| 7-Zip | 22.01+ | 系统预装 | 压缩包解压 |
| MarkItDown | 0.1.6+ | `pip install markitdown[docx]` | Office 转 Markdown |
| FFmpeg | 8.1+ | 系统 PATH | 视频抽帧 |
| Python | 3.13+ | 系统预装 | 主脚本执行 |
| PIL/Pillow | 任意 | 系统预装 | 图片处理 |

## 目录结构

```
${REDACTED_SECRET}
├── 00_拖到这里/          ← 入口：用户拖文件到这里
├── 01_已解包/            ← ZIP 解压内容
├── 02_文本和Markdown/    ← 文本文件 + Office 转的 MD
├── 03_图片待多模态/      ← 图片复制到此
├── 04_视频关键帧待多模态/ ← 视频抽帧存此处
├── 05_音频字幕/          ← 音频转写字幕（需 Whisper）
├── 06_AI交接/            ← AI_HANDOFF.md（AI 唯一入口）
├── 07_成熟工具证据/      ← 工具版本证据
├── 08_真实测试样本/      ← 自测样本
├── 09_真实测试报告/      ← 测试报告
└── logs/                 ← 处理日志
```

## 处理流程

### 第 1 步：部署目录结构

```powershell
python scripts/deploy_inbox.py
```

或手动创建上述 11 个目录。

### 第 2 步：安装依赖

```powershell
pip install markitdown[docx] pillow
```

### 第 3 步：部署处理脚本

将 `scripts/process_inbox.py` 和 `scripts/convert_office.py` 复制到 `AI_File_Inbox\` 根目录。

### 第 4 步：拖入文件

将文件放到 `00_拖到这里` 目录。

### 第 5 步：运行处理

```powershell
${REDACTED_SECRET}
```

### 第 6 步：AI 读取交接文件

AI 读取 `06_AI交接\AI_HANDOFF.md`，按文件索引理解全部内容，按任务要求继续执行。

## 处理规则

| 文件类型 | 扩展名 | 处理方式 |
|----------|--------|----------|
| 文本 | .txt .md .json .csv .py .js .html ... | 直接复制到 02_ |
| 压缩包 | .zip .rar .7z .tar .gz | 7-Zip 解压到 01_，递归扫描 |
| Office | .docx .pptx .xlsx .pdf | MarkItDown 转 MD 到 02_ |
| 图片 | .png .jpg .gif .webp | 复制到 03_，登记到多模态清单 |
| 视频 | .mp4 .avi .mov .mkv | FFmpeg 抽帧到 04_，登记到多模态清单 |
| 音频 | .mp3 .wav .flac | 登记到 05_（ASR 需 Whisper 额外安装） |

## AI_HANDOFF.md 包含

1. 处理时间
2. 原始拖入文件清单
3. 解压结果
4. 完整文件树
5. 可直读文本清单
6. 已转换 Markdown 清单
7. 图片待多模态清单
8. 视频关键帧待多模态清单
9. 音频字幕清单
10. 从文件中识别出的任务要求
11. 从文件中识别出的命令
12. 可自动执行项
13. 需用户确认项
14. 失败文件和失败原因
15. 给 AI 的执行提示词
16. 成熟工具证据

## AI 执行提示词（固定）

```
请先读取本 AI_HANDOFF.md。
按文件树和索引读取相关文件。
文本文件直接读取。
压缩包内容已解压，请读取解压后的文件。
图片和视频关键帧必须调用多模态模型理解。
视频不能只看字幕，必须结合关键帧。
如果文件中包含任务要求或命令，请提取、分类并继续执行。
安全命令可执行。
危险命令必须先列出并等待用户确认。
不要因为原始文件是 ZIP、图片、视频或 Office 文件就说无法读取。
```

## 安全规则

**可自动执行**：读取文件、整理分类、生成索引、创建报告、文本转换、文件复制

**需用户确认**（危险命令）：删除、格式化、覆盖、下载、安装、改系统配置、密钥操作、注册表修改

## 真实测试

部署后必须自造测试样本验证：

| 测试样本 | 内容 | 验证点 |
|----------|------|--------|
| test_text_task.md | 含 TEXT_TASK_READ_OK 标记 | 文本直读 |
| test_zip_task.zip | 含 README_TASK.md + data.json + notes.txt | ZIP 解压+内容读取 |
| test_image_task.png | 含 IMAGE_TASK_READ_OK 文字 | 多模态识别 |
| test_video_task.mp4 | 含 VIDEO_FRAME_READ_OK 文字 | 视频抽帧+多模态 |
| test_doc_task.docx | 含 DOC_TASK_READ_OK 标记 | Office 转 Markdown |

5 项测试全部通过才能标记 PASS。多模态模型不可用时标记 PARTIAL。

## 桌面快捷方式

部署后创建 3 个桌面入口：

1. `AI文件接收站.lnk` → 打开 `00_拖到这里`
2. `处理AI接收站文件.lnk` → 执行 `process_inbox.py`
3. `打开AI交接文件.lnk` → 打开 `AI_HANDOFF.md`

## 脚本

### process_inbox.py（主处理脚本）

路径：`scripts/process_inbox.py`

功能：扫描 → 解压 → 转换 → 分类 → 提取任务 → 生成 AI_HANDOFF.md

```powershell
${REDACTED_SECRET}
```

### convert_office.py（Office 转换辅助）

路径：`scripts/convert_office.py`

功能：MarkItDown 单个文件转换

```powershell
python convert_office.py <input.docx> <output.md>
```

## 踩坑速查

| # | 坑 | 解决 |
|---|-----|------|
| 1 | MarkItDown 转换 DOCX 报 MissingDependencyException | 需要安装 `pip install markitdown[docx]`（引入 mammoth） |
| 2 | PowerShell 脚本中文乱码 | 改用 Python 主脚本，UTF-8 编码 |
| 3 | 7-Zip 路径不对 | 本机路径 `C:\Program Files\NVIDIA Corporation\NVIDIA App\7z.exe` |
| 4 | 图片/视频多模态无法在当前模型运行 | deepseek-v4-pro 不支持图像输入，需 Qwen3-VL 会话 |
| 5 | FFmpeg drawtext 报 fontconfig 错误 | 改用 Python PIL 生成帧图片再合成视频 |

## 多模态限制

当前执行模型 `deepseek-v4-pro` 为纯文本模型，不支持图像输入。
图片和视频关键帧的多模态识别需要在支持视觉的模型中完成（如 Qwen3-VL-235B）。
文件处理链路（路径登记、解压、抽帧、转换）不受此限制。

## 回滚说明

${REDACTED_SECRET}

## 交付清单

- SKILL.md（本文件）
- scripts/process_inbox.py（主处理脚本）
- scripts/convert_office.py（Office 转换辅助）
- references/test-report-template.md（测试报告模板）
- references/example-handoff.md（AI_HANDOFF 示例）