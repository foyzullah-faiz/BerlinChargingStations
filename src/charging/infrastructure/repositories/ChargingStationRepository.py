import pandas as pd
from pathlib import Path

class ChargingStationRepository:
    """
    Infrastructure Repository that reads charging station data from a CSV file.
    """
    def __init__(self):
        # Dynamically find the project root and the dataset path
        current_file = Path(__file__).resolve()
        root = next(p for p in current_file.parents if p.name == "BerlinChargingStations")
        self.path = root / "src" / "shared" / "infrastructure" / "datasets" / "Ladesaeulenregister.csv"

    def find_by_postal_code(self, zip_str: str) -> list:
        if not self.path.exists():
            return []
            
        # Implementation to satisfy the 'assert len(stations) > 0' test
        # 1. Read the CSV (handling the German semicolon separator and encoding)
        df = pd.read_csv(self.path, sep=';', encoding='utf-8-sig', low_memory=False)
        
        # 2. Clean the column names (remove quotes and whitespace)
        df.columns = [c.strip().strip("'") for c in df.columns]
        
        # 3. Clean the 'Postleitzahl' column (it often has .0 if read as float)
        # We find the column name that contains 'Postleitzahl'
        plz_col = [c for c in df.columns if 'Postleitzahl' in c][0]
        df[plz_col] = df[plz_col].astype(str).str.split('.').str[0].str.strip()
        
        # 4. Filter by the ZIP string and return as a list of dictionaries
        results = df[df[plz_col] == str(zip_str)]
        
        return results.to_dict('records')