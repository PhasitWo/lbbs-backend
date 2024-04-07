import math
import BTrees
from module.book import Book, BookStatus
from module.bookCatalog import BookCatalog

# b = BookCatalog("123", "The fault in Our Stars", author="Earth")
# b.editBook(title="test", genre="JOHN!!!")
# print(b.getBookData())
b = Book("123", BookStatus.RESERVE)
b.setStatus("aaa")
print(b)


# https://btrees.readthedocs.io/en/latest/api.html#id5
# a = BTrees.OOBTree.OOBTree()
# a.insert("1", Book(1))
# print(a.pop("2", -1))


# class Test:
#     def __init__(self, x, y) -> None:
#         self.__x = x
#         self.__y = y

#     def getY(self) -> int:
#         return self.__y

# t = Test(5, 1)
# print(t.getY())
