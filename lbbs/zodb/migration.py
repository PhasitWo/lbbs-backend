import ZODB, transaction
import persistent
import BTrees


connection = ZODB.connection('lbbs/zodb/db.fs')
root = connection.root

root.author[1].name = "bell"
print(root.book[1].author)
# a = Author(1, "John")
# root.author = BTrees.IOBTree.IOBTree()
# root.author[1] = a

# root.book = BTrees.IOBTree.IOBTree()
# root.book[1] = Book(1, "example_book", a)

# transaction.commit()
