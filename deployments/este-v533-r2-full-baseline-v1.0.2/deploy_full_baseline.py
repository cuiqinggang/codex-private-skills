"""Frozen R2 deployment v1.0.2. Stdlib only; no privilege or policy changes.

Production CLI is pinned to the reported Windows target and workspace. Tests call
functions on temporary fixtures; sandbox tests do not certify Windows deployment.
"""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone

SKILL_ID = 'first-principles-physical-limit-convergence'
TARGET = Path(r'C:\Users\A\.codex\skills\first-principles-physical-limit-convergence')
WORK = Path(r'C:\Users\A\Documents\Codex\2026-09-27\este-baseline-v533-r2-03')
OLD_SKILL_SHA256 = '84e1f003590ab1dd37bfd24ed362ae0595b480dabbcef4c63b48b28c73c3686c'
PAYLOAD_SHA256 = '469567e166f2dedcf8d97c06969092f3ce0630585070aa7f6b7bb3c9a8be7a20'
MODULES = ('fsm_v5_3_0', 'scope_gate_v5_2_2', 'production_handoff_v5_2_0',
           'acceptance_supervisor_v5_3_3', 'acceptance_review_v1_0_1',
           'acceptance_isolation_guard_v1')
REQUIRED = {'SKILL.md','VERSION','CANONICAL.md','DEPLOYMENT.json','contracts/ACTIVE-R2.json',
            'tests/test_acceptance_integration_v1_0_1.py','tests/test_acceptance_isolation_guard_v1.py'} | {'runtime/'+m+'.py' for m in MODULES}

class DeploymentBlocked(RuntimeError):
    pass

def require(value, code):
    if not value:
        raise DeploymentBlocked(code)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def utc():
    return datetime.now(timezone.utc).isoformat(timespec='microseconds').replace('+00:00','Z')

def no_link(path):
    """Reject symlinks and Windows reparse points instead of following them."""
    st = path.lstat()
    require(not stat.S_ISLNK(st.st_mode), 'REPARSE_OR_SYMLINK:'+str(path))
    require(not (getattr(st, 'st_file_attributes', 0) & 0x400), 'REPARSE_POINT:'+str(path))
    require(stat.S_ISDIR(st.st_mode) or stat.S_ISREG(st.st_mode), 'NON_REGULAR_PATH:'+str(path))

def safe_ancestors(path):
    for p in reversed((path, *path.parents)):
        if os.path.lexists(p):
            no_link(p)

def inventory(root):
    no_link(root)
    require(root.is_dir(), 'DIRECTORY_REQUIRED')
    rows={}
    for p in sorted(root.rglob('*')):
        no_link(p)
        rel=p.relative_to(root).as_posix()
        rows[rel]={'kind':'dir'} if p.is_dir() else {'kind':'file','bytes':p.stat().st_size,'sha256':digest(p.read_bytes())}
    return rows

def safe_name(name):
    require(isinstance(name,str) and name and '\\' not in name and ':' not in name, 'INVALID_PAYLOAD_PATH')
    q=PurePosixPath(name)
    require(not q.is_absolute() and '..' not in q.parts and '.' not in q.parts and q.as_posix()==name, 'INVALID_PAYLOAD_PATH')
    require(all(not p.endswith((' ','.')) for p in q.parts), 'INVALID_WINDOWS_PATH')
    require(all(p.split('.')[0].upper() not in {'CON','PRN','AUX','NUL',*(f'COM{i}' for i in range(1,10)),*(f'LPT{i}' for i in range(1,10))} for p in q.parts),'RESERVED_WINDOWS_PATH')
    return name

def read_payload(path, expected_sha=PAYLOAD_SHA256):
    no_link(path)
    raw=path.read_bytes()
    require(digest(raw)==expected_sha, 'PAYLOAD_HASH_MISMATCH')
    obj=json.loads(raw.decode('utf-8'))
    require(obj['deployment_version']=='1.0.2','PAYLOAD_VERSION_MISMATCH')
    files={}; lowered=set()
    for r in obj['files']:
        name=safe_name(r['path'])
        require(name.casefold() not in lowered,'DUPLICATE_PAYLOAD_PATH')
        lowered.add(name.casefold())
        b=r['content'].encode('utf-8')
        require(len(b)==r['bytes'] and digest(b)==r['sha256'],'SOURCE_FILE_HASH_MISMATCH:'+name)
        files[name]=b
    require(set(files)==REQUIRED,'PAYLOAD_FILE_SET_MISMATCH')
    require(files['VERSION']==b'5.3.3\n','VERSION_MISMATCH')
    require(b'version: "5.3.3"' in files['SKILL.md'],'SKILL_VERSION_MISMATCH')
    for r in obj['frozen_runtime_sources']:
        b=files[r['path']]
        require(digest(b)==r['sha256'],'UPSTREAM_HASH_MISMATCH')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob_sha'],'UPSTREAM_BLOB_MISMATCH')
    # Verify all statically declared local imports and the two known dynamic imports.
    for name,b in files.items():
        if not name.startswith('runtime/') or not name.endswith('.py'):
            continue
        tree=ast.parse(b,filename=name)
        for node in ast.walk(tree):
            names=[a.name for a in node.names] if isinstance(node,ast.Import) else ([node.module] if isinstance(node,ast.ImportFrom) else [])
            for mod in names:
                if mod and mod.split('.')[0] not in sys.stdlib_module_names:
                    require('runtime/'+mod.split('.')[0]+'.py' in files,'DEPENDENCY_MISSING:'+mod)
    return files

