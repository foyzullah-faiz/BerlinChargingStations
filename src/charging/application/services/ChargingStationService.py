from src.shared.domain.value_objects.PostalCode import PostalCode

class ChargingStationService:
    """
    Application Service that orchestrates the Charging Station Search use case.
    """
    def __init__(self, repository):
        self.repository = repository

    def find_charging_stations(self, zip_input: str):
        # 1. Use the Domain Value Object for validation
        postal_code = PostalCode(zip_input)
        
        # 2. Delegate data retrieval to the Infrastructure Layer (Repository)
        return self.repository.find_by_postal_code(postal_code.value)