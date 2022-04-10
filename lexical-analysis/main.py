from NFA import *
from NFAtoDFA import *
from lexer import *

# 读取的sql文件路径
path = "./test.sql"
text = ""


# 读取sql文件返回字符串
def read_sql_file(path):
    f = open(path, 'r')
    return f.read()


# 主函数
def main():
    global path
    nfa = NFA()
    dfa = DFA(nfa)
    token_table = TokenTable()
    lexer = Lexer(path, token_table, dfa)
    lexer.run()
    print(lexer)
    # pattern = "[ ]"
    # if re.match(pattern, " "):
    #     print("Hello")
    # print("No")


if __name__ == '__main__':
    main()
