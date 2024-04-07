from datetime import datetime
from enum import Enum
from .book import Book


class BorrowStatus(Enum):
    BORROW = "borrow"
    RESERVE = "reserve"
    RETURN = "return"
    CANCEL = "cancel"


class Borrowing:
    def __init__(
        self,
        borrow_id: str,
        status: BorrowStatus,
        book: Book,
        reserve_date: tuple[int],
        borrow_date: tuple[int],
        due_date: tuple[int],
        return_date: tuple[int],
    ) -> None:
        self.__borrow_id = None
        self.__status = None
        self.__reserve_date = None
        self.__borrow_date = None
        self.__due_date = None
        self.__return_date = None
        # TEST
        self.__book = None
