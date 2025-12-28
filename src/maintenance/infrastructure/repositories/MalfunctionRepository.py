from pathlib import Path

class MalfunctionRepository:
    def __init__(self):
        current_file = Path(__file__).resolve()
        root = next(p for p in current_file.parents if p.name == "BerlinChargingStations")
        self.path = root / "src" / "shared" / "infrastructure" / "datasets" / "malfunctions.csv"

    def save(self, report):
        # RED PHASE: Do nothing
        return False