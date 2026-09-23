from dataclasses import dataclass
from typing import FrozenSet, Iterable

@dataclass(frozen=True)
class MatureComponent:
    name: str
    requires: FrozenSet[str]
    provides: FrozenSet[str]
    mature: bool = True
    contract_compatible: bool = True
    unresolved_science: bool = False

def mature_composition_closure(
    initial_facts: Iterable[str],
    goal_facts: Iterable[str],
    components: Iterable[MatureComponent],
) -> dict:
    known=set(initial_facts)
    goals=set(goal_facts)
    used=[]
    remaining=list(components)

    progress=True
    while progress and not goals.issubset(known):
        progress=False
        for c in list(remaining):
            if not c.mature or not c.contract_compatible or c.unresolved_science:
                continue
            if c.requires.issubset(known):
                before=len(known)
                known.update(c.provides)
                remaining.remove(c)
                used.append(c.name)
                progress = progress or len(known)>before

    missing=sorted(goals-known)
    return {
        "closed": not missing,
        "used_components": used,
        "missing_goals": missing,
        "known_facts": sorted(known),
    }
