from logging import root
import sys

from requests import delete


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
                        n2.keys = n2.keys+(insert_place.keys[(len(insert_place.keys))//2:])
                        up_node_val = insert_place.keys[(len(insert_place.keys))//2]
                        n2.keys.sort()
                        insert_place.keys = insert_place.keys[:(len(insert_place.keys))//2]
                        n2.parent=insert_place.parent
                    else:
                        n2 = Node()
                        #n2.keys.append(insert_place.keys[(len(insert_place.keys)+1)//2:])
                        n2.keys = n2.keys+(insert_place.keys[(len(insert_place.keys))//2+1:])
                        up_node_val = insert_place.keys[(len(insert_place.keys))//2]
                        n2.keys.sort()
                        insert_place.keys = insert_place.keys[:(len(insert_place.keys))//2]
                        n2.subTrees = n2.subTrees+insert_place.subTrees[(len(insert_place.subTrees))//2+1:]
                        for i in n2.subTrees:
                            i.parent = n2
                        insert_place.subTrees = insert_place.subTrees[:(len(insert_place.subTrees))//2+1]
                        for i in insert_place.subTrees:
                            i.parent = insert_place
                        n2.parent=insert_place.parent
                    #leaf node면 values에도 추가해 주어야 한다. 또한 leaf 설정도 해 주어야 한다.
                    if(insert_place.isLeaf == True):#작업하는 영역이 자식 노드일 경우에는 values값도 추가해 주어야 한다.
                        insert_place.values.append(k)
                        insert_place.values.sort()
                        n2.values = n2.values+(insert_place.values[(len(insert_place.values))//2:])
                        insert_place.values = insert_place.values[:(len(insert_place.values))//2]
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
                insert_place.keys.sort()
                insert_place.values.sort()
        pass
    
    def delete(self, k):
        #return
        delete_place = self.find_node(k)
        delete_place.values.remove(k)
        delete_place.keys.remove(k)
        renew_place = delete_place.parent
        while(1):
            if(renew_place==None):
                break
            if(k in renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                #place = renew_place.keys.index(k)
                #renew_place.keys[k] = renew_place.subTrees[place+1]
                for i in range(len(renew_place.subTrees)):
                    renew_place.keys[i] = renew_place.subTrees[i][0]
            renew_place = renew_place.parent
        #삭제후 절반이상 차있다면 종료한다. 절반 이하라면
        #삭제 후 절반 이하라면
        #근데 그냥 삭제만 해준 경우 업데이트를 해주긴 해야되는데 이건 어찌할까....그냥
        if(self.root != delete_place):
            if(len(delete_place.keys) < (self.order)//2):#절반 이하라고 해서 일단 <=사용해야되는데 ppt엔 미만일때 발동
                del_node_index = delete_place.parent.subTrees.index(delete_place)
                if((0<del_node_index) and (del_node_index<len(delete_place.parent.subTrees)-1)):
                    #양옆에 존재하는 경우 양옆을 살펴봐서 절반 이하인 친구를 찾는다.
                    #일단 왼쪽 노드를 먼저 보고 오른쪽 노드를 보자
                    if(len(delete_place.subTrees[del_node_index-1]) > (self.order-1)//2):#절반 초과일 경우
                        #재분배하고 엔트리를 빌려온다
                        a=1
                    elif(len(delete_place.subTrees[del_node_index-1]) <= (self.order-1)//2):
                        #정확히 절반일 경우, 삭제한거랑 이걸 병합한다.
                        delete_place.subTrees[del_node_index-1].keys = delete_place.subTrees[del_node_index-1].keys + delete_place.keys
                        if(delete_place.isLeaf == True):
                            delete_place.subTrees[del_node_index-1].values = delete_place.subTrees[del_node_index-1].values + delete_place.values
                        delete_place.subTrees[del_node_index-1].nextNode = delete_place.nextNode
                    elif(len(delete_place.subTrees[del_node_index+1]) > (self.order-1)//2):#절반 초과일 경우
                        a=1
                    elif(len(delete_place.subTrees[del_node_index+1]) <= (self.order-1)//2):
                        #정확히 절반일 경우, 삭제한거랑 이걸 병합한다.
                        delete_place.subTrees[del_node_index+1].keys = delete_place.subTrees[del_node_index+1].keys + delete_place.keys
                        if(delete_place.isLeaf == True):
                            delete_place.subTrees[del_node_index+1].values = delete_place.subTrees[del_node_index+1].values + delete_place.values
                        delete_place.subTrees[del_node_index+1].nextNode = delete_place.nextNode
                elif(del_node_index == 0):
                    #오른쪽 노드껏들로만 처리
                    a=1 
                elif(del_node_index == len(delete_place.parent.subTrees)-1):
                    #왼쪽 노드껏들로만 처리
                    a=1
        pass
    
    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass
    
    def print_tree(self):
        print_result = []
        queue = []
        queue.append(self.root)#맨 처음 노드 추가
        while(len(queue)!=0):
            result_append_temp_list = []
            temp = []#지금들어있는거 다 뺴자
            while(len(queue)!=0):
                temp.append(queue[0])
                del queue[0]
            for i in temp:
                result_append_temp_list.append(str(i.keys))
            for i in temp:#큐에서 뺀 노드들
                for j in i.subTrees:#그 노드들의 서브 트리를 넣어주자.
                    queue.append(j)
            #print(','.join(result_append_temp_list))
            print_result.append(','.join(result_append_temp_list))
        print('-'.join(print_result))
        pass
        
    def find_range(self, k_from, k_to):
        pathes = []
        target_node = self.find_node(k_from)
        break_state=False
        while(1):
            for i in target_node.keys:
                if(i>=k_from and i<=k_to):
                    pathes.append(i)
                    if(i == k_to):
                        break_state = True
                        break
            if(break_state):
                break
            #print(target_node.keys[-1],k_to)
            target_node = target_node.nextNode
            if(target_node == None):
                break
        print(pathes)
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
            if((k not in return_val.keys)):
                return_val = None
            if(return_val == None):
                print('NONE')
            else:
                print(*pathes,sep='-')
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