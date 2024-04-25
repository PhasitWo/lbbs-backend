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

print(root.book.get(62))