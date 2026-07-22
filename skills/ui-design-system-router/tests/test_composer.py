import subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestComposer(unittest.TestCase):
 def test_compose_and_validate(self):
  with tempfile.TemporaryDirectory() as d:
   out=Path(d)/'DESIGN.md'
   subprocess.run([sys.executable,str(ROOT/'scripts/compose_design_md.py'),'--product-type','ai-saas','--audience','enterprise','--output',str(out)],check=True)
   r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_design_md.py'),str(out)])
   self.assertEqual(0,r.returncode)
if __name__=='__main__':unittest.main()

