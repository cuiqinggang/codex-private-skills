import argparse
import json
from pathlib import Path


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--local", required=True)
    parser.add_argument("--postdeploy")
    parser.add_argument("--screenshots", required=True)
    args = parser.parse_args()

    errors = []
    local = load(args.local)
    cases = local.get("cases", [])
    if local.get("result") != "5/5 PASS":
        errors.append("local result is not 5/5 PASS")
    if len(cases) != 5 or any(case.get("result") != "PASS" for case in cases):
        errors.append("VT case results are incomplete")
    if local.get("severe_regressions") != 0:
        errors.append("severe regressions must be 0")
    if local.get("console_errors") != 0:
        errors.append("local console errors must be 0")
    if local.get("real_samples") != 0 or local.get("maturity") != "L3" or local.get("decision") != "REVISE":
        errors.append("capability boundary changed")

    screenshots = list(Path(args.screenshots).glob("*.png"))
    if len(screenshots) != 15:
        errors.append(f"expected 15 screenshots, found {len(screenshots)}")

    post = None
    if args.postdeploy:
        post = load(args.postdeploy)
        if post.get("deployment_status") != "succeeded":
            errors.append("deployment did not succeed")
        commits = {post.get("local_commit"), post.get("remote_main_commit"), post.get("saved_version_commit")}
        if None in commits or len(commits) != 1:
            errors.append("local/remote/Sites commits differ")
        if post.get("console_errors") != 0:
            errors.append("production console errors must be 0")
        if post.get("online_full_e2e") != "VT-01 PASS" or len(post.get("online_key_paths", [])) != 4:
            errors.append("production 1+4 verification is incomplete")
        if post.get("real_samples") != 0 or post.get("maturity") != "L3" or post.get("decision") != "REVISE":
            errors.append("production capability boundary changed")

    result = {
        "result": "PASS" if not errors else "BLOCKED",
        "errors": errors,
        "screenshots": len(screenshots),
        "local_cases": len(cases),
        "postdeploy_checked": post is not None,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if not errors else 2)


if __name__ == "__main__":
    main()

