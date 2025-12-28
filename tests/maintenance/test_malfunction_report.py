import pytest
from src.maintenance.domain.entities.MalfunctionReport import MalfunctionReport

def test_report_should_fail_with_empty_description():
    # TDD RED: We expect a failure if the description is too short
    with pytest.raises(ValueError, match="Description too short"):
        MalfunctionReport(station_id="123", description="Fix")