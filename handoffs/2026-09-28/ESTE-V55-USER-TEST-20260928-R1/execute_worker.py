"""从冻结候选 tests/test_integration.py 的 execute_data/execute 分支提取的现实执行载荷。
仅处理本01包输入；不包含 receipt/restore/测试审核角色。
"""
from pathlib import Path
import json
import sys

def execute_data(source, target, corrupt=False):
    """独立执行进程：只读输入、计算、写出；不知道审核器的预期字节。"""
    rows = json.loads(Path(source).read_bytes())
    unique = {}
    for row in rows:
        key = row['任务编号']
        if key in unique and unique[key] != row:
            raise ValueError('重复任务编号内容冲突')
        unique[key] = row
    ordered = sorted(unique.values(), key=lambda row: (row['优先级'], row['任务编号']))
    if corrupt:
        ordered[0] = dict(ordered[0], 任务='故意错误产物')
    Path(target).write_bytes((json.dumps(ordered, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode('utf-8'))

if __name__ == "__main__":
    if len(sys.argv) < 4 or sys.argv[1] != "execute":
        raise SystemExit("usage: execute_worker.py execute SOURCE TARGET")
    execute_data(sys.argv[2], sys.argv[3], len(sys.argv) > 4 and sys.argv[4] == "corrupt")
