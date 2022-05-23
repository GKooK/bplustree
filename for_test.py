from bptree_201720697 import Node
from bptree_201720697 import B_PLUS_TREE as btree

temp = btree(5)
#temp.insert(1)
#temp.insert(2)
#temp.insert(3)
#temp.find(1)
#temp.print_tree()
temp.insert(5)
temp.insert(7)
temp.insert(8)
temp.insert(9)
temp.insert(3)
temp.insert(11)
temp.print_root()
temp.print_tree()
temp.find_range(5,8)