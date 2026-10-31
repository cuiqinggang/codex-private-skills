from pathlib import Path
import numpy as np,subprocess,json,hashlib,wave
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/FINAL'
raw=R/'R9/EDIT/HotMeal-R9-Native-15s-Review.mp4'
b=subprocess.check_output(['ffmpeg','-v','error','-i',str(raw),'-vn','-ar','48000','-ac','2','-f','f32le','-'])
a=np.frombuffer(b,np.float32).reshape(-1,2).copy()[:720000];assert len(a)==720000
sr=48000;start=48000;length=6720;t=np.arange(length)/sr
env=np.minimum(t/.008,1)*np.minimum((.14-t)/.05,1);env=np.clip(env,0,1)*np.exp(-10*t)
tone=.045*env*(np.sin(2*np.pi*1046.5*t)+.32*np.sin(2*np.pi*1569.75*t))
a[start:start+length]+=tone[:,None];assert np.max(abs(a))<1
wav=D/'sound-edited-15s.wav'
with wave.open(str(wav),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr);w.writeframes(np.round(a*32767).clip(-32768,32767).astype('<i2').tobytes())
stats=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(wav),'-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True).stderr
m=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0];(D/'loudness-edited-first-pass.json').write_text(json.dumps(m,indent=2))
af=f"loudnorm=I=-16:TP=-1:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true:print_format=json"
out=D/'HotMeal-R9-15s-Human-Review.mp4'
mix=subprocess.run(['ffmpeg','-hide_banner','-nostats','-y','-i',str(D/'picture-15s-silent.mp4'),'-i',str(wav),'-map','0:v:0','-map','1:a:0','-af',af,'-ar','48000','-c:v','copy','-c:a','aac','-b:a','192k','-t','15','-movflags','+faststart',str(out)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True)
(D/'loudness-final-mix.log').write_text(mix.stderr,encoding='utf-8')
stats=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True).stderr
m=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0]
report=json.loads((D/'technical-review.json').read_text(encoding='utf-8'));report.update(sha256=hashlib.sha256(out.read_bytes()).hexdigest(),loudness=m,audio='Native original AV timeline and room tone, same B contact and C speech. One independently designed soft generic phone notification added at1.000s,0.140s length; 2pass loudness. No voice speed change/music/old rejected hit.')
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True);assert float(m['input_tp'])<=-.9
report['probe']=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]))
(D/'technical-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
ed={'cause':'Native intro has bowl transient0.6..0.8s and quiet room/sleeve, but no clear narrowband notification; two audio semantic reports hallucinated times or repeated events and were rejected','fix':'F stage: one generic soft electronic notification before pickup. Own procedural sound, not stock brand tone. Native ambience/bowl/cloth retained; native P no additional event. No action or timing altered.','onset_seconds':1.0,'duration_seconds':.14,'frequencies_hz':[1046.5,1569.75],'speech_rate':1,'bowl_native_onset_approx':.6,'B_native_contact_onset_global':6.621667,'B_first_contact_global':6.625,'human_timbre_approval':False}
(D/'sound-rework.json').write_text(json.dumps(ed,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps({'file':str(out),'sha256':report['sha256'],'loudness':m,'sound_rework':ed},ensure_ascii=True),flush=True)
