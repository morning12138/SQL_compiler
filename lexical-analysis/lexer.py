from NFA import *
from NFAtoDFA import *


class Token:
    def __init__(self, lexeme: str, token_type: str, token_num: str):
        self.lexeme = lexeme
        self.tokenType = token_type
        # 说是num，其实不是全是num，所以还是用str类型
        self.tokenNum = token_num


class TokenTable:
    def __init__(self):
        self.tokens = []

    def print_token_table(self):
        for token in self.tokens:
            print("{}   <{},{}>".format(token.lexeme, token.tokenType, token.tokenNum))

    def push_token(self, token: Token):
        self.tokens.append(token)

    def save_token_table(self, path):
        f = open(path, "w+")
        for token in self.tokens:
            f.write("{}   <{},{}>\n".format(token.lexeme, token.tokenType, token.tokenNum))
        f.close()


class Lexer:
    def __init__(self, path: str, token_table: TokenTable, dfa: DFA):
        self.source = open(path, 'r').read()
        self.source += " "
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

            # GROUP BY和ORDER BY特殊处理
            if token_now == "GROUP" or token_now == "ORDER":
                i += 1
                token_now += " "
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

        # 如果最后一个词是属于IDNorKWorOP那么也要加入token_list中

        if not self.dfa.is_final(ID):
            print("Lexical error: 最终一个词不是完整的token")
            return

