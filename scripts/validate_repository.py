#!/usr/bin/env python3
from __future__ import annotations
import argparse, fnmatch, hashlib, json, re, sys
from pathlib import Path

EXPECTED={"ordinary":181,"active":190,"inactive":4,"unique_routed":194}
CATALOG=["skill-inventory.json","sanitization-manifest.json","system-skills.json","inactive-skills.json","repository-schema.json"]
BINARY={".png",".jpg",".jpeg",".gif",".webp",".ico",".woff",".woff2",".ttf"}
DENY=(".env",".env.*","*.pem","*.key","id_rsa*","credentials*.json","auth*.json","cookies*","config.toml","*.sqlite","*.db")
_SENSITIVE_KEYS="pass"+"word|pass"+"wd|sec"+"ret|api[_-]?"+"key|access[_-]?"+"token|coo"+"kie|connection[_-]?"+"string"
_PERSONAL_NAME="崔"+"青岗"
RULES=(
 re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{16,}\b"),re.compile(r"(?i)\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b"),
 re.compile(r"(?i)\bfc-[A-Za-z0-9_-]{16,}\b"),re.compile(r"\bAIza[A-Za-z0-9_-]{20,}\b"),re.compile(r"(?i)\bbearer\s+[A-Za-z0-9._~+/=-]{16,}"),
 re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"),re.compile(r"(?i)(?:"+_SENSITIVE_KEYS+r")\s*[:=]\s*['\"]?(?!\$\{REDACTED_)[^\s'\"${}<][^\r\n]{5,}"),
 re.compile(r"(?i)(?:C:)?[\\/]+Users[\\/]+A(?:[\\/]|$)"),re.compile(r"(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b"),re.compile(_PERSONAL_NAME),
)
def sensitive(text): return any(rx.search(text) for rx in RULES)
def digest(p):
 h=hashlib.sha256()
 with p.open("rb") as f:
  for b in iter(lambda:f.read(1048576),b""): h.update(b)
 return h.hexdigest().upper()
