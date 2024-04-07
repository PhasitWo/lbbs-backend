import BTrees
import persistent
from .book import Book


class BookCatalog(persistent.Persistent):

    def __init__(
        self,
        book_id: str,
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
        self.__bookList = BTrees.OOBTree.OOBTree()

    # TODO what ways to connect to db?
    @staticmethod
    def searchBook(keyword) -> Book:
        pass

    def getBookList(self) -> list[Book]:
        """
        return book list as [(unique_id, book_object), ...]
        """
        return list(self.__bookList.items())

    def getBookData(self) -> dict:
        return {
            "id": self.__id,
            "title": self.__title,
            "genre": self.__genre,
            "author": self.__author,
            "detail": self.__detail,
            "cover": self.__cover,
            "amount": self.__amount,
        }

    def addBook(self, unique_id: str) -> int:
        """
        Return 1 if the item was added, or 0 otherwise.
        """
        new_book = Book(unique_id)
        ret = self.__bookList.insert(unique_id, new_book)
        if ret:
            self.__amount += 1
        return ret

    def removeBook(self, unique_id: str) -> int:
        """
        Return 1 if the item was removed, or 0 otherwise.
        """
        ret = self.__bookList.pop(unique_id, 0)
        ret = 1 if ret else ret
        if ret:
            self.__amount -= 1
        return ret

    def editBook(
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

    def __str__(self) -> str:
        return f"{self.id}-{self.title}"
