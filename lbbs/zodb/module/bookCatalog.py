import BTrees
import persistent
from .book import Book
import json


class BookCatalog(persistent.Persistent):
    def __init__(
        self, id: str, title: str, genre: str, author: str, detail: str
    ) -> None:
        self.__id = id
        self.__title = title
        self.__genre = genre
        self.__author = author
        self.__detail = detail
        self.__amount = 0
        self.__bookList = BTrees.OOBTree.OOBTree()

    # TODO what ways to connect to db?
    @staticmethod
    def searchBook(keyword) -> Book:
        pass

    # TODO:TEST
    def getBookList(self) -> list[Book]:
        return list(self.__bookList)

    # TODO:TEST
    def getBookData(self) -> str:
        return json.dumps(
            {
                "id": self.__id,
                "title": self.__title,
                "genre": self.__genre,
                "author": self.__author,
                "detail": self.__detail,
                "amount": self.__amount,
            }
        )

    # TODO:TEST
    def addBook(self, unique_id: str) -> int:
        """
        Return 1 if the item was added, or 0 otherwise.
        """
        new_book = Book(unique_id)
        ret = self.__bookList.insert(unique_id, new_book)
        return ret

    # TODO:TEST
    def removeBook(self, unique_id: str):
        """
        Return 1 if the item was removed, or 0 otherwise.
        """
        ret = self.__bookList.pop(unique_id, 0)
        ret = 1 if ret else ret
        return ret

    # TEST
    # FIXME
    def editBook(self):
        pass

    def __str__(self) -> str:
        return f"{self.id}-{self.title}"
