import json,subprocess,time,pathlib,math,hashlib
p=pathlib.Path(__file__).resolve().parent
m=json.loads((p/'scene-timing.json').read_text())
d=m['decoded_seconds'];total=sum(d);b1=round(d[0]*25)/25;b2=round(sum(d[:2])*25)/25;end=math.ceil(total*25)/25
durations=[b1,b2-b1,end-b2]
cmd=['ffmpeg','-y','-v','error']
for i in range(3):cmd+=['-loop','1','-framerate','25','-i',str(p/f'scene-{i}.png')]
cmd+=['-i',str(p/'avatar-promo-raw.mp4')]
f=[]
for i,dur in enumerate(durations):f.append(f'[{i}:v]trim=duration={dur:.3f},setpts=PTS-STARTPTS[b{i}]')
f+=['[b0][b1][b2]concat=n=3:v=1:a=0[bg]','[3:v]split=3[h0][h1][h2]','[h0]scale=384:384[h0s]','[h1]scale=250:250[h1s]','[h2]scale=384:384[h2s]',f"[bg][h0s]overlay=64:178:enable='lt(t,{b1})'[v0]",f"[v0][h1s]overlay=955:299:enable='gte(t,{b1})*lt(t,{b2})'[v1]",f"[v1][h2s]overlay=64:178:enable='gte(t,{b2})',format=yuv420p[v]"]
cmd+=['-filter_complex',';'.join(f),'-map','[v]','-map','3:a:0','-t',str(total),'-c:v','libx264','-preset','medium','-crf','18','-c:a','aac','-b:a','128k','-movflags','+faststart',str(p/'avatar-promo.mp4')]
t=time.perf_counter();subprocess.run(cmd,check=True)
record={'command':cmd,'composite_seconds':time.perf_counter()-t,'caption_cuts_seconds':[b1,b2],'audio_seconds':total,'output_sha256':hashlib.sha256((p/'avatar-promo.mp4').read_bytes()).hexdigest(),'note':'FFmpeg trim/concat/scale/overlay, original avatar timing retained, no manual mouth repair or speed warp.'}
(p/'compose-run.json').write_text(json.dumps(record,indent=2))
print(json.dumps({k:v for k,v in record.items() if k!='command'}))
