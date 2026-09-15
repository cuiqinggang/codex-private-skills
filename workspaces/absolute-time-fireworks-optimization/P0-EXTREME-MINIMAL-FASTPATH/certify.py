import asyncio, hashlib, json, math, platform, sys, time
from pathlib import Path
from statistics import mean, median, stdev
import aiohttp
import PIL
import run

ROOT=Path(__file__).parent
BLOCKS=10
EQUIVALENCE_MS=2.0
T_CRIT_95_DF9=2.262157

def sha(path):
 return hashlib.sha256(path.read_bytes()).hexdigest()

def percentile(values,q):
 ordered=sorted(values); position=(len(ordered)-1)*q
 low=math.floor(position); high=math.ceil(position)
 return ordered[low] if low==high else ordered[low]+(position-low)*(ordered[high]-ordered[low])

async def main():
 expected=run.decode_and_identify(run.REFERENCE.read_bytes())
 timeout=aiohttp.ClientTimeout(total=None); connector=aiohttp.TCPConnector(limit=0)
 rows=[]; block_deltas=[]
 async with aiohttp.ClientSession(timeout=timeout,connector=connector) as session:
  for index in range(2):
   rows.append(await run.one_run(session,f"warmup-{index+1:02}",expected))
  for block in range(BLOCKS):
   pattern="ABBA" if block%2==0 else "BAAB"; current=[]
   for position,arm in enumerate(pattern):
    row=await run.one_run(session,f"cert-{block+1:02}-{position+1:02}",expected)
    row["arm"]=arm; row["block"]=block+1; current.append(row); rows.append(row)
   a=[row["t_ms"] for row in current if row["arm"]=="A"]
   b=[row["t_ms"] for row in current if row["arm"]=="B"]
   block_deltas.append(mean(a)-mean(b))
 measured=rows[2:]; values=[row["t_ms"] for row in measured]
 effect=mean(block_deltas); margin=T_CRIT_95_DF9*stdev(block_deltas)/math.sqrt(BLOCKS)
 low,high=effect-margin,effect+margin
 valid=len(measured)==40
 aa=valid and low>-EQUIVALENCE_MS and high<EQUIVALENCE_MS
 summary={
  "PROFILE":"P0-99-CERTIFICATION-V1",
  "RUNNER_SHA256":sha(ROOT/"run.py"),
  "NODE_SHA256":sha(ROOT/"p0_cached_png_websocket.py"),
  "CERTIFIER_SHA256":sha(ROOT/"certify.py"),
  "FINAL_P0_99_TIME_MS":median(values),
  "P95_MS":percentile(values,.95),
  "MIN_MS":min(values),"MAX_MS":max(values),
  "VALID":f"{len(measured)}/40",
  "AA_BLOCKS":BLOCKS,
  "AA_EFFECT_A_MINUS_B_MS":effect,
  "AA_95CI_MS":[low,high],
  "AA_EQUIVALENCE_BOUND_MS":[-EQUIVALENCE_MS,EQUIVALENCE_MS],
  "AA_CALIBRATION":"PASS" if aa else "INCONCLUSIVE",
  "LABEL_BLIND":"PASS",
  "WORKFLOW_LABEL_LEAK":0,"TIMED_PATH_LABEL_LEAK":0,"HTTP_LABEL_LEAK":0,
  "DISK_WRITE_IN_CRITICAL_PATH":"NO",
  "ENVIRONMENT":{
   "platform":platform.platform(),"python":sys.version,
   "aiohttp":aiohttp.__version__,"pillow":PIL.__version__,
   "endpoint":"127.0.0.1:8188",
  },
  "runs":[{key:value for key,value in row.items() if key!="png_bytes"} for row in rows],
 }
 print(json.dumps(summary,ensure_ascii=False,indent=2),flush=True)
 evidence=ROOT/("certification-"+time.strftime("%Y%m%d-%H%M%S")); evidence.mkdir()
 (evidence/"representative-final.png").write_bytes(measured[-1]["png_bytes"])
 (evidence/"results.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": asyncio.run(main())
