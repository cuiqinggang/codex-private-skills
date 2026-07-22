#!/usr/bin/env python3
"""从用户授权的签名图片生成自包含 SVG 练习纸。"""

from __future__ import annotations

import argparse
import base64
import html
import mimetypes
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="生成可打印的签名练习纸 SVG")
    parser.add_argument("--name", required=True, help="已确认姓名，仅写入本地练习纸")
    parser.add_argument("--variant-label", default="定稿方案", help="方案名称")
    parser.add_argument("--signature-image", required=True, help="用户授权使用的 PNG/JPG/SVG 签名图")
    parser.add_argument("--output", required=True, help="输出 SVG 路径")
    return parser.parse_args()


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> int:
    args = parse_args()
    image_path = Path(args.signature_image).resolve()
    output_path = Path(args.output).resolve()
    if not image_path.is_file():
        raise SystemExit(f"签名图不存在：{image_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    uri = data_uri(image_path)

    rows = []
    opacities = (1.0, 0.55, 0.25, 0.0)
    for row in range(4):
        y = 210 + row * 250
        cells = []
        for col, opacity in enumerate(opacities):
            x = 70 + col * 260
            cells.append(f'<rect x="{x}" y="{y}" width="230" height="180" fill="none" stroke="#b9c2cc"/>')
            if opacity:
                cells.append(f'<use href="#signature-source" x="{x + 12}" y="{y + 20}" opacity="{opacity}"/>')
        rows.append("\n".join(cells))

    title = html.escape(args.name)
    label = html.escape(args.variant_label)
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="1320" viewBox="0 0 1120 1320">
  <defs>
    <image id="signature-source" href="{uri}" width="206" height="140" preserveAspectRatio="xMidYMid meet"/>
  </defs>
  <rect width="1120" height="1320" fill="#ffffff"/>
  <text x="70" y="80" font-family="Microsoft YaHei, sans-serif" font-size="36" fill="#173A67">中文姓名艺术签名练习纸</text>
  <text x="70" y="132" font-family="Microsoft YaHei, sans-serif" font-size="24" fill="#333333">姓名：{title}　方案：{label}</text>
  <text x="70" y="174" font-family="Microsoft YaHei, sans-serif" font-size="18" fill="#666666">看范写 → 半透明跟写 → 淡线复写 → 独立书写，最后做真人三写测试。</text>
  {''.join(rows)}
  <text x="70" y="1240" font-family="Microsoft YaHei, sans-serif" font-size="17" fill="#666666">三写记录：第1次____秒 / ____次抬笔　 第2次____秒 / ____次抬笔　 第3次____秒 / ____次抬笔</text>
  <text x="70" y="1280" font-family="Microsoft YaHei, sans-serif" font-size="16" fill="#8a3b2b">仅供本人练习；未经授权不要公开他人的姓名或笔迹。</text>
</svg>
'''
    output_path.write_text(svg, encoding="utf-8", newline="\n")
    print(f"已生成：{output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
