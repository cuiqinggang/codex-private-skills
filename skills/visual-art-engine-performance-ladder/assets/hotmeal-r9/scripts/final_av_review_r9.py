from pathlib import Path
import json,re,base64,urllib.request,urllib.error
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/FINAL_AV_REVIEW';D.mkdir(exist_ok=True);assert not(D/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
p=R/'R9/FINAL/HotMeal-R9-15s-Human-Review.mp4'
assert (R/'R9/FINAL/sound-rework.json').exists()
prompt='''实际查看并听这一段15秒768x640短片，这是画面修复和声音整理后的内部最终候选。先按观众角度描述因果、真实情绪与完整对白，再查：信息是否可读；放碗和拿手机、抢夺、击打受击、指饭动作是否自然连贯；口型是否有明显提前/滞后、冻结/错口；声音有无额外人声/音乐、重复提示/击打、无来源事件或可听截断；修复有没有脸部身份改变、手指/手机变形、闪烁。不能把采样没看到的短接触断言为没发生；不能用左右术语的猜测代替可见事实。若低帧采样无法判定，写UNCERTAIN，局部可用原生逐帧审核补充。技术、艺术分别结论，有缺陷要给秒数和具体可见/可听证据；不要凑通过。这里只作AI内部审查，不代替人工最终审片。输出JSON：story_and_emotion,dialogue,readability,continuity,lip_sync,sound,restoration_defects,blocking_failures,uncertain_items,technical_status,artistic_status,return_stage。'''
payload={'model':'google/gemini-2.5-flash','messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'video_url','video_url':{'url':'data:video/mp4;base64,'+base64.b64encode(p.read_bytes()).decode()}}]}],'temperature':0,'max_tokens':2400}
(D/'submission.claim').write_text('one final restored audiovisual candidate review')
(D/'request-manifest.json').write_text(json.dumps({'prompt':prompt,'file':str(p),'bytes':p.stat().st_size},ensure_ascii=False,indent=2),encoding='utf-8')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True),flush=True)
