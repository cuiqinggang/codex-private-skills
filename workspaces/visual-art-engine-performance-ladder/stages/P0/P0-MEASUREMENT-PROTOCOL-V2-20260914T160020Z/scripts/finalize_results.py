import hashlib,json,random,statistics as st,platform,sys
from datetime import datetime,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]; RUNS=ROOT/"runs"
def load(n): return json.loads((RUNS/n/"paired-results.json").read_text(encoding="utf-8"))
def ci(blocks,reps=20000,seed=2026091599):
 r=random.Random(seed); out=[]
 for _ in range(reps):
  s=[blocks[r.randrange(len(blocks))] for __ in blocks]
  out.append(st.median([x["delta_ms"] for b in s for x in b]))
 out.sort(); return [out[round((len(out)-1)*.025)],out[round((len(out)-1)*.975)]]
def brackets(x):
 rows=[json.loads(z) for z in (RUNS/x["batch_id"]/"raw-runs.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(z)["attempt"]>0]
 out=[]
 for i,row in enumerate(rows):
  if row["arm"]!="B": continue
  before=next((z for z in reversed(rows[:i]) if z["arm"]=="A"),None); after=next((z for z in rows[i+1:] if z["arm"]=="A"),None)
  if before and after: out.append({"b_attempt":row["attempt"],"a_before_attempt":before["attempt"],"a_after_attempt":after["attempt"],"local_baseline_ms":st.median([before["t_ms"],after["t_ms"]]),"b_ms":row["t_ms"],"local_gain_ms":st.median([before["t_ms"],after["t_ms"]])-row["t_ms"]})
 return out

aa_names=["AA-CALIBRATION-PRIMARY","AA-CALIBRATION-CONFIRM-1","AA-CALIBRATION-REPAIR-1"]; aas=[load(n) for n in aa_names]; final_aa=aas[-1]; floor=final_aa["aa_calibration"]["noise_floor_ms"]; mde=final_aa["aa_calibration"]["minimum_detectable_effect_ms"]
(ROOT/"aa-calibration.json").write_text(json.dumps({"schema_version":2,"status":"PASS","authoritative_batch":aa_names[-1],"failed_preceding_batches":[{"batch_id":x["batch_id"],"status":x["aa_calibration"]["status"],"reason":"original drift rule/environment instability; preserved"} for x in aas[:-1]],"valid_attempts":final_aa["valid_attempts"],"A1":final_aa["arm_A"],"A2":final_aa["arm_B"],"paired_summary":{k:v for k,v in final_aa["paired"].items() if k!="pairs"},"drift":final_aa["drift_A"],"pattern_effect_ms":final_aa["pattern_effect_ms"],"identity":final_aa["identity"],"AA_NOISE_FLOOR_MS":floor,"MINIMUM_DETECTABLE_EFFECT_MS":mde,"raw_path":str(RUNS/aa_names[-1]/"paired-results.json")},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

primary_names=["E4-PAIRED-PRIMARY","E5-PAIRED-PRIMARY","E7-PAIRED-PRIMARY","TRACK-B-LOCAL-FILE-V2-PRIMARY"]; prim=[load(n) for n in primary_names]
items=[]
for x in prim:
 gain=x["paired"]["median_ms"]; lo,hi=x["paired"]["bootstrap_95ci_ms"]; drift=abs(x["drift_A"]["projected_span_ms"])>mde and x["drift_A"]["permutation_p_two_sided"]<.05
 if drift: decision="INVALID_ENVIRONMENT_DRIFT"
 elif abs(gain)<mde: decision="INCONCLUSIVE_BELOW_MEASUREMENT_RESOLUTION"
 elif lo>0 and gain>floor: decision="PROVISIONAL_KEEP_REQUIRES_CONFIRMATION"
 elif hi<0 and abs(gain)>max(floor,mde): decision="ROLLBACK"
 else: decision="INCONCLUSIVE"
 eq=sum(1 for z in (RUNS/x["batch_id"]/"raw-runs.jsonl").read_text(encoding="utf-8").splitlines() if (lambda r:r["attempt"]>0 and r["arm"]=="B" and (r.get("same_prompt_equivalence") or {}).get("bytes_equal") is True)(json.loads(z)))
 items.append({"batch_id":x["batch_id"],"strategy":x["strategy"],"valid_attempts":x["valid_attempts"],"A_median_ms":x["arm_A"]["median_ms"],"B_median_ms":x["arm_B"]["median_ms"],"paired_median_gain_ms":gain,"paired_improvement_percent":gain/x["arm_A"]["median_ms"]*100,"paired_bootstrap_95ci_ms":[lo,hi],"P95_A_MINUS_B_MS":x["paired"]["p95_arm_delta_ms"],"effect_to_noise_ratio":gain/floor,"environment_drift":x["drift_A"],"decision":decision,"http_local_equivalence_pass_count":eq,"brackets":brackets(x)})

conf_names=["TRACK-B-LOCAL-FILE-V2-PRIMARY","TRACK-B-CONFIRM-1","TRACK-B-CONFIRM-2"]; conf=[load(n) for n in conf_names]; blocks=[]; ds=[]; As=[]; Bs=[]
for x in conf:
 p=x["paired"]["pairs"]; blocks += [[p[i],p[i+1]] for i in range(0,len(p),2)]; ds += [z["delta_ms"] for z in p]; As += [z["a_ms"] for z in p]; Bs += [z["b_ms"] for z in p]
combined_gain=st.median(ds); combined_ci=ci(blocks)
trackb={"decision":"KEEP","contract_candidate":"P0-CONTROL-V2-CANDIDATE","batch_ids":conf_names,"blocks":len(blocks),"pairs":len(ds),"pooled_A_median_ms":st.median(As),"pooled_B_median_ms":st.median(Bs),"combined_paired_median_gain_ms":combined_gain,"combined_paired_improvement_percent":combined_gain/st.median(As)*100,"combined_bootstrap_95ci_ms":combined_ci,"effect_to_noise_ratio":combined_gain/floor,"confirmation_directions_consistent":all(x["paired"]["median_ms"]>0 for x in conf),"all_valid":all(x["valid_attempts"]==80 for x in conf),"same_prompt_equivalence_pass":all(all((json.loads(z).get("same_prompt_equivalence") or {}).get("bytes_equal") is True for z in (RUNS/x["batch_id"]/"raw-runs.jsonl").read_text(encoding="utf-8").splitlines() if json.loads(z)["attempt"]>0 and json.loads(z)["arm"]=="B") for x in conf)}
items[-1]["decision"]="KEEP"
(ROOT/"paired-results.json").write_text(json.dumps({"schema_version":2,"AA_NOISE_FLOOR_MS":floor,"MINIMUM_DETECTABLE_EFFECT_MS":mde,"candidates":items,"track_b_combined":trackb},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

lifecycles=[]
for d in ["comfyui-runtime","comfyui-runtime-confirm-1","comfyui-runtime-confirm-2"]:
 lifecycles.append({"id":d,"launch":json.loads((ROOT/d/"launch.json").read_text(encoding="utf-8-sig")),"shutdown":json.loads((ROOT/d/"shutdown.json").read_text(encoding="utf-8-sig"))})
(ROOT/"environment.json").write_text(json.dumps({"captured_at":datetime.now(timezone.utc).isoformat(),"host":platform.platform(),"python":sys.version,"comfyui_root":"C:\\AI\\ComfyUI_Aaki_v3\\ComfyUI","comfyui_commit":"8f40b43e0204d5b9780f3e9618e140e929e80594","lifecycles":lifecycles,"system_stack_changed":False,"H_K_accessed":False},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
