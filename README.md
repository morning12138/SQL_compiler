# SQL_compiler
TJU编译原理大作业
## 1 词法分析器设计

### 1.1 需要识别的单词符号

#### 1.1.1 关键词

- [ ] SELECT, FROM, WHERE, AS
- [ ] INSERT, INTO, VALUES

- [ ] UPDTE
- [ ] DELETE
- [ ] JOIN, LEFT, RIGHT
- [ ] MIN, MAX, AVG, SUM
- [ ] UNION, ALL
- [ ] GROUP BY, HAVING, DISTINCT, ORDER BY
- [ ] TRUE, FALSE, IS, NOT, NULL

#### 1.1.2 运算符

- [ ]  =, >, < , >=, <=, !=, <=>
- [ ] AND, &&, ||, OR, XOR
- [ ] .

#### 1.1.3 界符

- [ ] (, ), **,**  注：**逗号也是**

#### 1.1.4 标识符

- [ ] 由字母、数字和下划线（_）组成的不以数字开头的串

#### 1.1.5 整数和浮点数

- [ ] 整数（sql支持16进制二进制吗？）
- [ ] 浮点数

#### 1.1.6 字符串

- [ ] 字符串



### 1.2 输出

**[待测代码中的单词符号] [TAB] <[单词符号种别],[单词符号内容]>**

![image-20220404154348601](C:\Users\86150\AppData\Roaming\Typora\typora-user-images\image-20220404154348601.png)
