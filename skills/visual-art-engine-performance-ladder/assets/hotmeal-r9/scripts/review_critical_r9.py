from pathlib import Path
import json,re,base64,urllib.request,urllib.error
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/CRITICAL_REVIEW';D.mkdir(exist_ok=True);assert not(D/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
prompt='''这是同一短片原生帧的补充检查，格上有帧号和原镜头时间，不是新表演。前一次整段视频分析只采到少量时刻，误把接触叙述为“挡开手机”，还把解剖学左右说反，因此不能据其笼统PASS放行。请依据这次逐帧序列独立纠错，不为既定方案辩护。1. B格：辨认手机实际在哪一只解剖学手，另一手是否一次击中男人脸，哪边脸、受击后头向何处转，是否回正；动作是快速击打还是缓慢推触？f47/48间隔1/24秒，不是长时间推压。2. C格：头是否跨镜复位、手机和饭碗位置是否保持、食指是否指到饭碗、脸上是否愤怒。3. A拾手机近格：刚体形状、抓握、手指数是否有明显穿透或变形。4. 所有仅见缩小原生画面，不得把看不清细节当通过，也不能把AI修复可解决的清晰度当已修复。输出JSON：corrected_anatomical_hands,contact_sequence,head_retention,point_target,grasp,emotion,visible_defects,unresolved_limits,blocking_rework_required,reason。只写可见证据。'''
paths=[R/'R9/VIDEO_REVIEW/B_AV-critical-frames.jpg',R/'R9/VIDEO_REVIEW/C-critical-frames.jpg',R/'R9/A/pickup-detail.jpg']
content=[{'type':'text','text':prompt}]+[{'type':'image_url','image_url':{'url':'data:image/jpeg;base64,'+base64.b64encode(p.read_bytes()).decode()}} for p in paths]
payload={'model':'google/gemini-2.5-flash','messages':[{'role':'user','content':content}],'temperature':0,'max_tokens':2200}
(D/'submission.claim').write_text('critical frame supplement, never blanket automatic approval')
(D/'request-manifest.json').write_text(json.dumps({'prompt':prompt,'inputs':[str(p) for p in paths]},ensure_ascii=False,indent=2),encoding='utf-8')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=150) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True),flush=True)
