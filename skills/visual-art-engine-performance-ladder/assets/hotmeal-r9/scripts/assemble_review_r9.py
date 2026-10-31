from pathlib import Path
import subprocess,json,hashlib,base64,urllib.request,urllib.error,re,time
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/EDIT';D.mkdir(exist_ok=True)
sources=[R/'R9/A/native.mp4',R/'R9/P/screen-fixed.mp4',R/'R8/B_AV/native.mp4',R/'R8/C/native.mp4']
for x in sources: assert x.exists(),str(x)
segments=[(0,0,50,'A: serving and discovery'),(1,0,39,'P: message'),(0,50,73,'A: look at husband'),(2,0,73,'B: reaching/contact'),(3,0,175,'C: accusation')]
flt=['[0:v]split=2[a0][a1]','[0:a]asplit=2[s0][s1]'];ins=['a0','1:v','a1','2:v','3:v'];aud=['s0','1:a','s1','2:a','3:a']
rows=[];cur=0
for k,(idx,start,end,label) in enumerate(segments):
 flt += [f'[{ins[k]}]trim=start_frame={start}:end_frame={end},setpts=PTS-STARTPTS[v{k}]',f'[{aud[k]}]atrim=start={start/24:.9f}:end={end/24:.9f},asetpts=PTS-STARTPTS,aresample=48000,aformat=sample_fmts=fltp:channel_layouts=stereo[a{k}]']
 rows.append(dict(segment=label,source=str(sources[idx]),source_frames=[start,end-1],timeline_frames=[cur,cur+end-start-1],playback_rate=1));cur+=end-start
flt += [''.join(f'[v{k}][a{k}]' for k in range(5))+'concat=n=5:v=1:a=1[v][a]']
out=D/'HotMeal-R9-Native-15s-Review.mp4'
cmd=['ffmpeg','-v','error','-y']
for x in sources:cmd+=['-i',str(x)]
cmd+=['-filter_complex',';'.join(flt),'-map','[v]','-map','[a]','-c:v','libx264','-crf','16','-preset','fast','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k','-t','15','-movflags','+faststart',str(out)]
subprocess.run(cmd,check=True);assert cur==360
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]))
(D/'timeline.json').write_text(json.dumps({'fps':24,'frames':360,'seconds':15,'segments':rows,'speed_changes':False,'probe':probe,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
V=R/'R9/VIDEO_REVIEW';V.mkdir(exist_ok=True)
assert not (V/'submission.claim').exists()
key=None
for line in Path('C:/Users/A/AppData/Roaming/reasonix/.env').read_text(encoding='utf-8-sig').splitlines():
 m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
 if m:key=m.group(1);break
assert key
prompt='''你是这段15秒短片的内部视听审片工具。必须实际查看上传的视频和听声音。先不参照任何预期叙事，自行描述观众能理解的因果和逐字对白。然后严格检查：人物服装/空间/饭碗位置/手机形状和持握手跨切镜是否连续；开场放饭、拾手机是否可信；手机信息是否读得清和停留足够；男人伸手抢、女人保护手机、单次接触与受击方向、受击后是否回正；末段手指是不是指向饭而不是端碗；愤怒表情、口型、对白、气息是否同步且真实；音效来源和节奏；有没有画面变形、穿透、手指异常。不要因为画面漂亮就通过。给出具体秒数和可见证据，不确定就明确。技术和艺术分别结论，只能作AI内部审核，不能代替人工。输出JSON：observed_story,verbatim_dialogue,shot_notes,continuity_findings,action_findings,lip_sync_findings,sound_findings,emotion_and_rhythm,blocking_failures,technical_status,artistic_status,required_rework。状态PASS/REWORK/UNCERTAIN。不许把无法确认的项目写成通过。'''
payload={'model':'google/gemini-2.5-flash','messages':[{'role':'user','content':[{'type':'text','text':prompt},{'type':'video_url','video_url':{'url':'data:video/mp4;base64,'+base64.b64encode(out.read_bytes()).decode()}}]}],'temperature':0,'max_tokens':3200}
(V/'submission.claim').write_text('one complete 15s native audiovisual review',encoding='utf-8')
(V/'request-manifest.json').write_text(json.dumps({'model':payload['model'],'prompt':prompt,'input':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()},ensure_ascii=False,indent=2),encoding='utf-8')
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=180) as q:reply=json.load(q)
 (V/'response.json').write_text(json.dumps(reply,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','model':reply.get('model'),'usage':reply.get('usage'),'content':reply['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:result={'state':'UNAVAILABLE','http_status':e.code}
(V/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True),flush=True)
