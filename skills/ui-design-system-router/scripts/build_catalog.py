#!/usr/bin/env python3
import hashlib, json, re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
KEYWORDS={'04':['cursor','vercel','warp','github','raycast'],'05':['claude','cohere','mistral','ollama','replicate','x.ai','minimax'],'06':['airtable','clickhouse','mongodb','posthog'],'08':['apple','bmw','bugatti','ferrari','lamborghini','porsche'],'11':['airbnb','nike'],'12':['binance','coinbase','kraken','mastercard','wise'],'14':['figma','framer','pinterest'],'15':['superhuman','spacex','runway']}
def archetype(name):
    for k,names in KEYWORDS.items():
        if name.lower() in names:return k
    return '02'
def main():
    entries=[]
    for f in sorted((ROOT/'references/bundled').glob('*/DESIGN.md')):
        b=f.read_bytes(); text=b.decode('utf-8',errors='replace')
        entries.append({'id':f.parent.name,'source_path':str(f.relative_to(ROOT)).replace('\\','/'),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'headings':len(re.findall(r'(?m)^#{1,6}\s+',text)),'primary_archetype':archetype(f.parent.name),'complete':len(b)>4000,'runtime_offline':True,'brand_reference_only':True})
    (ROOT/'catalog/catalog.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# Offline Design Reference Catalog','','| ID | Archetype | Bytes | Complete |','|---|---:|---:|:---:|']+[f"| {e['id']} | {e['primary_archetype']} | {e['bytes']} | {'yes' if e['complete'] else 'no'} |" for e in entries]
    (ROOT/'catalog/catalog.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f'CATALOG_BUILD=PASS count={len(entries)}')
if __name__=='__main__':main()

