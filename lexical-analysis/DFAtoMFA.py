from NFA import *
from NFAtoDFA import *

class DFAtoMFA: #DFA最小化
    def __init__(self,dfa):
        self.dfa = dfa
        # 存放节点
        self.nodes = []
        self.edges = []
        # 当前状态机所在的位置
        self.nowId = 0
        # 开始节点
        self.startId = 0
        self.buildMFA()

    #  从 node 经过 tag 转移能到达的所有状态的集合
    def getToNode(self,nodeId,tag):
        for i in self.dfa.edges:
            if(i.fromNodeId == nodeId and i.tag == tag):
                return i.toNodeIds
        return 100

    def buildMFA(self):
        # 如果只有一个节点，那它本身为MFA
        if len(self.dfa.nodes) <= 1:
            self.mfa = self.dfa
            return
        finalNoBackNodesOP = [] # 存储终态并且不会回退的节点的编号
        finalNoBackNodesSE = []
        finalNoBackNodesID = []
        finalNoBackNodesSTR = []

        finalBackNodesOP = [] #存储终态并且会回退的节点的编号
        finalBackNodesID = []
        finalBackNodesINT = []
        finalBackNodesFL = []

        noFinalNodes = []
        nodeIds = [] #存储所有节点的Id
        for i in self.dfa.nodes:
            nodeIds.append(i.id)
            if i.isFinal == 1 and i.isBackOff == 1 :
                if i.tag == 'OP':
                    finalBackNodesOP.append(i.id)
                if i.tag == 'IDNorKWorOP':
                    finalBackNodesID.append(i.id)
                if i.tag == 'INT':
                    finalBackNodesINT.append(i.id)
                if i.tag == 'FLOAT':
                    finalBackNodesFL.append(i.id)
                
            if i.isFinal == 1 and i.isBackOff == 0 :
                if i.tag == 'OP':
                    finalNoBackNodesOP.append(i.id)
                if i.tag == 'SE':
                    finalNoBackNodesSE.append(i.id)
                if i.tag == 'IDNorKWorOP':
                    finalNoBackNodesID.append(i.id)
                if i.tag == 'STR':
                    finalNoBackNodesSTR.append(i.id)
            
            if i.isFinal == 0:
                noFinalNodes.append(i.id)
        pos = dict(zip(nodeIds,range(len(nodeIds))))#pos 中存储每一个节点对应处于的集合编号  一直处于不断地变化中
        pos[100] = 9

        set1 = set(finalBackNodesOP)
        set2 = set(finalBackNodesID)
        set3 = set(finalBackNodesINT)
        set4 = set(finalBackNodesFL)
        
        set5 = set(finalNoBackNodesID)
        set6 = set(finalNoBackNodesOP)
        set7 = set(finalNoBackNodesSE)
        set8 = set(finalNoBackNodesSTR)

        set9 = set(noFinalNodes)

        set1 = list(set1)
        set2 = list(set2)
        set3 = list(set3)
        set4 = list(set4)
        set5 = list(set5)
        set6 = list(set6)
        set7 = list(set7)
        set8 = list(set8)
        set9 = list(set9)

        for i in set1:
            pos[i] = 0
        for i in set2:
            pos[i] = 1
        for i in set3:
            pos[i] = 2
        for i in set4:
            pos[i] = 3
        for i in set5:
            pos[i] = 4
        for i in set6:
            pos[i] = 5
        for i in set7:
            pos[i] = 6
        for i in set8:
            pos[i] = 7
        for i in set9:
            pos[i] = 8
        
        allsets = [set1,set2,set3,set4,set5,set6,set7,set8,set9]
        counts = 10
        flag = True
        while flag:
            flag = False
            for char in tags:
                for sub_set in allsets:
                    dic = dict() # 存储节点和新对应的编号
                    lists = []
                    # 找出某个set中通过某个tag能够到达的所有节点
                    for oneNode in sub_set:
                        num = self.getToNode(oneNode,char)
                        num = pos[num] #获取转移状态对应的集合编号
                        # print(num)

                        if num not in  dic.keys():   #如果没有建立 该状态对应的集合编号  的字典关系  新建
                            dic[num] =counts
                            counts+=1
                        lists.append(dic[num])
                    if len(lists) == 0:
                        continue
                    # print(lists)
                        
                    if len(dic) >1: #证明该集合中状态转移 不是转移到同一处 拆分元素 跳出循环
                        flag = True
                        tmp_set=dict()   #新编号与新数值相对应  加入不同的新list
                        for i1 in range(len(sub_set)):
                            if lists[i1] not  in tmp_set.keys():
                                tmp_set[lists[i1]]=list()
                            tmp_set[ lists[i1] ].append(sub_set[i1])
                            pos[sub_set[i1]] = lists[i1] #更新pos  更新状态 所在的集合的编号
                            
                        allsets.remove(sub_set) #将旧的list移除
                        for i1 in tmp_set.values(): #将新的list 加入
                            allsets.append(i1)
                        break

                if flag == True:
                    break


        for i in range(len(allsets)):    #计算出每个数值对应的新的数值
            for j in allsets[i]:
                pos[j] =i+1

        # print(pos)
        # print(set1)
        pos.pop(100)
        # print(pos)
        # for i in self.dfa.nodes:
        #     print('id: ' + str(i.id) + 'isBackOff: ' + str(i.isBackOff))



        self.getnewDfa(pos,self.dfa)
            

    # 添加节点
    def add_node(self, id, is_final, is_back_off, tag):
        new_node = Node(id, is_final, is_back_off, tag)
        self.nodes.append(new_node)

    # 添加边
    def add_edges(self, from_node_id, to_node_id: int, tag):
        new_edge = DFAEdge(from_node_id, to_node_id, tag)
        self.edges.append(new_edge)

    # 将指针指向开始节点
    def get_start(self):
        self.nowId = self.startId
    
    # 获得下一个ID
    def next_id(self, tag):
        for edge in self.edges:
            if edge.fromNodeId == self.nowId and re.match(edge.tag, tag):
                # 并将nowId指向新的位置
                self.nowId = edge.toNodeIds
                # 说明成功找到下一个节点
                return True
        return False
    
    def is_final(self, id):
        # 因为是按照顺序添加的节点,所以nodes的下标对应着一样的id
        for i in self.nodes:
            if i.id == id:
                return i.isFinal

    # 是否需要退出一个字符
    def is_back_off(self, id):
        for i in self.nodes:
            if i.id == id:
                return i.isBackOff

    # 获得tag
    def get_tag(self, id):
        # 可以根据tag返回需要的内容
        for i in self.nodes:
            if i.id == id:
                return i.tag
    def get_token_type(self, token, node_tag):
        # KW, OP, SE, IDN, INT, FLOAT, STR

        # OP, SE, INT, FLOAT,STR都可以直接判断
        if node_tag == "OP" or node_tag == "SE" or node_tag == "INT" or node_tag == "FLOAT" or node_tag == "STR":
            return node_tag
        elif node_tag == "IDNorKWorOP":
            keywords = TYPE_TO_CONTENT_DICT_KW.keys()
            ops = TYPE_TO_CONTENT_DICT_OP.keys()
            if token in keywords:
                return "KW"
            elif token in ops:
                return "OP"
            else:
                return "IDN"

    # 判断编号
    def get_token_num(self, token, token_type):
        if token_type == "IDN" or token_type == "INT" or token_type == "FLOAT" or token_type == "STR":
            return token
        elif token_type == "KW":
            return TYPE_TO_CONTENT_DICT_KW[token]
        elif token_type == "OP":
            return TYPE_TO_CONTENT_DICT_OP[token]
        elif token_type == "SE":
            return TYPE_TO_CONTENT_DICT_SE[token]
    
    def getnewDfa(self,dicts,dfa):
        self.startId = dicts[dfa.startId]
        # print(self.startId)
        
        addSets = [] # 存储加入新的DFA的节点
        # 在新的DFA加入节点
        for key,value in dicts.items():
            if value not in addSets:
                addSets.append(value)
                self.add_node(value,dfa.nodes[key].isFinal,dfa.nodes[key].isBackOff,dfa.nodes[key].tag)
        addEdges = []
        for edge in dfa.edges:
            tup = (dicts[edge.fromNodeId],dicts[edge.toNodeIds],edge.tag)
            if tup not in addEdges:
                self.add_edges(dicts[edge.fromNodeId],dicts[edge.toNodeIds],edge.tag)
                addEdges.append(tup)
        # print('addSets: ' + str(addSets))