def frontmatter(text):
 if not text.startswith("---"): return False
 lines=text.splitlines(); end=next((i for i in range(1,len(lines)) if lines[i].strip()=="---"),-1)
 if end<0: return False
 block="\n".join(lines[1:end]); return bool(re.search(r"(?m)^name\s*:\s*\S",block) and re.search(r"(?m)^description\s*:\s*\S",block))
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--repo",default=str(Path(__file__).resolve().parents[1])); ap.add_argument("--self-test",action="store_true"); a=ap.parse_args()
 if a.self_test:
  bad=["ghp_"+"A"*24,"fc-"+"B"*24,"Bearer "+"C"*24,"pass"+"word="+"D"*12,"C:"+"\\"+"Users\\A\\secret"]
  ok=all(sensitive(x) for x in bad) and not sensitive("${REDACTED_SECRET}")
  print(json.dumps({"status":"PASS" if ok else "FAIL","cases":len(bad)+1})); return 0 if ok else 1
 root=Path(a.repo).resolve(); errors=[]
 for d in ("skills","catalog","governance","tests","scripts","benchmarks",".github"):
  if not (root/d).is_dir(): errors.append("MISSING_DIRECTORY:"+d)
 for name in CATALOG:
  if not (root/"catalog"/name).is_file(): errors.append("MISSING_CATALOG:"+name)
 try:
  inv=json.loads((root/"catalog"/"skill-inventory.json").read_text(encoding="utf-8")); skills=inv["skills"]
  inactive=json.loads((root/"catalog"/"inactive-skills.json").read_text(encoding="utf-8"))["skills"]
  systems=json.loads((root/"catalog"/"system-skills.json").read_text(encoding="utf-8"))["skills"]
  schema=json.loads((root/"catalog"/"repository-schema.json").read_text(encoding="utf-8"))
  if inv.get("counts")!=EXPECTED or schema.get("counts")!=EXPECTED: errors.append("COUNT_CONTRACT")
  if len(skills)!=190 or len(inactive)!=4 or len(systems)!=6: errors.append("LEDGER_LENGTH")
  for field in ("skill_id","name","repo_relative_path"):
   vals=[str(x.get(field,"")).casefold() for x in skills]
   if len(vals)!=len(set(vals)) or any(not x for x in vals): errors.append("DUPLICATE_OR_EMPTY:"+field)
  for row in skills:
   if row.get("classification","").startswith("METADATA_ONLY"): continue
   skill=root/row["repo_relative_path"]
   if not (skill/"SKILL.md").is_file(): errors.append("MISSING_SKILL_MD:"+row["skill_id"]); continue
   text=(skill/"SKILL.md").read_text(encoding="utf-8")
   if not frontmatter(text): errors.append("FRONTMATTER:"+row["skill_id"])
   for link in re.findall(r"\[[^\]]*\]\(([^)#]+)",text):
    clean=link.strip().replace("\\","/")
    if clean.startswith(("references/","scripts/","./references/","./scripts/")) and not (skill/clean).resolve().is_file(): errors.append("DANGLING_REFERENCE:"+row["skill_id"])
  v75=[x for x in skills if x.get("skill_id")=="ultrafusion-low-cost-multi-model-extreme-fusion-v7.5-cn"]
  if len(v75)!=1 or v75[0].get("special_status")!="READ_ONLY_BASELINE": errors.append("V75_CLASSIFICATION")
  custom=[x for x in skills if x.get("skill_id")=="custom-openai-docs"]
  if len(custom)!=1 or custom[0].get("repo_relative_path")!="skills/_special/custom-openai-docs": errors.append("CUSTOM_OPENAI_DOCS")
  fire=[x for x in skills if x.get("skill_id")=="firecrawl-web-api"]
  if len(fire)!=1 or fire[0].get("classification")!="FULL_SANITIZED_FIRECRAWL": errors.append("FIRECRAWL_CLASSIFICATION")
 except Exception as exc: errors.append("CATALOG_PARSE:"+type(exc).__name__)
 if (root/"skills"/".system").exists(): errors.append("SYSTEM_CONTENT_PRESENT")
 sm=root/"catalog"/"sanitization-manifest.json"
 if sm.is_file():
  try:
   for row in json.loads(sm.read_text(encoding="utf-8"))["files"]:
    p=root/row["path"]
    if not p.is_file() or digest(p)!=row["sha256"]: errors.append("CHECKSUM:"+row["path"])
  except Exception as exc: errors.append("SANITIZATION_MANIFEST:"+type(exc).__name__)
 for p in root.rglob("*"):
  rel=p.relative_to(root)
  if rel.parts and rel.parts[0]==".git": continue
  if p.is_symlink(): errors.append("SYMLINK:"+rel.as_posix()); continue
  if p.is_dir():
   if p.name in {"node_modules","__pycache__",".pytest_cache",".mypy_cache","backups","archive"} or p.name==".git": errors.append("FORBIDDEN_DIRECTORY:"+rel.as_posix())
   continue
  name=p.name.casefold()
  if any(fnmatch.fnmatch(name,x) for x in DENY): errors.append("CREDENTIAL_FILE:"+rel.as_posix())
  if p.stat().st_size>10*1024*1024: errors.append("FILE_OVER_10MB:"+rel.as_posix())
  if p.suffix.lower() in BINARY: continue
  try: text=p.read_text(encoding="utf-8")
  except UnicodeDecodeError: errors.append("NON_UTF8_TEXT:"+rel.as_posix()); continue
  if any(sensitive(line) for line in text.splitlines()): errors.append("SENSITIVE_TEXT:"+rel.as_posix())
 wf=(root/".github"/"workflows"/"validate-skills.yml")
 if wf.is_file():
  text=wf.read_text(encoding="utf-8")
  allowed=("actions/checkout@v4","actions/setup-python@v5")
  if "permissions:\n  contents: read" not in text or "pull_request_target" in text or "secrets." in text or "pip install" in text: errors.append("WORKFLOW_SAFETY")
  for action in re.findall(r"uses:\s*([^\s]+)",text):
   if action not in allowed: errors.append("UNKNOWN_ACTION:"+action)
 print(json.dumps({"status":"PASS" if not errors else "FAIL","error_count":len(errors),"errors":errors},ensure_ascii=False))
 return 0 if not errors else 1
if __name__=="__main__": raise SystemExit(main())
