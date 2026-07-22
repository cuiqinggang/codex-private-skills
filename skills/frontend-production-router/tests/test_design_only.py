import json,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class TestDesignOnly(unittest.TestCase):
 def test_design_capabilities(self):
  d=json.loads((ROOT/'capability-map.json').read_text(encoding='utf-8'))['design_skill']['capabilities'];self.assertIn('design-md',d)
if __name__=='__main__':unittest.main()

