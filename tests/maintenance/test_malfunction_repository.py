import os
import pandas as pd
from src.maintenance.infrastructure.repositories.MalfunctionRepository import MalfunctionRepository
from src.maintenance.domain.entities.MalfunctionReport import MalfunctionReport

def test_repository_should_append_multiple_reports():
    repo = MalfunctionRepository()
    # Ensure a clean start for this specific test if needed, 
    # or just check that count increases
    initial_count = len(repo.get_all())
    
    report1 = MalfunctionReport(station_id="REF-001", description="Broken screen")
    report2 = MalfunctionReport(station_id="REF-002", description="Broken cable")
    
    repo.save(report1)
    repo.save(report2)
    
    final_reports = repo.get_all()
    assert len(final_reports) == initial_count + 2
    assert final_reports[-1]['station_id'] == "REF-002"