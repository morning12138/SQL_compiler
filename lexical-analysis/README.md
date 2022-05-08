# SQL_compiler
TJU编译原理大作业
## 词法分析器设计

### 1 简介

#### 1.1 实现思路

1. 根据实验指导书的单词符号**构造出对应的NFA**。
2. 编写**确定化、最小化算法**将构造的NFA自动转换成DFA。
3. 编写词法分析器的类执行词法分析。

#### 1.2 单词符号

![image-20220420112938537](C:\Users\86150\AppData\Roaming\Typora\typora-user-images\image-20220420112938537.png)

#### 1.3 输入输出说明

输入：在`main.py`中修改`path`为sql文件的路径.

输出：输出将保存在`output`文件夹下，也会在终端打印

### 2 NFA定义与实现

​	根据NFA定义依据四元组构造成一个**类**，使用面向对象的编程方式来进行词法分析器的编写。

#### 2.1 定义的类

##### 2.1.1 Node

表示NFA中的一个节点，DFA中的节点定义并无区别，所以仍然使用该`class`

* `id`是节点的编号；

* `isFinal`用来判断是否是终止节点；
* `isBackoff`用来判断是否需要回退；
* `tag`用于判定最终得到的token类别。

```python
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
```

##### 2.1.2 Edge

表示NFA中的边。

要注意的是由于是`NFA`，所以同一个`tag`可以<font color="red">去往多个不同的节点</font>，因此这里`toNodeIds`使用的是`set`的数据结构，用来存放多个可能的节点。

* `fromNodeId`表示有向边的出发节点；
* `tag`表示获得`tag`可以从`fromNodeId`转化为`toNodeIds`；
* `toNodeIds`使用集合表示通过`tag`可以抵达的节点集合。

```python
class Edge:
    def __init__(self, from_node_id, to_node_id: set, tag):
        # from 节点
        self.fromNodeId = from_node_id
        # to 节点 同一个tag可以去到的所有节点集合
        self.toNodeIds = to_node_id
        # 转化需要的信息，使用正则表达式表示
        self.tag = tag
```

##### 2.1.3  NFA

依据绘制的NFA状态转化图进行初始化。

属性：

* `nodes`数组中元素类型为`class Node`
* `edges`数组中元素类型为`class Edge`
* `nowId`代表当前状态机指向的位置；
* `startId`代表初始节点的`id`(与`node`的`id`属性对应)

函数：

* `add_node`：添加节点至`nodes`
* `add_edges`：添加节点至`edges`
* `get_start`: 将指针指向开始节点
* `is_final`：判定当前指针是否在**终止节点**
* `is_back_off`：判定是否需要退出一个字符
* `get_tag`：获得`node`的tag

```python
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

```

### 3 DFA定义与实现

#### 3.1 定义的类

##### 3.1.1 DFAEdge

与Edge的定义类似，不同点在于`toNodeIds`的定义。`DFA`中通过一个`tag`只能抵达一个确定的`node`，所以在`DFAEdge`中`toNodeIds`是一个int类型数据。

* `fromNodeId`表示有向边的出发节点；
* `tag`表示获得`tag`可以从`fromNodeId`转化为`toNodeIds`；
* `toNodeIds`使用集合表示通过`tag`可以抵达的节点。

```python
class DFAEdge:
    def __init__(self, from_node_id, to_node_id: int, tag):
        # from 节点
        self.fromNodeId = from_node_id
        # to 节点 同一个tag可以去到的所有节点集合
        self.toNodeIds = to_node_id
        # 转化需要的信息
        self.tag = tag

```

##### 3.1.2 DFA

通过已有的NFA进行<font color='red'>确定化和最小化算法</font>生成DFA。

属性：

* `nodes`数组中元素类型为`class Node`
* `edges`数组中元素类型为`class DFAEdge`
* `nowId`代表当前状态机指向的位置；
* `startId`代表初始节点的`id`(与`node`的`id`属性对应)

函数：

* `epsilon_closure`：计算闭包
* `move`：计算move集合
* `determine`：确定化算法
* `minimize`：最小化算法

* `add_node`：添加节点至`nodes`
* `add_edges`：添加节点至`edges`
* `get_start`: 将指针指向开始节点
* `is_final`：判定当前指针是否在**终止节点**
* `is_back_off`：判定是否需要退出一个字符
* `get_tag`：获得`node`的tag
* `next_id`：通过得到的`ch`获得一个`node`的`id`
* `get_token_type`：根据给出的`token`判断类型，用于输出
* `get_token_num`：根据给出的`token`判定编号，用于输出

```python
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

    # 最小化
    def minimize(self):
        return

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

```

#### 3.2 关键算法介绍

##### 3.2.1 确定化算法

* 首先从S0出发，仅经过任意条e箭弧所能到达的状态所组成的集合I作为M’ 的初态q0.
* 分别把从q0（对应于M的状态子集I）出发，经过任意![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps3.jpg)的a弧转换![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps4.jpg) 所组 成的集合作为M’ 的状态，如此继续，直到不再有新的状态为止。

##### 3.2.2 最小化算法

DFA M = ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps5.jpg), 最小状态DFA M’ 

