"""
AI File Inbox Processor v2
Main processing pipeline using Python.
"""
import os
import sys
import json
import shutil
import subprocess
import zipfile
from datetime import datetime

${REDACTED_SECRET}
DROP_ZONE = os.path.join(INBOX_ROOT, "00_拖到这里")
UNPACKED = os.path.join(INBOX_ROOT, "01_已解包")
TEXT_DIR = os.path.join(INBOX_ROOT, "02_文本和Markdown")
IMAGE_DIR = os.path.join(INBOX_ROOT, "03_图片待多模态")
VIDEO_FRAME_DIR = os.path.join(INBOX_ROOT, "04_视频关键帧待多模态")
AUDIO_DIR = os.path.join(INBOX_ROOT, "05_音频字幕")
HANDOFF_DIR = os.path.join(INBOX_ROOT, "06_AI交接")
LOG_DIR = os.path.join(INBOX_ROOT, "logs")
HANDOFF_FILE = os.path.join(HANDOFF_DIR, "AI_HANDOFF.md")

SEVEN_ZIP = r"C:\Program Files\NVIDIA Corporation\NVIDIA App\7z.exe"
CONVERT_SCRIPT = os.path.join(INBOX_ROOT, "convert_office.py")

TEXT_EXTS = {".txt", ".md", ".json", ".csv", ".xml", ".yaml", ".yml", ".html", ".htm", ".css", ".js", ".ts", ".py", ".sh", ".bat", ".ps1", ".cfg", ".ini", ".log", ".env", ".sql", ".c", ".cpp", ".h", ".java", ".go", ".rs", ".toml"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".tiff", ".ico"}
VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".flv", ".wmv"}
AUDIO_EXTS = {".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma"}
ARCHIVE_EXTS = {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"}
OFFICE_EXTS = {".pdf", ".docx", ".pptx", ".xlsx", ".doc", ".ppt", ".xls"}

TASK_KEYWORDS = ["任务", "要求", "请", "命令", "执行", "任务要求", "task", "TODO", "FIXME", "HACK", "NOTE", "IMPORTANT", "说明", "注意事项", "警告", "危险"]
DANGER_KEYWORDS = ["删除", "delete", "rm", "格式化", "format", "清空", "覆盖", "overwrite", "下载", "download", "wget", "curl", "安装", "install", "改系统", "密钥", "key", "token", "密码", "password", "secret", "sudo", "admin", "注册表"]

log_lines = []

def log(msg, level="INFO"):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] [{level}] {msg}"
    log_lines.append(line)
    print(line)

