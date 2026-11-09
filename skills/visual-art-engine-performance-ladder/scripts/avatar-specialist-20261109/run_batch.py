import pathlib,json,subprocess,os,datetime,time
p=pathlib.Path('C:/AI/Video-Recipe-Reproduction-20261108/Avatar-Specialist-20261109'); root=pathlib.Path('C:/AI/MuseTalk')
ff='C:/Users/A/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin'
tts=json.loads((p/'tts-run.json').read_text(encoding='utf-8'));assert tts['status']=='AUDIO_FILES_CREATED_REVIEW_PENDING'
cmd=[ff+'/ffmpeg.exe','-y','-v','error']
for i in range(3):cmd+=['-i',str(p/('speech-'+str(i)+'.mp3'))]
cmd+=['-filter_complex','[0:a][1:a][2:a]concat=n=3:v=0:a=1,aresample=16000[a]','-map','[a]','-ac','1','-c:a','pcm_s16le',str(p/'promotion.wav')]
subprocess.run(cmd,check=True)
durations=[]
for i in range(3):
 r=subprocess.run([ff+'/ffprobe.exe','-v','error','-show_entries','format=duration','-of','json',str(p/('speech-'+str(i)+'.mp3'))],capture_output=True,text=True,check=True)
 durations.append(float(json.loads(r.stdout)['format']['duration']))
(p/'timeline.json').write_text(json.dumps({'parts':tts['parts'],'segment_mp3_container_durations':durations,'note':'Actual decoded sample durations used for final timing; source MP3 container includes padding.'},ensure_ascii=False,indent=2),encoding='utf-8')
src=str(p/'d24-input.mp4').replace('\\','/');oldaudio=str(p/'d24-speech.wav').replace('\\','/');newaudio=str(p/'promotion.wav').replace('\\','/')
(p/'batch.yaml').write_text('replay_repeat:\n  video_path: "'+src+'"\n  audio_path: "'+oldaudio+'"\n  result_name: replay-r2.mp4\npromotion:\n  video_path: "'+src+'"\n  audio_path: "'+newaudio+'"\n  result_name: avatar-promo-raw.mp4\n',encoding='utf-8')
first=json.loads((p/'replay-run.json').read_text(encoding='utf-8'));cmd=first['command'];cmd[cmd.index('--inference_config')+1]=str(p/'batch.yaml');cmd[cmd.index('--result_dir')+1]=str(p/'batch-output')
env=os.environ.copy();env.update({'PATH':ff+os.pathsep+env.get('PATH',''),'TORCH_HOME':str(root/'.torch_cache'),'HF_HOME':str(root/'.hf_cache'),'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','PYTHONUNBUFFERED':'1'})
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'inference_changes':'none; repeated original case plus same source video with new Chinese narration via native batch configuration','status':'RUNNING'}
(p/'batch-run.json').write_text(json.dumps(record,indent=2),encoding='utf-8');start=time.perf_counter()
with (p/'batch.log').open('w',encoding='utf-8') as log:r=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
record.update({'process_returncode':r.returncode,'process_seconds':time.perf_counter()-start,'finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PROCESS_EXITED_QUALITY_PENDING'})
(p/'batch-run.json').write_text(json.dumps(record,indent=2),encoding='utf-8');print(json.dumps(record),flush=True)
