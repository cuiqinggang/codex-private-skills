"""
AI File Inbox Processor - MarkItDown conversion helper
Converts Office documents to Markdown using MarkItDown.
Usage: python convert_office.py <input_file> <output_md>
"""
import sys
import os
from markitdown import MarkItDown

def convert(input_path, output_path):
    md = MarkItDown()
    result = md.convert(input_path)
    text = result.text_content
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"OK: {os.path.basename(input_path)} -> {os.path.basename(output_path)} ({len(text)} chars)")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python convert_office.py <input> <output>")
        sys.exit(1)
    convert(sys.argv[1], sys.argv[2])
