from pathlib import Path
import json,re,base64,urllib.request,urllib.error,time
ROOT=Path('C:/AI/TenYears-Animatic-20261030');D=ROOT/'R9/AUDIO_FULL_RECHECK';D.mkdir(exist_ok=True)
assert not (D/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
assert key
p=ROOT/'R9/ASR/C/audio_16k.wav'
prompt='''请实际听这段完整中文音频，不依据任何剧本或上下文预设。先逐字写出全部原话，不替换同义词；再把最后一句的动词按你听到的实际读音写成带声调拼音。说明发音是否清楚、有无可听截断、声音是否像当面愤怒控诉或平淡旁白。只输出JSON：raw_transcript,final_verb,pinyin,uncertainty,cutoff,emotion,evidence。'''
payload={'model':'openai/gpt-audio-mini','messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'input_audio','input_audio':{'data':base64.b64encode(p.read_bytes()).decode(),'format':'wav'}}]}],'modalities':['text'],'temperature':0,'max_tokens':700}
(D/'submission.claim').write_text('one full-utterance context recheck; prior short-fragment answer retained and not treated as approval')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'prompt':prompt,'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True),flush=True)
