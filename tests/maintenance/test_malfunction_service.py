import pytest
from src.maintenance.application.services.MalfunctionService import MalfunctionService

def test_service_should_successfully_process_valid_report():
    # We use a Mock Repository to test the Service without needing a real CSV
    class MockRepo:
        def save(self, report): return True

    service = MalfunctionService(MockRepo())
    
    # Act
    result = service.report_malfunction(station_id="BCS-001", description="Cable is damaged")
    
    # Assert
    assert result is True

def test_service_should_propagate_domain_validation_error():
    class MockRepo:
        def save(self, report): return True

    service = MalfunctionService(MockRepo())
    
    # Act & Assert: The service should let the Domain's ValueError bubble up
    with pytest.raises(ValueError, match="Description too short"):
        service.report_malfunction(station_id="BCS-001", description="Fix")