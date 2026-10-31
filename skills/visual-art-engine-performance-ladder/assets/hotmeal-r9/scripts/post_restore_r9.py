from pathlib import Path
import cv2,numpy as np,json,subprocess,hashlib,time
from skimage.metrics import structural_similarity
from PIL import Image,ImageDraw
R=Path('C:/AI/TenYears-Animatic-20261030');D=R/'R9/FINAL';D.mkdir(exist_ok=True)
def read(p):
 cap=cv2.VideoCapture(str(p));fs=[]
 while True:
  ok,f=cap.read()
  if not ok:break
  fs.append(f)
 cap.release();return fs
def writevideo(p,fs):
 proc=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','bgr24','-s','768x640','-r','24','-i','pipe:0','-an','-c:v','libx264','-preset','fast','-crf','16','-pix_fmt','yuv420p','-movflags','+faststart',str(p)],stdin=subprocess.PIPE)
 for f in fs:proc.stdin.write(f.tobytes())
 proc.stdin.close();assert proc.wait()==0
src={'A':R/'R9/A/native.mp4','P':R/'R9/P/native.mp4','B_AV':R/'R8/B_AV/native.mp4','C':R/'R8/C/native.mp4'};sizes={'A':73,'P':39,'B_AV':73,'C':175}
frames={};qa={};sheet=Image.new('RGB',(768*2,664*4),'white');dr=ImageDraw.Draw(sheet)
for row,(label,raw) in enumerate(src.items()):
 restored=R/f'R9/RESTORE/{label}/restored.mp4';assert restored.exists(),str(restored)
 a=read(raw);b=read(restored);assert len(a)==len(b)==sizes[label];assert all(f.shape==(640,768,3) for f in b)
 vals=[];errors=[]
 for i,(x,y) in enumerate(zip(a,b)):
  sm=cv2.resize(y,(384,320),interpolation=cv2.INTER_AREA);vals.append(float(structural_similarity(cv2.cvtColor(x,cv2.COLOR_BGR2GRAY),cv2.cvtColor(sm,cv2.COLOR_BGR2GRAY),data_range=255)));errors.append(float(np.mean(np.abs(x.astype(float)-sm))))
 frames[label]=b;qa[label]={'frames':len(b),'downsampled_ssim_min':min(vals),'downsampled_ssim_mean':float(np.mean(vals)),'downsampled_mae_mean':float(np.mean(errors)),'framewise_ssim':vals,'note':'structural comparison only, not proof of perfect identity or absence of flicker'}
 idx={'A':32,'P':24,'B_AV':48,'C':144}[label]
 for col,f in enumerate([cv2.resize(a[idx],(768,640)),b[idx]]):
  sheet.paste(Image.fromarray(cv2.cvtColor(f,cv2.COLOR_BGR2RGB)),(768*col,row*664+24));dr.text((768*col+5,row*664+4),f'{label} f{idx} '+('NATIVE x2 view' if col==0 else 'RESTORED'),fill='black')
sheet.save(D/'restoration-comparison.jpg',quality=90)
(D/'restoration-structure.json').write_text(json.dumps(qa,indent=2),encoding='utf-8')
phone=json.loads((R/'R9/PHONE/tracking-review.json').read_text(encoding='utf-8'))
guide=cv2.imread('C:/AI/MiniMax-H3/projects/H3-MINIMAL-20261015/input/HOTMEAL_R9_P_GUIDE.jpg')
quad=np.array(json.loads((R/'R9/PHONE/screen-source-candidates.json').read_text())['candidates'][0]['quad'],np.float32)
mask=np.zeros(guide.shape[:2],np.uint8);cv2.fillConvexPoly(mask,np.round(quad).astype(np.int32),255);mask=cv2.erode(mask,np.ones((5,5),np.uint8))
pf=[]
for f,row in zip(frames['P'],phone['rows']):
 h=np.diag([2.,2.,1.])@np.array(row['homography_base384_to_frame384'])@np.diag([.5,.5,1.])
 patch=cv2.warpPerspective(guide,h,(768,640),flags=cv2.INTER_CUBIC);alpha=cv2.warpPerspective(mask,h,(768,640),flags=cv2.INTER_LINEAR).astype(np.float32)/255
 pf.append(np.round(f*(1-alpha[:,:,None])+patch*alpha[:,:,None]).clip(0,255).astype(np.uint8))
frames['P']=pf
cv2.imwrite(str(D/'phone-final-f24.jpg'),pf[24]);writevideo(D/'phone-screen-fixed-768-silent.mp4',pf)
timeline=frames['A'][:50]+pf+frames['A'][50:]+frames['B_AV']+frames['C'];assert len(timeline)==360
writevideo(D/'picture-15s-silent.mp4',timeline)
audio=R/'R9/EDIT/HotMeal-R9-Native-15s-Review.mp4'
stats=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(audio),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True).stderr
measure=json.JSONDecoder().raw_decode(stats[stats.rfind('{'):])[0];(D/'loudness-first-pass.json').write_text(json.dumps(measure,indent=2))
af=f"loudnorm=I=-16:TP=-1:LRA=11:measured_I={measure['input_i']}:measured_TP={measure['input_tp']}:measured_LRA={measure['input_lra']}:measured_thresh={measure['input_thresh']}:offset={measure['target_offset']}:linear=true:print_format=json"
out=D/'HotMeal-R9-15s-Human-Review.mp4'
mix=subprocess.run(['ffmpeg','-hide_banner','-nostats','-y','-i',str(D/'picture-15s-silent.mp4'),'-i',str(audio),'-map','0:v:0','-map','1:a:0','-af',af,'-ar','48000','-c:v','copy','-c:a','aac','-b:a','192k','-t','15','-movflags','+faststart',str(out)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,check=True)
(D/'loudness-mix.log').write_text(mix.stderr,encoding='utf-8')
probe=json.loads(subprocess.check_output(['ffprobe','-v','error','-count_frames','-show_streams','-show_format','-of','json',str(out)]))
v=next(s for s in probe['streams'] if s['codec_type']=='video');a=next(s for s in probe['streams'] if s['codec_type']=='audio')
assert int(v['nb_read_frames'])==360 and float(v['duration'])==15 and v['r_frame_rate']=='24/1'
assert v['codec_name']=='h264' and v['pix_fmt']=='yuv420p' and a['sample_rate']=='48000' and a['codec_name']=='aac'
subprocess.run(['ffmpeg','-v','error','-i',str(out),'-f','null','-'],check=True)
finalstats=subprocess.run(['ffmpeg','-hide_banner','-nostats','-i',str(out),'-vn','-af','loudnorm=I=-16:TP=-1:LRA=11:print_format=json','-f','null','-'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,text=True).stderr
finalmeasure=json.JSONDecoder().raw_decode(finalstats[finalstats.rfind('{'):])[0];assert float(finalmeasure['input_tp'])<=-0.9
report={'file':str(out),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'frames':360,'fps':24,'duration_seconds':15,'dimensions':[768,640],'native_dimensions':[384,320],'restoration':'official RealESRGAN_x2plus; no motion generation or frame interpolation','phone':'exact source screen recomposited after restoration,39 tracked frames','audio':'original native audiovisual timeline, 2pass loudness, speech rate1.0, no old rejected slap/music/new voice','loudness':finalmeasure,'restoration_structure':qa,'probe':probe,'full_decode':'PASS','human_approval':False,'final_artistic_approval':False,'status':'AWAITING_RESTORED_IMAGE_AND_AV_REVIEW'}
(D/'technical-review.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in report.items() if k not in ['probe','restoration_structure']},ensure_ascii=True),flush=True)