def extract_archive(filepath, dest_dir):
    os.makedirs(dest_dir, exist_ok=True)
    try:
        result = subprocess.run(
            [SEVEN_ZIP, "x", filepath, f"-o{dest_dir}", "-y"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log(f"Extract OK: {os.path.basename(filepath)}")
            return True
        else:
            log(f"Extract FAILED: {os.path.basename(filepath)} {result.stderr[:200]}", "ERROR")
            return False
    except Exception as e:
        log(f"Extract EXCEPTION: {os.path.basename(filepath)} {e}", "ERROR")
        return False

def extract_video_frames(filepath, frame_dir):
    os.makedirs(frame_dir, exist_ok=True)
    pattern = os.path.join(frame_dir, "frame_%03d.png")
    try:
        result = subprocess.run(
            ["ffmpeg", "-y", "-i", filepath, "-vf", "fps=1/2", "-frames:v", "10", pattern],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            frames = [f for f in os.listdir(frame_dir) if f.endswith(".png")]
            log(f"Frames: {len(frames)} from {os.path.basename(filepath)}")
            return frames
        else:
            log(f"Frame extraction FAILED: {os.path.basename(filepath)}", "ERROR")
            return []
    except Exception as e:
        log(f"Frame extraction EXCEPTION: {os.path.basename(filepath)} {e}", "ERROR")
        return []

def convert_office(filepath, md_dest):
    try:
        result = subprocess.run(
            [sys.executable, CONVERT_SCRIPT, filepath, md_dest],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            log(f"Converted: {os.path.basename(filepath)} -> {os.path.basename(md_dest)}")
            return True
        else:
            log(f"Conversion FAILED: {os.path.basename(filepath)} {result.stderr[:200]}", "ERROR")
            return False
    except Exception as e:
        log(f"Conversion EXCEPTION: {os.path.basename(filepath)} {e}", "ERROR")
        return False

def extract_tasks(text):
    tasks = []
    for line in text.split("\n"):
        for kw in TASK_KEYWORDS:
            if kw.lower() in line.lower():
                tasks.append(line.strip())
                break
    return tasks

def is_danger(line):
    for kw in DANGER_KEYWORDS:
        if kw.lower() in line.lower():
            return True
    return False

def build_file_tree():
    tree = []
    for root, dirs, files in os.walk(INBOX_ROOT):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), INBOX_ROOT)
            tree.append(rel)
    return sorted(tree)

def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

def main():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"=== AI_File_Inbox Processing Started ===")
    log(f"InboxRoot: {INBOX_ROOT}")

    # Data collectors
    original_files = []
    text_files = []
    markdown_files = []
    image_files = []
    video_frame_files = []
    audio_files = []
    all_tasks = []
    auto_exec = []
    need_confirm = []
    failed_files = []

    # Step 1: Scan drop zone
    log("Step 1: Scanning drop zone")
    if os.path.isdir(DROP_ZONE):
        for name in os.listdir(DROP_ZONE):
            fpath = os.path.join(DROP_ZONE, name)
            size = os.path.getsize(fpath) if os.path.isfile(fpath) else 0
            ext = os.path.splitext(name)[1].lower()
            original_files.append({"name": name, "path": fpath, "size": size, "ext": ext})
            log(f"Found: {name} ({size} bytes)")

    if not original_files:
        log("No files in drop zone.", "WARN")

    # Step 2: Extract archives
    log("Step 2: Extracting archives")
    for f in original_files:
        if f["ext"] in ARCHIVE_EXTS:
            dest = os.path.join(UNPACKED, os.path.splitext(f["name"])[0])
            if extract_archive(f["path"], dest):
                pass
            else:
                failed_files.append({"file": f["name"], "reason": "7z extraction failed"})

    # Step 3: Process files
    log("Step 3: Processing files")
    for f in original_files:
        if f["ext"] in ARCHIVE_EXTS:
            continue

        if f["ext"] in TEXT_EXTS:
            dest = os.path.join(TEXT_DIR, f["name"])
            shutil.copy2(f["path"], dest)
            text_files.append({"name": f["name"], "path": dest, "source": "drop zone"})
            log(f"Text: {f['name']}")

        elif f["ext"] in IMAGE_EXTS:
            dest = os.path.join(IMAGE_DIR, f["name"])
            shutil.copy2(f["path"], dest)
            image_files.append({"name": f["name"], "path": dest, "source": "drop zone"})
            log(f"Image: {f['name']}")

        elif f["ext"] in VIDEO_EXTS:
            base = os.path.splitext(f["name"])[0]
            frame_dir = os.path.join(VIDEO_FRAME_DIR, base)
            frames = extract_video_frames(f["path"], frame_dir)
            for fr in frames:
                video_frame_files.append({
                    "name": fr,
                    "path": os.path.join(frame_dir, fr),
                    "source": f["name"]
                })
            if not frames:
                failed_files.append({"file": f["name"], "reason": "FFmpeg frame extraction failed"})

        elif f["ext"] in OFFICE_EXTS:
            base = os.path.splitext(f["name"])[0]
            md_dest = os.path.join(TEXT_DIR, f"{base}.md")
            if convert_office(f["path"], md_dest):
                markdown_files.append({
                    "name": f"{base}.md",
                    "path": md_dest,
                    "source": f["name"],
                    "tool": "MarkItDown"
                })
            else:
                failed_files.append({"file": f["name"], "reason": "MarkItDown conversion failed"})

        elif f["ext"] in AUDIO_EXTS:
            audio_files.append({"name": f["name"], "path": f["path"], "note": "ASR not executed"})
            log(f"Audio registered: {f['name']}")

    # Step 4: Process unpacked files
    log("Step 4: Processing unpacked files")
    for root, dirs, files in os.walk(UNPACKED):
        for name in files:
            fpath = os.path.join(root, name)
            ext = os.path.splitext(name)[1].lower()

            if ext in TEXT_EXTS:
                text_files.append({"name": name, "path": fpath, "source": "unpacked"})
                log(f"Unpacked text: {name}")

            elif ext in IMAGE_EXTS:
                dest = os.path.join(IMAGE_DIR, name)
                shutil.copy2(fpath, dest)
                image_files.append({"name": name, "path": dest, "source": "unpacked"})
                log(f"Unpacked image: {name}")

            elif ext in OFFICE_EXTS:
                base = os.path.splitext(name)[0]
                md_dest = os.path.join(TEXT_DIR, f"{base}.md")
                if convert_office(fpath, md_dest):
                    markdown_files.append({
                        "name": f"{base}.md",
                        "path": md_dest,
                        "source": name,
                        "tool": "MarkItDown"
                    })
                else:
                    failed_files.append({"file": name, "reason": "MarkItDown conversion failed"})

    # Step 5: Build file tree
    log("Step 5: Building file tree")
    file_tree = build_file_tree()

    # Step 6: Extract tasks
    log("Step 6: Extracting task requirements")
    all_text_files = text_files + markdown_files
    for tf in all_text_files:
        content = read_file_safe(tf["path"])
        if content:
            tasks = extract_tasks(content)
            for t in tasks:
                all_tasks.append({"file": tf["name"], "line": t})

    # Step 7: Classify
    log("Step 7: Classifying tasks")
    for t in all_tasks:
        if is_danger(t["line"]):
            need_confirm.append(t)
        else:
            auto_exec.append(t)

    # Step 8: Generate AI_HANDOFF.md
    log("Step 8: Generating AI_HANDOFF.md")

    lines = []
    lines.append("# AI_HANDOFF.md")
    lines.append("")
    lines.append("> AI 文件接收站交接文件")
    lines.append(f"> 处理时间: {start_time}")
    lines.append("> 工具链: 7-Zip / MarkItDown / FFmpeg / Python PIL")
    lines.append(f"> 接收站根目录: {INBOX_ROOT}")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 1. 原始拖入文件清单")
    lines.append("")
    lines.append("| # | 文件名 | 大小 | 类型 |")
    lines.append("|---|--------|------|------|")
    for i, f in enumerate(original_files, 1):
        lines.append(f"| {i} | {f['name']} | {f['size']} | {f['ext']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 2. 解压结果")
    lines.append("")
    unpacked_files = []
    for root, dirs, files in os.walk(UNPACKED):
        for name in files:
            fpath = os.path.join(root, name)
            rel = os.path.relpath(fpath, UNPACKED)
            unpacked_files.append((name, rel))
    if unpacked_files:
        lines.append("| # | 文件名 | 路径 |")
        lines.append("|---|--------|------|")
        for i, (name, rel) in enumerate(unpacked_files, 1):
            lines.append(f"| {i} | {name} | {rel} |")
    else:
        lines.append("无压缩包，或解压无文件。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 3. 文件树")
    lines.append("")
    lines.append("```")
    for ft in file_tree:
        lines.append(ft)
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 4. 可直读文本清单")
    lines.append("")
    lines.append("| # | 文件名 | 路径 | 来源 |")
    lines.append("|---|--------|------|------|")
    for i, tf in enumerate(text_files, 1):
        lines.append(f"| {i} | {tf['name']} | {tf['path']} | {tf.get('source', 'drop zone')} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 5. 已转换 Markdown 清单")
    lines.append("")
    lines.append("| # | 文件名 | 路径 | 来源 | 工具 |")
    lines.append("|---|--------|------|------|------|")
    for i, mf in enumerate(markdown_files, 1):
        lines.append(f"| {i} | {mf['name']} | {mf['path']} | {mf['source']} | {mf['tool']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 6. 图片待多模态清单")
    lines.append("")
    lines.append("| # | 文件名 | 路径 | 来源 |")
    lines.append("|---|--------|------|------|")
    for i, img in enumerate(image_files, 1):
        lines.append(f"| {i} | {img['name']} | {img['path']} | {img.get('source', 'drop zone')} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 7. 视频关键帧待多模态清单")
    lines.append("")
    lines.append("| # | 帧文件名 | 路径 | 来源视频 |")
    lines.append("|---|----------|------|----------|")
    for i, vf in enumerate(video_frame_files, 1):
        lines.append(f"| {i} | {vf['name']} | {vf['path']} | {vf['source']} |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 8. 音频字幕清单")
    lines.append("")
    if audio_files:
        lines.append("| # | 文件名 | 路径 | 备注 |")
        lines.append("|---|--------|------|------|")
        for i, af in enumerate(audio_files, 1):
            lines.append(f"| {i} | {af['name']} | {af['path']} | {af.get('note', '')} |")
    else:
        lines.append("无音频文件。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 9. 从文件中识别出的任务要求")
    lines.append("")
    seen = set()
    if all_tasks:
        for t in all_tasks:
            key = f"{t['file']}:{t['line']}"
            if key not in seen:
                lines.append(f"- **{t['file']}** : {t['line']}")
                seen.add(key)
    else:
        lines.append("未识别到明确任务要求。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 10. 从文件中识别出的命令")
    lines.append("")
    lines.append("未识别到命令。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 11. 可自动执行项")
    lines.append("")
    if auto_exec:
        for a in auto_exec:
            lines.append(f"- **{a['file']}** : {a['line']}")
    else:
        lines.append("无可自动执行项。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 12. 需用户确认项")
    lines.append("")
    if need_confirm:
        for n in need_confirm:
            lines.append(f"- **{n['file']}** : {n['line']} [需确认]")
    else:
        lines.append("无需用户确认项。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 13. 失败文件和失败原因")
    lines.append("")
    if failed_files:
        for f in failed_files:
            lines.append(f"- **{f['file']}** : {f['reason']}")
    else:
        lines.append("无失败文件。")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 14. 下一步给 Claude Code / Kilo 的执行提示词")
    lines.append("")
    lines.append("```")
    lines.append("请先读取本 AI_HANDOFF.md。")
    lines.append("按文件树和索引读取相关文件。")
    lines.append("文本文件直接读取。")
    lines.append("压缩包内容已解压，请读取解压后的文件。")
    lines.append("图片和视频关键帧必须调用多模态模型理解。")
    lines.append("视频不能只看字幕，必须结合关键帧。")
    lines.append("如果文件中包含任务要求或命令，请提取、分类并继续执行。")
    lines.append("安全命令可执行。")
    lines.append("危险命令必须先列出并等待用户确认。")
    lines.append("不要因为原始文件是 ZIP、图片、视频或 Office 文件就说无法读取。")
    lines.append("```")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("## 15. 成熟工具证据")
    lines.append("")
    lines.append("| 工具 | 版本 | 路径 | 用途 |")
    lines.append("|------|------|------|------|")
    lines.append(f"| 7-Zip | NVIDIA App | {SEVEN_ZIP} | 压缩包解压 |")
    lines.append("| FFmpeg | 8.1.1 | ffmpeg | 视频抽帧 |")
    lines.append("| MarkItDown | 0.1.6 | pip | Office 文档转 Markdown |")
    lines.append("| Python | 3.13.12 | python | 脚本执行 |")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append(f"*自动生成于: {start_time}*")

    handoff_content = "\n".join(lines)
    os.makedirs(HANDOFF_DIR, exist_ok=True)
    with open(HANDOFF_FILE, "w", encoding="utf-8") as f:
        f.write(handoff_content)
    log(f"AI_HANDOFF.md written: {HANDOFF_FILE}")

    # Summary
    log("=== Processing Complete ===")
    log(f"Original files: {len(original_files)}")
    log(f"Text files: {len(text_files)}")
    log(f"Markdown converted: {len(markdown_files)}")
    log(f"Images: {len(image_files)}")
    log(f"Video frames: {len(video_frame_files)}")
    log(f"Audio: {len(audio_files)}")
    log(f"Task requirements: {len(all_tasks)}")
    log(f"Auto-executable: {len(auto_exec)}")
    log(f"Need confirm: {len(need_confirm)}")
    log(f"Failed: {len(failed_files)}")

    # Write log
    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"process_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log_lines))

    print(f"\n=== PROCESSING COMPLETE ===")
    print(f"AI_HANDOFF.md: {HANDOFF_FILE}")
    print(f"Log: {log_path}")

    return {
        "original_files": len(original_files),
        "text_files": len(text_files),
        "markdown_files": len(markdown_files),
        "image_files": len(image_files),
        "video_frames": len(video_frame_files),
        "audio_files": len(audio_files),
        "tasks": len(all_tasks),
        "auto_exec": len(auto_exec),
        "need_confirm": len(need_confirm),
        "failed": len(failed_files),
        "failed_list": failed_files,
        "handoff": HANDOFF_FILE
    }

if __name__ == "__main__":
    result = main()
    print("\n" + json.dumps(result, indent=2, ensure_ascii=False))