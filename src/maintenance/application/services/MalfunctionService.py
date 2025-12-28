from src.maintenance.domain.entities.MalfunctionReport import MalfunctionReport

class MalfunctionService:
    def __init__(self, repository):
        self.repository = repository

    def report_malfunction(self, station_id: str, description: str) -> bool:
        # 1. Create Domain Entity (This triggers Layer 1 validation)
        report = MalfunctionReport(station_id=station_id, description=description)
        
        # 2. Persist via Infrastructure (Layer 3)
        return self.repository.save(report)