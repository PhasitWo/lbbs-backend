import ZODB, transaction, sys

connection = ZODB.connection("lbbs/zodb/db.fs")
root = connection.root

print(sys.path)