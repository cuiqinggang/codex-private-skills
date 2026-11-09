import pathlib,subprocess,json,datetime,time
p=pathlib.Path('C:/AI/Video-Recipe-Reproduction-20261108/Avatar-Specialist-20261109')
python=str(p/'tts-env/Scripts/python.exe')
parts=["\u5927\u5bb6\u597d\uff0c\u8fd9\u662f\u6570\u5b57\u4eba\u4ecb\u7ecd\u89c6\u9891\u6f14\u793a\u3002","\u51c6\u5907\u4e00\u6bb5\u6587\u6848\uff0c\u5c31\u80fd\u642d\u914d\u56fe\u7247\u3001\u6f14\u793a\u6587\u7a3f\u548c\u529f\u80fd\u753b\u9762\u3002","\u66f4\u6362\u6587\u6848\u540e\uff0c\u540c\u4e00\u4e2a\u4eba\u7269\u53ef\u4ee5\u7ee7\u7eed\u8bb2\u89e3\uff0c\u8ba9\u91cd\u70b9\u66f4\u6e05\u695a\u3002"]
record={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'voice':'zh-CN-XiaoxiaoNeural','rate':'+0%','pitch':'+0Hz','parts':parts,'results':[],'status':'RUNNING'}
(p/'promo-text.txt').write_text('\n'.join(parts),encoding='utf-8')
for i,text in enumerate(parts):
 cmd=[python,'-m','edge_tts','--voice',record['voice'],'--rate=+0%','--pitch=+0Hz','--text',text,'--write-media',str(p/('speech-'+str(i)+'.mp3')),'--write-subtitles',str(p/('speech-'+str(i)+'.srt'))]
 start=time.perf_counter()
 with (p/('tts-'+str(i)+'.log')).open('w',encoding='utf-8') as log:r=subprocess.run(cmd,stdout=log,stderr=subprocess.STDOUT)
 item={'index':i,'returncode':r.returncode,'seconds':time.perf_counter()-start,'command':cmd}
 record['results'].append(item);(p/'tts-run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(item),flush=True)
 if r.returncode: break
record['status']='AUDIO_FILES_CREATED_REVIEW_PENDING' if len(record['results'])==3 and all(x['returncode']==0 for x in record['results']) else 'TTS_BLOCKED'
(p/'tts-run.json').write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
print(record['status'],flush=True)
