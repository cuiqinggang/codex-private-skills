"""HIPE 0.3.5 production adapter. Frozen R4/R5 remain byte-identical."""
import argparse, dataclasses, hashlib, importlib.util, json, os, sys, uuid
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
ROOT = Path(__file__).resolve().parent.parent
FROZEN = ROOT/'runtime/inherited/frozen/v0.3.4'
sys.path.insert(0, str(FROZEN))
spec = importlib.util.spec_from_file_location('hipe_r4', FROZEN/'HIPE-v0.3.4-real-verify.py')
r4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r4)
VERSION = '0.3.5'
BASE, ORACLE = r4.load()
TASKS = {t['id']: t for t in BASE['tasks']}
SQL = {t['id']: t for t in ORACLE['sql_cases']}

def source_check():
    locked = json.loads((ROOT/'CURRENT_STATE.json').read_text(encoding='utf-8'))['inherited_files']
    if len(locked) != 9 or any(hashlib.sha256((ROOT/n).read_bytes()).hexdigest() != h for n,h in locked.items()):
        raise r4.timing_boundary.BoundaryError('FROZEN_SOURCE_CHANGED')

def is_code(t):
    return (set(t) == {'id','operation','value','limit','operator'}
            and t.get('operation') == 'compare_threshold' and t.get('operator') == '<='
            and type(t.get('value')) is int and type(t.get('limit')) is int)

def certified(t):
    return is_code(t) or t == TASKS.get(t.get('id'))

def node_route(t):
    f = r4.node_facts(t)
    f = dataclasses.replace(f, deterministic_exact=is_code(t), deterministic_executor_available=is_code(t),
        certified_action_ontology=certified(t) and f.certified_action_ontology,
        unresolved_hidden_information=t.get('unresolved_hidden_information') is True,
        requires_open_generation=f.requires_open_generation or t.get('requires_open_generation') is True,
        timed_retry_required=t.get('timed_retry_required') is True)
    return r4.fc.route(f)

def gate(job):
    tasks = job.get('tasks')
    if not isinstance(tasks,list) or not tasks or any(not isinstance(t,dict) for t in tasks):
        raise ValueError('TASKS_REQUIRED')
    ids = [t.get('id') for t in tasks]
    if any(not isinstance(i,str) or not i for i in ids) or len(set(ids)) != len(ids):
        raise ValueError('BAD_OR_DUP_ID')
    match = all(certified(t) for t in tasks)
    if match:
        # The installed evidence establishes maturity even on a first encounter.
        facts = r4.rsg.SolvabilityFacts(True,True,True,len(tasks)==1,len(tasks)>1,False,True)
    else:
        supplied = job.get('solvability',{})
        allowed = {f.name for f in dataclasses.fields(r4.rsg.SolvabilityFacts)}-{'certified_compilable_domain'}
        if any(type(supplied.get(k,False)) is not bool for k in allowed):
            raise ValueError('SOLVABILITY_FACTS_MUST_BE_BOOL')
        values = {k:supplied.get(k,False) for k in allowed}
        refs = job.get('evidence_refs')
        if not isinstance(refs,list) or not refs or any(not isinstance(x,str) or not x.strip() for x in refs):
            values['evidence_search_complete'] = False
        facts = r4.rsg.SolvabilityFacts(**values)
    return {'version':r4.rsg.VERSION,'classification':r4.rsg.classify(facts),
            'DOMAIN_MATCH':'YES' if match else 'NO','research_allowed':r4.rsg.frontier_unknown_formula(facts),
            'acceptance_verifiable':facts.acceptance_verifiable,
            'evidence':['INSTALLED_FROZEN_DOMAIN'] if match else job.get('evidence_refs',[])}

def plan(job):
    g = gate(job)
    nodes = [{'id':t['id'],'route':node_route(t)} for t in job['tasks']]
    return {'gate':g,'forward_compiler_version':r4.fc.VERSION,'nodes':nodes,
            'route':'+'.join(x for x in ('CODE','JEV','GPT') if any(n['route']==x for n in nodes)),
            'frozen_fast_path':g['DOMAIN_MATCH']=='YES'}

def optional_usage(response):
    u = response.get('usage') or {}
    return {k:v for k,v in {'cost_usd':u.get('cost'),'model':response.get('model'),
            'generation_id':response.get('id',response.get('generation_id'))}.items() if v is not None}

