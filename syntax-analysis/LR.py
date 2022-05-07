# 不符合LR（0）文法（存在推出空的文法规则），符合LR(1)文法
# sql_syntax语法终结符中有. ,在构造项目时用`代替.

from ctypes import sizeof
import os
from re import S
from turtle import dot, st
from hamcrest import none
from matplotlib.pyplot import new_figure_manager
from tabulate import tabulate
from torch import le
import wcwidth

class Standard_item:
    def __init__(self, left, right):
        self.left = left
        self.right = right


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

# 读取sql语法文件
def read_sql_syntax():
    global rules
    file_path = "./sql_syntax.txt"
    with open(file_path, encoding='utf-8') as file_obj:
        rules = file_obj.readlines()
    file_obj.close()

    # 对lines进行处理
    for i in range(len(rules)):
        rules[i] = rules[i].split()
        rules[i].pop(0)
    
    rules[19] = ['groupByClause', '->', 'GROUP BY', 'expressions']
    rules[23] = ['orderByClause', '->', 'ORDER BY', 'expressions']

def init_first():
    for vn_index in range(len(VN)):
        first_list = []
        first.append(first_list)

def get_first():
    
    init_first()
    while(True):
        flag = 0
        
        for rule in rules:
            vn_index = get_v_index(rule[0], 2)
            for j in range(2, len(rule)):
                if rule[j] in VT and rule[j] not in first[vn_index]:
                    first[vn_index].append(rule[j])
                    flag = 1
                    break
                if rule[j] in VN:
                    vn2_index = get_v_index(rule[j], 2)
                    if first[vn2_index] != []:
                        for first_index in range(len(first[vn2_index])):
                            if first[vn2_index][first_index] not in first[vn_index] and first[vn2_index][first_index] != '$':
                                first[vn_index].append(first[vn2_index][first_index])
                                flag = 1

                if in_empty_rule(rule[j]) == -1:
                    break
                elif j == len(rule) - 1:
                    if '$' not in first[vn_index]:
                        first[vn_index].append('$')

        if flag == 0:
            break


def in_empty_rule(this_vn):
    for rule in rules:
        if rule[0] == this_vn and rule[2] == '$':
            return 0
    return -1


# 构造文法项目
def get_items():
    items.append(['root\'', '->', '`', 'root'])
    items.append(['root\'', '->', 'root', '`'])
    for rule in rules:
        for i in range(len(rule)-1):
            if rule[-1] != '$':
                tmp = rule[:2+i] + list('`') + rule[2+i:]
                items.append(tmp)
            else:
                tmp = rule[:2] + list('`')
                items.append(tmp)
    
# 划分终结符和非终结符
def get_V():
    for rule in rules:
        if rule[0] not in VN:
            VN.append(rule[0])
            V.append(rule[0])
    for rule in rules:
        for ru in rule[2:]:
            if ru not in VT and ru not in VN:
                VT.append(ru)
                V.append(ru)
    VT.append('#')
    V.append('#')


# 闭包运算
def get_closeure(set):
    closure = []
    tag = 0
    for it in set:
        if in_closure(it, closure) == -1:
            closure.append(it)
        it_left = it.left[:]
        it_right = it.right[:]
        dot_index = it_left.index('`')
        if dot_index != len(it_left) - 1:
            if it_left[dot_index + 1] in VN:
                tmp_right = []
                
                if len(it_left) - dot_index == 2:
                    tmp_right = it_right[:]
                elif it_left[dot_index + 2] in VT:
                    tmp_right.append(it_left[dot_index + 2])
                elif it_left[dot_index + 2] in VN:
                    vn_index = get_v_index(it_left[dot_index + 2], 2)
                    tmp_right = first[vn_index][:]

                for item in items:
                    if item[0] == it_left[dot_index + 1] and item[2] == '`' :
                        tmp = Standard_item(item, tmp_right)
                        if in_closure(tmp, closure) == -1:                        
                            set.append(tmp)
                            closure.append(tmp)
                        elif in_closure(tmp, closure) == 1:
                            for i in range(len(closure)):
                                if it_left == closure[i].left:
                                    for j in range(it_right):
                                        if it_right[j] not in closure[i].right: 
                                            closure[i].right.append(it_right[j])
            else:
                continue 
        
        else:
            continue
    return closure

