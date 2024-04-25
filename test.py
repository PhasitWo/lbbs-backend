import datetime
import time
import ZODB, transaction, sys
from datetime import date
from lbbs.zodb.module.bookCatalog import BookCatalog
from lbbs.zodb.module.book import Book
from lbbs.zodb.module.constant import BookStatus
from lbbs.zodb.module.borrowing import Borrowing
from lbbs.zodb.module.member import Member
import jwt

my_transaction_manager = transaction.TransactionManager()
db = ZODB.DB("lbbs/zodb/db.fs")
connection = db.open(my_transaction_manager)
root = connection.root

# root.member.insert(1, Member(1, "test_member1", "test_member1", "student"))
# root.member.insert(2, Member(2, "test_member2", "test_member2", "student"))
# root.member.insert(3, Member(3, "test_member3", "test_member3", "student"))

# my_transaction_manager.commit()