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
b.start_borrow()
a = Borrowing("02", mybook, m)
print(a.start_reserve())
print(b.get_borrow_detail()["book"])

# https://btrees.readthedocs.io/en/latest/api.html#id5
# a = BTrees.OOBTree.OOBTree()
# a.insert("1", Book(1))
# print(a.pop("2", -1))
