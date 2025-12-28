import pandas as pd
from pathlib import Path
from typing import List, Dict

class MalfunctionRepository:
    """
    Handles persistence for malfunction reports.
    Refactored to include robust error handling and type safety.
    """
    def __init__(self) -> None:
        current_file = Path(__file__).resolve()
        root = next(p for p in current_file.parents if p.name == "BerlinChargingStations")
        self.path = root / "src" / "shared" / "infrastructure" / "datasets" / "malfunctions.csv"

    def save(self, report) -> bool:
        """Appends a new report to the CSV file safely."""
        try:
            new_data = pd.DataFrame([{
                "station_id": report.station_id,
                "description": report.description
            }])

            # Use header=False if file exists to avoid duplicating headers
            file_exists = self.path.exists()
            new_data.to_csv(
                self.path, 
                mode='a', 
                index=False, 
                header=not file_exists, 
                encoding='utf-8'
            )
            return True
        except Exception as e:
            print(f"Repository Error: {e}")
            return False

    def get_all(self) -> List[Dict]:
        """Utility method added during refactor to retrieve all reports."""
        if not self.path.exists():
            return []
        return pd.read_csv(self.path).to_dict('records')