# 构造项目集规范族standard_items
def get_standard_items():
    # 构造第一项
    set = []
    tmp = Standard_item(items[0], ['#'])
    set.append(tmp)
    standard_items.append(get_closeure(set))

    for standard_item in standard_items:
        for v in V:
            new_item = get_new_item(standard_item, v)
            if new_item != None and in_standard_items(new_item) == -1:           
                standard_items.append(new_item)


# 得到新的standard_item
def get_new_item(standard_item, v):

    set = []
    for i in range(len(standard_item)):
        it = standard_item[i].left[:]

        dot_index =it.index('`')
        if dot_index != len(it) - 1:
            if it[dot_index + 1] == v:
                tmp_left = it[:]
                tmp_left[dot_index] = tmp_left[dot_index + 1]
                tmp_left[dot_index + 1] = '`'  
                tmp_right = standard_item[i].right[:]
                tmp = Standard_item(tmp_left, tmp_right)
                set.append(tmp)

        if set != []:
            return get_closeure(set)
    return None

def in_closure(it, closure):
    for i in range(len(closure)):
        if it.left == closure[i].left and it.right == closure[i].right:
            return 0
        if it.left == closure[i].left and it.right != closure[i].right:
            return 1
    return -1

# 判断standard_item是否已存在
def in_standard_items(new_item):

    for standard_item in standard_items:
        flag = 0
        for i in range(len(standard_item)):
            for j in range(len(new_item)):
                if standard_item[i].left == new_item[j].left and standard_item[i].right == new_item[j].right:
                    flag = flag + 1
                    break
        if flag == len(standard_item) and len(standard_item) == len(new_item):
            return 0
    return -1


# 构造action
def init_action():
    for item_index in range(len(standard_items)):
        ac_list = []
        for vt_index in range(len(VT)):
            ac_list.append(" ") 
        action.append(ac_list)


def get_action():
    # action表初始化
    init_action()
    for standard_item in standard_items:
        item_index = get_standard_item_index(standard_item)
        for it in standard_item:
            it_left = it.left[:]
            it_right = it.right[:]
            dot_index = it_left.index('`')
            if it_left[dot_index + 1:] == []:
                # 规约
                rule_index = get_rule_index(it_left)
                
                if '$' in it_right:
                    for vt_index in range(len(VT)):
                        if action[item_index][vt_index] == ' ':
                            action[item_index][vt_index] = 'r' + str(rule_index)
                    
                else:
                    for vt_index in range(len(VT)):
                        if VT[vt_index] in it_right:
                            action[item_index][vt_index] = 'r' + str(rule_index)
                       
            else:
                for vt in VT: 
                    vt_index = get_v_index(vt, 1)
                    if vt == it_left[dot_index + 1]:
                        next_item_index = get_standard_item_index(get_new_item(standard_item, vt))
                        action[item_index][vt_index] = 's' + str(next_item_index)
                        
    action[1][len(VT)-1] = 'acc'

def init_goto():
    for item_index in range(len(standard_items)):
        goto_list = []
        for vn_index in range(len(VN)): 
            goto_list.append(" ") 
        goto.append(goto_list)


def get_goto():
    # 初始化goto表
    init_goto()

    for standard_item in standard_items:
        item_index = get_standard_item_index(standard_item)
        for vn in VN:
            vn_index = get_v_index(vn, 2)
            next_item = get_new_item(standard_item, vn)
            if next_item != None and in_standard_items(next_item) != -1:
                next_item_index = get_standard_item_index(next_item)
                goto[item_index][vn_index] = next_item_index

def get_standard_item_index(this_item):
    index = 0
    for standard_item in standard_items:
        flag = 0
        for i in range(len(standard_item)):
            for j in range(len(this_item)):
                if standard_item[i].left == this_item[j].left and standard_item[i].right == this_item[j].right:
                    flag = flag + 1
                    break
        if flag == len(standard_item) and len(standard_item) == len(this_item):
            return index
        index = index + 1
    return -1

def get_v_index(this_v, FLAG): 
    if FLAG == 0:
        index = 0
        for v in V:
            if(this_v == v):
                return index
            index = index + 1
        return -1
    elif FLAG == 1:
        index = 0
        for vt in VT:
            if this_v == vt:
                return index
            index = index + 1
        return -1
    elif FLAG == 2:
        index = 0
        for vn in VN:
            if this_v == vn:
                return index
            index = index + 1
        return -1
    else:
        return -1

