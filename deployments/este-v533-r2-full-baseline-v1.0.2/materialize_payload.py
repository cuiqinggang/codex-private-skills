"""Reconstruct the frozen payload from existing Git blob objects; no network/config writes."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import subprocess


def materialize(spec_path, repository, destination):
    spec=json.loads(spec_path.read_text(encoding='utf-8'))
    expected=spec.pop('payload_sha256')
    files=[]
    for r in spec['files']:
        r=copy.deepcopy(r)
        if 'git_blob_sha' in r:
            sha=r.pop('git_blob_sha')
            p=subprocess.run(['git','-C',str(repository),'cat-file','blob',sha],capture_output=True,timeout=60)
            if p.returncode:
                raise RuntimeError('FROZEN_BLOB_UNAVAILABLE:'+sha+'; read/fetch the pinned source via the authorized Git channel; no alternate bytes')
            raw=p.stdout
            if hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()!=sha:
                raise RuntimeError('GIT_BLOB_BYTES_MISMATCH')
            r['content']=raw.decode('utf-8')
        raw=r['content'].encode('utf-8')
        if len(raw)!=r['bytes'] or hashlib.sha256(raw).hexdigest()!=r['sha256']:
            raise RuntimeError('SOURCE_BYTES_MISMATCH:'+r['path'])
        files.append(r)
    spec['files']=files
    # Restore field order used by the frozen payload writer.
    for r in spec['files']:
        r.update({'content':r.pop('content')})
    raw=(json.dumps(spec,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    if hashlib.sha256(raw).hexdigest()!=expected:
        raise RuntimeError('RECONSTRUCTED_PAYLOAD_HASH_MISMATCH')
    if destination.exists():
        if destination.read_bytes()!=raw:raise RuntimeError('DESTINATION_CONFLICT')
    else:
        with destination.open('xb') as f:f.write(raw)
    return {'result':'PAYLOAD_MATERIALIZED','sha256':expected,'file_count':len(files),'bytes':len(raw)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--repository',type=Path,required=True)
    p.add_argument('--spec',type=Path,default=Path(__file__).with_name('FULL-BASELINE-SPEC.json'))
    p.add_argument('--output',type=Path,default=Path(__file__).with_name('FULL-BASELINE-PAYLOAD.json'))
    a=p.parse_args()
    print(json.dumps(materialize(a.spec,a.repository,a.output),ensure_ascii=False))
