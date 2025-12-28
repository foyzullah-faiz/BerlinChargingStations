from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository

def test_repository_should_return_data_from_csv():
    repo = ChargingStationRepository()
    stations = repo.find_by_postal_code("10117")
    assert len(stations) > 0  # Should find stations in Mitte