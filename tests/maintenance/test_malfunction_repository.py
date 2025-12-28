import os
import pandas as pd
from src.maintenance.infrastructure.repositories.MalfunctionRepository import MalfunctionRepository
from src.maintenance.domain.entities.MalfunctionReport import MalfunctionReport

def test_repository_should_save_report_to_csv():
    repo = MalfunctionRepository()
    report = MalfunctionReport(station_id="TEST-001", description="Broken display")
    
    # Act
    success = repo.save(report)
    
    # Assert
    assert success is True
    # Verify file was created/updated
    assert os.path.exists(repo.path)
    
    # Cleanup after test
    df = pd.read_csv(repo.path)
    assert "TEST-001" in df['station_id'].values