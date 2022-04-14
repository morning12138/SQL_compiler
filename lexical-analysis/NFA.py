
# 定义类
class Node:
    def __init__(self, id, is_final, is_back_off, tag):
        # id
        self.id = id
        # 是否是终结节点 1代表是，0代表不是
        self.isFinal = is_final
        # 是否需要回退 1代表需要，0代表不需要
        self.isBackOff = is_back_off
        # 只有终结节点需要tag
        self.tag = tag


# 创建一个集合
# tag不应该有歧义
tags = [" ", "=", ">", "<", "!", "&", "[^=]", "[^>]",
        "[\|]", "[\.]", "_",
        "[_a-zA-Z]", "[_0-9a-zA-Z]", "[^_0-9a-zA-Z]",
        "[(]", "[)]", ",",
        "\"", ".",
        "[1-9]", "[0-9]", "[^\.0-9]", "[^0-9]",
        "[\*]", "-", "[^!]" #新增加的
        ]


TYPE_TO_CONTENT_DICT_KW = {
    "SELECT": 1, "FROM": 2, "WHERE": 3, "AS": 4, "*": 5,
    "INSERT": 6, "INTO": 7, "VALUES": 8, "VALUE": 9, "DEFAULT": 10,
    "UPDATE": 11, "SET": 12,
    "DELETE": 13,
    "JOIN": 14, "LEFT": 15, "RIGHT": 16, "ON": 17,
    "MIN": 18, "MAX": 19, "AVG": 20, "SUM": 21,
    "UNION": 22, "ALL": 23,
    "GROUP BY": 24, "HAVING": 25, "DISTINCT": 26, "ORDER BY": 27,
    "TRUE": 28, "FALSE": 29, "UNKNOWN": 30, "IS": 31, "NULL": 32
}

TYPE_TO_CONTENT_DICT_OP = {
    "=": 1, ">": 2, "<": 3, ">=": 4, "<=": 5, "!=": 6, "<=>": 7,
    "AND": 8, "&&": 9, "OR": 10, "||": 11, "XOR": 12, "NOT": 13, "!": 14,
    "-": 15,
    ".": 16
}

TYPE_TO_CONTENT_DICT_SE = {
    "(": 1, ")": 2, ",": 3
}


class Edge:
    def __init__(self, from_node_id, to_node_id: set, tag):
        # from 节点
        self.fromNodeId = from_node_id
        # to 节点 同一个tag可以去到的所有节点集合
        self.toNodeIds = to_node_id
        # 转化需要的信息，使用正则表达式表示
        self.tag = tag


# NFA状态机
class NFA:
    def __init__(self):
        # 存放节点
        self.nodes = []
        self.edges = []
        # 当前状态机所在的位置
        self.nowId = 0
        # 开始节点
        self.startId = 0

        # 初始化nodes和edges
        # OP
        self.add_node(0, 0, 0, "")
        self.add_node(1, 1, 0, "OP")
        self.add_node(2, 0, 0, "")
        self.add_node(3, 1, 1, "OP")
        self.add_node(4, 1, 0, "OP")
        self.add_node(5, 0, 0, "")
        self.add_node(6, 1, 1, "OP")
        self.add_node(7, 0, 0, "")
        self.add_node(8, 1, 1, "OP")
        self.add_node(9, 1, 0, "OP")
        self.add_node(10, 0, 0, "")
        self.add_node(11, 1, 0, "OP")
        # self.add_node(12, 0, 0, "")
        # self.add_node(13, 0, 0, "")
        # self.add_node(14, 1, 0, "AND")
        self.add_node(12, 0, 0, "")
        self.add_node(13, 1, 0, "OP")
        self.add_node(14, 0, 0, "")
        self.add_node(15, 1, 0, "OP")
        self.add_node(16, 1, 0, "OP")
        # 标识符IDN
        self.add_node(17, 0, 0, "")
        self.add_node(18, 1, 1, "IDNorKWorOP")
        # 界符 SE
        self.add_node(19, 1, 0, "SE")
        self.add_node(20, 1, 0, "SE")
        self.add_node(21, 1, 0, "SE")
        # 整数、浮点数
        self.add_node(22, 0, 0, "")
        self.add_node(23, 1, 1, "INT")
        self.add_node(24, 0, 0, "")
        self.add_node(25, 1, 1, "FLOAT")
        # 字符串
        self.add_node(26, 0, 0, "")
        self.add_node(27, 1, 0, "STR")

        # 后续补充的节点
        self.add_node(28, 1, 0, "IDNorKWorOP")
        self.add_node(29, 1, 0, "OP")
        self.add_node(30, 1, 1, "OP")

        # 添加边的信息
        # 部分OP到 <=>为止
        self.add_edges(0, {0}, " ")
        self.add_edges(0, {1}, "=")
        self.add_edges(0, {2}, ">")
        self.add_edges(2, {3}, "[^=]")
        self.add_edges(2, {4}, "=")
        self.add_edges(0, {5}, "<")
        self.add_edges(5, {6}, "[^=]")
        self.add_edges(5, {7}, "=")
        self.add_edges(7, {8}, "[^>]")
        self.add_edges(7, {9}, ">")
        self.add_edges(0, {10}, "!")
        self.add_edges(10, {11}, "=")

        self.add_edges(0, {12}, "&")
        self.add_edges(12, {13}, "&")
        self.add_edges(0, {14}, "[\|]")
        self.add_edges(14, {15}, "[\|]")

        self.add_edges(0, {16}, "[\.]")

        # 标识符和keyword
        self.add_edges(0, {17}, "[_a-zA-Z]")
        self.add_edges(17, {17}, "[_0-9a-zA-Z]")
        self.add_edges(17, {18}, "[^_0-9a-zA-Z]")

        self.add_edges(0, {19}, "[(]")
        self.add_edges(0, {20}, "[)]")
        self.add_edges(0, {21}, ",")

        # int, float
        self.add_edges(0, {22}, "[1-9]")
        self.add_edges(22, {22}, "[0-9]")
        self.add_edges(22, {23}, "[^\.0-9]")
        self.add_edges(22, {24}, "[\.]")
        self.add_edges(24, {24}, "[0-9]")
        self.add_edges(24, {25}, "[^0-9]")

        # string
        self.add_edges(0, {26}, "\"")
        self.add_edges(26, {26}, ".")
        self.add_edges(26, {27}, "\"")

        # 后续补充的边
        self.add_edges(0, {28}, "[\*]")
        self.add_edges(0, {29}, "-")
        self.add_edges(10, {30}, "[^!]")

    # 添加节点
    def add_node(self, id, is_final, is_back_off, tag):
        new_node = Node(id, is_final, is_back_off, tag)
        self.nodes.append(new_node)

    # 添加边
    def add_edges(self, from_node_id, to_node_ids: set, tag):
        new_edge = Edge(from_node_id, to_node_ids, tag)
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
