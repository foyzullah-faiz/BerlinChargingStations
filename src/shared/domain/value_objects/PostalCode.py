class PostalCode:
    def __init__(self, value: str):
        # Enforces 5-digit numeric rule for German ZIPs
        if not str(value).isdigit() or len(str(value)) != 5:
            # FIX: Match the regex expected by your tests
            raise ValueError(f"Invalid Berlin ZIP: {value}")
        self.value = str(value)