def verify_tree(root,files):
    inv=inventory(root)
    actual={k for k,v in inv.items() if v['kind']=='file'}
    require(actual==set(files),'INSTALLED_FILE_SET_MISMATCH')
    for name,b in files.items():
        require(inv[name]['sha256']==digest(b),'INSTALLED_HASH_MISMATCH:'+name)
    return inv

def run_checks(root, work):
    """Fresh interpreter, exact module paths, then the frozen 50-test suite."""
    env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
    for k in ('PYTHONPATH','PYTHONHOME'): env.pop(k,None)
    probe='''import json,sys,importlib,pathlib
root=pathlib.Path(sys.argv[1]).resolve();sys.path.insert(0,str(root/'runtime')); out={}
for name in sys.argv[2:]:
 m=importlib.import_module(name); p=pathlib.Path(m.__file__).resolve()
 if p.parent != root/'runtime': raise RuntimeError('WRONG_RUNTIME_PATH:'+str(p))
 out[name]=str(p)
print(json.dumps(out,ensure_ascii=False))
'''
    p=subprocess.run([sys.executable,'-I','-B','-c',probe,str(root),*MODULES],cwd=work,env=env,capture_output=True,text=True,timeout=120)
    require(p.returncode==0,'FRESH_IMPORT_FAILED:'+p.stderr[-1800:])
    binding=json.loads(p.stdout)
    p=subprocess.run([sys.executable,'-I','-B','-m','unittest','discover','-s',str(root/'tests'),'-p','test_*.py','-v'],cwd=work,env=env,capture_output=True,text=True,timeout=120)
    log=p.stdout+p.stderr
    (work/('checks-'+str(time.time_ns())+'.txt')).write_text(log,encoding='utf-8')
    require(p.returncode==0 and re.search(r'Ran 50 tests?\b',log) is not None,'FROZEN_50_TESTS_FAILED:'+log[-1800:])
    return binding

def baseline(target,files,expected_old_hash):
    inv=inventory(target)
    if {k:v['sha256'] for k,v in inv.items() if v['kind']=='file'}=={k:digest(b) for k,b in files.items()}:
        return 'ALREADY_INSTALLED', inv
    require((target/'VERSION').is_file(),'OLD_VERSION_FILE_MISSING')
    require((target/'VERSION').read_text(encoding='utf-8-sig').strip()=='3.1.6','UNAPPROVED_BASE_VERSION')
    require(digest((target/'SKILL.md').read_bytes())==expected_old_hash,'OLD_SKILL_CHANGED')
    for name in ('SKILL.md','CANONICAL.md'):
        require('3.1.6' in (target/name).read_text(encoding='utf-8-sig'),'OLD_METADATA_CONFLICT')
    require(not any((target/'runtime'/ (m+'.py')).exists() for m in MODULES),'BASELINE_RUNTIME_CHANGED')
    return 'APPROVED_V3_1_6', inv

