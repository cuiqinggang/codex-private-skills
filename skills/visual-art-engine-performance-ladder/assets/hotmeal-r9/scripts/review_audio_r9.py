from pathlib import Path
import json,base64,re,urllib.request,urllib.error,time,hashlib
ROOT=Path('C:/AI/TenYears-Animatic-20261030');D=ROOT/'R9/AUDIO_REVIEW';D.mkdir(parents=True,exist_ok=True)
assert not (D/'submission.claim').exists()
keyfile=Path('C:/Users/A/AppData/Roaming/reasonix/.env')
key=None
if keyfile.exists():
 for line in keyfile.read_text(encoding='utf-8-sig').splitlines():
  m=re.match(r'''OPENROUTER_API_KEY\s*=\s*["']?([^"'\s]+)''',line.strip())
  if m:key=m.group(1);break
if not key:
 (D/'result.json').write_text(json.dumps({'state':'UNAVAILABLE','reason':'configured OpenRouter key unavailable','heard_audio':False}));print('AUDIO_REVIEW_UNAVAILABLE');raise SystemExit(0)
prompt='''You are an audio quality reviewer of two short fictional Mandarin drama takes. You MUST base conclusions on actual audio, not the supplied labels or a remembered script. File1 is C, a 7.292-second woman's continuous accusation. File2 is B, a 3.042-second man's short utterance followed by a single contact event. First transcribe verbatim in Simplified Chinese WITHOUT repairing synonyms or grammar. For the woman's final verb, provide the syllables/pinyin you actually hear and indicate uncertainty; do not replace it with a plausible idiom. Then assess whether each voice is visibly/aurally an in-room performance or a detached flat narrator, anger versus sadness, clear final syllable and breath continuity, whether clipping/harshness is actually audible, and the B impact's nature and approximate onset. Do not claim to inspect lips or spatial geometry because only audio is supplied. Output JSON with audio_received boolean; C{raw_transcript,final_verb_heard,pinyin,confidence,emotional_delivery,breath_and_end,quality_failures,timed_evidence}; B{raw_transcript,delivery,impact_onset_seconds,impact_character,quality_failures,timed_evidence}; overall_decision PASS/RETAKE/UNCERTAIN. Mark unsupported claims uncertain. This is an internal AI audio review, never human approval.'''
content=[{'type':'text','text':prompt}]
hashes={}
for label in ['C','B_AV']:
 p=ROOT/'R9/ASR'/label/'audio_16k.wav';b=p.read_bytes();hashes[label]=hashlib.sha256(b).hexdigest()
 content.extend([{'type':'text','text':'Next audio: '+label},{'type':'input_audio','input_audio':{'data':base64.b64encode(b).decode(),'format':'wav'}}])
payload={'model':'google/gemini-2.5-flash','messages':[{'role':'user','content':content}],'temperature':0,'max_tokens':2200,'response_format':{'type':'json_object'}}
(D/'submission.claim').write_text('single existing-provider audio review, no retries')
(D/'request-manifest.json').write_text(json.dumps({'model':payload['model'],'prompt':prompt,'source_sha256':hashes,'max_tokens':2200,'attempt_limit':1},ensure_ascii=False,indent=2),encoding='utf-8')
start=time.monotonic()
try:
 req=urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=120) as r:response=json.load(r)
 (D/'response.json').write_text(json.dumps(response,ensure_ascii=False,indent=2),encoding='utf-8')
 result={'state':'COMPLETED','elapsed_seconds':time.monotonic()-start,'model':response.get('model'),'id':response.get('id'),'usage':response.get('usage'),'content':response['choices'][0]['message']['content'],'human_approval':False}
except urllib.error.HTTPError as e:
 result={'state':'UNAVAILABLE','http_status':e.code,'elapsed_seconds':time.monotonic()-start,'heard_audio':False}
except Exception as e:
 result={'state':'UNAVAILABLE','error_type':type(e).__name__,'elapsed_seconds':time.monotonic()-start,'heard_audio':False}
(D/'result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=True),flush=True)
