class PostalCode:
    def __init__(self, value: str):
        if not str(value).isdigit() or len(str(value)) != 5:
            raise ValueError(f"Invalid Berlin ZIP: {value}")
        self.value = str(value)