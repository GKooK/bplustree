from logging import root
import sys


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []
        
        # |order| / 2 <= # of subTree pointers <= |order|
        self.subTrees = []
        
        self.parent = None
        self.isLeaf = False
        
        # leaf node has next node pointer
        self.nextNode = None   
        self.values = []


class B_PLUS_TREE:
    '''
    Implement below functions
    '''
    def __init__(self, order):
        self.order = order
        self.root  = None
        pass      
        
    def find_node(self, k):
        if(self.root.isLeaf == True):
            return self.root
        else:
            start = self.root
            pathes = []
            return_val = None
            while(1):
                if(start.isLeaf==True):#최종 리프 노드까지 오게 되면
                    pathes.append(start.keys)
                    return_val = start
                    break
                if(start.keys[0] > k): #제일 작은 key보다 작은은 값을 찾을 경우
                    pathes.append(start.keys)
                    start = start.subTrees[0]
                elif(start.keys[-1] <= k): #제일 큰 key보다 크거나 같은 값을 찾을 경우
                    pathes.append(start.keys)
                    start = start.subTrees[-1]
                else:#특정 key 보다 작거나 같거나 key+1인 것보다 큰 값 찾는 경우
                    for i in range(len(start.keys)-1):
                        if(start.keys[i]>=k and start.keys[i+1]<k):
                            pathes.append(start.keys)
                            start = start.subTrees[i+1]
                            break
            return return_val
        return None
        pass

    def insert(self, k):        
        if(self.root==None):#최초로 값 삽입할 때
            n = Node()
            n.keys.append(k)
            n.values.append(k)
            self.root = n
            self.root.isLeaf = True
        else:#최초로 값 입력할 때가 아닐 때
            insert_place = self.find_node(k)
            if(len(insert_place.keys)==self.order-1):#찾은 부분이 꽉차있다면
                insert_place.keys.append(k)
                insert_place.keys.sort()
                while(len(insert_place.keys)>self.order-1):#쪼개지지 않은 부모를 발견할때까지 반복한다.
                    #새로 채워넣고 쪼갠 다음 parent업데이트 해주자
                    #채워넣기
                    if(insert_place.isLeaf==True):
                        n2 = Node()
                        #n2.keys.append(insert_place.keys[(len(insert_place.keys)+1)//2:])
                        n2.keys = n2.keys+(insert_place.keys[(len(insert_place.keys)+1)//2:])
                        up_node_val = insert_place.keys[(len(insert_place.keys)+1)//2]
                        n2.keys.sort()
                        insert_place.keys = insert_place.keys[:(len(insert_place.keys)+1)//2]
                        n2.parent=insert_place.parent
                    else:
                        n2 = Node()
                        #n2.keys.append(insert_place.keys[(len(insert_place.keys)+1)//2:])
                        n2.keys = n2.keys+(insert_place.keys[(len(insert_place.keys)+1)//2+1:])
                        up_node_val = insert_place.keys[(len(insert_place.keys)+1)//2]
                        n2.keys.sort()
                        insert_place.keys = insert_place.keys[:(len(insert_place.keys)+1)//2]
                        n2.subTrees = n2.subTrees+insert_place.subTrees[(len(insert_place.subTrees)+1)//2:]
                        for i in n2.subTrees:
                            i.parent = n2
                        insert_place.subTrees = insert_place.subTrees[:(len(insert_place.subTrees)+1)//2]
                        for i in insert_place.subTrees:
                            i.parent = insert_place
                        n2.parent=insert_place.parent
                    #leaf node면 values에도 추가해 주어야 한다. 또한 leaf 설정도 해 주어야 한다.
                    if(insert_place.isLeaf == True):#작업하는 영역이 자식 노드일 경우에는 values값도 추가해 주어야 한다.
                        insert_place.values.append(k)
                        insert_place.values.sort()
                        n2.values = n2.values+(insert_place.values[(len(insert_place.values)+1)//2:])
                        insert_place.values = insert_place.values[:(len(insert_place.values)+1)//2]
                        n2.isLeaf = True
                        n2.nextNode = insert_place.nextNode#기존의 nextnode를 n2 nextnode로 설정
                        insert_place.nextNode = n2#지금 다음에는 n2가 와야됨
                    #다음 노드들 설정해 주어야 한다.
                    if((insert_place.parent != None)):#부모가 존재하면
                        insert_place.parent.subTrees.append(n2)#부모에 새로만든거2추가
                        insert_place.parent.keys.append(up_node_val)
                        insert_place.parent.values = []#부모니까 leaf가 아니고 values 존재 불가능
                        insert_place.parent.isLeaf=False
                        insert_place.parent.nextNode=None
                    elif(insert_place.parent == None):#처음 으로 해서 루트가 리프일 경우
                        new_root = Node()
                        new_root.keys.append(up_node_val)
                        new_root.subTrees = [insert_place, n2]
                        insert_place.parent = new_root
                        n2.parent = new_root
                        self.root = new_root

                    #작업이 끝났다면 부모 노드로 올라가서 검증하자.
                    insert_place = insert_place.parent
                    if(insert_place == None):
                        break
                    k = n2.keys[0]
            else:#찾은 부분이 꽉 차있지 않다면 값들을 추가한다.
                insert_place.keys.append(k)
                insert_place.values.append(k)

        pass
    
    def delete(self, k):

        pass
    
    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self):
        queue = []
        queue.append(self.root)
        while(len(queue)!=0):
            a=1
        pass
        
    def find_range(self, k_from, k_to):
        pass
        
    def find(self, k):
        if(self.root.isLeaf == True):
            print(self.root.keys)
            return self.root
        else:
            start = self.root
            pathes = []
            return_val = None
            while(1):
                if(start.isLeaf==True):#최종 리프 노드까지 오게 되면
                    pathes.append(start.keys)
                    return_val = start
                    break
                if(start.keys[0] > k):#제일 작은 key보다 작은은 값을 찾을 경우
                    pathes.append(start.keys)
                    start = start.subTrees[0]
                elif(start.keys[-1] <= k): #제일 큰 key보다 크거나 같은 값을 찾을 경우
                    pathes.append(start.keys)
                    start = start.subTrees[-1]
                else:#특정 key 보다 작거나 같거나 key+1인 것보다 큰 값 찾는 경우
                    for i in range(len(start.keys)-1):
                        if(start.keys[i]<=k and start.keys[i+1]>k):
                            pathes.append(start.keys)
                            start = start.subTrees[i+1]
                            break
            print(pathes)
            return return_val
        return None
        pass


def main():
    '''
    Input: test_bp.txt
    Output: result.txt
    '''
    sys.stdin = open("test_bp.txt",'r')
    sys.stdout = open("result.txt","w")
    myTree = None
    
    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue
        
        print(comm)
        
        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)
            
        elif params[0] == "EXIT":
            return
            
        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)
            
        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)            
            
        elif params[0] == "ROOT":            
            myTree.print_root()            
            
        elif params[0] == "PRINT":            
            myTree.print_tree()            
                  
        elif params[0] == "FIND":            
            k = int(params[1])
            myTree.find(k)
            
        elif params[0] == "RANGE":            
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)
        
        elif params[0] == "SEP":
            print("-------------------------")
    
if __name__ == "__main__":
    main()