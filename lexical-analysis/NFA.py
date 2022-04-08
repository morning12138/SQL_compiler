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
        self.add_edges(0, {10}, "!")
        self.add_edges(10, {11}, "=")
        # AND, AS, AVG, ALL
        self.add_edges(0, {12, 51, 100, 111}, "A")
        self.add_edges(12, {13}, "N")
        self.add_edges(13, {14}, "D")
        self.add_edges(51, {52}, "S")
        self.add_edges(100, {101}, "V")
        self.add_edges(101, {102}, "G")
        self.add_edges(111, {112}, "L")
        self.add_edges(112, {113}, "L")

        self.add_edges(0, {15}, "&")
        self.add_edges(15, {16}, "&")
        self.add_edges(0, {17}, "|")
        self.add_edges(17, {18}, "|")
        # OR, ORDER BY
        self.add_edges(0, {19, 136}, "O")
        self.add_edges(19, {20}, "R")
        self.add_edges(0, {21}, "X")
        self.add_edges(21, {22}, "O")
        self.add_edges(22, {23}, "R")
        self.add_edges(0, {24}, ".")

        # 标识符
        self.add_edges(0, {25}, "_,a-zA-Z")
        self.add_edges(25, {25}, "_,0-9,a-zA-Z")
        self.add_edges(25, {26}, "not _,0-9,a-zA-Z")
        self.add_edges(0, {27}, "(")
        self.add_edges(0, {28}, ")")
        self.add_edges(0, {29}, ",")

        # int, float
        self.add_edges(0, {30}, "1-9")
        self.add_edges(30, {30}, "0-9")
        self.add_edges(30, {31}, "not .,0-9")
        self.add_edges(30, {32}, ".")
        self.add_edges(32, {32}, "0-9")
        self.add_edges(32, {33}, "not 0-9")

        # string
        self.add_edges(0, {34}, "\"")
        self.add_edges(34, {34}, "all")
        self.add_edges(34, {35}, "\"")

        # keyword
        # SELECT, SUM
        self.add_edges(0, {36, 103}, "S")
        self.add_edges(36, {37}, "E")
        self.add_edges(37, {38}, "L")
        self.add_edges(38, {39}, "E")
        self.add_edges(39, {40}, "C")
        self.add_edges(40, {41}, "T")
        self.add_edges(103, {104}, "U")
        self.add_edges(104, {105}, "M")
        # FROM, FALSE
        self.add_edges(0, {42, 148}, "F")
        self.add_edges(42, {43}, "R")
        self.add_edges(43, {44}, "O")
        self.add_edges(44, {45}, "M")
        self.add_edges(148, {149}, "A")
        self.add_edges(149, {150}, "L")
        self.add_edges(150, {151}, "S")
        self.add_edges(151, {152}, "E")
        # WHERE
        self.add_edges(0, {46}, "W")
        self.add_edges(46, {47}, "H")
        self.add_edges(47, {48}, "E")
        self.add_edges(48, {49}, "R")
        self.add_edges(49, {50}, "E")
        # INSERT, INTO, IS
        self.add_edges(0, {53, 59, 153}, "I")
        self.add_edges(53, {54}, "N")
        self.add_edges(54, {55}, "S")
        self.add_edges(55, {56}, "E")
        self.add_edges(56, {57}, "R")
        self.add_edges(57, {58}, "T")
        self.add_edges(59, {60}, "N")
        self.add_edges(60, {61}, "T")
        self.add_edges(61, {62}, "O")
        # VALUES
        self.add_edges(0, {63}, "V")
        self.add_edges(63, {64}, "A")
        self.add_edges(64, {65}, "L")
        self.add_edges(65, {66}, "U")
        self.add_edges(66, {67}, "E")
        self.add_edges(67, {68}, "S")
        # UPDATE, UNION
        self.add_edges(0, {69, 106}, "U")
        self.add_edges(69, {70}, "P")
        self.add_edges(70, {71}, "D")
        self.add_edges(71, {72}, "A")
        self.add_edges(72, {73}, "T")
        self.add_edges(73, {74}, "E")
        self.add_edges(106, {107}, "N")
        self.add_edges(107, {108}, "I")
        self.add_edges(108, {109}, "O")
        self.add_edges(109, {110}, "N")
        # DELETE, DISTINCT
        self.add_edges(0, {75, 128}, "D")
        self.add_edges(75, {76}, "E")
        self.add_edges(76, {77}, "L")
        self.add_edges(77, {78}, "E")
        self.add_edges(78, {79}, "T")
        self.add_edges(79, {80}, "E")
        self.add_edges(128, {129}, "I")
        self.add_edges(129, {130}, "S")
        self.add_edges(130, {131}, "T")
        self.add_edges(131, {132}, "I")
        self.add_edges(132, {133}, "N")
        self.add_edges(133, {134}, "C")
        self.add_edges(134, {135}, "T")
        # JOIN
        self.add_edges(0, {81}, "J")
        self.add_edges(81, {82}, "O")
        self.add_edges(82, {83}, "I")
        self.add_edges(83, {84}, "N")
        # LEFT
        self.add_edges(0, {85}, "L")
        self.add_edges(85, {86}, "E")
        self.add_edges(86, {87}, "F")
        self.add_edges(87, {88}, "T")
        # RIGHT
        self.add_edges(0, {89}, "R")
        self.add_edges(89, {90}, "I")
        self.add_edges(90, {91}, "G")
        self.add_edges(91, {92}, "H")
        self.add_edges(92, {93}, "T")
        # MIN, MAX
        self.add_edges(0, {94, 97}, "M")
        self.add_edges(94, {95}, "I")
        self.add_edges(95, {96}, "N")
        self.add_edges(97, {98}, "A")
        self.add_edges(98, {99}, "X")
        # GROUP BY
        self.add_edges(0, {114}, "G")
        self.add_edges(114, {115}, "R")
        self.add_edges(115, {116}, "O")
        self.add_edges(116, {117}, "U")
        self.add_edges(117, {118}, "P")
        self.add_edges(118, {119}, " ")
        self.add_edges(119, {120}, "B")
        self.add_edges(120, {121}, "Y")
        # HAVING
        self.add_edges(0, {122}, "H")
        self.add_edges(122, {123}, "A")
        self.add_edges(123, {124}, "V")
        self.add_edges(124, {125}, "I")
        self.add_edges(125, {126}, "N")
        self.add_edges(126, {127}, "G")
        # TRUE
        self.add_edges(0, {144}, "T")
        self.add_edges(144, {145}, "R")
        self.add_edges(145, {146}, "U")
        self.add_edges(146, {147}, "E")
        # NOT, NULL
        self.add_edges(0, {155, 158}, "N")
        self.add_edges(155, {156}, "O")
        self.add_edges(156, {157}, "T")
        self.add_edges(158, {159}, "U")
        self.add_edges(159, {160}, "L")
        self.add_edges(160, {161}, "L")





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
