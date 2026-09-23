from itertools import product
from forward_compiler import NodeFacts, route

FIELDS = [
    "semantic_preserved",
    "deterministic_exact",
    "deterministic_executor_available",
    "explicit_or_extractable_state",
    "finite_or_enumerable_choice",
    "certified_action_ontology",
    "deterministic_verifier",
    "requires_open_generation",
    "unresolved_hidden_information",
    "timed_retry_required",
]

def oracle(d):
    if d["semantic_preserved"] and d["deterministic_exact"] and d["deterministic_executor_available"]:
        return "CODE"
    if (
        d["semantic_preserved"]
        and d["explicit_or_extractable_state"]
        and d["finite_or_enumerable_choice"]
        and d["certified_action_ontology"]
        and d["deterministic_verifier"]
        and not d["requires_open_generation"]
        and not d["unresolved_hidden_information"]
        and not d["timed_retry_required"]
    ):
        return "JEV"
    return "GPT"

def current_48_fixture():
    rows=[]
    for _ in range(16):
        rows.append((NodeFacts(True,True,True,False,False,False,True,False,False,False),"CODE"))
    for _ in range(24):
        rows.append((NodeFacts(True,False,False,True,True,True,True,False,False,False),"JEV"))
    for _ in range(8):
        rows.append((NodeFacts(True,False,False,True,False,False,True,True,False,False),"GPT"))
    return rows

def main():
    exhaustive=0
    counts={"CODE":0,"JEV":0,"GPT":0}
    for values in product([False,True], repeat=len(FIELDS)):
        d=dict(zip(FIELDS,values))
        got=route(NodeFacts(**d))
        want=oracle(d)
        assert got==want,(d,got,want)
        counts[got]+=1
        exhaustive+=1

    fixture=current_48_fixture()
    for node,want in fixture:
        assert route(node)==want

    print(f"FORMAL_RULE_SPACE_CASES={exhaustive}")
    print("FORMAL_RULE_SPACE_PASS=1024/1024")
    print(f"FORMAL_ROUTE_COUNTS={counts}")
    print("CURRENT_48_ROUTE_PASS=48/48")
    print("SEMANTIC_GENERALIZATION_REAL_CERT=NOT_DONE")

if __name__=="__main__":
    main()
