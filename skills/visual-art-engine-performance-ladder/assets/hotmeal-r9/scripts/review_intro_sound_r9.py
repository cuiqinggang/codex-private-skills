from pathlib import Path
import json,re,base64,urllib.request,urllib.error,subprocess
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/INTRO_SOUND_REVIEW';D.mkdir(exist_ok=True);assert not(D/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
paths=[]
for label in ['A','P']:
 p=D/(label+'.wav');subprocess.run(['ffmpeg','-v','error','-y','-i',str(R/f'R9/{label}/native.mp4'),'-vn','-ar','16000','-ac','1',str(p)],check=True);paths.append(p)
prompt='''只听上传的两段短音频。分别描述实际听到的环境声、动作声、人声、音乐，给出粗略时间和声音特征。特别区分陶瓷/桌面落物接触声和手机电子提示声：有没有电子通知提示音、响了几次、何时；没有就明确没有。不要假定视频中的动作，也不要为了符合情节补出声音。输出JSON：clips，每个包含label,events,notification_count,speech,music,uncertainty。'''
content=[{'type':'text','text':prompt}]
for label,p in zip(['A','P'],paths):content+=[{'type':'text','text':'clip '+label},{'type':'input_audio','input_audio':{'data':base64.b64encode(p.read_bytes()).decode(),'format':'wav'}}]
payload={'model':'openai/gpt-audio-mini','messages':[{'role':'user','content':content}],'modalities':['text'],'temperature':0,'max_tokens':1000}
(D/'submission.claim').write_text('one native intro effects audit')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(result,ensure_ascii=True),flush=True)
