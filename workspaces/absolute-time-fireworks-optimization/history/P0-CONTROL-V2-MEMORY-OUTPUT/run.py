import asyncio,hashlib,io,json,math,struct,time,uuid,zlib
from pathlib import Path
from statistics import median
import aiohttp
from PIL import Image
BEST=32.55975; ROOT=Path(__file__).parent; URL="http://127.0.0.1:8188"
FIXTURE=Path(r"C:\Users\A\Documents\Codex\2026-09-14\P0-CONTINUOUS-CONVERGENCE-20260914\workspaces\visual-art-engine-performance-ladder\stages\P0\P0-MEASUREMENT-PROTOCOL-V2-20260914T160020Z\assets\black-256.png")
INPUT=Path(r"C:\AI\ComfyUI_Aaki_v3\data\input\p0-control-black-256.png")
REFERENCE=Path(r"C:\Users\A\Documents\Codex\2026-09-14\P0-CONTINUOUS-CONVERGENCE-20260914\workspaces\visual-art-engine-performance-ladder\stages\P0\P0-E4-MINIMAL-DEFER-WS-CLOSE-20260914T152000Z\runtime-evidence\warmup-01-result.png")
WF={"1":{"class_type":"LoadImage","inputs":{"image":"p0-control-black-256.png"},"_meta":{"title":"P0 Deterministic Input"}},"2":{"class_type":"SaveImageWebsocket","inputs":{"images":["1",0]},"_meta":{"title":"P0 Memory PNG Output"}}}
def sha(b): return hashlib.sha256(b).hexdigest()
def png(data):
 if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError("signature")
 pos=8; ids=bytearray(); chunks=[]; wh=None; color=depth=interlace=None
 while pos+12<=len(data):
  n=struct.unpack(">I",data[pos:pos+4])[0]; k=data[pos+4:pos+8]; end=pos+8+n; stop=end+4; payload=data[pos+8:end]
  if stop>len(data) or zlib.crc32(k+payload)&0xffffffff!=struct.unpack(">I",data[end:stop])[0]: raise ValueError("chunk/CRC")
  chunks.append(k.decode()); pos=stop
  if k==b"IHDR": w,h,depth,color,_,_,interlace=struct.unpack(">IIBBBBB",payload); wh=(w,h)
  elif k==b"IDAT": ids.extend(payload)
  elif k==b"IEND": break
 if chunks[-1]!="IEND" or pos!=len(data) or wh!=(256,256): raise ValueError("structure/dimensions")
 raw=zlib.decompress(ids); channels={0:1,2:3,3:1,4:2,6:4}[color]
 if interlace!=0 or len(raw)!=wh[1]*(1+math.ceil(wh[0]*channels*depth/8)): raise ValueError("zlib full decode")
 with Image.open(io.BytesIO(data)) as im: im.load(); pixels=im.convert("RGBA").tobytes()
 return {"signature":True,"chunks":chunks,"crc":True,"zlib_full_decode":True,"width":wh[0],"height":wh[1],"sha256":sha(data),"decoded_pixel_sha256":sha(pixels)}
