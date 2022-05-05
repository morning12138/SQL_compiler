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
##### 1.1.3 main函数
1. 依次调用函数`read_sql_syntax()`读取sql语法、`get_V()`划分终结符集和非终结符集、`get_first()`构造first集、`get_follow()`构造follow集、`get_table`构造table分析表。
2. 输入分析串，例如：
```sql
SELECT IDN . IDN FROM IDN WHERE IDN . IDN > INT
```
3. 初始化`test_str`分析串（在输入串后加#并进行预处理）。初始化`v_stack`符号栈，即将`# root`进栈。初始化`state_stack`状态栈，即将`0`进栈。
4. 从左依次编历`test_str`分析串，每次取`a = test_str[0]`直至`test_str == None`:
* `a`不是终极符，终止循环，输入串不符合语法规则，输出`error`。
* `a`是终结符，`a`等于`v_stack[-1]`且`a`为`#`，则输入串符合语法规则，输出`accept`。
* `a`是终结符，`a`等于`v_stack[-1]`且`a`不为`#`，则对`a`进行移入，输出`move`。
```python
    v_stack.pop()
    test_str.pop(0)
```
* `a`是终结符，`a`不等于`v_stack[-1]`，则查找分析表`table`进行规约，输出`reduction`。注意：所用规约的语法规则`rule`中的`$`不需`push`符号栈。
```python
    rule = []
    vt_index = get_v_index(a, 1)
    vn_index = get_v_index(v_stack[-1], 2)
    rule_index = table[vn_index][vt_index]
    rule = rules[rule_index - 1][:]

    print(step, rule_index, v_stack[-1] + '#' + a, 'reduction')
    step = step + 1

    v_stack.pop()
    
    for i in range(len(rule) - 2):
        tmp = rule[len(rule) - i - 1][:]
        if tmp != '$':
            v_stack.append(tmp)
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

##### 2.1.3 main函数
1. 依次调用函数`read_sql_syntax()`读取sql语法、`get_V()`划分终结符集和非终结符集、 `get_items()`构造文法项目、`get_first()`构造first集、`get_standard_items()`构造项目集规范族、`get_action`构造action分析表、`get_goto`构造goto分析表。
2. 输入分析串，例如：
```sql
SELECT IDN . IDN FROM IDN WHERE IDN . IDN > INT
```
3. 初始化`test_str`分析串（在输入串后加#并进行预处理）。初始化`v_stack`符号栈，即将`# root`进栈。初始化`state_stack`状态栈，即将`0`进栈。
4. 从左依次编历`test_str`分析串，每次取`a = test_str[0]`直至`test_str == None`:
* `a`不是终极符，终止循环，输入串不符合语法规则，输出`error`。
* `a`是终结符，获取`a`的终结符索引`a_index`,通过`action`分析表得到该执行的动作`act`。
```python
    a_index = get_v_index(a, 1)
    act = action[state_stack[-1]][a_index]
```
* 如果`act == 'acc'`，即则输入串符合语法规则，输出`accept`。
* 如果`act[0] == 's'`，即为移进动作，将当前符号`a`进符号栈，将`int(act[1:])`进状态栈，输出`move`。
```python
    test_str.pop(0)
    state_stack.append(int(act[1:]))
    print(step, '/', v_stack[-1] + '#' + a, 'move')
    v_stack.append(a)
    step = step + 1
```
* 如果`act[0] == 'r'`，即为规约动作，先将状态栈前规约后符号数`len(rules[int(act[1:]) - 1]) - 2`个状态移出，`$`不需将状态移出。将符号栈栈顶移出，将规约后的符号`next_v`进栈。将`next_state = goto[state_stack[-1]][v_index]`进状态栈。
```python
    if rules[int(act[1:]) - 1][-1] != '$' or len(rules[int(act[1:]) - 1]) != 3:
        for j in range(len(rules[int(act[1:]) - 1]) - 2):
            state_stack.pop()
            
    v_stack.pop()
    next_v = rules[int(act[1:]) - 1][0]
    v_stack.append(next_v)              
    v_index = get_v_index(v_stack[-1], 2)       
    next_state = goto[state_stack[-1]][v_index]
    state_stack.append(next_state)

    print(step, int(act[1:]), v_stack[-1] + '#' + a, 'reduction')
                step = step + 1
```


* 注意通过A->$规约时，不需要pop状态栈顶
* 通过规则规约时，pop状态栈顶数 = 规约符号数