from enum import Enum
import persistent

class BookStatus(Enum):
    AVAILABLE = "available"
    BORROW = "borrow"
    RESERVE = "reserve"

class Book(persistent.Persistent):
    def __init__(self, unique_id:str, status:BookStatus=BookStatus.AVAILABLE) -> None:
        self.unique_id = unique_id
        self.status = status

    def __str__(self) -> str:
        return f"{self.unique_id}-{self.status.value}"