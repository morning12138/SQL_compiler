from NFA import *
from NFAtoDFA import *
from lexer import *
from DFAtoMFA import *

# 读取的sql文件路径
path = "./test0A.sql"
text = ""


# 读取sql文件返回字符串
def read_sql_file(path):
    f = open(path, 'r')
    return f.read()


# 主函数
def main():
    global path
    nfa = NFA()
    dfa = DFA()
    dfa.determine(nfa)
    mfa = DFAtoMFA(dfa)
    # for i in mfa.nodes:
    #     print('id: ' + str(i.id) + ' isFinal: ' + str(i.isFinal) + ' isBackOff: ' + str(i.isBackOff) + ' tag: ' + str(i.tag))
    # for i in mfa.edges:
    #     print('fromId:'+str(i.fromNodeId)+' tag:'+str(i.tag)+' toNodeId: '+str(i.toNodeIds))
    token_table = TokenTable()
    lexer = Lexer(path, token_table, mfa)
    lexer.run()
    lexer.tokenTable.print_token_table()
    lexer.tokenTable.save_token_table("./test.txt")


if __name__ == '__main__':
    main()
