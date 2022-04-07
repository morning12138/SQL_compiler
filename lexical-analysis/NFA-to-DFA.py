from NFA import *


# 初始化使用一个NFA，然后使用确定化和最小化算法
class DFA:
    def __init__(self, nfa: NFA):
        # 存放节点
        self.nodes = []
        self.edges = []
        # 当前状态机所在的位置
        self.nowId = nfa.nowId
        # 开始节点
        self.startId = nfa.startId

        # 确定化将NFA转化为DFA，将nodes和edges填上
        self.determine(nfa)

        # 最小化DFA，修改nodes和edges
        self.minimize()

    @staticmethod
    # e-closure计算
    def epsilon_closure(self, node_set: list, nfa: NFA):
        # 查找node_set经过任意条epsilon弧能抵达的节点们
        edges = nfa.edges

        # 用于判断是否已经出现过了
        node_id_set = []
        # 获得所有的node的id
        for node in node_set:
            node_id_set.append(node.id)

        for node in node_set:
            node_id = node.id
            for edge in edges:
                if edge.tag == "epsilon" and edge.fromNodeId == node_id:
                    # 如果新的node不在node_set中则加入，否则跳过
                    if edge.toNodeId in node_id_set:
                        continue
                    else:
                        # 将能够抵达的node加入new_node_set
                        node_set.append(nfa.nodes[edge.toNodeId])

        return node_set

    @staticmethod
    def move(self, node_set: list, nfa: NFA, tag):

        edges = nfa.edges
        # 返回的全新node集合
        new_node_set = []
        # 用于判断是否已经出现过了
        node_id_set = []
        # 获得所有的node的id
        for node in node_set:
            node_id_set.append(node.id)

        # 遍历每一个node
        for node in node_set:
            now_id = node.id
            for edge in edges:
                if edge.fromNodeId == now_id and edge.tag == tag:
                    if edge.toNodeId in node_id_set:
                        continue
                    else:
                        new_node_set.append(nfa.nodes[edge.toNodeId])
        return new_node_set

    # 确定化算法
    def determine(self, nfa):
        return

    # 最小化
    def minimize(self):
        return
