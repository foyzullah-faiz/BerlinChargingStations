import pandas as pd
from pathlib import Path

class MalfunctionRepository:
    def __init__(self):
        current_file = Path(__file__).resolve()
        # Navigate 4 levels up to Project Root
        root = current_file.parents[3]
        self.path = root / "shared" / "infrastructure" / "datasets" / "malfunctions.csv"

    def save(self, report) -> bool:
        """Appends the report to the CSV file on disk."""
        new_data = pd.DataFrame([{
            "station_id": report.station_id, 
            "description": report.description
        }])
        
        header = not self.path.exists()
        # Ensure the directory exists on the server
        self.path.parent.mkdir(parents=True, exist_ok=True)
        
        new_data.to_csv(self.path, mode='a', index=False, header=header, encoding='utf-8')
        return True

    def get_all(self):
        """Fetches all reports to show the Operator."""
        if not self.path.exists():
            return []
        return pd.read_csv(self.path).to_dict('records')