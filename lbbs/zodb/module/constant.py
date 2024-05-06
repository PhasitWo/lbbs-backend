from enum import Enum


class BookStatus(Enum):
    AVAILABLE = "available"
    BORROW = "borrow"
    RESERVE = "reserve"
    WAIT = "wait"
    REMOVED = "removed"

class BorrowStatus(Enum):
    BORROW = "borrow"
    RESERVE = "reserve"
    RETURN = "return"
    CANCEL = "cancel"
