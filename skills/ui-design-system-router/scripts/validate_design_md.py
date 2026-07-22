#!/usr/bin/env python3
import re, sys
from pathlib import Path

REQUIRED=['Product Intent','Design Direction','Color Tokens','Typography','Spacing','Layout','Components','Accessibility',"Do / Don't"]

def validate(path):
    text=Path(path).read_text(encoding='utf-8')
    errors=[]; warnings=[]
    for s in REQUIRED:
        if s.lower() not in text.lower(): errors.append('missing_section:'+s)
    colors=re.findall(r'#[0-9A-Fa-f]{3,8}\b', text)
    if not colors: errors.append('no_valid_color_token')
    if 'sans-serif' not in text and 'serif' not in text: errors.append('font_fallback_missing')
    for token,label in [('px','type_or_size_scale'),('Spacing','spacing_scale'),('loading','loading_state'),('empty','empty_state'),('error','error_state'),('responsive','responsive_rules'),('44x44','touch_target')]:
        if token.lower() not in text.lower(): errors.append('missing_'+label)
    if re.search(r'https?://',text): errors.append('unresolved_external_link')
    forbidden=['must copy logo','必须复制 logo','must copy trademark','use hotlinked assets']
    if any(x in text.lower() for x in forbidden): errors.append('forbidden_brand_asset_instruction')
    if len(text)>50000: warnings.append('document_over_50kb')
    if 'always animate' in text.lower() and 'reduced-motion' in text.lower(): warnings.append('possible_motion_contradiction')
    status='FAIL' if errors else ('PASS_WITH_WARNINGS' if warnings else 'PASS')
    print('STATUS='+status)
    for e in errors: print('ERROR='+e)
    for w in warnings: print('WARNING='+w)
    return 1 if errors else 0

if __name__=='__main__':
    if len(sys.argv)!=2: print('usage: validate_design_md.py DESIGN.md'); sys.exit(2)
    sys.exit(validate(sys.argv[1]))
