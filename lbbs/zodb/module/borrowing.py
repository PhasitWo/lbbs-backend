from datetime import date, timedelta
from enum import Enum
from .book import Book
from .member import Member


class BorrowStatus(Enum):
    BORROW = "borrow"
    RESERVE = "reserve"
    RETURN = "return"
    CANCEL = "cancel"


# TODO how to check if this reservation is void (does not borrow within expected date) -> use lib called 'schedule'
class Borrowing:
    def __init__(self, borrow_id: str, book: Book, member: Member) -> None:
        self.__id = borrow_id
        self.__book = book  # TEST
        self.__member = member  # TEST
        self.__status = None
        # Reserve
        self.__reserve_date = None
        self.__expected_date = None
        # Borrow
        self.__borrow_date = None
        self.__due_date = None
        self.__return_date = None
        self.__fine = 0.0

    # TODO what ways to connect to db?
    @staticmethod
    def search_borrowing(keyword) -> list['Borrowing']:
        pass

    # TEST
    def start_reserve(self) -> None:
        self.__reserve_date = date.today()
        self.__status = BorrowStatus.RESERVE
        # TODO find expected date from current borrowing for this book

    # TEST
    def start_borrow(self) -> None:
        self.__borrow_date = date.today()
        self.__due_date = self.__borrow_date + timedelta(days=7)
        self.__status = BorrowStatus.BORROW

    # TEST
    def calculate_fine(self) -> float:
        FINE_PER_DAY = 100.0  # TODO clarify policy
        day_exceed = max(0, (self.__return_date - self.__due_date).days)
        return FINE_PER_DAY * day_exceed

    # TEST
    def return_book(self) -> None:
        self.__reserve_date = date.today()
        self.__status = BorrowStatus.RETURN
        self.__fine = self.calculateFine()

    # TEST
    def get_borrow_detail(self):
        return {
            "id": self.__id,
            "book": self.__book,
            "member": self.__member,
            "status": self.__status,
            "reserve_date": self.__reserve_date,
            "expected_date": self.__expected_date,
            "borrow_date": self.__borrow_date,
            "due_date": self.__due_date,
            "return_date": self.__return_date,
            "fine": self.__fine
        }
