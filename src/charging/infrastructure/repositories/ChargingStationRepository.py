import pandas as pd
from pathlib import Path

class ChargingStationRepository:
    def __init__(self):
        current_file = Path(__file__).resolve()
        src_root = next(p for p in current_file.parents if p.name == 'src')
        self.dataset_dir = src_root / "shared" / "infrastructure" / "datasets"
        
        # Paths for both datasets
        self.charging_path = self.dataset_dir / "Ladesaeulenregister.csv"
        self.geo_path = self.dataset_dir / "geodata_berlin_plz.csv"

    def find_by_postal_code(self, zip_str: str) -> list:
        if not self.charging_path.exists():
            return []
            
        # 1. Load and clean Charging Station Data
        df = pd.read_csv(self.charging_path, sep=';', encoding='utf-8-sig', low_memory=False)
        df.columns = [c.strip().strip("'") for c in df.columns]
        
        plz_col = [c for c in df.columns if 'Postleitzahl' in c][0]
        df[plz_col] = (df[plz_col].astype(str).str.split('.').str[0]
                       .str.strip().str.strip("'"))
        
        # Filter for the target ZIP
        target = str(zip_str).strip()
        stations_df = df[df[plz_col] == target].copy()
        
        # 2. INTEGRATION: Join with Geodata
        if self.geo_path.exists() and not stations_df.empty:
            geo_df = pd.read_csv(self.geo_path, sep=';', encoding='utf-8')
            # Ensure geodata PLZ is string for matching
            geo_df['PLZ'] = geo_df['PLZ'].astype(str).str.strip()
            
            # Merge stations with their geographic polygons
            stations_df = stations_df.merge(
                geo_df, 
                left_on=plz_col, 
                right_on='PLZ', 
                how='left'
            )
        
        # 3. Final Clean and Return
        records = stations_df.to_dict('records')
        for r in records:
            for k in r:
                if isinstance(r[k], str): 
                    r[k] = r[k].strip().strip("'")
        return records