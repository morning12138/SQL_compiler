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
tags = {"=", ">", "not =", "=", "<", "not >", ">", "!", "&",
        "|", ".", "_,a-zA-Z", "_,0-9,a-zA-Z", "not _,0-9,a-zA-Z",
        "(", ")", ","
        "1-9", "0-9", "not .,0-9", ".", "0-9", "not 0-9",
        "\"", "all",
        "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
        "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"
        }


class Edge:
    def __init__(self, from_node_id, to_node_id: set, tag):
        # from 节点
        self.fromNodeId = from_node_id
        # to 节点 同一个tag可以去到的所有节点集合
        self.toNodeIds = to_node_id
        # 转化需要的信息
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
        self.add_node(1, 1, 0, "=")
        self.add_node(2, 0, 0, "")
        self.add_node(3, 1, 1, ">")
        self.add_node(4, 1, 0, ">=")
        self.add_node(5, 0, 0, "")
        self.add_node(6, 1, 1, "<")
        self.add_node(7, 0, 0, "")
        self.add_node(8, 1, 1, "<=")
        self.add_node(9, 1, 0, "<=>")
        self.add_node(10, 0, 0, "")
        self.add_node(11, 1, 0, "!=")
        self.add_node(12, 0, 0, "")
        self.add_node(13, 0, 0, "")
        self.add_node(14, 1, 0, "AND")
        self.add_node(15, 0, 0, "")
        self.add_node(16, 1, 0, "&&")
        self.add_node(17, 0, 0, "")
        self.add_node(18, 1, 0, "||")
        self.add_node(19, 0, 0, "")
        self.add_node(20, 1, 0, "OR")
        self.add_node(21, 0, 0, "")
        self.add_node(22, 0, 0, "")
        self.add_node(23, 1, 0, "XOR")
        self.add_node(24, 1, 0, ".")
        # 标识符IDN
        self.add_node(25, 0, 0, "")
        self.add_node(26, 1, 1, "IDN")
        # 界符 SE
        self.add_node(27, 1, 0, "(")
        self.add_node(28, 1, 0, ")")
        self.add_node(29, 1, 0, ",")
        # 整数、浮点数
        self.add_node(30, 0, 0, "")
        self.add_node(31, 1, 1, "INT")
        self.add_node(32, 0, 0, "")
        self.add_node(33, 1, 1, "FLOAT")
        # 字符串
        self.add_node(34, 0, 0, "")
        self.add_node(35, 1, 0, "STRING")
        # 关键字 keyword
        self.add_node(36, 0, 0, "")
        self.add_node(37, 0, 0, "")
        self.add_node(38, 0, 0, "")
        self.add_node(39, 0, 0, "")
        self.add_node(40, 0, 0, "")
        self.add_node(41, 1, 0, "SELECT")
        self.add_node(42, 0, 0, "")
        self.add_node(43, 0, 0, "")
        self.add_node(44, 0, 0, "")
        self.add_node(45, 1, 0, "FROM")
        self.add_node(46, 0, 0, "")
        self.add_node(47, 0, 0, "")
        self.add_node(48, 0, 0, "")
        self.add_node(49, 0, 0, "")
        self.add_node(50, 1, 0, "WHERE")
        self.add_node(51, 0, 0, "")
        self.add_node(52, 1, 0, "AS")
        self.add_node(53, 0, 0, "")
        self.add_node(54, 0, 0, "")
        self.add_node(55, 0, 0, "")
        self.add_node(56, 0, 0, "")
        self.add_node(57, 0, 0, "")
        self.add_node(58, 1, 0, "INSERT")
        self.add_node(59, 0, 0, "")
        self.add_node(60, 0, 0, "")
        self.add_node(61, 0, 0, "")
        self.add_node(62, 1, 0, "INTO")
        self.add_node(63, 0, 0, "")
        self.add_node(64, 0, 0, "")
        self.add_node(65, 0, 0, "")
        self.add_node(66, 0, 0, "")
        self.add_node(67, 0, 0, "")
        self.add_node(68, 1, 0, "VALUES")
        self.add_node(69, 0, 0, "")
        self.add_node(70, 0, 0, "")
        self.add_node(71, 0, 0, "")
        self.add_node(72, 0, 0, "")
        self.add_node(73, 0, 0, "")
        self.add_node(74, 1, 0, "UPDATE")
        self.add_node(75, 0, 0, "")
        self.add_node(76, 0, 0, "")
        self.add_node(77, 0, 0, "")
        self.add_node(78, 0, 0, "")
        self.add_node(79, 0, 0, "")
        self.add_node(80, 1, 0, "DELETE")
        self.add_node(81, 0, 0, "")
        self.add_node(82, 0, 0, "")
        self.add_node(83, 0, 0, "")
        self.add_node(84, 1, 0, "JOIN")
        self.add_node(85, 0, 0, "")
        self.add_node(86, 0, 0, "")
        self.add_node(87, 0, 0, "")
        self.add_node(88, 1, 0, "LEFT")
        self.add_node(89, 0, 0, "")
        self.add_node(90, 0, 0, "")
        self.add_node(91, 0, 0, "")
        self.add_node(92, 0, 0, "")
        self.add_node(93, 1, 0, "RIGHT")
        self.add_node(94, 0, 0, "")
        self.add_node(95, 0, 0, "")
        self.add_node(96, 1, 0, "MIN")
        self.add_node(97, 0, 0, "")
        self.add_node(98, 0, 0, "")
        self.add_node(99, 1, 0, "MAX")
        self.add_node(100, 0, 0, "")
        self.add_node(101, 0, 0, "")
        self.add_node(102, 1, 0, "AVG")
        self.add_node(103, 0, 0, "")
        self.add_node(104, 0, 0, "")
        self.add_node(105, 1, 0, "SUM")
        self.add_node(106, 0, 0, "")
        self.add_node(107, 0, 0, "")
        self.add_node(108, 0, 0, "")
        self.add_node(109, 0, 0, "")
        self.add_node(110, 1, 0, "UNION")
        self.add_node(111, 0, 0, "")
        self.add_node(112, 0, 0, "")
        self.add_node(113, 1, 0, "ALL")
        self.add_node(114, 0, 0, "")
        self.add_node(115, 0, 0, "")
        self.add_node(116, 0, 0, "")
        self.add_node(117, 0, 0, "")
        self.add_node(118, 0, 0, "")
        self.add_node(119, 0, 0, "")
        self.add_node(120, 0, 0, "")
        self.add_node(121, 1, 0, "GROUP BY")
        self.add_node(122, 0, 0, "")
        self.add_node(123, 0, 0, "")
        self.add_node(124, 0, 0, "")
        self.add_node(125, 0, 0, "")
        self.add_node(126, 0, 0, "")
        self.add_node(127, 1, 0, "HAVING")
        self.add_node(128, 0, 0, "")
        self.add_node(129, 0, 0, "")
        self.add_node(130, 0, 0, "")
        self.add_node(131, 0, 0, "")
        self.add_node(132, 0, 0, "")
        self.add_node(133, 0, 0, "")
        self.add_node(134, 0, 0, "")
        self.add_node(135, 1, 0, "DISTINCT")
        self.add_node(136, 0, 0, "")
        self.add_node(137, 0, 0, "")
        self.add_node(138, 0, 0, "")
        self.add_node(139, 0, 0, "")
        self.add_node(140, 0, 0, "")
        self.add_node(141, 0, 0, "")
        self.add_node(142, 0, 0, "")
        self.add_node(143, 1, 0, "ORDER BY")
        self.add_node(144, 0, 0, "")
        self.add_node(145, 0, 0, "")
        self.add_node(146, 0, 0, "")
        self.add_node(147, 1, 0, "TRUE")
        self.add_node(148, 0, 0, "")
        self.add_node(149, 0, 0, "")
        self.add_node(150, 0, 0, "")
        self.add_node(151, 0, 0, "")
        self.add_node(152, 1, 0, "FALSE")
        self.add_node(153, 0, 0, "")
        self.add_node(154, 1, 0, "IS")
        self.add_node(155, 0, 0, "")
        self.add_node(156, 0, 0, "")
        self.add_node(157, 1, 0, "NOT")
        self.add_node(158, 0, 0, "")
        self.add_node(159, 0, 0, "")
        self.add_node(160, 0, 0, "")
        self.add_node(161, 1, 0, "NULL")

        # 添加边的信息
        # 部分OP到 <=>为止
        self.add_edges(0, {0}, " ")
        self.add_edges(0, {1}, "=")
        self.add_edges(0, {2}, ">")
        self.add_edges(2, {3}, "not =")
        self.add_edges(2, {4}, "=")
        self.add_edges(0, {5}, "<")
        self.add_edges(5, {6}, "not =")
        self.add_edges(5, {7}, "=")
        self.add_edges(7, {8}, "not >")
        self.add_edges(7, {9}, ">")

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
