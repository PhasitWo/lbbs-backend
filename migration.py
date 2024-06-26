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
from lbbs.zodb.module.librarian import Librarian

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root

# root.librarian = BTrees.IOBTree.IOBTree()
# root.librarian.insert(0, Librarian(0, "admin", "admin"))
# root.bookCatalog = BTrees.IOBTree.IOBTree()
# root.book = BTrees.IOBTree.IOBTree()
# root.member = BTrees.IOBTree.IOBTree()
# root.borrowing = BTrees.IOBTree.IOBTree()


# with open("data.json", "r") as openfile:
#     data = json.load(openfile)
#     for index, item in enumerate(data):
#         b = BookCatalog(
#             index, item["title"], None, item["author"], None, item["cover_img"]
#         )
#         root.bookCatalog.insert(index, b)

# c = root.bookCatalog.get(0)
# b = Book(0)
# c.add_book_by_object(b)
# root.book.insert(0, b)

# for catalog in list(root.bookCatalog.values()):
#     for _ in range(3):
#         new_id = root.book.maxKey() + 1
#         b = Book(new_id)
#         catalog.add_book_by_object(b)
#         root.book.insert(new_id, b)

# root.member.insert(0, Member(0, "test", "John", "student"))

transaction.commit()
