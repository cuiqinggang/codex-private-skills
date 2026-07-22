#!/usr/bin/env python3
import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXPLICIT = re.compile(r"(找|寻找|推荐|比较|替代|有没有).{0,12}(免费|公共|开放|无需.{0,3}(key|密钥)|api|接口)|free public api|public api|api alternative", re.I)
DATA = re.compile(r"天气|地图|汇率|新闻|图片|音乐|电影|测试数据|地理编码|文件(转换|处理)|机器学习|weather|maps?|exchange rate|news|image|music|movie|test data|geocod|document|machine learning", re.I)
NEED = re.compile(r"缺少|需要|依赖|数据源|接口|api|不可用|收费|额度|cors|external data", re.I)
BLOCK = re.compile(r"绕过|破解|规避.{0,6}(付费|认证|限速|访问)|bypass|只有本地|离线数据足够|已(经)?指定.{0,30}(只写|调用代码|api)|只(需|要).{0,8}(调用|代码|修复)", re.I)

def classify(text):
    if BLOCK.search(text): return "P0", "禁止场景、已有唯一数据源或只需既定 API 代码"
    if EXPLICIT.search(text): return "P1", "明确要求寻找、比较或替换公共 API"
    if DATA.search(text) and NEED.search(text): return "P2", "开发任务明确缺少外部数据源"
    if DATA.search(text): return "P3", "外部数据源可能有帮助，但尚非必要"
    return "P0", "语义上不是第三方数据服务发现任务"

def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ap=argparse.ArgumentParser(); ap.add_argument("--text", required=True); ap.add_argument("--log", type=Path)
    a=ap.parse_args(); level, reason=classify(a.text)
    rec={"timestamp":datetime.now(timezone.utc).astimezone().isoformat(),"route_id":"ROUTE-PUBLIC-API-DISCOVERY","trigger_level":level,"reason":reason,"user_need":a.text,"skill_called":level in {"P1","P2"},"external_api_called":False,"official_docs_verified":False}
    if a.log:
        a.log.parent.mkdir(parents=True, exist_ok=True)
        with a.log.open("a", encoding="utf-8") as f: f.write(json.dumps(rec, ensure_ascii=False)+"\n")
    print(json.dumps(rec, ensure_ascii=False, indent=2))

if __name__ == "__main__": main()
