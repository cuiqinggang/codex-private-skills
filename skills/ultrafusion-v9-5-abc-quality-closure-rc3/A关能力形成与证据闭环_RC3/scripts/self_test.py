from pathlib import Path
import json, hashlib, sys

root = Path(__file__).resolve().parents[1]
required = [
"00_先看这里/README_能力形成来源层.md",
"01_能力来源与成熟度/01_A关能力来源链.md",
"01_能力来源与成熟度/02_A关能力成熟度等级.md",
"01_能力来源与成熟度/03_能力来源账本.json",
"02_A关正式量化合同/A关正式量化测试合同_RC1_冻结版.md",
"03_A关测试网站/index.html",
"03_A关测试网站/style.css",
"03_A关测试网站/app.js",
"04_十二道关口与证据矩阵/01_十二道核心关口详细规范.md",
"04_十二道关口与证据矩阵/02_十二项图片证据矩阵模板.md",
"05_模拟与真实测试/十次模拟检测报告_10_OF_10_PASS.md",
"05_模拟与真实测试/十次模拟检测原始结果.json",
"06_发布闸门与版本治理/01_版本治理与发布闸门.md",
"06_发布闸门与版本治理/02_Codex只读集成说明.md",
"07_技能触发与运行规则/01_SKILL增量运行规则.md",
]
missing=[x for x in required if not (root/x).exists()]
results=json.loads((root/"05_模拟与真实测试/十次模拟检测原始结果.json").read_text(encoding="utf-8"))
sim_ok=len(results)==10 and all(x.get("match") for x in results)
ledger=json.loads((root/"01_能力来源与成熟度/03_能力来源账本.json").read_text(encoding="utf-8"))
level_ok=ledger.get("current_maturity")=="L3_SIMULATION_VALIDATED"
evidence_count=len(list((root/"evidence_templates").glob("*.txt")))
weights=[15,25,15,20,15,10]
evidence_files=sorted((root/"05_模拟与真实测试/十次模拟原始证据").glob("*.json"))
weighted_pressure_ok=len(evidence_files)==10
for evidence_file in evidence_files:
    evidence=json.loads(evidence_file.read_text(encoding="utf-8"))
    actions=evidence.get("input",{}).get("actions",[])
    expected_pressure=sum(weight*int(bool(action)) for weight,action in zip(weights,actions))
    weighted_pressure_ok = weighted_pressure_ok and len(actions)==6 and evidence.get("result",{}).get("pressure")==expected_pressure
weighted_pressure_ok = weighted_pressure_ok and all(x.get("pressure")==100 for x in results)
prompt=root/"03_A关测试网站/assets/V15.1-A_正式只读提示词.txt"
prompt_hash=hashlib.sha256(prompt.read_bytes()).hexdigest().upper() if prompt.exists() else None
readonly_prompt_ok=prompt_hash=="1E85CF5234527B7F491823EF8755C6940D4FD96C608B0D0866A0CFE8D0BF4EDE"
site_test_file=root/"03_A关测试网站/docs/10轮站点系统测试结果_RC3.json"
site_test=json.loads(site_test_file.read_text(encoding="utf-8")) if site_test_file.exists() else {}
site_system_10_of_10=(site_test.get("tests")==10 and site_test.get("passed")==10 and site_test.get("failed")==0)
deployment=ledger.get("site_deployment",{})
private_site_deployed=(
    ledger.get("site_status")=="PRIVATE_CODEX_SITE_DEPLOYED_SUCCEEDED"
    and deployment.get("deployment_status")=="succeeded"
    and deployment.get("access_mode")=="custom_owner_only"
    and deployment.get("allowed_users")==1
    and deployment.get("allowed_groups")==0
    and str(deployment.get("url","")).startswith("https://")
)
manifest_path=root/"00_先看这里/FILE_MANIFEST.json"
manifest=json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else []
manifest_verified=bool(manifest)
for entry in manifest:
    path=root/entry.get("path","")
    manifest_verified=(manifest_verified and path.is_file()
        and path.stat().st_size==entry.get("size")
        and hashlib.sha256(path.read_bytes()).hexdigest().upper()==entry.get("sha256"))
ok=(not missing and sim_ok and level_ok and evidence_count==12 and weighted_pressure_ok
    and readonly_prompt_ok and site_system_10_of_10 and private_site_deployed and manifest_verified)
print(json.dumps({
"status":"PASS" if ok else "FAIL",
"missing_files":missing,
"simulation_10_of_10":sim_ok,
"weighted_pressure_0_to_100":weighted_pressure_ok,
"readonly_prompt_sha256_verified":readonly_prompt_ok,
"readonly_prompt_sha256":prompt_hash,
"site_system_test_10_of_10":site_system_10_of_10,
"private_site_deployed_owner_only":private_site_deployed,
"site_url":deployment.get("url"),
"manifest_entries":len(manifest),
"manifest_verified":manifest_verified,
"maturity_level_locked_at_L3":level_ok,
"evidence_template_count":evidence_count
},ensure_ascii=False,indent=2))
sys.exit(0 if ok else 1)
