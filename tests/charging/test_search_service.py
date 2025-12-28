from src.charging.application.services.ChargingStationService import ChargingStationService

def test_service_should_call_repository_get_all():
    # Mocking the new repository structure
    class MockRepo:
        def get_all(self): 
            return [
                {"Postleitzahl": "10117", "Betreiber": "Test Op"},
                {"Postleitzahl": "12345", "Betreiber": "Other Op"}
            ]

    service = ChargingStationService(MockRepo())
    results = service.find_charging_stations("10117")
    
    # Assert service filtered correctly
    assert len(results) == 1
    assert results[0]["Postleitzahl"] == "10117"

def test_service_should_return_empty_for_unmatched_zip():
    class MockRepo:
        def get_all(self): return [{"Postleitzahl": "10117"}]
        
    service = ChargingStationService(MockRepo())
    results = service.find_charging_stations("99999")
    assert len(results) == 0