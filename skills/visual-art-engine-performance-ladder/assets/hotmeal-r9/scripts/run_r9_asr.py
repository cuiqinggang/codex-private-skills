from pathlib import Path
import subprocess,json,hashlib,time
ROOT=Path('C:/AI/TenYears-Animatic-20261030');R=ROOT/'R9/ASR'
MODEL=Path('C:/Users/A/.codex/tools/whispercpp/models/ggml-large-v3.bin')
EXE=Path('C:/Users/A/.codex/tools/whispercpp-gpu/Release/whisper-cli.exe')
start=time.monotonic();h=hashlib.sha1()
with MODEL.open('rb') as f:
 for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
assert h.hexdigest().upper()=='AD82BF6A9043CEED055076D0FD39F5F186FF8062'
for shot in ['C','B_AV']:
 D=R/shot;D.mkdir(parents=True,exist_ok=True)
 assert not (D/'transcript.json').exists(),'ALREADY_DONE'
 src=ROOT/'R8'/shot/'native.mp4';wav=D/'audio_16k.wav'
 subprocess.run(['ffmpeg','-v','error','-y','-i',str(src),'-vn','-ac','1','-ar','16000','-c:a','pcm_s16le',str(wav)],check=True)
 a=time.monotonic()
 with (D/'whisper.log').open('wb') as log:
  subprocess.run([str(EXE),'-m',str(MODEL),'-f',str(wav),'-l','zh','-t','4','-osrt','-otxt','-ojf','-of',str(D/'transcript')],stdout=log,stderr=subprocess.STDOUT,check=True)
 text=(D/'transcript.txt').read_text(encoding='utf-8-sig').strip();assert text
 (D/'run-manifest.json').write_text(json.dumps({'input':str(src),'engine':'existing whisper.cpp GPU large-v3','model_sha1':h.hexdigest(),'elapsed_seconds':time.monotonic()-a,'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'wrapper_fix':'Python subprocess avoids PowerShell5 stderr-as-error on FFmpeg informational banner','raw_text':text,'artistic_approval':False},ensure_ascii=False,indent=2),encoding='utf-8')
 print(shot,json.dumps(text,ensure_ascii=True),flush=True)
print('R9_ASR_TERMINAL',round(time.monotonic()-start,3),flush=True)
