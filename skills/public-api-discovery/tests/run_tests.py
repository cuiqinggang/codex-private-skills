#!/usr/bin/env python3
import json
import subprocess
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SEARCH=ROOT/'scripts'/'search_public_apis.py'; ROUTE=ROOT/'scripts'/'route_public_api.py'
scenarios=[
 ('weather',['--query','weather','--category','Weather','--auth','No','--https','Yes']),
 ('photos',['--query','image','--category','Photography','--cors','Yes']),
 ('test-data',['--query','test data']), ('currency',['--query','exchange','--category','Currency Exchange']),
 ('geocoding',['--query','geocoding','--category','Geocoding']), ('news',['--query','news','--category','News']),
 ('ml',['--query','machine learning','--category','Machine Learning']), ('documents',['--query','document','--category','Documents'])]
route_cases=[
 ('帮我找一个免费的天气 API',True,'P1'),('比较几个公共汇率 API',True,'P1'),('现有地图 API 太贵，找替代 API',True,'P1'),
 ('这个原型需要新闻外部数据源',True,'P2'),('有没有无需 Key 的图片接口',True,'P1'),('为 MVP 找测试数据 API',True,'P1'),
 ('已经指定 OpenWeather，只写调用代码',False,'P0'),('解释 REST 接口是什么',False,'P0'),('本地离线数据足够，不用第三方 API',False,'P0'),
 ('帮我绕过 API 付费限制',False,'P0'),('修复现有唯一 API 的调用代码',False,'P0'),('天气页面配色怎么设计',False,'P3')]
results=[]; ok=True
for name,args in scenarios:
    data=json.loads(subprocess.check_output([sys.executable,str(SEARCH),*args,'--limit','5'],text=True,encoding='utf-8'))
    passed=0 < data['count'] <= 8 and all(x['review_status']=='unverified' for x in data['results'])
    results.append({'type':'search','name':name,'passed':passed,'count':data['count']}); ok &= passed
for text,expected,level in route_cases:
    data=json.loads(subprocess.check_output([sys.executable,str(ROUTE),'--text',text],text=True,encoding='utf-8'))
    passed=data['skill_called']==expected and data['trigger_level']==level and not data['external_api_called']
    results.append({'type':'route','text':text,'passed':passed,'actual':data['trigger_level']}); ok &= passed
summary={'passed':ok,'search_passed':sum(x['passed'] for x in results if x['type']=='search'),'search_total':8,'route_passed':sum(x['passed'] for x in results if x['type']=='route'),'route_total':12,'results':results}
out=ROOT/'tests'/'round2-results.json'; out.write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,ensure_ascii=False,indent=2)); raise SystemExit(0 if ok else 1)
