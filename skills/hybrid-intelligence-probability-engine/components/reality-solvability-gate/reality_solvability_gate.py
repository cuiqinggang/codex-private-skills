from dataclasses import dataclass

@dataclass(frozen=True)
class SolvabilityFacts:
    spec_complete: bool
    evidence_search_complete: bool
    physically_admissible: bool
    mature_direct_solution: bool
    mature_component_closure: bool
    mature_exploration_protocol: bool
    acceptance_verifiable: bool

def classify(f: SolvabilityFacts) -> str:
    if not f.spec_complete:
        return "INCOMPLETE_SPEC"
    if not f.evidence_search_complete:
        return "SOLUTION_SEARCH_REQUIRED"
    if not f.physically_admissible:
        return "INFEASIBLE_OR_CONTRADICTORY"
    if f.mature_direct_solution:
        return "MATURE_DIRECT"
    if f.mature_component_closure:
        return "MATURE_COMPOSABLE"
    if f.mature_exploration_protocol:
        return "MATURE_EXPLORATORY"
    return "FRONTIER_UNKNOWN"

def world_solved(f: SolvabilityFacts) -> bool:
    return bool(
        f.mature_direct_solution
        or f.mature_component_closure
        or f.mature_exploration_protocol
    )

def frontier_unknown_formula(f: SolvabilityFacts) -> bool:
    return bool(
        f.spec_complete
        and f.evidence_search_complete
        and f.physically_admissible
        and not world_solved(f)
    )

def production_certifiable(f: SolvabilityFacts) -> bool:
    return classify(f) in {
        "MATURE_DIRECT",
        "MATURE_COMPOSABLE",
        "MATURE_EXPLORATORY",
    } and f.acceptance_verifiable
