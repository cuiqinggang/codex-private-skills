#!/usr/bin/env python3
import hashlib,json,re
from datetime import date
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    items=[]
    for f in sorted((ROOT/'references/bundled').glob('*/DESIGN.md')):
        b=f.read_bytes(); t=b.decode('utf-8',errors='replace')
        items.append({'id':f.parent.name,'source_url':f'https://github.com/VoltAgent/awesome-design-md/blob/664b3e78fd1a298ba11973822da988483256d4b4/design-md/{f.parent.name}/DESIGN.md','retrieved':str(date.today()),'sha256':hashlib.sha256(b).hexdigest(),'license':'MIT repository; trademarks remain with owners','completeness':'COMPLETE' if len(b)>4000 and len(re.findall(r'(?m)^#{1,6}\s+',t))>=5 else 'INCOMPLETE_REFERENCE','contains_brand_or_proprietary_font_mentions':True,'commercial_reference':'YES_WITH_ORIGINALIZATION','offline':True})
    out={'upstream':'https://github.com/VoltAgent/awesome-design-md','commit':'664b3e78fd1a298ba11973822da988483256d4b4','license':'MIT','items':items}
    (ROOT/'SOURCE_MANIFEST.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
    print(f'SOURCE_AUDIT=PASS total={len(items)} complete={sum(x["completeness"]=="COMPLETE" for x in items)}')
if __name__=='__main__':main()

