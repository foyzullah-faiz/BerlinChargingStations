import pytest
from src.charging.application.services.ChargingStationService import ChargingStationService
from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository

def test_service_finds_stations_with_valid_zip():
    # Arrange: Setup repository and service [cite: 82, 94]
    repo = ChargingStationRepository()
    service = ChargingStationService(repo)
    
    # Act: Perform search with a valid Berlin ZIP [cite: 9, 20]
    stations = service.find_charging_stations("10117")
    
    # Assert: Success scenario [cite: 83]
    assert isinstance(stations, list)
    assert len(stations) > 0

def test_service_raises_error_for_invalid_zip():
    # Arrange
    repo = ChargingStationRepository()
    service = ChargingStationService(repo)
    
    # Act & Assert: Error scenario (Domain rule enforcement) [cite: 83, 103]
    with pytest.raises(ValueError, match="Invalid Berlin ZIP"):
        service.find_charging_stations("123")