# SQL_compiler
TJU编译原理大作业
## 词法分析器与语法分析器设计

### 1 目录结构
```
SQL_COMPLIER
 |-lexical-analysis
    |-input
      |-test0A.sql
      |-test0B.sql
    |-output
      |-13Alex.tsv
      |-13Blex.tsv
    |-NFA.py
    |-NFAtoDFA.py
    |-DFAtoMFA.py
    |-lexer.py
    |-main.py
    |-README.md
 |-synatax-annalysis
    |-input
      |-0Alex.tsv
      |-0Blex.tsv
    |-output
      |-13Agra.tsv
      |-13Bgra.tsv
    |-LL.py
    |-LR.py
    |-sql_syntax.txt
    |-README.md
 |-README.md
```
 ### 2 运行词法分析器
 * 修改词法分析输入文件，即修改`mian.py`中`path`变量，输入文件在`input`文件夹下。
   ```python
    path = "./input/test0B.sql"
   ```
 * 修改词法分析器结果输出文件，即修改`lexer.tokenTable.save_token_table()`函数的参数，结果保存在`output`文件夹下。
   ```python
   lexer.tokenTable.save_token_table("./output/13Blex.tsv")
   ```
 * 运行词法分析器命令
   ```Batch
    cd lexical-analysis
    python main.py
   ```

 ### 3 运行语法分析器
 * 运行语法分析器命令
   ```Batch
    cd syntax-analysis
    python LL.py
    python LR.py
   ```
 * 输入语法分析结果文件名，例：13Agra.tsv，结果保存在`output`文件夹下。
 * 输入`input`文件夹下需进行语法分析的文件名，例：0Alex.tsv。



 
