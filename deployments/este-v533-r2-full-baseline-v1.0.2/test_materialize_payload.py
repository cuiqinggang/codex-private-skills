from pathlib import Path
import json
import subprocess
import tempfile
import unittest
from materialize_payload import materialize
HERE=Path(__file__).resolve().parent
class Materializer(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.repo=self.root/'repo';self.repo.mkdir()
        subprocess.run(['git','init','--quiet',str(self.repo)],check=True)
        p=json.loads((HERE/'FULL-BASELINE-PAYLOAD.json').read_text())
        lookup={r['path'] for r in p['frozen_runtime_sources']}
        for r in p['files']:
            if r['path'] in lookup:
                subprocess.run(['git','-C',str(self.repo),'hash-object','-w','--stdin'],input=r['content'].encode(),check=True,capture_output=True)
    def tearDown(self):self.tmp.cleanup()
    def test_31_exact_git_bytes_materialization(self):
        out=self.root/'out.json';r=materialize(HERE/'FULL-BASELINE-SPEC.json',self.repo,out)
        self.assertEqual(out.read_bytes(),(HERE/'FULL-BASELINE-PAYLOAD.json').read_bytes());self.assertEqual(r['file_count'],13)
    def test_32_materialization_idempotent(self):
        out=self.root/'out.json';materialize(HERE/'FULL-BASELINE-SPEC.json',self.repo,out);materialize(HERE/'FULL-BASELINE-SPEC.json',self.repo,out)
    def test_33_conflicting_destination_not_overwritten(self):
        out=self.root/'out.json';out.write_bytes(b'keep')
        with self.assertRaisesRegex(RuntimeError,'DESTINATION_CONFLICT'):materialize(HERE/'FULL-BASELINE-SPEC.json',self.repo,out)
        self.assertEqual(out.read_bytes(),b'keep')
    def test_34_missing_git_object_fails(self):
        empty=self.root/'empty';empty.mkdir();subprocess.run(['git','init','--quiet',str(empty)],check=True)
        with self.assertRaisesRegex(RuntimeError,'FROZEN_BLOB_UNAVAILABLE'):materialize(HERE/'FULL-BASELINE-SPEC.json',empty,self.root/'out.json')
    def test_35_metadata_corruption_fails(self):
        obj=json.loads((HERE/'FULL-BASELINE-SPEC.json').read_text());obj['files'][0]['content']='wrong';p=self.root/'bad.json';p.write_text(json.dumps(obj))
        with self.assertRaisesRegex(RuntimeError,'SOURCE_BYTES_MISMATCH'):materialize(p,self.repo,self.root/'out.json')
if __name__=='__main__':unittest.main(verbosity=2)
