from temp_import_new import Node
from temp_import_new import B_PLUS_TREE as btree

#temp = btree(3)
#temp.insert(1)
#temp.insert(2)
#temp.insert(3)
#temp.find(2)
#temp.print_tree()

#temp = btree(5)
#temp.insert(5)
#temp.insert(3)
#temp.delete(3)
#temp.insert(7)
#temp.insert(8)
#temp.insert(9)
#temp.insert(3)
#temp.insert(11)
#temp.find(11)
#temp.print_tree()
#temp.find_range(5,8)

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

#temp = btree(5)
#temp.insert(5)
#temp.insert(10)
#temp.insert(15)
#temp.insert(20)
#temp.insert(25)
#temp.insert(30)
#temp.insert(50)
#temp.insert(55)
#temp.print_tree()
#temp.insert(60)
#temp.insert(65)
#temp.print_tree()
#temp.insert(75)
#temp.insert(80)
#temp.print_tree()
#temp.insert(85)
#temp.insert(90)
#temp.print_tree()
#temp.insert(28)
#temp.print_tree()

temp = btree(3)
#temp.insert(1)
#temp.insert(2)
#temp.insert(3)
#temp.find(2)
#temp.print_tree()
for i in range(1, 26+1):
    temp.insert(i)
temp.print_root
temp.find(2)
temp.find_range(5,8)
temp.print_tree()
print('---------------')
temp.delete(15)
temp.print_tree()
print('---------------')
temp.delete(7)
temp.print_tree()
print('---------------')
temp.delete(8)
temp.print_tree()
print('---------------')
temp.delete(9)
temp.print_tree()
print('---------------')
temp.delete(13)
temp.print_tree()
print('---------------')
temp.delete(11)
temp.print_tree()
print('---------------')
temp.delete(19)
temp.print_tree()
print('---------------')
temp.delete(14)
temp.print_tree()
print('---------------')
temp.delete(15)
temp.print_tree()
print('---------------')
temp.delete(5)
temp.print_tree()
print('---------------')
temp.delete(4)
temp.print_tree()
print('---------------')
temp.delete(2)
temp.print_tree()
print('---------------')
temp.delete(1)
temp.print_tree()
print('---------------')
temp.find_range(6,19)
temp.find(16)
temp.print_root()
print('---------------')