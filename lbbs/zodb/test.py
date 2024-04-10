import math
import BTrees
from module.book import Book, BookStatus
from module.bookCatalog import BookCatalog
from module.member import Member
from module.borrowing import Borrowing
from datetime import date, timedelta

m = Member("1001", "1234", "JOHN", "student")
mybook = Book("1234", status=BookStatus.AVAILABLE)
b = Borrowing("01", mybook, m)
print(id(m))
print(m.get_borrow_list()[0].get_borrow_detail())

# https://btrees.readthedocs.io/en/latest/api.html#id5
# a = BTrees.OOBTree.OOBTree()
# a.insert("1", Book(1))
# print(a.pop("2", -1))
