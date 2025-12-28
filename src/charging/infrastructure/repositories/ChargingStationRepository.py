import pandas as pd
from pathlib import Path
from typing import List, Dict

class ChargingStationRepository:
    """
    Handles data access for charging stations using a CSV dataset.
    Follows the Repository Pattern to decouple domain logic from data sources.
    """
    def __init__(self) -> None:
        current_file = Path(__file__).resolve()
        # Finding the project root dynamically
        root = next(p for p in current_file.parents if p.name == "BerlinChargingStations")
        self.path = root / "src" / "shared" / "infrastructure" / "datasets" / "Ladesaeulenregister.csv"

    def find_by_postal_code(self, zip_str: str) -> List[Dict]:
        """
        Retrieves a list of charging stations filtered by postal code.
        
        Args:
            zip_str: A validated 5-digit postal code string.
            
        Returns:
            A list of dictionaries representing charging stations.
        """
        if not self.path.exists():
            return []
            
        # Read dataset with proper encoding for German characters
        df = pd.read_csv(self.path, sep=';', encoding='utf-8-sig', low_memory=False)
        
        # Clean headers: remove spaces and single quotes
        df.columns = [c.strip().strip("'") for c in df.columns]
        
        # Robustly find the Postal Code column and clean numeric values
        plz_col = [c for c in df.columns if 'Postleitzahl' in c][0]
        df[plz_col] = df[plz_col].astype(str).str.split('.').str[0].str.strip()
        
        # Filter and convert to domain-friendly list of dicts
        results = df[df[plz_col] == zip_str]
        return results.to_dict('records')