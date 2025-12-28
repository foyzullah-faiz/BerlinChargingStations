import pandas as pd
from pathlib import Path

class ChargingStationRepository:
    def __init__(self):
        # Resolve the absolute path of this file
        current_file = Path(__file__).resolve()
        
        # Navigate 4 levels up to reach project root:
        # Repositories(0) -> Infrastructure(1) -> Charging(2) -> src(3) -> Root(4)
        root = current_file.parents[3]
        
        self.path = root / "shared" / "infrastructure" / "datasets" / "Ladesaeulenregister.csv"

    def get_all(self):
        """Reads the CSV. Works on both Mac and Cloud Server."""
        if not self.path.exists():
            return []
        df = pd.read_csv(self.path, sep=';', encoding='utf-8-sig', low_memory=False)
        return df.to_dict('records')