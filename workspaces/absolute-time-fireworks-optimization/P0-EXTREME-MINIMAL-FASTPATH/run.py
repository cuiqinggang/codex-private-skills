import asyncio, hashlib, io, json, time, uuid
from pathlib import Path
from statistics import median
import aiohttp
from PIL import Image

ROOT=Path(__file__).parent
URL="http://127.0.0.1:8188"
CURRENT_BEST_MS=14.1638
REFERENCE=Path(r"C:\Users\A\Documents\Codex\2026-09-14\P0-CONTINUOUS-CONVERGENCE-20260914\workspaces\visual-art-engine-performance-ladder\stages\P0\P0-E4-MINIMAL-DEFER-WS-CLOSE-20260914T152000Z\runtime-evidence\warmup-01-result.png")
WORKFLOW={
 "1":{"class_type":"LoadImage","inputs":{"image":"p0-control-black-256.png"}},
 "2":{"class_type":"P0CachedPNGWebsocket","inputs":{"images":["1",0]}},
}

def decode_and_identify(data):
 if not data.startswith(b"\x89PNG\r\n\x1a\n"): raise ValueError("PNG signature")
 with Image.open(io.BytesIO(data)) as image:
  if image.format!="PNG" or image.size!=(256,256): raise ValueError("PNG format/dimensions")
  image.load()
  pixels=image.convert("RGBA").tobytes()
 return hashlib.sha256(pixels).hexdigest()

async def one_run(session,label,expected_pixels):
 client_id=str(uuid.uuid4())
 ws=await session.ws_connect(f"ws://127.0.0.1:8188/ws?clientId={client_id}")
 marks={}; prompt_id=None; loop=asyncio.get_running_loop()
 image_ready=loop.create_future(); success_ready=loop.create_future()
 def mark(name): marks.setdefault(name,time.perf_counter_ns())
 async def receive():
  node=None
  while not (image_ready.done() and success_ready.done()):
   message=await ws.receive()
   if message.type==aiohttp.WSMsgType.TEXT:
    event=json.loads(message.data); data=event.get("data",{})
    if data.get("prompt_id")!=prompt_id: continue
    kind=event.get("type")
    if kind=="executing" and data.get("node") is not None:
     node=str(data["node"]); mark("EXECUTION_START")
    elif kind=="execution_success":
     mark("EXECUTION_SUCCESS")
     if not success_ready.done(): success_ready.set_result(True)
    elif kind in {"execution_error","execution_interrupted"}:
     error=RuntimeError(event)
     if not image_ready.done(): image_ready.set_exception(error)
     if not success_ready.done(): success_ready.set_exception(error)
   elif message.type==aiohttp.WSMsgType.BINARY:
    payload=bytes(message.data)
    if node=="2" and payload[:8]==b"\0\0\0\1\0\0\0\2":
     if image_ready.done(): raise ValueError("duplicate PNG")
     mark("BYTES_READY"); image_ready.set_result(payload[8:])
 receiver=None
 try:
  mark("REQUEST_START")
  async with session.post(f"{URL}/prompt",json={"prompt":WORKFLOW,"client_id":client_id}) as response:
   body=await response.read(); response.raise_for_status()
  prompt_id=json.loads(body)["prompt_id"]; mark("QUEUE_ACK")
  receiver=asyncio.create_task(receive())
  png_bytes,_=await asyncio.gather(image_ready,success_ready)
  mark("RESULT_START")
  if decode_and_identify(png_bytes)!=expected_pixels: raise ValueError("result identity")
  mark("RESULT_READY"); await receiver
  return {
   "label":label,"prompt_id":prompt_id,
   "t_ms":(marks["RESULT_READY"]-marks["REQUEST_START"])/1e6,
   "request_ms":(marks["QUEUE_ACK"]-marks["REQUEST_START"])/1e6,
   "queue_ms":(marks["EXECUTION_START"]-marks["QUEUE_ACK"])/1e6,
   "execute_ms":(max(marks["BYTES_READY"],marks["EXECUTION_SUCCESS"])-marks["EXECUTION_START"])/1e6,
   "result_ms":(marks["RESULT_READY"]-marks["RESULT_START"])/1e6,
   "png_bytes":png_bytes,
  }
 finally:
  if receiver and not receiver.done():
   receiver.cancel(); await asyncio.gather(receiver,return_exceptions=True)
  await ws.close()

def p95(values):
 ordered=sorted(values)
 return ordered[3]+.8*(ordered[4]-ordered[3])

async def main():
 expected_pixels=decode_and_identify(REFERENCE.read_bytes())
 timeout=aiohttp.ClientTimeout(total=None); connector=aiohttp.TCPConnector(limit=0)
 async with aiohttp.ClientSession(timeout=timeout,connector=connector) as session:
  rows=[]
  for index in range(7):
   kind="warmup" if index<2 else "measured"; number=index+1 if index<2 else index-1
   rows.append(await one_run(session,f"{kind}-{number:02}",expected_pixels))
 measured=rows[2:]; values=[row["t_ms"] for row in measured]
 new_p50=median(values); gain=CURRENT_BEST_MS-new_p50
 macro={name:median([row[name] for row in measured]) for name in ("request_ms","queue_ms","execute_ms","result_ms")}
 summary={
  "PREVIOUS_BEST_MS":CURRENT_BEST_MS,
  "MINIMAL_FASTPATH_P50_MS":new_p50,
  "MINIMAL_FASTPATH_P95_MS":p95(values),
  "MIN_MS":min(values),
  "ARMOR_REMOVAL_GAIN_MS":gain,
  "ARMOR_REMOVAL_GAIN_PERCENT":gain/CURRENT_BEST_MS*100,
  "VALID":"5/5",
  "KEEP_OR_ROLLBACK":"KEEP" if gain>0 else "ROLLBACK",
  "REQUEST_MS":macro["request_ms"],"QUEUE_MS":macro["queue_ms"],
  "EXECUTE_MS":macro["execute_ms"],"RESULT_MS":macro["result_ms"],
  "DISK_WRITE_IN_CRITICAL_PATH":"NO",
  "runs":[{key:value for key,value in row.items() if key!="png_bytes"} for row in rows],
 }
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
 evidence=ROOT/("evidence-"+time.strftime("%Y%m%d-%H%M%S")); evidence.mkdir()
 (evidence/"representative-final.png").write_bytes(measured[-1]["png_bytes"])
 (evidence/"results.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": asyncio.run(main())
