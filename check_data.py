import pandas as pd
from pathlib import Path

class ChargingStationRepository:
    def __init__(self):
        # Reliable path resolution
        this_file = Path(__file__).resolve()
        project_root = this_file.parents[4] 
        self.path = project_root / "src" / "shared" / "infrastructure" / "datasets" / "Ladesaeulenregister.csv"

    def find_by_postal_code(self, zip_str: str) -> list:
        if not self.path.exists():
            return []
            
        # Load with latin-1 for German characters and semicolon separator
        df = pd.read_csv(self.path, sep=';', encoding='latin-1', low_memory=False)
        
        # FIX: Convert ZIP column to string and remove '.0' if it exists (float artifact)
        # This is the "Deep Retrieval" logic needed for this specific dataset
        df['Postleitzahl'] = df['Postleitzahl'].astype(str).str.split('.').str[0].str.strip()
        
        # Filter (standardize the search input too)
        target = str(zip_str).strip()
        results = df[df['Postleitzahl'] == target]
        
        return results.to_dict('records')