import ZODB, transaction, sys
from datetime import date
from zodb.module.bookCatalog import BookCatalog
from zodb.module.book import Book
from zodb.module.constant import BookStatus
from zodb.module.borrowing import Borrowing
from zodb.module.member import Member

my_transaction_manager = transaction.TransactionManager()
db = ZODB.DB("lbbs/zodb/db.fs")
connection = db.open(my_transaction_manager)
root = connection.root

print(root.x)
