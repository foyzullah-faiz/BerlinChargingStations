from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository

def test_repository_should_return_all_data():
    repo = ChargingStationRepository()
    all_stations = repo.get_all()
    
    # Assert that it returns a list and is not empty (assuming dataset is present)
    assert isinstance(all_stations, list)
    if len(all_stations) > 0:
        assert "Postleitzahl" in all_stations[0]