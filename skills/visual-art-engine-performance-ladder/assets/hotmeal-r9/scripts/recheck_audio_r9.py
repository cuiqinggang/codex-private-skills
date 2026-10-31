from pathlib import Path
import json,subprocess,base64,re,urllib.request,urllib.error,numpy as np,time
ROOT=Path('C:/AI/TenYears-Animatic-20261030');D=ROOT/'R9/AUDIO_RECHECK';D.mkdir(exist_ok=True)
wav=D/'C-final-verb.wav'
subprocess.run(['ffmpeg','-v','error','-y','-ss','5.2','-i',str(ROOT/'R8/C/native.mp4'),'-t','1.6','-vn','-ar','16000','-ac','1',str(wav)],check=True)
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
assert key
assert not (D/'submission.claim').exists()
prompt='''只听这个短音频。先逐字转写你确实听到的中文，再逐个音节写出带声调拼音。不要补全上下文，不要替换同义词，不要猜测剧本。不清楚的字写[不清楚]。同时说明最后一个字是否完整结束、有无明显截断。仅输出JSON：heard_text,pinyin,uncertain_syllables,last_word_complete,reason。'''
payload={'model':'openai/gpt-audio-mini','messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'input_audio','input_audio':{'data':base64.b64encode(wav.read_bytes()).decode(),'format':'wav'}}]}],'modalities':['text'],'temperature':0,'max_tokens':500}
(D/'submission.claim').write_text('one independent cropped-audio review')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=100) as q:reply=json.load(q)
 (D/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'audio_source_seconds':[5.2,6.8],'prompt':prompt}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
raw=subprocess.check_output(['ffmpeg','-v','error','-i',str(ROOT/'R8/B_AV/native.mp4'),'-vn','-ar','32000','-ac','1','-f','f32le','-'])
a=np.frombuffer(raw,'<f4');rows=[]
for st in np.arange(1.3,2.35,.005):
 x=a[round(st*32000):round((st+.02)*32000)]
 sp=np.abs(np.fft.rfft(x*np.hanning(len(x))))**2;freq=np.fft.rfftfreq(len(x),1/32000)
 rows.append({'start':round(float(st),4),'rms':float(np.sqrt(np.mean(x*x))),'hf_energy':float(sp[freq>1200].sum())})
peak=max(rows,key=lambda x:x['hf_energy']);base=[x['hf_energy'] for x in rows if x['start']<1.55];thr=max(float(np.mean(base)+8*np.std(base)),peak['hf_energy']*.08)
onset=next((x['start'] for x in rows if x['hf_energy']>=thr),None)
diag={'expected_contact_seconds':2.0,'hf_energy_peak':peak,'candidate_onset_seconds':onset,'onset_minus_contact_seconds':None if onset is None else onset-2.0,'rows':rows,'scope':'spectral transient timing only; does not certify timbre or audible impact realism'}
(D/'B-transient-timing.json').write_text(json.dumps(diag,indent=2))
print(json.dumps({'audio_review':result,'impact_peak_seconds':peak['start'],'impact_candidate_onset':onset},ensure_ascii=True),flush=True)