* 构造状态的初始划分 ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps6.jpg)：终态St 和非终态S- St 两组 
* 对![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps7.jpg)施用传播性原则构造新划分![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps8.jpg)
* 如 ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps9.jpg) == ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps10.jpg),则令 ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps11.jpg)= ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps12.jpg) 并继续步骤4，否则![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps13.jpg) := ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps14.jpg)重复2 
* 为![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps15.jpg)中的每一组选一代表，这些代表构成M’的状态。若s是一代表,且 ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps16.jpg), 令r是t组的代表，则M’中有一转换![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps17.jpg)。 M’ 的开始状态是含有 ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps18.jpg)的那组的代表, M’的终态是含有![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps19.jpg)的那组的代表 
* 去掉M’中的死状态



对![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps55.jpg)施用传播性原则构造新划分![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps56.jpg)步骤：

* 假设![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps57.jpg)被分成m个子集![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps58.jpg),, 且属于不同子集的状态是可区别 的，检查![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps59.jpg)的每一个子集![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps60.jpg) , 看是否能够进一步划分。 
* 对于某个Si , 令![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps61.jpg), 若存在数据字符a使得![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps62.jpg)不全包含在现行![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps63.jpg) 的某一子集![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps64.jpg) 中，则将![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps65.jpg)一分为二：即假定状态s1, s2，经过a弧分别达到 状态t1, t2, 且t1, t2属于现行![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps66.jpg)的两个不同子集，那么将Si 分成两半，一半含有![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps67.jpg): ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps68.jpg)且s经a弧到达t1所在子集中的某状态}；另一半含有![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps69.jpg)
* 由于t1, t2是可区别的，即存在w, 使得t1读出w而停于终态，t2读不出w或 读出w却未停于终态。因而aw可以将s1, s2区分开。也就是说![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps70.jpg)和![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps71.jpg)中的 状态时可区别的。 
* ![img](file:///C:\Users\86150\AppData\Local\Temp\ksohtml8672\wps72.jpg)

### 4 LEXER定义与实现

##### 4.1 定义的类

##### 4.1.1 Token

根据实验指导书要求的输出格式定义`Token`类

```python
class Token:
    def __init__(self, lexeme: str, token_type: str, token_num: str):
        self.lexeme = lexeme
        self.tokenType = token_type
        # 说是num，其实不是全是num，所以还是用str类型
        self.tokenNum = token_num
```

##### 4.1.2 TokenTable

保存解析后的Token，并编写输出与保存的函数

```python
class TokenTable:
    def __init__(self):
        self.tokens = []

    def print_token_table(self):
        for token in self.tokens:
            print("{}   <{}, {}>".format(token.lexeme, token.tokenType, token.tokenNum))

    def push_token(self, token: Token):
        self.tokens.append(token)

    def save_token_table(self, path):
        f = open(path, "w+")
        for token in self.tokens:
            f.write("{}   <{}, {}>\n".format(token.lexeme, token.tokenType, token.tokenNum))
        f.close()

```

##### 4.1.3 Lexer

执行词法分析的主体，利用DFA进行词法分析。

```python
class Lexer:
    def __init__(self, path: str, token_table: TokenTable, dfa: DFA):
        self.source = open(path, 'r').read()
        self.tokenTable = token_table
        self.dfa = dfa

    # 执行词法分析
    def run(self):
        # 流程：
        #   token_now = ""
        #   1.读取字符
        #   2.查找对应的状态转换
        #       2.1 如果找不到则说明错误的词法，报错
        #       2.2 如果找到了则状态转换到新的状态
        #           2.2.1 非终结态则继续读取
        #           2.2.2 终结态判断is_back_off
        #               2.2.2.1 true：从token_now退出一个ch,将生成的token_now加入tokentable
        #               2.2.2.2 false: 将token_now加入token list中
        #           2.2.3 修改DFA的指针指向初始位置，token_now = ""

        # 初始化
        text = self.source
        token_now = ""
        self.dfa.get_start()
        ID = 0
        i = 0
        while i < len(text):
            # 需要跳过的情况
            ch = text[i]
            if token_now == "" and (ch == "\n" or ch == ' '):
                i += 1
                continue

            token_now += ch
            # 匹配成功到下一个节点
            if self.dfa.next_id(ch):
                ID = self.dfa.nowId
                # 判断is_final
                if self.dfa.is_final(ID):
                    # 判断is_back_off
                    if self.dfa.is_back_off(ID):
                        # 指针回退一个
                        token_now = token_now[0:-1]
                        i -= 1

                    # 将token_now加入tokenTable
                    # 根据token_now判断tokenType和tokenNum
                    # ！！！暂时还没写！！！

                    # 获得最终节点的tag
                    node_tag = self.dfa.get_tag(ID)
                    # 这个判断应该是dfa提供的
                    token_type = self.dfa.get_token_type(token_now, node_tag)
                    token_num = self.dfa.get_token_num(token_now, token_type)

                    self.tokenTable.push_token(Token(token_now, token_type, token_num))
                    token_now = ""
                    self.dfa.get_start()
                i += 1
            # 匹配失败，则抛出异常
            else:
                print("Lexical error: 不符合sql词法！")
                return

        if not self.dfa.is_final(ID):
            print("Lexical error: 最终一个词不是完整的token")
            return


```

