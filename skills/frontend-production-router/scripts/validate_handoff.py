#!/usr/bin/env python3
import argparse,json,sys
from pathlib import Path
CLONE=['contract_version','source_authorization','source_url_or_image','desktop_screenshot','mobile_screenshot','page_structure','colors','fonts','type_scale','spacing_scale','radii','shadows','components','breakpoints','motion','page_files','stack','known_defects']
DESIGN=['contract_version','design_md','tokens','originalize','preserve','forbidden_brand_elements','component_rules','extension_rules','validator_status']
def main():
 p=argparse.ArgumentParser();p.add_argument('--clone',required=True);p.add_argument('--design');a=p.parse_args();errors=[]
 c=json.loads(Path(a.clone).read_text(encoding='utf-8'))
 for k in CLONE:
  if k not in c:errors.append('clone_missing:'+k)
 if c.get('contract_version')!='1.0':errors.append('clone_contract_version')
 if c.get('source_authorization') not in ('owned','authorized','analysis-only'):errors.append('source_authorization')
 if c.get('caller')=='frontend-production-router' and c.get('callee')=='frontend-production-router':errors.append('circular_call')
 if len(c.get('page_files',[]))!=len(set(c.get('page_files',[]))):errors.append('duplicate_page_owner')
 if a.design:
  d=json.loads(Path(a.design).read_text(encoding='utf-8'))
  for k in DESIGN:
   if k not in d:errors.append('design_missing:'+k)
  if d.get('contract_version')!='1.0':errors.append('design_contract_version')
 print('HANDOFF_VALIDATION='+('PASS' if not errors else 'FAIL'))
 for e in errors:print('ERROR='+e)
 sys.exit(1 if errors else 0)
if __name__=='__main__':main()

