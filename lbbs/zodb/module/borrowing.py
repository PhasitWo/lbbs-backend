from datetime import date, timedelta
from enum import Enum
from .constant import BookStatus, BorrowStatus
from .book import Book
from .member import Member
import persistent

# TODO how to check if this reservation is void (does not borrow within expected date) -> use lib called 'schedule'
class Borrowing(persistent.Persistent):
    def __init__(self, borrow_id: str, book: Book, member: Member) -> None:
        self.__id = borrow_id
        self.__book = book
        self.__member = member
        self.__member.add_borrowing(self)
        self.__status = None
        # Reserve
        self.__reserve_date = None
        # Borrow
        self.__borrow_date = None
        self.__due_date = None
        self.__return_date = None
        self.__fine = 0.0

    # TODO what ways to connect to db?
    @staticmethod
    def search_borrowing(keyword) -> list["Borrowing"]:
        pass

    def start_reserve(self) -> int:
        """
        Return 1 if the reserve attempt succeed, or 0 otherwise.
        """
        if self.__book.get_book_data()["status"] != BookStatus.BORROW:
            return 0
        self.__reserve_date = date.today()
        self.__status = BorrowStatus.RESERVE
        self.__book.set_status(BookStatus.RESERVE)
        return 1

    def start_borrow(self) -> int:
        """
        Return 1 if the borrow attempt succeed, or 0 otherwise.
        """
        if self.__book.get_book_data()["status"] != BookStatus.AVAILABLE:
            return 0
        self.__borrow_date = date.today()
        self.__due_date = self.__borrow_date + timedelta(days=7)
        self.__status = BorrowStatus.BORROW
        self.__book.set_status(BookStatus.BORROW)
        self.__book.set_expected_date(self.__due_date)
        return 1

    def calculate_fine(self) -> float:
        FINE_PER_DAY = 100.0  # TODO clarify policy
        day_exceed = max(0, (self.__return_date - self.__due_date).days)
        return FINE_PER_DAY * day_exceed

    def return_book(self) -> None:
        self.__return_date = date.today()
        self.__status = BorrowStatus.RETURN
        self.__fine = self.calculate_fine()
        self.__book.set_status(BookStatus.AVAILABLE)
        self.__book.set_expected_date(None)

    def get_borrow_detail(self) -> dict:
        return {
            "id": self.__id,
            "book": self.__book,
            "member": self.__member,
            "status": self.__status,
            "reserve_date": self.__reserve_date,
            "expected_date": self.__book.get_book_data()["expected_date"],
            "borrow_date": self.__borrow_date,
            "due_date": self.__due_date,
            "return_date": self.__return_date,
            "fine": self.__fine,
        }
