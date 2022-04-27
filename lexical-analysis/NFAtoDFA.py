from NFA import *
import re


class DFAEdge:
    def __init__(self, from_node_id, to_node_id: int, tag):
        # from 节点
        self.fromNodeId = from_node_id
        # to 节点 同一个tag可以去到的所有节点集合
        self.toNodeIds = to_node_id
        # 转化需要的信息
        self.tag = tag


# 初始化使用一个NFA，然后使用确定化和最小化算法
class DFA:
    def __init__(self):
        # 存放节点
        self.nodes = []
        self.edges = []
        # 当前状态机所在的位置
        self.nowId = 0
        # 开始节点
        self.startId = 0

        # 确定化将NFA转化为DFA，将nodes和edges填上
        # self.determine(nfa)


    @staticmethod
    # e-closure计算
    def epsilon_closure(self, node_set: set, nfa: NFA):
        # 查找node_set经过任意条epsilon弧能抵达的节点们
        edges = nfa.edges

        # 用于判断是否已经出现过了
        node_id_set = set()
        # 获得所有的node的id
        for node in node_set:
            node_id_set.add(node.id)

        for node in node_set:
            node_id = node.id
            for edge in edges:
                if edge.tag == "epsilon" and edge.fromNodeId == node_id:
                    # 如果新的node不在node_set中则加入，否则跳过
                    # 遍历所有的可以抵达的node
                    for toNodeId in edge.toNodeIds:
                        if toNodeId in node_id_set:
                            continue
                        else:
                            # 将能够抵达的node加入new_node_set
                            node_set.add(nfa.nodes[toNodeId])

        return node_set

    @staticmethod
    def move(self, node_set: set, nfa: NFA, tag):

        edges = nfa.edges
        # 返回的全新node集合
        new_node_set = set()
        # 用于判断是否已经出现过了
        node_id_set = set()
        # # 获得所有的node的id
        # for node in node_set:
        #     node_id_set.add(node.id)

        # 遍历每一个node
        for node in node_set:
            for edge in edges:
                # 相同tag的匹配
                if edge.fromNodeId == node.id and edge.tag == tag:
                    for toNodeId in edge.toNodeIds:
                        if toNodeId in node_id_set:
                            continue
                        else:
                            new_node_set.add(nfa.nodes[toNodeId])
        return new_node_set

    # 确定化算法
    def determine(self, nfa: NFA):
        self.nodes = []

        # 先计算nfa的起始节点的闭包
        start_node = nfa.nodes[nfa.startId]

        # new_start_node_set = self.epsilon_closure(self, {start_node}, nfa)
        new_start_node_set = {start_node}

        # 初始化将初始点加入集合中
        node_queue = [new_start_node_set]
        now_id = 0
        self.add_node(now_id, 0, 0, "")

        # 因为是按照顺序进入的，所以point和from_node_id是相同的
        point = 0
        while point < len(node_queue):
            # 取出队列中未计算的最靠前的set
            node_set = node_queue[point]
            # 对每一个tag进行move计算
            for tag in tags:
                move_node_set = self.move(self, node_set, nfa, tag)
                # 如果是空则忽略
                if len(move_node_set) == 0:
                    continue
                # 非空且未出现过需要连接edge，并添加node
                elif not (move_node_set in node_queue):
                    # 先加入队列，用于继续计算
                    node_queue.append(move_node_set)
                    # 对DFA处理node和edges

                    # 从move_node_set中的第一个节点获得is_final 和 is_back_off
                    is_final = 0
                    is_back_off = 0
                    # 获得一个isFinal, isBackOff
                    node_tag = ""
                    for one in move_node_set:
                        is_final = one.isFinal
                        is_back_off = one.isBackOff
                        node_tag = one.tag
                        break
                    now_id += 1
                    # 这里node的tag添加错误了！
                    # self.add_node(now_id, is_final, is_back_off, tag)
                    # print(now_id, is_final, is_back_off, node_tag)
                    self.add_node(now_id, is_final, is_back_off, node_tag)
                    self.add_edges(point, now_id, tag)
                # 非空但出现过只需要连接edge
                else:
                    # 计算to_node_id，就是在node_queue中的index
                    to_node_id = node_queue.index(move_node_set)
                    self.add_edges(point, to_node_id, tag)
            point += 1
        # for i in self.edges:
        #     print('fromId:'+str(i.fromNodeId)+' tag:'+str(i.tag)+' toNodeId: '+str(i.toNodeIds))

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

    # 是否结束
    def is_final(self, id):
        # 因为是按照顺序添加的节点,所以nodes的下标对应着一样的id
        return self.nodes[id].isFinal

    # 是否需要退出一个字符
    def is_back_off(self, id):
        return self.nodes[id].isBackOff

    # 获得tag
    def get_tag(self, id):
        # 可以根据tag返回需要的内容
        return self.nodes[id].tag

    # 获得下一个ID
    def next_id(self, tag):
        for edge in self.edges:
            if edge.fromNodeId == self.nowId and re.match(edge.tag, tag):
                # 并将nowId指向新的位置
                self.nowId = edge.toNodeIds
                # 说明成功找到下一个节点
                return True
        return False

    # 根据给出的token判断类型
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


