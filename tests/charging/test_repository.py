from src.charging.infrastructure.repositories.ChargingStationRepository import ChargingStationRepository

def test_repository_should_return_data_for_known_mitte_zip():
    repo = ChargingStationRepository()
    # 10117 is a known dense area in Berlin
    stations = repo.find_by_postal_code("10117")
    assert len(stations) > 0
    assert all(s['Postleitzahl'] == '10117' for s in stations)

def test_repository_should_return_empty_list_for_non_existent_zip():
    repo = ChargingStationRepository()
    # 99999 is not a Berlin ZIP
    stations = repo.find_by_postal_code("99999")
    assert len(stations) == 0