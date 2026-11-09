import pathlib,json,subprocess,os,datetime,time,traceback
p=pathlib.Path('C:/AI/Video-Recipe-Reproduction-20261108/Avatar-Specialist-20261109')
root=pathlib.Path('C:/AI/MuseTalk')
ff='C:/Users/A/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.1-full_build/bin'
(p/'replay.yaml').write_text('task_0:\n  video_path: "'+str(p/'d24-input.mp4').replace('\\','/')+'"\n  audio_path: "'+str(p/'d24-speech.wav').replace('\\','/')+'"\n',encoding='utf-8')
cmd=[str(root/'.venv/Scripts/python.exe'),'-m','scripts.inference','--inference_config',str(p/'replay.yaml'),'--result_dir',str(p/'replay-r1'),'--unet_model_path','models/musetalkV15/unet.pth','--unet_config','models/musetalkV15/musetalk.json','--whisper_dir','models/whisper','--version','v15','--batch_size','2','--use_float16','--bbox_shift','0','--fps','25','--extra_margin','10','--parsing_mode','jaw','--left_cheek_width','90','--right_cheek_width','90','--ffmpeg_path',ff]
env=os.environ.copy();env.update({'PATH':ff+os.pathsep+env.get('PATH',''),'TORCH_HOME':str(root/'.torch_cache'),'HF_HOME':str(root/'.hf_cache'),'OMP_NUM_THREADS':'4','MKL_NUM_THREADS':'4','OPENBLAS_NUM_THREADS':'4','PYTHONUNBUFFERED':'1'})
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':cmd,'source_revision':subprocess.run(['git','rev-parse','HEAD'],cwd=root,capture_output=True,text=True).stdout.strip(),'tracked_changes':subprocess.run(['git','diff','--stat'],cwd=root,capture_output=True,text=True).stdout,'scope':'Original public D24 input and speech, same model hashes and inference settings; Windows path mapping only','status':'RUNNING'}
(p/'replay-run.json').write_text(json.dumps(record,indent=2),encoding='utf-8');start=time.perf_counter()
with (p/'replay.log').open('w',encoding='utf-8') as log:
 result=subprocess.run(cmd,cwd=root,env=env,stdout=log,stderr=subprocess.STDOUT)
record.update({'process_returncode':result.returncode,'process_seconds':time.perf_counter()-start,'status':'PROCESS_EXITED_QUALITY_NOT_YET_REVIEWED','finished_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()})
(p/'replay-run.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record),flush=True)
