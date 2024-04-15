import json
import ZODB, transaction
import persistent
import BTrees
from datetime import date
from lbbs.zodb.module.bookCatalog import BookCatalog
from lbbs.zodb.module.book import Book
from lbbs.zodb.module.constant import BookStatus
from lbbs.zodb.module.borrowing import Borrowing
from lbbs.zodb.module.member import Member

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root


member = root.member.get(0)
catalog = root.bookCatalog.get(0)
book = root.book.get(0)
b = Borrowing(5, member, catalog, book)
root.borrowing.insert(5, b)

transaction.commit()
# catalog: BookCatalog = root.bookCatalog.get(2)
# b = Book(300, BookStatus.BORROW)
# b.set_expected_date(date(2024,1,1))
# f = Book(400, BookStatus.BORROW)
# f.set_expected_date(date(2025,1,1))
# catalog.add_book_by_object(b)
# catalog.add_book_by_object(f)


# root.member.insert(1, Member(1, "1234", "JOHN", "Student"))
# new_catalog = BookCatalog(
#     1, "The Fault in Our Stars", "Romance", "Hazel Grace", "bra,..bra.."
# )
# root.bookCatalog.insert(1, new_catalog)
# new_book = Book(123)
# root.book.insert(123, new_book)
# new_catalog.add_book_by_object(new_book)