def get_rule_index(this_item):
    index = 1
    tmp = this_item[:]
    for rule in rules:
        if this_item == rule + list('`'):
            return index
        elif len(this_item) == 3 and this_item[2] == '`':
            if index == 1:
                tmp.insert(2, '$')
            if tmp == rule + list('`'):
                return index
        index = index + 1
    if this_item == items[1]:
        return 0
    return -1

def print_action():
    print('\n')
    print('----------------------------------------------ACTION---------------------------------------------')
    
    table_header = []
    table_header.append('state')
    for vt_index in range(10):
        table_header.append(VT[vt_index])

    part_of_action = []
    for item_index in range(10):
        tmp = []
        for vt_index in range(10):
            tmp.append(action[item_index][vt_index])
        part_of_action.append(list(str(item_index)) + tmp)

    print(tabulate(part_of_action, headers=table_header, tablefmt='grid'))


def print_goto():
    print('\n')
    print('-----------------------------------------------GOTO---------------------------------------------')
    table_header = []
    table_header.append('state')
    for vn_index in range(10):
        table_header.append(VN[vn_index])

    part_of_goto = []
    for item_index in range(10):
        tmp = []
        for vn_index in range(8):
            tmp.append(goto[item_index][vn_index])
        part_of_goto.append(list(str(item_index)) + tmp)

    print(tabulate(part_of_goto, headers=table_header, tablefmt='grid'))

def read_lex_result(lex_file):
    global test_str
    with open(lex_file, encoding='utf-8') as file_obj:
        lex_results = file_obj.readlines()
    file_obj.close()
    
    sql_words = []

    for i in range(len(lex_results)): 
        sql_word = {}
        line = lex_results[i].split('\t')
        comma_index = line[1].find(',')
        sql_word['word'] = line[0][:]
        sql_word['type'] = line[1][1:comma_index]
        sql_words.append(sql_word)
    
    for j in range(len(sql_words)):
        if sql_words[j]['type'] == 'IDN' or sql_words[j]['type'] == 'INT' or sql_words[j]['type'] == 'FLOAT' or sql_words[j]['type'] == 'STRING':
            test_str.append(sql_words[j]['type'])
        elif sql_words[j]['word'] == 'GROUP' or sql_words[j]['word'] == 'ORDER':
            test_str.append(sql_words[j]['word'] + 'BY')
        elif sql_words[j]['word'] == 'BY':
            pass
        else:
            test_str.append(sql_words[j]['word'])

    test_str.append('#')


def main():

    read_sql_syntax()  
    get_items()
    get_V()
    get_first()
    # print('first', first)
    get_standard_items()
    get_action()
    # print_action()
    get_goto()
    # print_goto()

    result_file = input('请输入输出结果文件名称：\n')
    result = open(result_file, 'w')
    
    lex_file = input('请输入词法分析结果文件名称：\n')
    read_lex_result(lex_file)

    state_stack.append(0)
    v_stack.append('#')

    step = 1
    while test_str != None:
        a = test_str[0]

        if a in VT:
            a_index = get_v_index(a, 1)
            act = action[state_stack[-1]][a_index]
            # 移进
            if act[0] == 's':
                test_str.pop(0)
                state_stack.append(int(act[1:]))
                print(step, '/', v_stack[-1] + '#' + a, 'move', file = result)

                v_stack.append(a)
                step = step + 1
            # 规约
            elif act[0] == 'r': 
                
                if rules[int(act[1:]) - 1][-1] != '$' or len(rules[int(act[1:]) - 1]) != 3:
                    for j in range(len(rules[int(act[1:]) - 1]) - 2):
                        state_stack.pop()
                    
                v_stack.pop()
                next_v = rules[int(act[1:]) - 1][0]
                v_stack.append(next_v)              
                v_index = get_v_index(v_stack[-1], 2)       
                next_state = goto[state_stack[-1]][v_index]
                state_stack.append(next_state)
                
                if a != '#':
                    print(step, int(act[1:]), v_stack[-1] + '#' + a, 'reduction', file = result)
                else:
                    print(step, int(act[1:]), v_stack[-1] + '#', 'reduction', file = result)
                step = step + 1
            # 接受
            elif act == 'acc':
                print(step, '1', v_stack[-1] + '#', 'accept', end="", file = result)
                break
            else:
                print(step, '/' , v_stack[-1] + '#' + a, 'error', file = result)
                break
        else:
            print(step, '/' , v_stack[-1] + '#' + a, 'error', file = result)
            break
# 对输入串进行语法分析
if __name__ == '__main__':
    main()




