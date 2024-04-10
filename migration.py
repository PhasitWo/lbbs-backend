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

# root.bookCatalog = BTrees.IOBTree.IOBTree()
# root.book = BTrees.IOBTree.IOBTree()
# root.member = BTrees.IOBTree.IOBTree()

# root.member.insert(1, Member(1, "1234", "JOHN", "Student"))
# new_catalog = BookCatalog(
#     1, "The Fault in Our Stars", "Romance", "Hazel Grace", "bra,..bra.."
# )
# root.bookCatalog.insert(1, new_catalog)
# new_book = Book(123)
# root.book.insert(123, new_book)
# new_catalog.add_book_by_object(new_book)


# transaction.commit()
