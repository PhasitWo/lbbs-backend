import BTrees

a = BTrees.OOBTree.OOBTree()
a.update({1:"123", 2:"456"})
print(a[1])
