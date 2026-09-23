from itertools import product
from reality_solvability_gate import (
    SolvabilityFacts, classify, frontier_unknown_formula
)

FIELDS = list(SolvabilityFacts.__dataclass_fields__)

def main():
    total=0
    frontier=0
    violations=0
    counts={}
    for values in product([False, True], repeat=len(FIELDS)):
        f=SolvabilityFacts(**dict(zip(FIELDS, values)))
        got=classify(f)
        counts[got]=counts.get(got,0)+1
        expected_frontier=frontier_unknown_formula(f)
        if (got=="FRONTIER_UNKNOWN") != expected_frontier:
            violations+=1
        if got=="FRONTIER_UNKNOWN":
            frontier+=1
            assert f.spec_complete
            assert f.evidence_search_complete
            assert f.physically_admissible
            assert not f.mature_direct_solution
            assert not f.mature_component_closure
            assert not f.mature_exploration_protocol
        if f.mature_direct_solution and f.spec_complete and f.evidence_search_complete and f.physically_admissible:
            assert got=="MATURE_DIRECT"
        total+=1

    assert violations==0
    print(f"RULE_SPACE={total}")
    print(f"RULE_SPACE_PASS={total}/{total}")
    print(f"FRONTIER_UNKNOWN_CASES={frontier}")
    print(f"FORMULA_VIOLATIONS={violations}")
    print(f"CLASS_COUNTS={counts}")

if __name__=="__main__":
    main()
