import pandas as pd
from pathlib import Path

path = Path("src/shared/infrastructure/datasets/Ladesaeulenregister.csv")

if not path.exists():
    print(f"❌ Error: File not found at {path}")
else:
    # 1. FIX ENCODING: Use 'utf-8-sig' to automatically handle the BOM (ï»¿)
    df = pd.read_csv(path, sep=';', encoding='utf-8-sig', low_memory=False)
    
    # 2. CLEAN HEADERS: Remove quotes and whitespace
    df.columns = [c.strip().strip("'") for c in df.columns]
    
    print(f"Cleaned Columns: {list(df.columns[:5])}...")

    # 3. FIND POSTLEITZAHL COLUMN (Fuzzy Match)
    plz_col = [c for c in df.columns if 'Postleitzahl' in c][0]
    
    # 4. NORMALIZE DATA: Handle floats (10117.0) and quotes
    df[plz_col] = (df[plz_col].astype(str)
                   .str.split('.').str[0]
                   .str.strip()
                   .str.strip("'"))
    
    # 5. FILTER
    berlin_data = df[df[plz_col] == '10117']
    
    print(f"✅ Success! Found {len(berlin_data)} charging stations in ZIP 10117.")
    
    if len(berlin_data) > 0:
        row = berlin_data.iloc[0]
        # Accessing with exact names now that encoding is fixed
        name = str(row['Betreiber']).strip().strip("'")
        addr = str(row['Straße']).strip().strip("'")
        
        print(f"First Station: {name} at {addr}")