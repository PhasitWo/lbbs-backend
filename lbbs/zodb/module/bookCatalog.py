import BTrees
import persistent
from .book import Book
from .constant import BookStatus

class BookCatalog(persistent.Persistent):

    def __init__(
        self,
        book_id: int,
        title: str,
        genre: str = None,
        author: str = None,
        detail: str = None,
        coverURL: str = None,
    ) -> None:
        self.__id = book_id
        self.__title = title
        self.__genre = genre
        self.__author = author
        self.__detail = detail
        self.__cover = coverURL
        self.__amount = 0
        self.__book_list = BTrees.IOBTree.IOBTree()

    @staticmethod
    def search_book_catalog(root, keyword: str) -> list["BookCatalog"]:
        """
        require root of the zodb
        """
        lst = []
        keyword = keyword.lower()
        bookCatalogs = list(root.bookCatalog.values())
        for catalog in bookCatalogs:
            title = catalog.get_book_data()["title"].lower()
            if keyword in title:
                lst.append(catalog)
        return lst

    def get_book_list(self) -> list[Book]:
        return self.__book_list

    def get_book_data(self) -> dict:
        return {
            "book_id": self.__id,
            "title": self.__title,
            "genre": self.__genre,
            "author": self.__author,
            "detail": self.__detail,
            "cover": self.__cover,
            "amount": self.__amount,
        }

    def add_book(self, unique_id: int) -> int:
        """
        Return 1 if the item was added, or 0 otherwise.
        """
        new_book = Book(unique_id)
        ret = self.__book_list.insert(unique_id, new_book)
        if ret:
            self.__amount += 1
        return ret

    def add_book_by_object(self, book:Book) -> int:
        """
        Return 1 if the item was added, or 0 otherwise.
        """
        ret = self.__book_list.insert(book.get_book_data()["unique_id"], book)
        if ret:
            self.__amount += 1
        return ret

    def remove_book(self, unique_id: int) -> int:
        """
        Return 1 if the item was removed, or 0 otherwise.
        """
        ret = self.__book_list.pop(unique_id, 0)
        ret = 1 if ret else ret
        if ret:
            self.__amount -= 1
        return ret

    def edit(
        self,
        title: str = None,
        genre: str = None,
        author: str = None,
        detail: str = None,
        coverURL: str = None,
    ) -> None:
        """
        Take only keyword arguments: title, genre. author, detail, amount
        This function only edits attributes based on keywords that are specified
        """
        self.__title = title if title != None else self.__title
        self.__genre = genre if genre != None else self.__genre
        self.__author = author if author != None else self.__author
        self.__detail = detail if detail != None else self.__detail
        self.__cover = coverURL if coverURL != None else self.__cover

    def get_available_for_reserve(self) -> Book:
        """
        return a book that has the closest expected that for reserve
        """
        lst = list(self.__book_list.items())
        candidate_book = None
        # find book that has status borrow and expected date is closest
        for unique_id, book in lst:
            status = book.get_book_data()["status"]
            if status != BookStatus.BORROW:
                continue
            if candidate_book == None:
                candidate_book = book
                continue
            if book.get_book_data()["expected_date"] < candidate_book.get_book_data()["expected_date"]:
                candidate_book = book
        return candidate_book

    def is_available(self) -> bool:
        """
        return true if there is a available book for borrowing (not reserve)
        """
        lst = list(self.__book_list.items())
        for unique_id, book in lst:
            status = book.get_book_data()["status"]
            if status == BookStatus.AVAILABLE:
                return True
        return False

    def __str__(self) -> str:
        return f"{self.__id}-{self.__title}"
