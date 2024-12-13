class StockNotFoundError(Exception):
    """Custom exception raised when a stock is not found in the repository."""
    def __init__(self, message: str = "Stock not found"):
        super().__init__(message)
