from bptree_201720697 import Node
from bptree_201720697 import B_PLUS_TREE as btree

temp = btree(4)
def insert_and_print(k):
    print('-------------------')
    temp.insert(k)
    for i in range(1, 1+k):
        temp.find(i)

insert_and_print(1)
insert_and_print(2)
insert_and_print(3)
insert_and_print(4)
insert_and_print(5)
insert_and_print(6)
insert_and_print(7)
insert_and_print(8)
insert_and_print(9)
insert_and_print(10)
insert_and_print(11)
insert_and_print(12)
insert_and_print(13)
insert_and_print(14)