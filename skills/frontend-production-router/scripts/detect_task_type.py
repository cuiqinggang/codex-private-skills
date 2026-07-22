#!/usr/bin/env python3
import argparse,json,re
ROUTES=[
 ('clone-and-originalize',[r'参考.*不要.*(照抄|复制)',r'originali[sz]e',r'inspired by',r'多页面.*(扩展|一致)']),
 ('screenshot-to-page',[r'截图.*(还原|转.*页面|转.*代码)',r'image.to.code',r'mockup']),
 ('clone-existing-website',[r'https?://',r'网站.*克隆',r'网页.*还原',r'pixel.?perfect']),
 ('redesign-existing-project',[r'现有.*(杂乱|不一致|重构|改版)',r'redesign',r'视觉.*统一']),
 ('visual-quality-review',[r'(审查|验收|review).*(视觉|UI|界面)',r'visual qa']),
 ('new-product-design',[r'新产品',r'从零',r'设计.*SaaS',r'landing page',r'仪表盘'])]
def detect(text):
 for route,patterns in ROUTES:
  if any(re.search(p,text,re.I) for p in patterns):return route
 return 'new-product-design'
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--text',required=True);p.add_argument('--json',action='store_true');a=p.parse_args();r=detect(a.text)
 print(json.dumps({'route':r},ensure_ascii=False) if a.json else 'ROUTE='+r)

