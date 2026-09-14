import hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

root=Path(sys.argv[1]).resolve()
items=[]
for p in sorted(root.rglob("*")):
    if not p.is_file() or p.name=="MANIFEST.json" or "__pycache__" in p.parts: continue
    b=p.read_bytes()
    items.append({"path":p.relative_to(root).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
out={"schema_version":2,"generated_at":datetime.now(timezone.utc).isoformat(),"root":str(root),"file_count":len(items),"files":items}
(root/"MANIFEST.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
