from temp_import import Node
from temp_import import B_PLUS_TREE as btree

#temp = btree(3)
#temp.insert(1)
#temp.insert(2)
#temp.insert(3)
#temp.find(2)
#temp.print_tree()

temp = btree(5)
temp.insert(5)
temp.insert(7)
temp.insert(8)
temp.insert(9)
temp.insert(3)
temp.insert(11)
temp.find(11)
temp.print_tree()
temp.find_range(5,8)

#temp = btree(4)
#def insert_and_print(k):
#    print('-------------------')
#    temp.insert(k)
#    for i in range(1, 1+k):
#        temp.find(i)
#
#insert_and_print(1)
#insert_and_print(2)
#insert_and_print(3)
#insert_and_print(4)
#insert_and_print(5)
#insert_and_print(6)
#insert_and_print(7)
#insert_and_print(8)
#insert_and_print(9)
#temp.insert(10)
##insert_and_print(10)
#insert_and_print(11)
#insert_and_print(12)
#insert_and_print(13)
#insert_and_print(14)
#temp.find_range(3, 11)
#temp.print_tree()