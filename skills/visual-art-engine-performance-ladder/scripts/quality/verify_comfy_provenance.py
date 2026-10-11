#!/usr/bin/env python3
"""Read-only ComfyUI source guard. DOES NOT generate pictures or certify visual quality.

Usage:
  python verify_comfy_provenance.py --dir EVIDENCE --mode T2I_INDEPENDENT --api http://127.0.0.1:8188 --output-root COMFY_OUTPUT

Expected: workflow_api.json, workflow.sha256, submit.json, history.json,
          generated.png, output.sha256. For image-conditioned paths, input
          hash verification is an additional human-side obligation.
This is a minimal task-specific validator, not a tool router or scheduler.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
from urllib.request import urlopen

ALLOWED = {
    "UNETLoader", "DualCLIPLoader", "VAELoader", "CLIPTextEncode", "ConditioningZeroOut",
    "FluxGuidance", "EmptySD3LatentImage", "EmptyLatentImage", "KSampler", "VAEDecode", "SaveImage",
}

class AuditError(Exception):
    pass


def check(ok, message):
    if not ok:
        raise AuditError(message)


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def refs(value):
    if isinstance(value, list) and len(value) == 2 and str(value[0]).isdigit() and isinstance(value[1], int):
        return [str(value[0])]
    if isinstance(value, dict):
        return [r for x in value.values() for r in refs(x)]
    if isinstance(value, list):
        return [r for x in value for r in refs(x)]
    return []


def ancestors(workflow, nodeid, seen=None):
    seen = set() if seen is None else seen
    if nodeid in seen:
        return seen
    check(nodeid in workflow, "MISSING_NODE_REFERENCE:" + nodeid)
    seen.add(nodeid)
    for prev in refs(workflow[nodeid].get("inputs", {})):
        ancestors(workflow, prev, seen)
    return seen


def verify_workflow(workflow, mode):
    check(isinstance(workflow, dict), "INVALID_WORKFLOW")
    types = {node.get("class_type") for node in workflow.values()}
    sampler = [key for key, node in workflow.items() if node.get("class_type") == "KSampler"]
    save = [key for key, node in workflow.items() if node.get("class_type") == "SaveImage"]
    check(len(sampler) == 1 and len(save) == 1, "REQUIRE_ONE_SAMPLER_AND_SAVE")
    chain = ancestors(workflow, save[0])
    check(sampler[0] in chain, "SAVE_NOT_LINKED_TO_SAMPLER")
    latent = workflow[sampler[0]].get("inputs", {}).get("latent_image")
    check(isinstance(latent, list) and len(latent) == 2, "UNKNOWN_LATENT_SOURCE")
    latentid = str(latent[0])
    latent_ancestors = ancestors(workflow, latentid)
    latent_types = {workflow[x]["class_type"] for x in latent_ancestors}
    if mode == "T2I_INDEPENDENT":
        check(types <= ALLOWED, "UNAPPROVED_OR_IMAGE_INPUT_NODE")
        check(workflow[latentid]["class_type"] in {"EmptySD3LatentImage", "EmptyLatentImage"}, "NOT_BLANK_LATENT")
        check(not types.intersection({"LoadImage", "VAEEncode", "ReferenceLatent", "ControlNetApply", "ControlNetApplyAdvanced"}), "IMAGE_CONDITION_IN_INDEPENDENT_TASK")
    elif mode == "IMG2IMG":
        check("VAEEncode" in latent_types and "LoadImage" in latent_types, "NOT_REAL_IMG2IMG")
    elif mode == "REF_CONDITIONED":
        check(workflow[latentid]["class_type"] in {"EmptySD3LatentImage", "EmptyLatentImage"}, "NOT_BLANK_LATENT")
        positive = workflow[sampler[0]].get("inputs", {}).get("positive")
        check(isinstance(positive, list) and len(positive) == 2, "REFERENCE_CONDITION_NOT_CONNECTED")
        positive_types = {workflow[x]["class_type"] for x in ancestors(workflow, str(positive[0]))}
        check(bool(positive_types.intersection({"ReferenceLatent", "ControlNetApply", "ControlNetApplyAdvanced"})), "NO_CONNECTED_REFERENCE_CONDITION")
        check("LoadImage" in types, "NO_REFERENCE_SOURCE_IMAGE")
    elif mode == "EDIT_INPAINT":
        raise AuditError("EDIT_INPAINT_REQUIRES_ADDITIONAL_MASK_AND_SCOPE_REVIEW")
    else:
        raise AuditError("INVALID_MODE")
    return save[0]


def live_history(base, prompt_id):
    check(base.startswith("http://127.0.0.1:") or base.startswith("http://localhost:"), "API_MUST_BE_LOCAL_LOOPBACK")
    with urlopen(base.rstrip("/") + "/history/" + prompt_id, timeout=15) as response:
        data = json.load(response)
    check(prompt_id in data, "LIVE_HISTORY_MISSING")
    return data[prompt_id]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dir", required=True)
    parser.add_argument("--mode", required=True, choices=["T2I_INDEPENDENT", "REF_CONDITIONED", "IMG2IMG", "EDIT_INPAINT"])
    parser.add_argument("--api", help="Local ComfyUI API. Required for runtime provenance certification")
    parser.add_argument("--output-root", help="ComfyUI output directory, required with --api")
    args = parser.parse_args()
    directory = Path(args.dir)
    try:
        wf_path = directory / "workflow_api.json"
        wf_hash = (directory / "workflow.sha256").read_text().strip().lower()
        check(sha256_file(wf_path) == wf_hash, "WORKFLOW_SHA_MISMATCH")
        workflow = read_json(wf_path)
        save_id = verify_workflow(workflow, args.mode)
        if not args.api or not args.output_root:
            print(json.dumps({"status":"PREFLIGHT_ONLY", "G1":"PASS", "G2":"UNVERIFIED", "FINAL_VALID":"NO"}))
            return 0
        submit = read_json(directory / "submit.json")
        response = submit.get("result", submit.get("prompt_response", submit))
        prompt_id = response.get("prompt_id")
        check(isinstance(prompt_id, str) and len(prompt_id) >= 20, "NO_NATIVE_COMFY_PROMPT_ID")
        check(not response.get("node_errors"), "SUBMIT_NODE_ERRORS")
        historical = read_json(directory / "history.json")
        if prompt_id in historical:
            historical = historical[prompt_id]
        current = live_history(args.api, prompt_id)
        check(historical == current, "SAVED_HISTORY_VS_LIVE_HISTORY_MISMATCH")
        check(current.get("status", {}).get("status_str") == "success" and current.get("status", {}).get("completed") is True, "NOT_SUCCESSFUL_COMFY_RUN")
        check(current["prompt"][1] == prompt_id, "HISTORY_PROMPT_ID_MISMATCH")
        check(current["prompt"][2] == workflow, "HISTORY_WORKFLOW_MISMATCH")
        files = current.get("outputs", {}).get(str(save_id), {}).get("images", [])
        check(len(files) == 1 and files[0]["type"] == "output", "HISTORY_SAVEIMAGE_MISSING")
        out_root = Path(args.output_root).resolve()
        path = (out_root / files[0].get("subfolder", "") / files[0]["filename"]).resolve()
        check(os.path.commonpath([str(path), str(out_root)]) == str(out_root), "UNSAFE_OUTPUT_PATH")
        check(path.is_file(), "ORIGINAL_COMFY_OUTPUT_MISSING")
        gen = directory / "generated.png"
        check(gen.is_file(), "EVIDENCE_GENERATED_MISSING")
        computed = sha256_file(gen)
        check(sha256_file(path) == computed, "HISTORY_OUTPUT_VS_EVIDENCE_PNG_MISMATCH")
        check((directory / "output.sha256").read_text().strip().split()[0].lower() == computed, "RECORDED_PNG_SHA_MISMATCH")
        with gen.open("rb") as stream:
            check(stream.read(8) == b"\x89PNG\r\n\x1a\n", "NOT_PNG")
        print(json.dumps({"status":"FILE_PROVENANCE_VERIFIED", "G1":"PASS", "G2":"PASS", "G3":"MANUAL_QUALITY_REQUIRED", "G4":"LIVE_HISTORY_RECHECKED", "FINAL_VALID":"NO_UNTIL_QUALITY", "prompt_id":prompt_id, "png_sha256":computed}, ensure_ascii=False))
        return 0
    except (AuditError, OSError, KeyError, ValueError, TypeError) as error:
        print(json.dumps({"status":"INVALID_OR_UNVERIFIED", "reason":str(error), "FINAL_VALID":"NO"}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
