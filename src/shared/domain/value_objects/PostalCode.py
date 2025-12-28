class PostalCode:
    """
    Domain Value Object for Berlin Postal Codes.
    As per DDD, it ensures its own validity upon creation.
    """
    def __init__(self, value: str):
        # Business Rule: Must be exactly 5 numeric digits
        if not str(value).isdigit() or len(str(value)) != 5:
            # This specific message is what our test is looking for
            raise ValueError(f"Invalid Berlin ZIP: {value}")
        
        self.value = str(value)

    def __repr__(self):
        return f"PostalCode({self.value})"