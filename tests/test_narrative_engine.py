import sys
import unittest
from pathlib import Path
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
import nfl_script_narrative_engine as engine

class NarrativeEngineTests(unittest.TestCase):
    def test_pythagorean_values(self):
        self.assertEqual(engine.ciphers("WASHINGTON")["pythagorean"],49)
        self.assertEqual(engine.ciphers("GIANTS")["pythagorean"],25)
    def test_ordinal_values(self):
        self.assertEqual(engine.ciphers("COMMANDERS")["ordinal"],105)
        self.assertEqual(engine.ciphers("GIANTS")["ordinal"],70)
    def test_record_uses_only_games_team_played(self):
        games=pd.DataFrame([
            {"away_team":"WAS","home_team":"NYG","away_score":20,"home_score":17},
            {"away_team":"DAL","home_team":"PHI","away_score":10,"home_score":24}])
        self.assertEqual(engine.team_record(games,"WAS")["record"],"1-0-0")
        self.assertEqual(engine.team_record(games,"NYG")["record"],"0-1-0")
    def test_digital_root(self):
        self.assertEqual(engine.digital_root(49),4)
        self.assertEqual(engine.digital_root(25),7)

if __name__=="__main__":
    unittest.main()
