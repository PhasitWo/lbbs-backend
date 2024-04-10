import ZODB, transaction
import persistent
import BTrees
from datetime import date
from .zodb.module.bookCatalog import BookCatalog
from .zodb.module.book import Book
from .zodb.module.constant import BookStatus
from .zodb.module.borrowing import Borrowing
from .zodb.module.member import Member

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root



# transaction.commit()
