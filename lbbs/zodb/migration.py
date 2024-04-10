import ZODB, transaction
import persistent
import BTrees
from datetime import date
from module.bookCatalog import BookCatalog
from module.book import Book
from module.constant import BookStatus
from module.borrowing import Borrowing
from module.member import Member

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root
# TODO check if date attribute will change value of _p_changed

b = root.bookCatalog["1"].get_book_list()["123"]
m: Member = root.member["007"]
t: Borrowing = root.borrowing["test"]
t.start_borrow()
print(root.member.maxKey())


# transaction.commit()
