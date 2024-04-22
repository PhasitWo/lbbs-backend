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

root.bookCatalog = BTrees.IOBTree.IOBTree()
root.book = BTrees.IOBTree.IOBTree()
root.member = BTrees.IOBTree.IOBTree()
root.borrowing = BTrees.IOBTree.IOBTree()


with open("data.json", "r") as openfile:
    data = json.load(openfile)
    for index, item in enumerate(data):
        b = BookCatalog(
            index, item["title"], None, item["author"], None, item["cover_img"]
        )
        root.bookCatalog.insert(index, b)

c = root.bookCatalog.get(0)
b = Book(0)
c.add_book_by_object(b)
root.book.insert(0, b)

for catalog in list(root.bookCatalog.values()):
    for _ in range(3):
        new_id = root.book.maxKey() + 1
        b = Book(new_id)
        catalog.add_book_by_object(b)
        root.book.insert(new_id, b)

root.member.insert(0, Member(0, "test_member0", "test_member0", "student"))
root.member.insert(1, Member(1, "test_member1", "test_member1", "student"))
root.member.insert(2, Member(2, "test_member2", "test_member2", "student"))
root.member.insert(3, Member(3, "test_member3", "test_member3", "student"))

transaction.commit()
