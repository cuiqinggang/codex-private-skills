import argparse, json, random
from pathlib import Path
from statistics import median

def q(xs, p):
    ys=sorted(xs); x=(len(ys)-1)*p; lo=int(x); hi=min(lo+1,len(ys)-1)
    return ys[lo]+(ys[hi]-ys[lo])*(x-lo)

def build(rows, repetitions=20000, seed=2026091507):
    rows=[r for r in rows if r.get("attempt",0)>0]
    out=[]
    if len(rows)%3: raise ValueError("bracket input must contain complete independent ABA triples")
    identities=[r.get("prompt_id",r["attempt"]) for r in rows]
    if len(set(identities))!=len(identities): raise ValueError("shared run identity across bracket clusters")
    for i in range(0,len(rows),3):
        before,r,after=rows[i:i+3]
        if [before["arm"],r["arm"],after["arm"]] != ["A","B","A"]: raise ValueError("each bracket must be an explicit ABA triple")
        local=median([before["t_ms"],after["t_ms"]]); drift=after["t_ms"]-before["t_ms"]
        out.append({"BLOCK_ID":i//3,"A_BEFORE_MS":before["t_ms"],"B_MS":r["t_ms"],"A_AFTER_MS":after["t_ms"],"LOCAL_BASELINE_MS":local,"LOCAL_DRIFT_MS":drift,"LOCAL_DRIFT_PERCENT":100*drift/before["t_ms"],"B_GAIN_MS":local-r["t_ms"],"B_GAIN_PERCENT":100*(local-r["t_ms"])/local})
    if not out: raise ValueError("no complete A_before/B/A_after brackets")
    rng=random.Random(seed); boots=[]
    for _ in range(repetitions):
        sample=[rng.choice(out)["B_GAIN_MS"] for _ in out]
        boots.append(median(sample))
    gains=[x["B_GAIN_MS"] for x in out]
    return {"brackets":out,"batch":{"n":len(out),"CLUSTER_COUNT":len(out),"EFFECTIVE_INDEPENDENT_BLOCKS":len(out),"BRACKET_CLUSTER_METHOD":"cluster_bootstrap_by_explicit_ABA_bracket_id","BRACKET_MEDIAN_GAIN_MS":median(gains),"BRACKET_P95_GAIN_MS":q(gains,.95),"CLUSTER_BOOTSTRAP_95CI":[q(boots,.025),q(boots,.975)],"BRACKET_BOOTSTRAP_95CI_MS":[q(boots,.025),q(boots,.975)],"bootstrap_unit":"complete_ABA_triple","bootstrap_repetitions":repetitions,"seed":seed}}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--input"); ap.add_argument("--output"); ap.add_argument("--selftest",action="store_true"); a=ap.parse_args()
    if a.selftest:
        rows=[{"attempt":i+1,"arm":arm,"t_ms":t} for i,(arm,t) in enumerate(zip("ABAABA",[10,9,10,11,10,11]))]
        result=build(rows,100,1); assert result["batch"]["n"]==2 and result["batch"]["BRACKET_MEDIAN_GAIN_MS"]==1
        print("BRACKET_SELFTEST_PASS"); return
    rows=[json.loads(x) for x in Path(a.input).read_text(encoding="utf-8").splitlines() if x.strip()]
    Path(a.output).write_text(json.dumps(build(rows),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if __name__=="__main__": main()
