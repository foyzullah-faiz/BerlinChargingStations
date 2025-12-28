from src.shared.domain.value_objects.PostalCode import PostalCode

class ChargingStationService:
    def __init__(self, repository):
        self.repository = repository

    def find_charging_stations(self, zip_input: str):
        # Coordinate Validation -> Infrastructure
        postal_code = PostalCode(zip_input)
        return self.repository.find_by_postal_code(postal_code.value)