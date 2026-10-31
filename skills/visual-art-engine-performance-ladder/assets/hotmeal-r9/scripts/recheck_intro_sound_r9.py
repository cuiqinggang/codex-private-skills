from pathlib import Path
import json,re,base64,urllib.request,urllib.error,subprocess
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/INTRO_SOUND_RECHECK';D.mkdir(exist_ok=True);assert not(D/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
p=D/'actual_intro_4p6667s.wav';subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/'R9/EDIT/HotMeal-R9-Native-15s-Review.mp4'),'-t','4.666666667','-vn','-ar','16000','-ac','1',str(p)],check=True)
prompt='''只听这一段4.6667秒连续音频，描述实际听到的声音。有没有能辨认的人声或音乐？有没有手机电子提示音（次数/大致时刻）？有没有桌面陶瓷接触声（大致时刻）？不要推测画面，不要编造4.6667秒之外的事件。先前另一个工具给出了超出片长的时间，是不可信记录，故不能沿用它。输出JSON：duration,speech,music,notification,contact_events,background,uncertainty。'''
payload={'model':'google/gemini-2.5-flash','messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'input_audio','input_audio':{'data':base64.b64encode(p.read_bytes()).decode(),'format':'wav'}}]}],'temperature':0,'max_tokens':900}
(D/'submission.claim').write_text('single continuous intro audio, independent duration bounded check')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True),flush=True)
