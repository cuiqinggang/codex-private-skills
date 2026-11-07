"""Versioned mature-first preference adapter; original OMP runtime and ACL retained."""
from pathlib import Path
import importlib.util,yaml
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'pi-memory-integration-v1-20261101/memory_runtime.py'
spec=importlib.util.spec_from_file_location('prior_memory_runtime_r57',BASE)
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
def command(cwd,task=None,session=None,cli_only=None):
    cmd,env=prior.command(cwd,task=task,session=session,cli_only=cli_only)
    if cli_only:return cmd,env
    # Preserve workspace ACL; ordinary write approval remains enabled.
    cmd[cmd.index('--approval-mode')+1]='write'
    p=Path(cwd)/'.omp/agent/config.yml'
    c=yaml.safe_load(p.read_text(encoding='utf-8'))
    c['tools']['approvalMode']='write'
    p.write_text(yaml.safe_dump(c,allow_unicode=True,sort_keys=False),encoding='utf-8')
    i=cmd.index('--append-system-prompt')+1
    original=Path(cmd[i]).read_text(encoding='utf-8')
    dest=Path(cwd)/'.omp/agent/mature-first-r57.md'
    guard=(ROOT/'ORACLE-GUARD.md').read_text(encoding='utf-8')
    dest.write_text(original+'\n\n'+(ROOT/'MATURE-POLICY.md').read_text(encoding='utf-8')+'\n'+guard+'\nAuthoritative Sanrenxing V5 reference snapshot: '+str(ROOT/'methods/SANRENXING_V5.md')+'\n',encoding='utf-8')
    cmd[i]=str(dest)
    return cmd,env
