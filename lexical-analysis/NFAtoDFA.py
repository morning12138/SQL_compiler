from NFA import *


# 初始化使用一个NFA，然后使用确定化和最小化算法
class DFA:
    def __init__(self, nfa: NFA):
        # 存放节点
        self.nodes = []
        self.edges = []
        # 当前状态机所在的位置
        self.nowId = 0
        # 开始节点
        self.startId = 0

        # 确定化将NFA转化为DFA，将nodes和edges填上
        self.determine(nfa)

        # 最小化DFA，修改nodes和edges
        self.minimize()

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
        # 获得所有的node的id
        for node in node_set:
            node_id_set.add(node.id)

        # 遍历每一个node
        for node in node_set:
            now_id = node.id
            for edge in edges:
                if edge.fromNodeId == now_id and edge.tag == tag:
                    for toNodeId in edge.toNodeIds:
                        if toNodeId in node_id_set:
                            continue
                        else:
                            new_node_set.add(nfa.nodes[toNodeId])
        return new_node_set

    # 确定化算法
    def determine(self, nfa: NFA):
        # 首先从开始节点开始
        # 计算各种tag的闭包
        self.nodes = []

        # 先计算nfa的起始节点的闭包
        start_node = nfa.nodes[nfa.startId]
        new_start_node_set = self.epsilon_closure(self, {start_node}, nfa)

        return

    # 最小化
    def minimize(self):
        return

    # 添加节点
    def add_node(self, id, is_final, is_back_off, tag):
        new_node = Node(id, is_final, is_back_off, tag)
        self.nodes.append(new_node)
