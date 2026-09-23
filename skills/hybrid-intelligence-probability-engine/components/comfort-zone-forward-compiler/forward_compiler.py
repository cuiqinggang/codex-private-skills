from dataclasses import dataclass, asdict

@dataclass(frozen=True)
class NodeFacts:
    semantic_preserved: bool
    deterministic_exact: bool
    deterministic_executor_available: bool
    explicit_or_extractable_state: bool
    finite_or_enumerable_choice: bool
    certified_action_ontology: bool
    deterministic_verifier: bool
    requires_open_generation: bool
    unresolved_hidden_information: bool
    timed_retry_required: bool

def route(node: NodeFacts) -> str:
    if (
        node.semantic_preserved
        and node.deterministic_exact
        and node.deterministic_executor_available
    ):
        return "CODE"

    jev_ok = (
        node.semantic_preserved
        and node.explicit_or_extractable_state
        and node.finite_or_enumerable_choice
        and node.certified_action_ontology
        and node.deterministic_verifier
        and not node.requires_open_generation
        and not node.unresolved_hidden_information
        and not node.timed_retry_required
    )
    if jev_ok:
        return "JEV"

    return "GPT"

def explain(node: NodeFacts) -> dict:
    return {"facts": asdict(node), "route": route(node)}
