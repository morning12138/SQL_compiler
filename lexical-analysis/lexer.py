from NFA import *
from NFAtoDFA import *


class Token:
    def __init__(self, lexeme: str, token_type: str, token_num: int):
        self.lexeme = lexeme
        self.tokenType = token_type
        self.tokenNum = token_num


class TokenTable:
    def __init__(self):
        self.tokens = []

    def print_token_table(self):
        for token in self.tokens:
            print(token.lexeme + "   " + "<" + token.tokenType + "," + token.tokenNum + ">")

    def push_token(self, token: Token):
        self.tokens.append(token)


class Laxer:
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
        for i in range(0, len(text)):
            # 需要跳过的情况
            ch = text[i]
            if ch == "\n":
                continue

            token_now += ch


        pass
