from ctypes import sizeof
import os
from tabulate import tabulate

VN = [] # 非终结符集
VT = [] # 终结符集
V = [] # 符号集 

rules = [] # 文法规则

first = [] # first集
follow = [] # follow集

table = []

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


def init_follow():
    for vn_index in range(len(VN)):
        follow_list = []
        follow.append(follow_list)
    root_index = get_v_index('root', 2)
    follow[root_index].append('#')

def get_follow():
    
    init_follow()
    while(True):
        flag = 0
        for rule in rules:
            for i in range(2, len(rule) - 1):
                vn_index = get_v_index(rule[i], 2)
                for j in range(i + 1, len(rule)):
                    if rule[i] in VN and rule[j] in VT and rule[j] not in follow[vn_index]:
                        follow[vn_index].append(rule[j])
                        flag = 1
                        break

                    elif rule[i] in VN and rule[j] in VN:
                        next_vn_index = get_v_index(rule[j], 2)
                        for k in range(len(first[next_vn_index])):
                            if first[next_vn_index][k] not in follow[vn_index]:
                                follow[vn_index].append(first[next_vn_index][k])
                                flag = 1
                    
                    if in_empty_rule(rule[j]) == -1:
                        break 
            
            for i in range(1, len(rule) - 1):
                
                if rule[len(rule) - i] in VN:
                    first_vn_index = get_v_index(rule[0], 2)
                    last_vn_index = get_v_index(rule[len(rule) - i], 2)
                    for j in range(len(follow[first_vn_index])):
                            if follow[first_vn_index][j] not in follow[last_vn_index]:
                                follow[last_vn_index].append(follow[first_vn_index][j])
                                flag = 1
                   
                                
                if in_empty_rule(rule[len(rule) - i]) == -1:
                    break

        if flag == 0:
            break


def init_table():

    for vn_index in range(len(VN)):
        tab_list = []
        for vt_index in range(len(VT)):
            tab_list.append(" ") 
        table.append(tab_list)

def get_table():

    init_table()
    for vn_index in range(len(VN)):
        for vt_index in range(len(VT)):
            for rule in rules:
                first_vn_index = get_v_index(rule[0], 2)
                if vn_index == first_vn_index:
                    if rule[2] in VT:
                        second_vt_index = get_v_index(rule[2], 1)
                        if second_vt_index  == vt_index:
                            rule_index = get_rule_index(rule)
                            table[vn_index][vt_index] = rule_index
                            
                    elif rule[2] in VN:
                        second_vn_index = get_v_index(rule[2], 2)
                        if VT[vt_index] in first[first_vn_index] and VT[vt_index] in first[second_vn_index]:
                            rule_index = get_rule_index(rule)
                            table[vn_index][vt_index] = rule_index
                            
    
        if '$' in first[vn_index] and follow[vn_index] != []:
            for i in range(len(follow[vn_index])):
                tmp_rule = [VN[vn_index], '->', '$']
                rule_index = get_rule_index(tmp_rule)
                    
                if rule_index != -1:
                    follow_vt_index = get_v_index(follow[vn_index][i], 1)
                    table[vn_index][follow_vt_index] = rule_index         
                    
    
def print_table(max_vn_index, max_vt_index):
    print('\n')
    print('----------------------------------------------TABLE---------------------------------------------')
    
    table_header = []
    table_header.append('VN')
    for vt_index in range(10):
        table_header.append(VT[vt_index])

    part_of_action = []
    for vn_index in range(max_vn_index):
        tmp = []
        tmp.append(VN[vn_index])
        for vt_index in range(max_vt_index):
            tmp.append(table[vn_index][vt_index])
        
        part_of_action.append(tmp)

    print(tabulate(part_of_action, headers=table_header, tablefmt='grid'))
 

def print_first():
    print('\n----------------------first------------------------------')
    for i in range(len(VN)):
        print(VN[i], first[i])


def print_follow():
    print('\n----------------------follow------------------------------')
    for i in range(len(VN)):
        print(VN[i], follow[i])


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

def get_rule_index(this_rule):
    index = 1
    for rule in rules:
        if this_rule == rule:
            return index
        index = index + 1
    return -1


def main():
    read_sql_syntax()
    get_V()
    get_first()
    # print_first()
    get_follow()
    # print_follow()
    get_table()


    # 输入形式 SELECT IDN . IDN FROM IDN WHERE IDN . IDN > INT
    str = input()
    str = str + ' #'
    test_str = str.split(' ')

    state_stack.append(0)
    v_stack.append('#')
    v_stack.append('root')

    step = 1
    while test_str != None:
        a = test_str[0][:]

        if a in VT:
            if a == v_stack[-1] and a != '#':

                print(step, '/', v_stack[-1] + '#' + a, 'move')
                step = step + 1

                v_stack.pop()
                test_str.pop(0)

            elif a == v_stack[-1] and a == '#':
                print(step, rule_index, v_stack[-1] + '#' + a, 'accept')
                break
            else:
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
        else:
            print(step, rule_index, v_stack[-1] + '#' + a, 'error')
            break

# 对输入串进行语法分析
if __name__ == '__main__':
    main()