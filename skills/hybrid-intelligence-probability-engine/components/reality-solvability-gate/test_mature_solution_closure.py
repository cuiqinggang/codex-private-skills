from mature_solution_closure import MatureComponent,mature_composition_closure

def c(name,req,out,**kw):
    return MatureComponent(name,frozenset(req),frozenset(out),**kw)

def main():
    cases=[]

    file_pipeline=[
        c("reader",["files"],["parsed"]),
        c("extractor",["parsed"],["facts"]),
        c("aggregator",["facts"],["summary"]),
        c("verifier",["summary"],["verified_summary"]),
    ]
    cases.append(("FILE_PIPELINE",mature_composition_closure(["files"],["verified_summary"],file_pipeline),True))

    software_deploy=[
        c("build",["source"],["artifact"]),
        c("test",["artifact"],["tested_artifact"]),
        c("deploy",["tested_artifact","target"],["deployed"]),
        c("healthcheck",["deployed"],["verified_deployment"]),
    ]
    cases.append(("DEPLOY",mature_composition_closure(["source","target"],["verified_deployment"],software_deploy),True))

    broken=[
        c("build",["source"],["artifact"]),
        c("deploy",["tested_artifact"],["deployed"]),
    ]
    cases.append(("MISSING_EDGE",mature_composition_closure(["source"],["deployed"],broken),False))

    frontier=[
        c("known_lab_setup",["materials"],["experiment_ready"]),
        c("new_physics_breakthrough",["experiment_ready"],["new_law"],mature=False,unresolved_science=True),
    ]
    cases.append(("FRONTIER_DEP",mature_composition_closure(["materials"],["new_law"],frontier),False))

    incompatible=[
        c("a",["x"],["y"]),
        c("b",["y"],["z"],contract_compatible=False),
    ]
    cases.append(("INCOMPATIBLE",mature_composition_closure(["x"],["z"],incompatible),False))

    passed=0
    for name,result,want in cases:
        ok=result["closed"]==want
        assert ok,(name,result,want)
        passed+=1
        print(name,result)

    print(f"CLOSURE_CASES={len(cases)}")
    print(f"CLOSURE_PASS={passed}/{len(cases)}")

if __name__=="__main__":
    main()
