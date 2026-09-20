// Precompiled deterministic validator for PE-P0-GENERAL-01 v1.1.
// No runtime schema compilation.
const ACTIONS = ["EXECUTE","HOLD","ROUTE","REJECT"];
export function validateInput(x) {
  const errors=[];
  if (!x || typeof x !== "object") return {ok:false,errors:["ROOT_NOT_OBJECT"]};
  if (x.benchmark_id !== "PE-P0-GENERAL-01") errors.push("BAD_BENCHMARK_ID");
  if (!x.action_ontology || ACTIONS.some(a => typeof x.action_ontology[a] !== "string")) errors.push("BAD_ACTION_ONTOLOGY");
  if (!Array.isArray(x.items) || x.items.length !== 24) return {ok:false,errors:[...errors,"ITEM_COUNT"]};
  const ids = new Set();
  for (let idx=0; idx<x.items.length; idx++) {
    const it=x.items[idx]; const id=String(idx+1).padStart(2,"0");
    if (!it || typeof it !== "object") { errors.push(`${id}:NOT_OBJECT`); continue; }
    if (it.item_id !== id) errors.push(`${id}:ID`);
    ids.add(it.item_id);
    if (typeof it.request !== "string" || !it.request) errors.push(`${id}:REQUEST`);
    if (it.current_state !== "PENDING") errors.push(`${id}:STATE`);
    if (!Array.isArray(it.evidence)) errors.push(`${id}:EVIDENCE`);
    if (!Array.isArray(it.constraints)) errors.push(`${id}:CONSTRAINTS`);
    if (JSON.stringify(it.allowed_actions) !== JSON.stringify(ACTIONS)) errors.push(`${id}:ALLOWED_ACTIONS`);
    const expectedDeps = idx < 20 ? [] : [String(idx-3).padStart(2,"0")];
    if (JSON.stringify(it.dependency_ids) !== JSON.stringify(expectedDeps)) errors.push(`${id}:DEPS`);
  }
  if (ids.size !== 24) errors.push("DUPLICATE_ID");
  return {ok:errors.length===0,errors};
}
