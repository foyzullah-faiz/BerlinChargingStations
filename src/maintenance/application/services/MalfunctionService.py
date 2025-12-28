from src.maintenance.domain.entities.MalfunctionReport import MalfunctionReport

class MalfunctionService:
    def __init__(self, repository):
        self.repository = repository

    def report_malfunction(self, station_id: str, description: str):
        """Orchestrates the reporting process."""
        if not station_id or not description:
            raise ValueError("Station ID and description are required")
        
        # Create the Domain Entity
        report = MalfunctionReport(station_id, description)
        
        # Pass the entity to the Infrastructure layer to save
        return self.repository.save(report)