import ZODB, transaction
import persistent
import BTrees

class Book(persistent.Persistent):
    def __init__(self, id,  title, author):
       self.id = id
       self.title = title
       self.author = author
    def __str__(self) -> str:
        return f"{self.id}-{self.title}"

class Author(persistent.Persistent):
    def __init__(self, id, name):
        self.id = id
        self.name = name
    def __str__(self) -> str:
        return f"{self.id}-{self.name}"


connection = ZODB.connection('lbbs/zodb/mydata.fs')
root = connection.root

root.author[1].name = "bell"
print(root.book[1].author)
# a = Author(1, "John")
# root.author = BTrees.IOBTree.IOBTree()
# root.author[1] = a

# root.book = BTrees.IOBTree.IOBTree()
# root.book[1] = Book(1, "example_book", a)

# transaction.commit()