async def run(session,label,pixel_sha):
 cid=str(uuid.uuid4()); ws=await session.ws_connect(f"ws://127.0.0.1:8188/ws?clientId={cid}"); marks={}; pid=None
 image=asyncio.get_running_loop().create_future(); ready=asyncio.Event(); events=[]
 def mark(k): marks.setdefault(k,time.perf_counter_ns())
 async def receive():
  node=None; terminal=False
  while not(image.done() and terminal):
   msg=await ws.receive(timeout=15)
   if msg.type==aiohttp.WSMsgType.TEXT:
    e=json.loads(msg.data); d=e.get("data",{})
    if d.get("prompt_id")!=pid: continue
    kind=e.get("type"); events.append(kind)
    if kind=="executing" and d.get("node") is not None: node=str(d["node"]); mark("EXECUTION_START")
    elif kind=="executing": terminal=True
    elif kind in {"execution_error","execution_interrupted"}: raise RuntimeError(e)
   elif msg.type==aiohttp.WSMsgType.BINARY:
    b=bytes(msg.data)
    if node=="2" and len(b)>=8 and struct.unpack(">II",b[:8])==(1,2):
     if image.done(): raise ValueError("duplicate PNG")
     mark("BYTES_READY"); image.set_result(b[8:]); ready.set()
 async def history():
  await ready.wait(); mark("HISTORY_START")
  while True:
   async with session.get(f"{URL}/history/{pid}") as r: body=await r.text(); r.raise_for_status()
   entry=json.loads(body).get(pid); status=entry.get("status",{}) if entry else {}
   if entry and status.get("completed"):
    if status.get("status_str")!="success" or entry.get("prompt",[])[1:3]!=[pid,WF]: raise ValueError("matching completion")
    mark("HISTORY_DONE"); return body
   await asyncio.sleep(0)
 async def verify():
  data=await image; mark("VERIFY_START"); v=await asyncio.to_thread(png,data); mark("VERIFY_DONE")
  if v["decoded_pixel_sha256"]!=pixel_sha: raise ValueError("pixel equivalence")
  return data,v
 tasks=[]
 try:
  mark("REQUEST_START")
  async with session.post(f"{URL}/prompt",json={"prompt":WF,"client_id":cid}) as r: body=await r.text(); r.raise_for_status()
  pid=json.loads(body)["prompt_id"]; mark("QUEUE_ACK")
  recv=asyncio.create_task(receive()); hist=asyncio.create_task(history()); verify=asyncio.create_task(verify()); tasks=[recv,hist,verify]
  h,(data,v)=await asyncio.gather(hist,verify); mark("RESULT_READY"); await recv
  return {"label":label,"prompt_id":pid,"t_ms":(marks["RESULT_READY"]-marks["REQUEST_START"])/1e6,"marks":marks,"validation":v,"data":data,"history":h,"events":events}
 finally:
  for t in tasks:
   if not t.done(): t.cancel()
  if tasks: await asyncio.gather(*tasks,return_exceptions=True)
  await ws.close()
async def main():
 fixture,server,reference=png(FIXTURE.read_bytes()),png(INPUT.read_bytes()),png(REFERENCE.read_bytes())
 if fixture["sha256"]!=server["sha256"] or fixture["decoded_pixel_sha256"]!=reference["decoded_pixel_sha256"]: raise ValueError("frozen input/SaveImage reference")
 async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=20)) as s:
  async with s.get(f"{URL}/object_info/SaveImageWebsocket") as r: info=await r.json(); r.raise_for_status()
  if "SaveImageWebsocket" not in info: raise RuntimeError("SaveImageWebsocket not loaded")
  rows=[]
  for i in range(8): rows.append(await run(s,("warmup" if i<3 else "measured")+f"-{i+1 if i<3 else i-2:02}",reference["decoded_pixel_sha256"]))
 values=[r["t_ms"] for r in rows[3:]]; p50=median(values); x=sorted(values); p95=x[3]+.8*(x[4]-x[3]); gain=BEST-p50
 decision="ROLLBACK" if p50>=30.5 else ("STRONG_KEEP" if p50<26 else "KEEP")
 summary={"CURRENT_BEST_MS":BEST,"MACRO_R1_P50_MS":p50,"MACRO_R1_P95_MS":p95,"ABSOLUTE_GAIN_MS":gain,"IMPROVEMENT_PERCENT":gain/BEST*100,"VALID":"5/5","DISK_WRITE_IN_CRITICAL_PATH":"NO","KEEP_OR_ROLLBACK":decision,"saveimage_reference":reference,"runs":[{k:v for k,v in r.items() if k not in {"data","history"}} for r in rows]}
 evidence=ROOT/("evidence-"+time.strftime("%Y%m%d-%H%M%S")); evidence.mkdir()
 for r in rows:
  (evidence/(r["label"]+".png")).write_bytes(r["data"]); (evidence/(r["label"]+"-history.json")).write_text(r["history"],encoding="utf-8")
 (evidence/"results.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(summary,ensure_ascii=False,indent=2))
if __name__=="__main__": asyncio.run(main())
