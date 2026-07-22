"""Guarded Douyin single-comment reply helpers for Windows.

The safe default is evidence generation. Public sending requires an explicit
confirmation token and must only follow visible reply-context verification.
"""

from __future__ import annotations

import argparse
import ctypes
import os
import sys
import time
from datetime import datetime
from pathlib import Path

from PIL import ImageDraw, ImageFont, ImageGrab


MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004
KEYEVENTF_KEYUP = 0x0002
VK_CONTROL = 0x11
VK_V = 0x56
VK_RETURN = 0x0D


def enable_per_monitor_dpi() -> None:
    """Enable physical coordinates before any screen/cursor API call."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except (AttributeError, OSError):
        pass


def parse_ints(value: str, count: int, label: str) -> tuple[int, ...]:
    parts = tuple(int(part.strip()) for part in value.split(","))
    if len(parts) != count:
        raise argparse.ArgumentTypeError(f"{label} requires {count} comma-separated integers")
    return parts


def output_dir(path: str | None) -> Path:
    base = Path(path) if path else Path.cwd() / "outputs" / "douyin-auto-reply"
    base.mkdir(parents=True, exist_ok=True)
    return base.resolve()


def screenshot(bbox: tuple[int, int, int, int]):
    return ImageGrab.grab(bbox=bbox, all_screens=True)


def draw_grid(image, step: int, target: tuple[int, int] | None = None):
    if step < 10 or step > 100:
        raise ValueError("grid step must be between 10 and 100 pixels")
    draw = ImageDraw.Draw(image)
    major = step * 4
    for x in range(0, image.width + 1, step):
        color = (255, 255, 255) if x % major == 0 else (255, 35, 35)
        draw.line((x, 0, x, image.height), fill=color, width=2 if x % major == 0 else 1)
    for y in range(0, image.height + 1, step):
        color = (255, 255, 255) if y % major == 0 else (0, 255, 80)
        draw.line((0, y, image.width, y), fill=color, width=2 if y % major == 0 else 1)
    for x in range(0, image.width, major):
        draw.text((x + 3, 3), str(x), fill=(255, 255, 0))
    for y in range(0, image.height, major):
        draw.text((3, y + 16), str(y), fill=(255, 255, 0))
    if target:
        tx, ty = target
        radius = max(10, step)
        draw.ellipse((tx - radius, ty - radius, tx + radius, ty + radius), outline=(255, 230, 0), width=5)
        draw.line((tx - radius * 2, ty, tx + radius * 2, ty), fill=(255, 230, 0), width=3)
        draw.line((tx, ty - radius * 2, tx, ty + radius * 2), fill=(255, 230, 0), width=3)
    return image


def command_grid(args: argparse.Namespace) -> int:
    bbox = parse_ints(args.screen_bbox, 4, "--screen-bbox")
    crop_x, crop_y, crop_w, crop_h = parse_ints(args.crop, 4, "--crop")
    target = parse_ints(args.target, 2, "--target") if args.target else None
    image = screenshot(bbox)
    if crop_x < 0 or crop_y < 0 or crop_w <= 0 or crop_h <= 0:
        raise ValueError("crop values must be monitor-image coordinates with positive width/height")
    crop = image.crop((crop_x, crop_y, crop_x + crop_w, crop_y + crop_h))
    draw_grid(crop, args.grid_step, target)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = output_dir(args.output_dir) / f"douyin-grid-{args.grid_step}px-{stamp}.png"
    crop.save(path)
    print(f"CHAT_IMAGE_REQUIRED={path}")
    print("NEXT=Embed the image in chat and explain the target grid before any click")
    return 0


def command_click(args: argparse.Namespace) -> int:
    if args.confirm_click != "CLICK_REPLY":
        raise SystemExit("Refusing click: pass --confirm-click CLICK_REPLY after current grid review")
    ctypes.windll.user32.SetCursorPos(args.x, args.y)
    time.sleep(0.2)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.12)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"CLICKED=({args.x},{args.y})")
    print("NEXT=Capture and visibly send the reply-context screenshot; do not paste yet")
    return 0


def set_clipboard(text: str) -> None:
    import tkinter as tk

    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()
    root.destroy()


def key_event(vk: int, up: bool = False) -> None:
    ctypes.windll.user32.keybd_event(vk, 0, KEYEVENTF_KEYUP if up else 0, 0)


def command_paste(args: argparse.Namespace) -> int:
    if not args.confirm_context.strip():
        raise SystemExit("Refusing paste: --confirm-context must name the visibly verified reply target")
    text = Path(args.text_file).read_text(encoding="utf-8").strip()
    if not text:
        raise SystemExit("Refusing paste: reply text is empty")
    set_clipboard(text)
    key_event(VK_CONTROL)
    key_event(VK_V)
    key_event(VK_V, up=True)
    key_event(VK_CONTROL, up=True)
    print(f"PASTED_FOR_CONTEXT={args.confirm_context}")
    print("NEXT=Capture and visibly send the text/context screenshot; do not send yet")
    return 0


def command_send(args: argparse.Namespace) -> int:
    if args.confirm_send != "SEND_PUBLIC_REPLY":
        raise SystemExit("Refusing public send: pass --confirm-send SEND_PUBLIC_REPLY after action-time confirmation")
    key_event(VK_RETURN)
    key_event(VK_RETURN, up=True)
    print("PUBLIC_SEND_KEY_PRESSED=Return")
    print("NEXT=Capture and visibly send proof that the result is a nested reply, not an independent comment")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Guarded Douyin coordinate screenshot reply helper")
    sub = parser.add_subparsers(dest="command", required=True)

    grid = sub.add_parser("grid", help="capture and generate a visible coordinate grid")
    grid.add_argument("--screen-bbox", required=True, help="left,top,right,bottom in physical virtual-screen coordinates")
    grid.add_argument("--crop", required=True, help="x,y,width,height inside the captured monitor image")
    grid.add_argument("--grid-step", type=int, default=25)
    grid.add_argument("--target", help="optional x,y target inside the crop")
    grid.add_argument("--output-dir")
    grid.set_defaults(func=command_grid)

    click = sub.add_parser("click", help="perform one DPI-aware negative-coordinate click")
    click.add_argument("--x", type=int, required=True)
    click.add_argument("--y", type=int, required=True)
    click.add_argument("--confirm-click", required=True)
    click.set_defaults(func=command_click)

    paste = sub.add_parser("paste", help="paste UTF-8 reply text without Ctrl+A")
    paste.add_argument("--text-file", required=True)
    paste.add_argument("--confirm-context", required=True)
    paste.set_defaults(func=command_paste)

    send = sub.add_parser("send", help="press Return only after explicit public-send confirmation")
    send.add_argument("--confirm-send", required=True)
    send.set_defaults(func=command_send)
    return parser


def main() -> int:
    if os.name != "nt":
        raise SystemExit("This helper is Windows-only")
    enable_per_monitor_dpi()
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
