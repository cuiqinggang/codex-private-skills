# AI_HANDOFF.md 示例

> 处理时间: 2026-06-26 21:24:13
> 工具链: 7-Zip / MarkItDown / FFmpeg / Python PIL
> 接收站根目录: C:\Users\A\Desktop\AI_File_Inbox

---

## 1. 原始拖入文件清单

| # | 文件名 | 大小 | 类型 |
|---|--------|------|------|
| 1 | report.docx | 45210 | .docx |
| 2 | screenshots.zip | 2048000 | .zip |
| 3 | demo.mp4 | 5120000 | .mp4 |
| 4 | instructions.txt | 800 | .txt |
| 5 | logo.png | 32000 | .png |

---

## 2. 解压结果

| # | 文件名 | 路径 |
|---|--------|------|
| 1 | screenshot_01.png | screenshots/screenshot_01.png |
| 2 | screenshot_02.png | screenshots/screenshot_02.png |
| 3 | captions.txt | screenshots/captions.txt |

---

## 3. 文件树

```
00_拖到这里\report.docx
00_拖到这里\screenshots.zip
00_拖到这里\demo.mp4
00_拖到这里\instructions.txt
00_拖到这里\logo.png
01_已解包\screenshots\screenshot_01.png
01_已解包\screenshots\screenshot_02.png
01_已解包\screenshots\captions.txt
02_文本和Markdown\report.md
02_文本和Markdown\instructions.txt
03_图片待多模态\logo.png
04_视频关键帧待多模态\demo\frame_001.png
04_视频关键帧待多模态\demo\frame_002.png
06_AI交接\AI_HANDOFF.md
```

---

## 4. 可直读文本清单

| # | 文件名 | 路径 | 来源 |
|---|--------|------|------|
| 1 | instructions.txt | 02_文本和Markdown\instructions.txt | drop zone |
| 2 | captions.txt | 01_已解包\screenshots\captions.txt | unpacked |

---

## 5. 已转换 Markdown 清单

| # | 文件名 | 路径 | 来源 | 工具 |
|---|--------|------|------|------|
| 1 | report.md | 02_文本和Markdown\report.md | report.docx | MarkItDown |

---

## 6. 图片待多模态清单

| # | 文件名 | 路径 | 来源 |
|---|--------|------|------|
| 1 | logo.png | 03_图片待多模态\logo.png | drop zone |
| 2 | screenshot_01.png | 01_已解包\screenshots\screenshot_01.png | unpacked |
| 3 | screenshot_02.png | 01_已解包\screenshots\screenshot_02.png | unpacked |

---

## 7. 视频关键帧待多模态清单

| # | 帧文件名 | 路径 | 来源视频 |
|---|----------|------|----------|
| 1 | frame_001.png | 04_视频关键帧待多模态\demo\frame_001.png | demo.mp4 |

---

## 8. 音频字幕清单

无音频文件。

---

## 9. 从文件中识别出的任务要求

- **instructions.txt** : 请根据 report.md 生成一份中文总结
- **captions.txt** : 请将截图描述整理为产品演示脚本

---

## 10. 从文件中识别出的命令

未识别到命令。

---

## 11. 可自动执行项

- **instructions.txt** : 请根据 report.md 生成一份中文总结
- **captions.txt** : 请将截图描述整理为产品演示脚本

---

## 12. 需用户确认项

无需用户确认项。

---

## 13. 失败文件和失败原因

无失败文件。

---

## 14. 下一步给 Claude Code / Kilo 的执行提示词

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

---

## 15. 成熟工具证据

| 工具 | 版本 | 路径 | 用途 |
|------|------|------|------|
| 7-Zip | 22.01 | C:\Program Files\NVIDIA Corporation\NVIDIA App\7z.exe | 压缩包解压 |
| FFmpeg | 8.1.1 | ffmpeg | 视频抽帧 |
| MarkItDown | 0.1.6 | pip | Office 文档转 Markdown |
| Python | 3.13.12 | python | 脚本执行 |

---

*自动生成处理时间*
*详细日志: logs/process_*.log*