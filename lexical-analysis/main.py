from NFA import *
from NFAtoDFA import *
# 读取的sql文件路径
path = "./test.sql"
text = ""


# 读取sql文件返回字符串
def read_sql_file(path):
    f = open(path, 'r')
    return f.read()


# 主函数
def main():
    # nfa = NFA()
    # dfa = DFA(nfa)
    # print(dfa)
    pattern = "[^\.0-9]"
    ret = re.match(pattern, "5")
    if ret:
        print(ret.group())


if __name__ == '__main__':
    main()
