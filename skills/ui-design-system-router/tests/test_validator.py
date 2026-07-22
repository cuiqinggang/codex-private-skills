import subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestValidator(unittest.TestCase):
 def test_rejects_incomplete(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.md';p.write_text('# DESIGN\nhttps://example.com',encoding='utf-8')
   self.assertNotEqual(0,subprocess.run([sys.executable,str(ROOT/'scripts/validate_design_md.py'),str(p)],capture_output=True).returncode)
if __name__=='__main__':unittest.main()