def execute_node(t, route, key, post):
    if route == 'CODE':
        # R4 inline threshold expression exposed through a single-node adapter.
        return ('ALLOW' if t['value']<=t['limit'] else 'BLOCK'), {}
    if route == 'JEV':
        if t['dependency_ids']:
            raise r4.timing_boundary.BoundaryError('DEPENDENT_CHOICE_REQUIRES_FROZEN_MIXED_PATH')
        payload = next(p for p in r4.jev_payloads({'tasks':[t],'initial_state':'READY'}) if p['questions'])
        d,_ = post(r4.JEV_URL,key,payload)
        return next(iter(r4.jparse(d,list(payload['questions'])).values())), optional_usage(d)
    if t == TASKS.get(t['id']) and t['id'] in SQL:
        body = r4.gpt_body({'tasks':[t],'variant':'V00'},True)
    else:
        body = {'model':'openai/gpt-5.6-sol','messages':[
            {'role':'system','content':'Return a JSON object mapping task id to your answer. Explain uncertainty; never invent missing state.'},
            {'role':'user','content':json.dumps(t,ensure_ascii=False)}]}
    d,_ = post(r4.GPT_URL,key,body)
    return r4.gparse(d).get(t['id']), optional_usage(d)

def verify_node(t, route, answer):
    if route == 'CODE':
        return answer in ('ALLOW','BLOCK') and (answer=='BLOCK') == (t['value']-t['limit']>0)
    if not certified(t):
        return False
    if route == 'JEV':
        return answer == ORACLE['expected_choices'].get('item_'+t['id']+'__current_action')
    return t['id'] in SQL and r4.sqlok(answer,SQL[t['id']])

def write_checked(path, value):
    raw = json.dumps(value,ensure_ascii=False,indent=2,allow_nan=False).encode('utf-8')
    with path.open('xb') as f:
        f.write(raw); f.flush(); os.fsync(f.fileno())
    actual = path.read_bytes()
    if hashlib.sha256(actual).digest()!=hashlib.sha256(raw).digest() or json.loads(actual)!=value:
        raise r4.timing_boundary.BoundaryError('FINAL_WRITE_READBACK_FAILED')

def run(job, output_dir, *, key=None, transport=None, offline=False):
    """Authoritative status requires candidate, successful receipt and status.json.
    No action such as publishing/deleting is enacted. Uncertified tasks are handed
    to GPT review, without claiming semantic validation of an arbitrary answer.
    """
    if transport is not None and not offline:
        raise ValueError('TRANSPORT_INJECTION_REQUIRES_OFFLINE')
    out = Path(output_dir).resolve()
    out.mkdir(parents=True,exist_ok=False)
    candidate,receipt = out/'candidate.json',out/'timing.json'
    post = transport or r4.post
    p = None
    run_id = str(uuid.uuid4())
    try:
        def operation():
            nonlocal p
            source_check()
            p = plan(job); g = p['gate']
            if g['classification'] in ('INCOMPLETE_SPEC','SOLUTION_SEARCH_REQUIRED','INFEASIBLE_OR_CONTRADICTORY'):
                raise RuntimeError(g['classification'])
            if not g['acceptance_verifiable']:
                raise r4.timing_boundary.BoundaryError('ACCEPTANCE_REQUIRED')
            if not all(certified(t) for t in job['tasks']):
                raise r4.timing_boundary.BoundaryError('GPT_RESIDUAL_REVIEW_REQUIRED')
            if any(n['route']!='CODE' for n in p['nodes']) and not key:
                raise r4.timing_boundary.BoundaryError('RUNTIME_CREDENTIAL_REQUIRED')
            if any(t.get('dependency_ids') for t in job['tasks']):
                raise r4.timing_boundary.BoundaryError('USE_MIXED_BENCHMARK_ENTRY')
            def one(pair):
                t,n = pair
                answer,u = execute_node(t,n['route'],key,post)
                return t['id'],answer,u,verify_node(t,n['route'],answer)
            with ThreadPoolExecutor(max_workers=min(3,len(job['tasks']))) as pool:
                rows = list(pool.map(one,zip(job['tasks'],p['nodes'])))
            errors = [i for i,a,u,valid in rows if not valid]
            result = {'path':'HYBRID','variant':0,'valid':not errors,'errors':errors,
                'answers':{i:a for i,a,u,valid in rows},'usage':{i:u for i,a,u,valid in rows},
                'route':p['route'],'plan':p,'mode':'OFFLINE_TEST' if offline else 'REAL',
                'run_id':run_id,'role':'candidate_requires_successful_timing_and_status'}
            write_checked(candidate,result)
            return result
        result,obs = r4.timing_boundary.observe_path(operation,run_id=run_id,path_name='HYBRID',variant=0,
            phase='OFFLINE_TEST' if offline else 'MEASURED',required_outputs=[candidate],receipt_path=receipt)
        r4.timing_boundary.verify_observation(receipt,run_id=run_id,path_name='HYBRID',variant=0,
            phase='OFFLINE_TEST' if offline else 'MEASURED')
        status = {'version':VERSION,'status':'VALID','valid':True,'route':p['route'],
            'T_VALID_MS':obs['elapsed_ms'],'FINAL_WRITE_INCLUDED':True,'verifier':'PASS',
            'external_runtime_error':None,'mode':result['mode'],'usage':result['usage'],
            'task_family':job.get('task_family','HIPE_COMMON'),'run_id':run_id,
            'result':str(candidate),'receipt':str(receipt),'plan':p}
    except Exception as e:
        status = {'version':VERSION,'status':'FAIL','valid':False,'T_VALID_MS':None,
            'route':p['route'] if p else None,'task_family':job.get('task_family','HIPE_COMMON'),
            'verifier':'NOT_PASSED','external_runtime_error':getattr(e,'category',type(e).__name__),
            'mode':'OFFLINE_TEST' if offline else 'REAL','usage':None,'run_id':run_id,'plan':p}
    # Observer metadata follows R5 convention. A write failure raises, never returns VALID.
    write_checked(out/'status.json',status)
    return status

