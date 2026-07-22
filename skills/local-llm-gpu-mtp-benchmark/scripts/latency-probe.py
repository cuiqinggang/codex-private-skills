import json
import time
import urllib.request


BASE_URL = "http://127.0.0.1:1234/v1"
MODEL = "qwen3.6-27b-iq4-xs-mtp"


def probe(prompt: str, max_tokens: int = 180):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "你是一个中文助手。必须用简体中文回答。"},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.2,
        "max_tokens": max_tokens,
        "stream": True,
    }
    req = urllib.request.Request(
        BASE_URL + "/chat/completions",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    start = time.perf_counter()
    first = None
    parts = []
    with urllib.request.urlopen(req, timeout=180) as resp:
        for raw in resp:
            line = raw.decode("utf-8", errors="replace").strip()
            if not line.startswith("data: "):
                continue
            data = line[6:]
            if data == "[DONE]":
                break
            obj = json.loads(data)
            delta = obj["choices"][0].get("delta", {}).get("content", "")
            if delta:
                if first is None:
                    first = time.perf_counter()
                parts.append(delta)
    end = time.perf_counter()
    text = "".join(parts)
    elapsed = end - start
    return {
        "ttft_sec": round((first - start) if first else elapsed, 3),
        "total_sec": round(elapsed, 3),
        "chars": len(text),
        "chars_per_sec": round(len(text) / elapsed, 2) if elapsed else None,
        "preview": text[:200],
    }


if __name__ == "__main__":
    result = probe("请用约200个汉字说明本地27B模型当前是否适合放在Kilo里作为可选模型。")
    print(json.dumps(result, ensure_ascii=False, indent=2))
