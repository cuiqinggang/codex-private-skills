import subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestCombined(unittest.TestCase):
 def test_contract(self):
  r=subprocess.run([sys.executable,str(ROOT/'scripts/validate_handoff.py'),'--clone',str(ROOT/'tests/fixtures/clone-analysis.json'),'--design',str(ROOT/'tests/fixtures/design-system-result.json')])
  self.assertEqual(0,r.returncode)
if __name__=='__main__':unittest.main()