def run_mixed(output_dir, key):
    """Full frozen benchmark: unchanged legal R4 parallelism, verifier and R5 boundary."""
    source_check()
    out = Path(output_dir).resolve(); out.mkdir(parents=True,exist_ok=False)
    try:
        result,timing = r4._observe_r4_path(r4.run_hybrid,key,BASE,ORACLE,0,out,'HYBRID')
        obs = timing['observation']
        if not result['valid'] or not obs['path_complete_and_correct']:
            raise r4.timing_boundary.BoundaryError('VERIFIER_REJECTED')
        r4.timing_boundary.verify_observation(timing['receipt_path'],run_id=obs['run_id'],
            path_name='HYBRID',variant=0,phase=obs['phase'])
        status = {'version':VERSION,'status':'VALID','valid':True,'route':'CODE+JEV+GPT',
            'task_family':r4.FAMILY,'T_VALID_MS':obs['elapsed_ms'],'FINAL_WRITE_INCLUDED':True,
            'verifier':'PASS','external_runtime_error':None,'cost_usd':result['cost_usd']}
    except Exception as e:
        status = {'version':VERSION,'status':'FAIL','valid':False,'route':'CODE+JEV+GPT',
            'task_family':r4.FAMILY,'T_VALID_MS':None,'verifier':'NOT_PASSED',
            'external_runtime_error':getattr(e,'category',type(e).__name__),'cost_usd':None}
    write_checked(out/'status.json',status)
    return status

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--task',type=Path); p.add_argument('--out',type=Path)
    p.add_argument('--plan-only',action='store_true'); p.add_argument('--mixed-benchmark',action='store_true')
    args = p.parse_args()
    if args.mixed_benchmark:
        if not args.out or not os.environ.get('OPENROUTER_API_KEY'):
            p.error('--out and inherited OPENROUTER_API_KEY required')
        result = run_mixed(args.out,os.environ['OPENROUTER_API_KEY'])
    else:
        if not args.task: p.error('--task required')
        job = json.loads(args.task.read_text(encoding='utf-8-sig'))
        if args.plan_only:
            source_check(); print(json.dumps(plan(job),ensure_ascii=False,indent=2)); return 0
        if not args.out: p.error('--out required')
        result = run(job,args.out,key=os.environ.get('OPENROUTER_API_KEY'))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if result['valid'] else 2

if __name__=='__main__':
    raise SystemExit(main())

