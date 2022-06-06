from logging import root
import sys
from tracemalloc import start

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
                #print(start.keys)
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
                        if(start.keys[i]<=k and k<start.keys[i+1]):
                            pathes.append(start.keys)
                            start = start.subTrees[i+1]
                            break
            #if(k not in return_val.keys):
            #    return None
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
                        if(self.order%2 == 0):
                            n2.subTrees = n2.subTrees+insert_place.subTrees[(len(insert_place.subTrees))//2+1:]
                        else:
                            n2.subTrees = n2.subTrees+insert_place.subTrees[(len(insert_place.subTrees))//2:]
                        for i in n2.subTrees:
                            i.parent = n2
                        if(self.order%2==0):
                            insert_place.subTrees = insert_place.subTrees[:(len(insert_place.subTrees))//2+1]
                        else:
                            insert_place.subTrees = insert_place.subTrees[:(len(insert_place.subTrees))//2]
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
        get_prev_node = None
        for i in reversed(range(1,k)):
            get_prev_node = self.find_node(i)
            if(get_prev_node!=None):
                break
        delete_place = self.find_node(k)
        if(delete_place == self.root):
            delete_place.keys.remove(k)
            delete_place.values.remove(k)
            return
        if(k not in delete_place.keys):
            return
        delete_place.values.remove(k)
        delete_place.keys.remove(k)
        renew_place = delete_place.parent
        next_sib_node_first_key = None
        cur_node_idx = delete_place.parent.subTrees.index(delete_place)
        if(cur_node_idx < len(delete_place.parent.subTrees)-1):
            next_sib_node_first_key = delete_place.parent.subTrees[cur_node_idx+1].keys[0]
        while(1):
            if(renew_place==None):
                break
            if(k in renew_place.keys):
                renew_place.keys.remove(k)
                if((next_sib_node_first_key!= None) and (next_sib_node_first_key not in renew_place.keys)):
                    renew_place.keys.append(next_sib_node_first_key)
                    renew_place.keys.sort()
            renew_place=renew_place.parent
        #삭제후 절반이상 차있다면 종료한다. 절반 이하라면
        #삭제 후 절반 이하라면
        #근데 그냥 삭제만 해준 경우 업데이트를 해주긴 해야되는데 이건 어찌할까....그냥
        if(self.root != delete_place):
            if(len(delete_place.keys) < (self.order)//2):#절반 이하라고 해서 일단 <=사용해야되는데 ppt엔 미만일때 발동
                del_node_index = delete_place.parent.subTrees.index(delete_place)#왼쪽이 없는경우 오른쪽이 없는경우
                if((del_node_index != 0) and (delete_place.nextNode!=None)):#좌우가 없는경우가 아니면
                    second_case = (len(delete_place.parent.subTrees[del_node_index-1].keys)>(self.order)//2)
                    if(second_case):
                    #steal key from left node
                        #왼쪽 노드의 제일 마지막 값을 옮겨야 한다.
                        left_back = delete_place.parent.subTrees[del_node_index-1].keys[-1]
                        left_back_val = delete_place.parent.subTrees[del_node_index-1].values[-1]
                        delete_place.parent.subTrees[del_node_index-1].keys.remove(delete_place.parent.subTrees[del_node_index-1].keys[-1])
                        delete_place.keys.append(left_back)
                        delete_place.keys.sort()
                        if(delete_place.parent.subTrees[del_node_index-1].isLeaf):
                            delete_place.parent.subTrees[del_node_index-1].values.remove(delete_place.parent.subTrees[del_node_index-1].values[-1])
                            delete_place.values.append(left_back_val)
                            delete_place.values.sort()
                    elif(len(delete_place.nextNode.keys)>(self.order)//2):#오른쪽에서 값 가져온다.
                        right_first = delete_place.nextNode.keys[0]
                        right_first_val = delete_place.nextNode.values[0]
                        #삭제된 노드에 추가해주기
                        delete_place.keys.append(right_first)
                        delete_place.nextNode.keys.remove(right_first)
                        delete_place.keys.sort()
                        if(delete_place.isLeaf):
                            delete_place.values.append(right_first_val)
                            delete_place.nextNode.values.remove(right_first_val)
                            delete_place.values.sort()
                        temp_renew_place = delete_place.nextNode.parent
                        temp_k = right_first
                        while(1):
                            if(temp_renew_place==None):
                                break
                            if(temp_k in temp_renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                                #place = renew_place.keys.index(k)
                                #renew_place.keys[k] = renew_place.subTrees[place+1]
                                find_upder_temp_k = None
                                temp_k_store = temp_k+1
                                while(find_upder_temp_k == None):
                                    find_upder_temp_k = self.find_node(temp_k_store)
                                    temp_k_store+=1
                                for i in range(1,len(temp_renew_place.subTrees)):
                                    if(len(temp_renew_place.subTrees[i].keys)==0):
                                        continue
                                    #temp_renew_place.keys[i-1] = temp_renew_place.subTrees[i].keys[0]
                                    temp_renew_place.keys[i-1] = delete_place.nextNode.keys[0]
                                #if(temp_k in temp_renew_place.keys):
                                #    temp_renew_place.keys.remove(temp_k)
                            temp_renew_place = temp_renew_place.parent
                        #if(delete_place!= self.root):
                        #    temp_balancing_place = delete_place.parent
                        #    while(1):
                        #        if(temp_balancing_place == None):
                        #            break
                        #        temp_balancing_place = temp_balancing_place.parent
                    else:#머지 윗 레프트 노드
                        delete_place.parent.subTrees[del_node_index-1].keys += delete_place.keys
                        #delete_place.parent.subTrees[del_node_index-1].keys.sort()
                        if(delete_place.isLeaf):
                            delete_place.parent.subTrees[del_node_index-1].values += delete_place.values
                            #delete_place.parent.subTrees[del_node_index-1].values.sort()
                        temp_renew_place = delete_place.parent
                        if(len(delete_place.keys)==0):
                            temp_k=k
                        else:
                            temp_k = delete_place.keys[0]
                        delete_place.parent.subTrees[del_node_index-1].nextNode = delete_place.nextNode
                        delete_place.parent.subTrees.remove(delete_place)
                        while(1):
                            if(temp_renew_place==None):
                                break
                            if(temp_k in temp_renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                                #place = renew_place.keys.index(k)
                                #renew_place.keys[k] = renew_place.subTrees[place+1]
                                find_upder_temp_k = None
                                temp_k_store = temp_k+1
                                while(find_upder_temp_k == None):
                                    find_upder_temp_k = self.find_node(temp_k_store)
                                    temp_k_store+=1
                                for i in range(1,len(temp_renew_place.subTrees)):
                                    if(len(temp_renew_place.subTrees[i].keys)==0):
                                        continue
                                    #temp_renew_place.keys[i-1] = temp_renew_place.subTrees[i].keys[0]
                                    temp_renew_place.keys[i-1] = delete_place.nextNode.keys[0]
                                #if(temp_k in temp_renew_place.keys):
                                #    temp_renew_place.keys.remove(temp_k)
                            temp_renew_place = temp_renew_place.parent
                        start_position = delete_place
                        while(1):
                            if(self.root==start_position):
                                break
                            if(start_position.parent==None):
                                break
                            if(start_position.isLeaf):#리프 단말일떄
                                #밸런싱하려면 항상 subtree개수가 key개수+1해야한다.
                                if(len(start_position.parent.subTrees)<=len(start_position.parent.keys)):#밸런싱하지 않다.
                                    #index_place = start_position.parent.keys.index(start_position.keys[0])
                                    start_position.parent.keys.remove(start_position.parent.subTrees[0].keys[0])
                                start_position=start_position.parent
                            else:
                                if(len(start_position.keys)<(self.order//2)):#언벨런스 조건 검사
                                    parent_node = start_position.parent
                                    delete_place_index = parent_node.subTrees.index(start_position)
                                    #왼쪽에 무엇인가가 있고 왼쪽에서 빌릴 수 있을 때
                                    need_merge = True
                                    if((0<delete_place_index) and (len(parent_node.subTrees[delete_place_index-1].keys)>self.order//2)):
                                            #둘다 있거나 왼쪽이 있으면 왼쪽에서 빌린다.
                                            left_node_back = parent_node.subTrees[delete_place_index-1]
                                            par_node_key = parent_node.keys[delete_place_index-1]
                                            start_position.keys.append(par_node_key)#부모키 아무것도없는데로
                                            start_position.keys.sort()
                                            start_position.subTrees.insert(0, left_node_back.subTrees[-1])#아무것도없는데에 포인터도 넣어줌
                                            for m in start_position.subTrees:
                                                m.parent = start_position
                                            parent_node.keys.remove(par_node_key)#부모키에 옮긴 대상이 된 키 삭제
                                            parent_node.keys.append(left_node_back.keys[-1])#부모키에 새 키 입력
                                            parent_node.keys.sort()
                                            left_node_back.keys.remove(left_node_back.keys[-1])#왼쪽노드 key삭제
                                            #parent_node.subTrees.remove(left_node_back)#왼쪽노드 서브트리 삭제
                                            left_node_back.subTrees.remove(left_node_back.subTrees[-1])#왼쪽노드 서브트리 삭제
                                            start_position = start_position.parent
                                            need_merge=False
                                    #오른쪽바로우되는지검사
                                    #왼쪽에무엇인가 없고 왼쪽에서 빌릴 수 있을 때 (논리적으로 불가능)
                                    #왼쪽에 무엇인가 있고 왼쪽에서 빌릴 수 없을 떄 (이걸 봐야하긴함)(오른쪽에서 빌려야 함.)
                                    #왼쪽에 무엇인가 없고 왼쪽에서 빌릴 수 없을때 위 세가지 케이스가 다 들어온다.
                                    else:#왼쪽에서 빌릴 수 없거나(맨 왼쪽이거나) 왼쪽은있는데 빌릴수 없을 경우
                                        if((delete_place_index<len(parent_node.subTrees)-1)):#오른쪽에 무엇인가가 존재할떄
                                            if(len(parent_node.subTrees[delete_place_index+1].keys)>self.order//2):#오른쪽에서 빌릴 수 있을때
                                                right_node = parent_node.subTrees[delete_place_index+1]
                                                par_node_key = parent_node.keys[delete_place_index]
                                                start_position.keys.append(par_node_key)
                                                start_position.keys.sort()
                                                start_position.subTrees.append(right_node.subTrees[0])
                                                for m in start_position.subTrees:
                                                    m.parent = start_position
                                                parent_node.keys.remove(par_node_key)
                                                parent_node.keys.append(right_node.keys[0])
                                                parent_node.keys.sort()
                                                right_node.keys.remove(right_node.keys[0])
                                                right_node.subTrees.remove(right_node.subTrees[0])
                                                start_position = start_position.parent
                                                need_merge=False
                                    if(need_merge):
                                        #머지 코드 작성
                                        #왼쪽과 머지할수있는지 오른쪽과 머지할수 있는지 보고 머지한다.
                                        if((0<delete_place_index)):#왼쪽에 노드가 있으면 왼쪽 검사하자.
                                            left_node = start_position.parent.subTrees[delete_place_index-1]
                                            parent_node = start_position.parent
                                            if(len(start_position.keys)==0):
                                                start_position.keys.append(parent_node.keys[delete_place_index-1])
                                                parent_node.keys.remove(parent_node.keys[delete_place_index-1])
                                            left_node.keys += start_position.keys#키 옮겨주고
                                            left_node.keys.sort()
                                            left_node.subTrees += start_position.subTrees#서브트리들 옮겨주고
                                            for i in left_node.subTrees:#서브트리들 parent도 최신화해줘야됨.
                                                i.parent = left_node
                                            parent_node.subTrees.remove(start_position)
                                            #if(parent_node.keys[delete_place_index-1] in start_position.keys):
                                            #    parent_node.keys[delete_place_index-1] = left_node
                                        else:
                                            right_node = start_position.parent.subTrees[delete_place_index+1]
                                            parent_node = start_position.parent
                                            if(len(start_position.keys)==0):
                                                start_position.keys.append(parent_node.keys[0])
                                                parent_node.keys.remove(parent_node.keys[0])
                                            right_node.keys += start_position.keys#키 옮겨주고
                                            right_node.keys.sort()
                                            right_node.subTrees = start_position.subTrees+right_node.subTrees#서브트리들 옮겨주고
                                            for i in right_node.subTrees:#서브트리들 parent도 최신화해줘야됨.
                                                i.parent = right_node
                                            parent_node.subTrees.remove(start_position)
                                    start_position = start_position.parent
                                else:
                                    start_position = start_position.parent
                elif(del_node_index != 0):#왼쪽이 없는경우가 아니면
                    if(len(delete_place.nextNode.keys)>(self.order)//2):
                        right_first = delete_place.nextNode.keys[0]
                        right_first_val = delete_place.nextNode.values[0]
                        #삭제된 노드에 추가해주기
                        delete_place.keys.append(right_first)
                        delete_place.nextNode.keys.remove(right_first)
                        delete_place.keys.sort()
                        if(delete_place.isLeaf):
                            delete_place.values.append(right_first_val)
                            delete_place.nextNode.values.remove(right_first_val)
                            delete_place.values.sort()
                        temp_renew_place = delete_place.nextNode.parent
                        temp_k = right_first
                        while(1):
                            if(temp_renew_place==None):
                                break
                            if(temp_k in temp_renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                                #place = renew_place.keys.index(k)
                                #renew_place.keys[k] = renew_place.subTrees[place+1]
                                find_upder_temp_k = None
                                temp_k_store = temp_k+1
                                while(find_upder_temp_k == None):
                                    find_upder_temp_k = self.find_node(temp_k_store)
                                    temp_k_store+=1
                                for i in range(1,len(temp_renew_place.subTrees)):
                                    if(len(temp_renew_place.subTrees[i].keys)==0):
                                        continue
                                    #temp_renew_place.keys[i-1] = temp_renew_place.subTrees[i].keys[0]
                                    temp_renew_place.keys[i-1] = delete_place.nextNode.keys[0]
                                #if(temp_k in temp_renew_place.keys):
                                #    temp_renew_place.keys.remove(temp_k)
                            temp_renew_place = temp_renew_place.parent
                    else:#머지 윗 레프트 노드
                        delete_place.parent.subTrees[del_node_index-1].keys += delete_place.keys
                        if(delete_place.isLeaf):
                            delete_place.parent.subTrees[del_node_index-1].values += delete_place.values
                        temp_renew_place = delete_place.parent
                        if(len(delete_place.keys)==0):
                            temp_k=k
                        else:
                            temp_k = delete_place.keys[0]
                        delete_place.parent.subTrees[del_node_index-1].nextNode = delete_place.nextNode
                        delete_place.parent.subTrees.remove(delete_place)
                        while(1):
                            if(temp_renew_place==None):
                                break
                            if(temp_k in temp_renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                                #place = renew_place.keys.index(k)
                                #renew_place.keys[k] = renew_place.subTrees[place+1]
                                find_upder_temp_k = None
                                temp_k_store = temp_k+1
                                while(find_upder_temp_k == None):
                                    find_upder_temp_k = self.find_node(temp_k_store)
                                    temp_k_store+=1
                                for i in range(1,len(temp_renew_place.subTrees)):
                                    if(len(temp_renew_place.subTrees[i].keys)==0):
                                        continue
                                    #temp_renew_place.keys[i-1] = temp_renew_place.subTrees[i].keys[0]
                                    temp_renew_place.keys[i-1] = delete_place.nextNode.keys[0]
                                #if(temp_k in temp_renew_place.keys):
                                #    temp_renew_place.keys.remove(temp_k)
                            temp_renew_place = temp_renew_place.parent
                elif(delete_place.nextNode==None):#오른쪽이 없는경우
                    second_case = (len(delete_place.parent.subTrees[del_node_index-1].keys)>(self.order)//2)
                    if(second_case):
                    #steal key from left node
                        #왼쪽 노드의 제일 마지막 값을 옮겨야 한다.
                        left_back = delete_place.parent.subTrees[del_node_index-1].keys[-1]
                        left_back_val = delete_place.parent.subTrees[del_node_index-1].values[-1]
                        delete_place.parent.subTrees[del_node_index-1].keys.remove(delete_place.parent.subTrees[del_node_index-1].keys[-1])
                        delete_place.keys.append(left_back)
                        delete_place.keys.sort()
                        if(delete_place.parent.subTrees[del_node_index-1].isLeaf):
                            delete_place.parent.subTrees[del_node_index-1].values.remove(delete_place.parent.subTrees[del_node_index-1].values[-1])
                            delete_place.values.append(left_back_val)
                            delete_place.values.sort()
                    else:#머지 윗 레프트 노드
                        delete_place.parent.subTrees[del_node_index-1].keys += delete_place.keys
                        if(delete_place.isLeaf):
                            delete_place.parent.subTrees[del_node_index-1].values += delete_place.values
                        temp_renew_place = delete_place.parent
                        if(len(delete_place.keys)==0):
                            temp_k=k
                        else:
                            temp_k = delete_place.keys[0]
                        delete_place.parent.subTrees[del_node_index-1].nextNode = delete_place.nextNode
                        delete_place.parent.subTrees.remove(delete_place)
                        while(1):
                            if(temp_renew_place==None):
                                break
                            if(temp_k in temp_renew_place.keys):#삭제한 요소가 부모 노드에 존재한다면 부모 노드에 최신화 시켜줘야댐
                                #place = renew_place.keys.index(k)
                                #renew_place.keys[k] = renew_place.subTrees[place+1]
                                find_upder_temp_k = None
                                temp_k_store = temp_k+1
                                while(find_upder_temp_k == None):
                                    find_upder_temp_k = self.find_node(temp_k_store)
                                    temp_k_store+=1
                                for i in range(1,len(temp_renew_place.subTrees)):
                                    if(len(temp_renew_place.subTrees[i].keys)==0):
                                        continue
                                    #temp_renew_place.keys[i-1] = temp_renew_place.subTrees[i].keys[0]
                                    temp_renew_place.keys[i-1] = delete_place.nextNode.keys[0]
                                #if(temp_k in temp_renew_place.keys):
                                #    temp_renew_place.keys.remove(temp_k)
                            temp_renew_place = temp_renew_place.parent
                else:#머지 or 바로우 윗 라이트 노드
                    temp_k2 = delete_place.nextNode.keys[0]
                    delete_place.nextNode.keys += delete_place.keys#nextnode에 키 넣어버리고
                    delete_place.nextNode.keys.sort()
                    if(delete_place.isLeaf):#value도 넣는다. 
                        delete_place.nextNode.values += delete_place.values
                        delete_place.nextNode.values.sort()
                    #delete_place.parent.subTrees[del_node_index-1].nextNode = delete_place.nextNode#노드 연결
                    if(get_prev_node!= None):
                        get_prev_node.nextNode = delete_place.nextNode
                    #삭제구역 밸런싱
                    temp_renew_place = delete_place.parent
                    if(len(delete_place.keys)==0):
                        temp_k=k
                    else:
                        temp_k = delete_place.keys[0]
                    #머지구역 벨런싱
                    temp_renew_place2 = delete_place.nextNode.parent
                    #temp_k2 = delete_place.nextNode.keys[0]
                    delete_place.parent.subTrees.remove(delete_place)
                    #밸런싱 코드
                    #self.print_tree()
                    start_position = delete_place
                    while(1):
                        if(self.root==start_position):
                            break
                        if(start_position.parent==None):
                            break
                        if(start_position.isLeaf):#리프 단말일떄
                            #밸런싱하려면 항상 subtree개수가 key개수+1해야한다.
                            if(len(start_position.parent.subTrees)<=len(start_position.parent.keys)):#밸런싱하지 않다.
                                #index_place = start_position.parent.keys.index(start_position.keys[0])
                                start_position.parent.keys.remove(start_position.parent.subTrees[0].keys[0])
                            start_position=start_position.parent
                        else:
                            if(len(start_position.keys)<(self.order//2)):#언벨런스 조건 검사
                                parent_node = start_position.parent
                                delete_place_index = parent_node.subTrees.index(start_position)
                                #왼쪽에 무엇인가가 있고 왼쪽에서 빌릴 수 있을 때
                                need_merge = True
                                if((0<delete_place_index) and (len(parent_node.subTrees[delete_place_index-1].keys)>self.order//2)):
                                        #둘다 있거나 왼쪽이 있으면 왼쪽에서 빌린다.
                                        left_node_back = parent_node.subTrees[delete_place_index-1]
                                        par_node_key = parent_node.keys[delete_place_index-1]
                                        start_position.keys.append(par_node_key)#부모키 아무것도없는데로
                                        start_position.keys.sort()
                                        start_position.subTrees.insert(0, left_node_back.subTrees[-1])#아무것도없는데에 포인터도 넣어줌
                                        for m in start_position.subTrees:
                                            m.parent = start_position
                                        parent_node.keys.remove(par_node_key)#부모키에 옮긴 대상이 된 키 삭제
                                        parent_node.keys.append(left_node_back.keys[-1])#부모키에 새 키 입력
                                        parent_node.keys.sort()
                                        left_node_back.keys.remove(left_node_back.keys[-1])#왼쪽노드 key삭제
                                        #parent_node.subTrees.remove(left_node_back)#왼쪽노드 서브트리 삭제
                                        left_node_back.subTrees.remove(left_node_back.subTrees[-1])#왼쪽노드 서브트리 삭제
                                        start_position = start_position.parent
                                        need_merge=False
                                #오른쪽바로우되는지검사
                                #왼쪽에무엇인가 없고 왼쪽에서 빌릴 수 있을 때 (논리적으로 불가능)
                                #왼쪽에 무엇인가 있고 왼쪽에서 빌릴 수 없을 떄 (이걸 봐야하긴함)(오른쪽에서 빌려야 함.)
                                #왼쪽에 무엇인가 없고 왼쪽에서 빌릴 수 없을때 위 세가지 케이스가 다 들어온다.
                                else:#왼쪽에서 빌릴 수 없거나(맨 왼쪽이거나) 왼쪽은있는데 빌릴수 없을 경우
                                    if((delete_place_index<len(parent_node.subTrees)-1)):#오른쪽에 무엇인가가 존재할떄
                                        if(len(parent_node.subTrees[delete_place_index+1].keys)>self.order//2):#오른쪽에서 빌릴 수 있을때
                                            right_node = parent_node.subTrees[delete_place_index+1]
                                            par_node_key = parent_node.keys[delete_place_index]
                                            start_position.keys.append(par_node_key)
                                            start_position.keys.sort()
                                            start_position.subTrees.append(right_node.subTrees[0])
                                            for m in start_position.subTrees:
                                                m.parent = start_position
                                            parent_node.keys.remove(par_node_key)
                                            parent_node.keys.append(right_node.keys[0])
                                            parent_node.keys.sort()
                                            right_node.keys.remove(right_node.keys[0])
                                            right_node.subTrees.remove(right_node.subTrees[0])
                                            start_position = start_position.parent
                                            need_merge=False
                                if(need_merge):
                                    #머지 코드 작성
                                    #왼쪽과 머지할수있는지 오른쪽과 머지할수 있는지 보고 머지한다.
                                    if((0<delete_place_index)):#왼쪽에 노드가 있으면 왼쪽 검사하자.
                                        left_node = start_position.parent.subTrees[delete_place_index-1]
                                        parent_node = start_position.parent
                                        if(len(start_position.keys)==0):
                                            start_position.keys.append(parent_node.keys[delete_place_index-1])
                                            parent_node.keys.remove(parent_node.keys[delete_place_index-1])
                                        left_node.keys += start_position.keys#키 옮겨주고
                                        left_node.keys.sort()
                                        left_node.subTrees += start_position.subTrees#서브트리들 옮겨주고
                                        for i in left_node.subTrees:#서브트리들 parent도 최신화해줘야됨.
                                            i.parent = left_node
                                        parent_node.subTrees.remove(start_position)
                                        #if(parent_node.keys[delete_place_index-1] in start_position.keys):
                                        #    parent_node.keys[delete_place_index-1] = left_node
                                    else:
                                        right_node = start_position.parent.subTrees[delete_place_index+1]
                                        parent_node = start_position.parent
                                        if(len(start_position.keys)==0):
                                            start_position.keys.append(parent_node.keys[0])
                                            parent_node.keys.remove(parent_node.keys[0])
                                        right_node.keys += start_position.keys#키 옮겨주고
                                        right_node.keys.sort()
                                        right_node.subTrees = start_position.subTrees+right_node.subTrees#서브트리들 옮겨주고
                                        for i in right_node.subTrees:#서브트리들 parent도 최신화해줘야됨.
                                            i.parent = right_node
                                        parent_node.subTrees.remove(start_position)

                                start_position = start_position.parent
                            else:
                                start_position = start_position.parent
        if(len(self.root.keys)==0 and self.root.isLeaf!=True):
            self.root = self.root.subTrees[0]
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
            for i in temp:#큐에서 뺀 노드들
                if(i.isLeaf):
                    return
                real_print = []
                for j in i.subTrees:#그 노드들의 서브 트리를 넣어주자.
                    real_print.append(j.keys)
                    queue.append(j)
                print(str(i.keys)+'-'+','.join(map(str,real_print)))
        #while(len(queue)!=0):
        #    result_append_temp_list = []
        #    temp = []#지금들어있는거 다 뺴자
        #    while(len(queue)!=0):
        #        temp.append(queue[0])
        #        del queue[0]
        #    for i in temp:
        #        result_append_temp_list.append(str(i.keys))
        #    for i in temp:#큐에서 뺀 노드들
        #        for j in i.subTrees:#그 노드들의 서브 트리를 넣어주자.
        #            queue.append(j)
        #    #print(','.join(result_append_temp_list))
        #    print_result.append(','.join(result_append_temp_list))
        #print('-'.join(print_result))
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
                #return return_val
            else:
                print(*pathes,sep='-')
            #if(k not in return_val.keys):
            #    print('NONE')
            #    return None
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