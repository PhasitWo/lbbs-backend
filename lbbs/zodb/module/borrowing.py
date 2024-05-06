from datetime import date, timedelta
from .constant import BookStatus, BorrowStatus
from .bookCatalog import BookCatalog
from .book import Book
from .member import Member
import persistent


# TODO how to check if this reservation is void (does not borrow within expected date) -> use lib called 'schedule'
class Borrowing(persistent.Persistent):
    def __init__(
        self, borrow_id: int, member: Member, book_catalog: BookCatalog, book: Book
    ) -> None:
        self.__id = borrow_id
        self.__member = member
        self.__member.add_borrowing(self)
        self.__book_catalog = book_catalog
        self.__book = book
        self.__status = None
        # Reserve
        self.__reserve_date = None
        # Borrow
        self.__borrow_date = None
        self.__due_date = None
        self.__return_date = None
        self.__fine = 0.0

    @staticmethod
    def search_borrowing(root, keyword: int) -> list["Borrowing"]:
        """
        require root of the zodb
        """
        lst = []
        all_borrowing = list(root.borrowing.values())
        for borrowing in all_borrowing:
            borrow_id = borrowing.get_borrow_detail()["borrow_id"]
            member_id = borrowing.get_borrow_detail()["member"].get_id()
            print(borrow_id, member_id)
            if keyword == borrow_id or keyword == member_id:
                lst.append(borrowing)
        return lst

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
        if (
            self.__book.get_book_data()["status"] != BookStatus.AVAILABLE
            or self.__book.get_book_data()["status"] != BookStatus.WAIT
        ):
            return 0
        self.__borrow_date = date.today()
        self.__due_date = self.__borrow_date + timedelta(days=7)
        self.__status = BorrowStatus.BORROW
        self.__book.set_status(BookStatus.BORROW)
        self.__book.set_expected_date(self.__due_date)
        return 1

    def calculate_fine(self) -> float:
        FINE_PER_DAY = 5.0
        day_exceed = max(0, (self.__return_date - self.__due_date).days)
        return FINE_PER_DAY * day_exceed

    def return_book(self) -> None:
        self.__return_date = date.today()
        self.__fine = self.calculate_fine()
        self.__status = BorrowStatus.RETURN
        if self.__book.get_book_data()["status"] == BookStatus.BORROW:
            self.__book.set_status(BookStatus.AVAILABLE)
        elif self.__book.get_book_data()["status"] == BookStatus.RESERVE:
            self.__book.set_status(BookStatus.WAIT)
        self.__book.set_expected_date(None)

    def cancel_reserve(self) -> None:
        self.__status = BorrowStatus.CANCEL
        self.__book.set_status(BookStatus.BORROW)

    def get_borrow_detail(self) -> dict:
        return {
            "borrow_id": self.__id,
            "member": self.__member,
            "book_catalog": self.__book_catalog,
            "book": self.__book,
            "status": self.__status,
            "reserve_date": self.__reserve_date,
            "expected_date": self.__book.get_book_data()["expected_date"],
            "borrow_date": self.__borrow_date,
            "due_date": self.__due_date,
            "return_date": self.__return_date,
            "fine": self.__fine,
        }
