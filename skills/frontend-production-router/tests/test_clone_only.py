import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestCloneOnly(unittest.TestCase):
 def test_clone_capabilities(self):
  d=json.loads((ROOT/'capability-map.json').read_text(encoding='utf-8'))['clone_skill']['capabilities'];self.assertIn('stage-gated-visual-comparison',d)
if __name__=='__main__':unittest.main()

