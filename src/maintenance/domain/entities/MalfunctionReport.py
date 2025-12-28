class MalfunctionReport:
    """
    Domain Entity representing a user-submitted malfunction report.
    """
    def __init__(self, station_id: str, description: str):
        # Business Rule: Description must be at least 5 characters
        if not description or len(description) < 5:
            raise ValueError("Description too short")
        
        self.station_id = station_id
        self.description = description

    def __repr__(self):
        return f"MalfunctionReport(station_id={self.station_id}, desc={self.description[:10]}...)"