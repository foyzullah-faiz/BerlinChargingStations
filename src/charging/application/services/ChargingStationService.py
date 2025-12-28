from src.shared.domain.value_objects.PostalCode import PostalCode

class ChargingStationService:
    def __init__(self, repository):
        self.repository = repository

    def find_charging_stations(self, zip_str: str):
        # 1. Validate using Domain Logic
        postal_code = PostalCode(zip_str)
        
        # 2. Get all data from repository
        all_stations = self.repository.get_all()
        
        # 3. Filter results (Standardizing PLZ format for comparison)
        filtered = [
            s for s in all_stations 
            if str(s.get('Postleitzahl', '')).split('.')[0].zfill(5) == postal_code.value
        ]
        
        return filtered