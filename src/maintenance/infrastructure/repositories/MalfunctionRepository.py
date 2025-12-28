import pandas as pd
import os
from pathlib import Path

class MalfunctionRepository:
    """
    Infrastructure Repository to persist malfunction reports in a CSV file.
    """
    def __init__(self):
        current_file = Path(__file__).resolve()
        root = next(p for p in current_file.parents if p.name == "BerlinChargingStations")
        self.path = root / "src" / "shared" / "infrastructure" / "datasets" / "malfunctions.csv"

    def save(self, report) -> bool:
        try:
            # 1. Prepare the data row
            new_data = pd.DataFrame([{
                "station_id": report.station_id,
                "description": report.description
            }])

            # 2. Append to existing file or create new
            if not self.path.exists():
                new_data.to_csv(self.path, index=False)
            else:
                new_data.to_csv(self.path, mode='a', header=False, index=False)
            
            return True
        except Exception:
            return False