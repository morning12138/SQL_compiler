path = "./test.sql"


# 扫描器
def scanner(text):
    return


# 读取sql文件返回字符串
def read_sql_file(path):
    f = open(path, 'r')
    return f.read()


# 主函数
if __name__ == '__main__':
    # global path
    # path = "./test.sql"
    text = read_sql_file(path)
    print(text)