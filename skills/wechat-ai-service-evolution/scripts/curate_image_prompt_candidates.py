#!/usr/bin/env python3
"""隔离审查外部图片提示词 JSON，只输出候选报告，不修改正式模板库。"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ALLOWED_FIELDS = {
    "id",
    "title",
    "name",
    "description",
    "prompt",
    "negative_prompt",
    "category",
    "tags",
    "source",
    "source_url",
    "source_media",
    "author",
    "license",
    "notes",
}

TEXT_FIELDS = ("title", "name", "description", "prompt", "negative_prompt", "category", "notes")

RISK_PATTERNS = {
    "提示注入": [
        r"ignore\s+(all\s+)?previous",
        r"disregard\s+(all\s+)?instructions",
        r"system\s+prompt",
        r"developer\s+message",
        r"忽略.{0,8}(以上|之前|前面).{0,8}(指令|规则)",
        r"你现在是.{0,30}(系统|管理员|开发者)",
    ],
    "凭据或私钥": [
        r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----",
        r"\b(api[_ -]?key|access[_ -]?token|secret[_ -]?key|password)\b\s*[:=]",
        r"\bAKIA[0-9A-Z]{16}\b",
    ],
    "命令或网络操作": [
        r"\b(curl|wget|powershell|cmd\.exe|bash|sh)\b.{0,80}(https?://|-[a-z])",
        r"\b(nmap|masscan|netcat|nc -[a-z])\b",
        r"\b(rm\s+-rf|del\s+/[sq]|format\s+[a-z]:)",
    ],
    "未成年人成人化": [
        r"\b(child|kid|minor|teen)\b.{0,80}\b(sexy|seductive|lingerie|nude)\b",
        r"\b(sexy|seductive|lingerie|nude)\b.{0,80}\b(child|kid|minor|teen)\b",
        r"(儿童|孩子|未成年|幼女|少年).{0,40}(性感|裸露|内衣|诱惑|成人化)",
    ],
    "冒充或名人换脸": [
        r"\b(deepfake|impersonat(e|ion)|celebrity face swap)\b",
        r"(深度伪造|名人换脸|冒充.{0,12}(本人|官方|客服|警察|医生))",
    ],
}

RELEVANT_TERMS = {
    "家庭", "合影", "照片", "修复", "纪念", "婚礼", "夫妻", "儿童", "生日", "头像",
    "微信", "表情包", "节日", "春节", "端午", "人物", "职业", "小店", "店铺", "商品",
    "产品", "食品", "蛋糕", "海报", "电商", "包装", "农产品", "family", "portrait", "photo",
    "wedding", "child", "birthday", "avatar", "wechat", "product", "food", "poster", "ecommerce",
}

LOW_PRIORITY_TERMS = {
    "nft", "met gala", "dnd", "south park", "ai girlfriend", "ai boyfriend", "虚拟女友",
    "虚拟男友", "吸引力测试", "黄金比例脸", "名人", "政治人物", "游戏素材",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="扫描外部图片提示词 JSON，生成隔离候选报告；不会自动修改正式库。"
    )
    parser.add_argument("input", type=Path, help="外部 JSON 文件")
    parser.add_argument("--output", type=Path, required=True, help="候选报告 JSON 输出路径")
    parser.add_argument(
        "--existing",
        action="append",
        type=Path,
        default=[],
        help="可重复指定，用于查重的已有 JSON；不会被修改",
    )
    return parser.parse_args()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def extract_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        items = payload
    elif isinstance(payload, dict):
        for key in ("items", "templates", "prompts", "data"):
            if isinstance(payload.get(key), list):
                items = payload[key]
                break
        else:
            items = [payload]
    else:
        raise ValueError("JSON 顶层必须是对象或数组")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("候选列表中的每一项都必须是对象")
    return items


def flatten_text(item: dict[str, Any]) -> str:
    values: list[str] = []
    for field in TEXT_FIELDS:
        value = item.get(field)
        if value is not None:
            values.append(str(value))
    tags = item.get("tags")
    if isinstance(tags, list):
        values.extend(str(tag) for tag in tags)
    elif tags is not None:
        values.append(str(tags))
    return "\n".join(values)


def normalized_fingerprint(item: dict[str, Any]) -> str:
    basis = str(item.get("prompt") or item.get("description") or item.get("title") or item.get("name") or "")
    normalized = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", basis.casefold())
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest() if normalized else ""


def collect_existing_fingerprints(paths: list[Path]) -> set[str]:
    fingerprints: set[str] = set()
    for path in paths:
        for item in extract_items(load_json(path)):
            fingerprint = normalized_fingerprint(item)
            if fingerprint:
                fingerprints.add(fingerprint)
    return fingerprints


def find_risks(text: str) -> list[str]:
    hits: list[str] = []
    for label, patterns in RISK_PATTERNS.items():
        if any(re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL) for pattern in patterns):
            hits.append(label)
    return hits


def purpose_score(text: str) -> tuple[int, list[str]]:
    lowered = text.casefold()
    matched = sorted(term for term in RELEVANT_TERMS if term in lowered)
    score = min(5, len(matched))
    if any(term in lowered for term in LOW_PRIORITY_TERMS):
        score -= 3
    return score, matched[:12]


def sanitize_item(item: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    unknown = sorted(set(item) - ALLOWED_FIELDS)
    sanitized = {key: item[key] for key in ALLOWED_FIELDS if key in item}
    return sanitized, unknown


def inspect(items: list[dict[str, Any]], existing: set[str]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    seen = set(existing)
    results: list[dict[str, Any]] = []
    counts = {"candidate": 0, "manual_review": 0, "rejected": 0, "duplicate": 0}

    for index, raw in enumerate(items, start=1):
        item, unknown = sanitize_item(raw)
        text = flatten_text(item)
        risks = find_risks(text)
        score, matched_terms = purpose_score(text)
        fingerprint = normalized_fingerprint(item)
        duplicate = bool(fingerprint and fingerprint in seen)
        if fingerprint:
            seen.add(fingerprint)

        missing = []
        if not (item.get("title") or item.get("name")):
            missing.append("title/name")
        if not (item.get("prompt") or item.get("description")):
            missing.append("prompt/description")
        if not (item.get("source_url") or item.get("source")):
            missing.append("source_url/source")

        reasons: list[str] = []
        if risks:
            status = "rejected"
            reasons.append("命中高风险特征：" + "、".join(risks))
        elif duplicate:
            status = "duplicate"
            reasons.append("与本批或已有 JSON 的规范化提示词重复")
        elif score <= 0:
            status = "rejected"
            reasons.append("与家庭照片、中年微信联系人或本地小商家用途不匹配")
        elif missing or unknown or score < 2:
            status = "manual_review"
            if missing:
                reasons.append("缺少字段：" + "、".join(missing))
            if unknown:
                reasons.append("已隔离非白名单字段：" + "、".join(unknown))
            if score < 2:
                reasons.append("用途匹配证据不足")
        else:
            status = "candidate"
            reasons.append("通过静态字段、安全、用途和重复检查；仍需人工与真实案例复验")

        counts[status] += 1
        results.append(
            {
                "input_index": index,
                "status": status,
                "reasons": reasons,
                "risk_hits": risks,
                "purpose_score": score,
                "matched_terms": matched_terms,
                "unknown_fields_removed": unknown,
                "fingerprint_sha256": fingerprint or None,
                "candidate": item,
            }
        )
    return results, counts


def main() -> int:
    args = parse_args()
    try:
        raw_bytes = args.input.read_bytes()
        items = extract_items(json.loads(raw_bytes.decode("utf-8-sig")))
        existing = collect_existing_fingerprints(args.existing)
        results, counts = inspect(items, existing)
        report = {
            "schema_version": 1,
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "mode": "isolated_candidate_report_only",
            "auto_ingest": False,
            "source_file": str(args.input.resolve()),
            "source_sha256": hashlib.sha256(raw_bytes).hexdigest(),
            "existing_files_checked": [str(path.resolve()) for path in args.existing],
            "allowed_fields": sorted(ALLOWED_FIELDS),
            "counts": {"total": len(items), **counts},
            "results": results,
            "next_step": "人工核验来源、授权、示例与中文配方；用自有或获授权素材试做，未达 3 个独立成功案例不得标为可用。",
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(report["counts"], ensure_ascii=False))
        print(f"候选报告已写入：{args.output.resolve()}")
        print("未修改任何正式模板库或服务登记表。")
        return 0
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"扫描失败：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
