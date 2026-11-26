import io
import json
import pathlib
import runpy
import sys
import tempfile
import urllib.error
from unittest.mock import patch

root = pathlib.Path(__file__).resolve().parents[1]
app = runpy.run_path(str(root / "run-v1.3.1.py"))["main"]
state = app.__globals__
url = "https://v.douyin.com/mjLFvVgNbu0/"
failure = urllib.error.HTTPError("https://demo.douyin.wtf/api/v1/parse", 503, "Service Unavailable", {}, io.BytesIO(b'{"error":{"code":"ENDPOINT_CIRCUIT_OPEN","retry_after":292}}'))
with tempfile.TemporaryDirectory(dir=root / "work") as tmp:
    out = pathlib.Path(tmp)
    report = {}
    with patch.dict(state, DESKTOP=out, save_report=report.update, clipboard_text=lambda: url), patch.dict(sys.modules, {}), patch.object(sys, "argv", ["run-v1.3.1.py", "--interactive"]), patch.dict(state, json_request=__import__("unittest.mock", fromlist=["Mock"]).Mock(side_effect=failure)):
        assert app() == 0, report
    assert report["route"] == "OFFICIAL_PUBLIC_SHARE" and report["source_full_decode"] == "PASS", report
    assert report["video_id"] == "7711392781416157001" and pathlib.Path(report["output"]).is_file()
    report.update(test="Injected third-party HTTP 503 and clipboard input; real official network, download and decode; isolated output")
    (root / "acceptance-v1.3.1.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(report["probe"], report["bytes"])