def save(path,obj):
    # The journal path and its parent are validated before every write.
    safe_ancestors(path)
    tmp=path.with_name(path.name+'.tmp')
    require(not os.path.lexists(tmp),'JOURNAL_TEMP_CONFLICT')
    with open(tmp,'x',encoding='utf-8',newline='\n') as f:
        json.dump(obj,f,ensure_ascii=False,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(tmp,path)

def deploy(target,work,files,expected_old_hash=OLD_SKILL_SHA256):
    """Recoverable directory replacement. Never merge new files into the old tree."""
    start=utc();t0=time.perf_counter_ns()
    safe_ancestors(target);safe_ancestors(work)
    require(target.is_absolute() and work.is_absolute(),'ABSOLUTE_PATH_REQUIRED')
    require(target != work and target not in work.parents and work not in target.parents,'OVERLAPPING_PATHS')
    require(target.exists(),'EXPECTED_EXISTING_BASELINE_MISSING')
    state,old=baseline(target,files,expected_old_hash)
    work.mkdir(parents=True,exist_ok=True)
    if state=='ALREADY_INSTALLED':
        bindings=run_checks(target,work)
        return {'result':'PASS','deployment':'ALREADY_INSTALLED_VERIFIED','bindings':bindings,'start_utc':start,'end_utc':utc(),'elapsed_ms':(time.perf_counter_ns()-t0)/1e6,'final_valid':False}
    lock=work/'DEPLOY.lock'
    require(not os.path.lexists(lock),'DEPLOYMENT_LOCK_EXISTS_REVIEW_REQUIRED')
    lock.mkdir()
    stage=work/'staging';backup=work/'backup-v3.1.6';quarantine=work/'failed-new-baseline'
    require(not any(os.path.lexists(p) for p in (stage,backup,quarantine)), 'STAGING_OR_BACKUP_CONFLICT')
    journal={'version':'1.0.2','target':str(target),'work':str(work),'start_utc':start,'old_inventory':old,'events':[],'new_file_hashes':{k:digest(v) for k,v in files.items()}}
    def event(s):
        journal['events'].append({'event':s,'utc':utc(),'elapsed_ms':(time.perf_counter_ns()-t0)/1e6});save(work/'JOURNAL.json',journal)
    moved=False;promoted=False
    try:
        stage.mkdir()
        for name,b in files.items():
            p=stage/name;p.parent.mkdir(parents=True,exist_ok=True)
            with open(p,'xb') as f:f.write(b)
        verify_tree(stage,files);run_checks(stage,work);event('STAGING_VERIFIED')
        require(inventory(target)==old,'SOURCE_CHANGED_DURING_STAGING')
        require(os.stat(stage).st_dev==os.stat(target.parent).st_dev,'CROSS_VOLUME_REPLACEMENT_FORBIDDEN')
        event('BEFORE_BACKUP_RENAME')
        target.rename(backup);moved=True
        require(inventory(backup)==old,'BACKUP_VERIFICATION_FAILED')
        event('BACKUP_VERIFIED_BEFORE_PROMOTION')
        stage.rename(target);promoted=True
        verify_tree(target,files)
        bindings=run_checks(target,work)
        require(inventory(backup)==old,'BACKUP_CHANGED')
        event('INSTALLED_AND_FRESH_PROCESS_VERIFIED')
        result={'result':'PASS','deployment':'FULL_BASELINE_INSTALLED','engine_version':'5.3.3','patch_version':'1.0.1','deployment_version':'1.0.2','backup':str(backup),'bindings':bindings,'start_utc':start,'end_utc':utc(),'elapsed_ms':(time.perf_counter_ns()-t0)/1e6,'final_valid':False,'business_execution':'NOT_RUN','browser_page_creation':'NOT_RUN'}
        save(work/'INSTALL-RESULT.json',result)
        lock.rmdir()
        return result
    except Exception as exc:
        # No cleanup deletion: retain failed new files and logs for inspection.
        rollback='NOT_NEEDED'
        if moved:
            try:
                if promoted:
                    target.rename(quarantine)
                require(not os.path.lexists(target),'ROLLBACK_TARGET_OCCUPIED')
                backup.rename(target)
                require(inventory(target)==old,'ROLLBACK_BYTES_MISMATCH')
                rollback='RESTORED_OLD_TREE_VERIFIED'
            except Exception as recovery:
                rollback='RECOVERY_REQUIRED:'+str(recovery)
        try:
            event('STOP:'+type(exc).__name__+':'+str(exc)+';'+rollback)
        except Exception:
            pass
        raise DeploymentBlocked(str(exc)+';ROLLBACK='+rollback) from exc

def recover_interrupted(target,work):
    """Only restore the recorded old tree; never overwrite an occupied target."""
    safe_ancestors(target);safe_ancestors(work)
    journal=json.loads((work/'JOURNAL.json').read_text(encoding='utf-8'))
    require(journal['target']==str(target) and journal['work']==str(work),'JOURNAL_PATH_MISMATCH')
    backup=work/'backup-v3.1.6'
    require(not os.path.lexists(target),'TARGET_EXISTS_NO_AUTOMATIC_RECOVERY')
    require(inventory(backup)==journal['old_inventory'],'BACKUP_BYTES_MISMATCH')
    backup.rename(target)
    require(inventory(target)==journal['old_inventory'],'RESTORE_BYTES_MISMATCH')
    return {'result':'RESTORED_OLD_TREE_VERIFIED','utc':utc(),'resume_requires_new_review':True}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['probe','install','recover'])
    parser.add_argument('--payload',type=Path,default=Path(__file__).with_name('FULL-BASELINE-PAYLOAD.json'))
    args=parser.parse_args()
    require(os.name=='nt','LIVE_DEPLOYMENT_REQUIRES_AUTHORIZED_WINDOWS_HOST')
    require(sys.version_info>=(3,10),'PYTHON_3_10_OR_NEWER_REQUIRED_NO_AUTOMATIC_INSTALL')
    files=read_payload(args.payload)
    if args.action=='probe':
        state,inv=baseline(TARGET,files,OLD_SKILL_SHA256)
        result={'result':state,'target':str(TARGET),'file_count':sum(v['kind']=='file' for v in inv.values()),'utc':utc(),'no_target_write':True}
    elif args.action=='recover':
        result=recover_interrupted(TARGET,WORK)
    else:
        result=deploy(TARGET,WORK,files)
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'result':'BLOCKED','reason':type(e).__name__+':'+str(e),'final_valid':False},ensure_ascii=False))
        sys.exit(2)
