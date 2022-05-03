# SQL_compiler
TJU编译原理大作业
## 语法分析器设计

实现LL(1)和LR(1)两种语法分析方法


### 1 LL(1)

#### 1.1 实现思路

1. 构造**first集**。
2. 构造**follow集**。
3. 根据first集和follow集构造**分析表table**。
4. 构造**符号栈v_stack**和**状态栈state_stack**根据分析表对输入串进行语法分析。

#### 1.1 具体实现

##### 1.1.1 数据结构定义

```python
VN = [] # 非终结符集
VT = [] # 终结符集
V = [] # 符号集 

rules = [] # 文法规则

first = [] # first集
follow = [] # follow集
table = [] # 分析表

test_str = [] # 输入串 
state_stack = [] # 状态栈
v_stack = [] # 符号栈
```
##### 1.1.2 函数定义

```python
# 读取sql语法文件
def read_sql_syntax()
# 划分终结符和非终结符
def get_V()
# 检测规则是否为A->$的形式
def in_empty_rule(this_vn)
# 初始化、构造及输出first集
def init_first()
def get_first()
def print_first()
# 初始化、构造及输出follow集
def init_follow()
def get_follow()
def print_follow()
# 初始化、构造及输出table分析表
def init_table()
def get_table()
def print_table(max_vn_index, max_vt_index)
# 计算符号在符号集中的索引(FLAG = 0 为总符号集；FLAG = 1 为终结符集；FLAG = 2 为非终结符集)

def get_v_index(this_v, FLAG)
#计算语法规则的索引
def get_rule_index(this_rule)

```

### 2 LR(1)

#### 2.1 实现思路

1. 构造**first集**
2. 构造**项目集items**
3. 根据项目集通过闭包运算构造**项目集规范族**
4. 根据项目集规范族构造**action表**和**goto表**
5. 构造**符号栈v_stack**和**状态栈state_stack**根据action表和goto表对输入串进行语法分析。

##### 2.1.1 数据结构定义

```python
# 规范项目
class Standard_item:
    def __init__(self, left, right):
        self.left = left # 项目
        self.right = right # 向前搜索符串

VN = [] # 非终结符集
VT = [] # 终结符集
V = [] # 符号集 

rules = [] # 文法规则
items = [] # 项目集
standard_items = [] # 规范项目集

first = [] # first集

action = [] # action表
goto = [] # goto表

test_str = [] # 输入串 
state_stack = [] # 状态栈
v_stack = [] # 符号栈
```
##### 2.1.1 函数定义

```python
# 读取sql语法文件
def read_sql_syntax()
# 划分终结符和非终结符
def get_V()
# 检测规则是否为A->$的形式
def in_empty_rule(this_vn)
# 初始化、构造及输出first集
def init_first()
def get_first()
def print_first()

# 构造文法项目
def get_items()
# 闭包运算
def get_closeure(set)
# 检测规范项目it是否在闭包中
def in_closure(it, closure)
# 得到新的规范项目集
def get_new_item(standard_item, v)
# 构造项目集规范族standard_items
def get_standard_items()
# 判断规范项目集new_item是否在项目集规范族standard_items中
def in_standard_items(new_item)

# 初始化、构造及输出action集
def init_action()
def get_action()
def print_action()
# 初始化、构造及输出goto集
def init_goto()
def get_goto()
def print_goto()

# 计算规范项目集在项目集规范族中的索引
def get_standard_item_index(this_item)
# 计算符号在符号集中的索引(FLAG = 0 为总符号集；FLAG = 1 为终结符集；FLAG = 2 为非终结符集)
def get_v_index(this_v, FLAG)
#计算语法规则的索引
def get_rule_index(this_rule)
```



* 注意通过A->$规约时，不需要pop状态栈顶
* 通过规则规约时，pop数 = 规约符号数