#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
 p=argparse.ArgumentParser();p.add_argument('name',choices=['clone','design']);a=p.parse_args()
 data=json.loads((ROOT/'capability-map.json').read_text(encoding='utf-8'))
 item=data['clone_skill' if a.name=='clone' else 'design_skill'];path=Path(item['path'])
 print(f'NAME={item["name"]}\nPATH={path}\nEXISTS={str(path.exists()).lower()}')
 raise SystemExit(0 if path.exists() else 1)
if __name__=='__main__':main()

