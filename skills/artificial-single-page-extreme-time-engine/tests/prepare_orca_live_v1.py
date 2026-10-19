from pathlib import Path
import uuid
src=Path(r"C:\Users\A\Desktop\SRX_V3_ReadPack\codex-private-skills\skills\artificial-single-page-extreme-time-engine\tasks\ORCA_CODEX_VALUE_VALIDATION_20261014\analysis\lifecycle-validation-r1.py")
dst=src.parents[3]/"tests"/"orca_live_lifecycle_v1.py"
t=src.read_text(encoding="utf-8")
old="TEST = ROOT / 'lifecycle-validation-20261016-r1'"
new="TEST = ROOT / 'lifecycle-v1-live-20261019-1945'"
assert t.count(old)==1
t=t.replace(old,new)
old2="""    cli('orchestration','send','--type','heartbeat','--subject','hashing',
        '--task-id',task,'--dispatch-id',ctx,'--phase','implementing')"""
new2="""    # Trigger a real CLI timeout (1 ms) in the control plane; do not mutate/re-send heartbeat.
    try:
        cli('orchestration','dispatch-show','--task',task,cap=0.001)
        control_fault='FAST_READ_SUCCEEDED'
    except subprocess.TimeoutExpired:
        control_fault='REAL_CLI_READ_TIMEOUT'
    write('control-fault.json',{'outcome':control_fault,'task':task,'dispatch':ctx,
                              'identity':ident,'business_interrupted':False})
    # Fresh independent official read reconciles the SAME dispatch/terminal.
    recovered=cli('orchestration','dispatch-show','--task',task,cap=25)['dispatch']
    assert recovered['id']==ctx and recovered['assignee_handle']==ident['handle']
    assert recovered['assignee_pane_key']==ident['pane']
    write('control-recovered.json',{'same_dispatch':True,'identity':ident,'task':task,
                                     'dispatch':ctx,'fault':control_fault})
    # Do not send another ambiguous control mutation. Continue child work on same identity."""
assert t.count(old2)==1
t=t.replace(old2,new2)
dst.write_text(t,encoding="utf-8")
print(str(dst))
