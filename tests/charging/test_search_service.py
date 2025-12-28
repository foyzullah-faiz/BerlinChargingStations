import pytest
from src.charging.application.services.ChargingStationService import ChargingStationService

def test_service_should_call_repository():
    # Mock or empty repo
    class MockRepo:
        def find_by_postal_code(self, plz): return []
    
    service = ChargingStationService(MockRepo())
    results = service.find_charging_stations("10117")
    assert isinstance(results, list)