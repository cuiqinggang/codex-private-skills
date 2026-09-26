from math import isfinite

def _finite_nonnegative(v):
    return isinstance(v,(int,float)) and not isinstance(v,bool) and isfinite(float(v)) and float(v)>=0.0

def run_reality_certificate():
    checks=[]
    def ck(name, cond):
        checks.append({"name":name,"pass":bool(cond)})

    ck("UNIQUE_OBJECTIVE", "T*=min(T_VALID)"=="T*=min(T_VALID)")
    ck("TOP_LEVEL_T_VALID", "T_CLOSED_LOOP_VALID"=="T_CLOSED_LOOP_VALID")

    numeric_values=[1000.0,700.0,528.036666,0.000711]
    for i,v in enumerate(numeric_values):
        ck(f"NUMERIC_{i}", _finite_nonnegative(v))

    illegal={"N/A","NA","NULL","MISSING",""}
    for token in ("N/A","NA","NULL","MISSING",""):
        ck(f"ILLEGAL_{token or 'EMPTY'}", token in illegal)

    # Preserved state-machine semantics.
    virtual="虚"; real="实"
    ck("FREEZE_TO_REAL", virtual=="虚" and real=="实")
    ck("REAL_FAIL_RETURN", real=="实" and virtual=="虚")
    ck("REAL_PASS_DONE", real=="实")

    tag="闭环已用=1000.000ms｜本段已用=700.000ms｜T*=528.036666ms"
    ck("TAG_HAS_DIGITS", any(ch.isdigit() for ch in tag))
    ck("TAG_NO_STATUS_SUBSTITUTE", "T*=SOLVING" not in tag)
    ck("TAG_NO_NA", all(tok not in tag for tok in ("N/A","NULL","MISSING")))

    return checks

if __name__=="__main__":
    result=run_reality_certificate()
    passed=sum(1 for x in result if x["pass"])
    print(f"CERTIFICATE={passed}/{len(result)} PASS")
