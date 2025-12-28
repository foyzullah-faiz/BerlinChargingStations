import os
from pathlib import Path

def initialize_structure():
    # Root folder: BerlinCharginStations
    base = Path.cwd()
    
    # 1. Define only the necessary folders for the two use cases [cite: 23, 31, 56]
    folders = [
        # Use Case 1: Charging Station Search (Bounded Context)
        "src/charging/application/services",
        "src/charging/domain/entities",
        "src/charging/infrastructure/repositories",
        
        # Use Case 2: Maintenance/Malfunctions (Bounded Context) [cite: 6, 43]
        "src/maintenance/application/services",
        "src/maintenance/domain",
        "src/maintenance/infrastructure/repositories",
        
        # Shared Layer (Value Objects and Data) [cite: 31, 78]
        "src/shared/domain/value_objects",
        "src/shared/infrastructure/datasets",
        "src/shared/infrastructure/repositories",
        
        # UI Layer [cite: 30, 109]
        "src/presentation",
        
        # TDD Test structure mirroring the source [cite: 56, 94]
        "tests/charging",
        "tests/maintenance",
        "tests/shared/domain"
    ]

    # 2. Create folders and __init__.py files [cite: 22, 54, 71]
    for folder in folders:
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        
        # Ensure every directory in the path has an __init__.py
        current = path
        while current != base:
            init_file = current / "__init__.py"
            if not init_file.exists():
                init_file.touch()
            current = current.parent

    # 3. Create the necessary files for TDD implementation [cite: 81-86, 96]
    files = {
        # Shared Domain (Postal Code Value Object) [cite: 9, 96]
        "src/shared/domain/value_objects/PostalCode.py": "",
        
        # Use Case 1: Search Implementation [cite: 13, 18]
        "src/charging/application/services/ChargingStationService.py": "",
        "src/charging/infrastructure/repositories/ChargingStationRepository.py": "",
        
        # Use Case 2: Malfunction Implementation [cite: 110]
        "src/maintenance/application/services/MalfunctionService.py": "",
        
        # Test Files for TDD Cycle [cite: 82, 94]
        "tests/shared/domain/test_postal_code.py": "",
        "tests/charging/test_search_service.py": ""
    }

    for file_path, content in files.items():
        with open(base / file_path, "w") as f:
            f.write(content)
            
    print("✅ Project structure and __init__.py files created successfully.")

if __name__ == "__main__":
    initialize_structure()