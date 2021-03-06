# AICorrect——面向初学者的人工智能辅助调试专家系统

## 项目背景

本学期我担任面向对象程序设计一课的助教，选修该门课程的学生多为大一新生，该门课程的所有作业需要使用C++完成。在我给同学们答疑的过程中，我发现因为C++这门语言的复杂性、现存的编译器报错信息不够智能化、及新生对链接机制和GDB等调试工具的不熟悉，许多同学无法独立解决程序中错误。很有趣的是，许多来找我问问题的同学错误都十分相似，甚至一模一样。

因此，我决定针对初学者，设计一个结合基于规则的推理系统和模糊逻辑系统的辅助调试专家系统。其能根据编译器警告和报错、链接器的报错、运行时行为及与标准答案的差异，提供一个辅助调试的工具。该工具将以面向对象程序设计实验2为例，展示其功能。

## 项目设计

初学者的常见错误一般可以分为以下三种:
- 编译错误：
  - 词法错误：
    - 关键字错误：初学者经常记错关键字，比如`int64_t`和`int64`，这是一个词法错误。
      - 原生类型错误(exp1_1_1.cpp)
      - 预处理指令错误(exp1_1_2.cpp)
      - 语言关键字错误(exp1_1_3.cpp):g++的报错几乎无法猜出是拼错了，一般会写xxx does not name a type
    - 名错误：初学者容易记错/打错变量名或者函数名，如前文写的是handleInput()，而实际输入的是handlelnput()，因为有的字体下I和l比较难区分，初学者看到undefined variable handlelnput()，就会比较迷惑。
      - 变量名错误(exp1_2_1.cpp)
      - 函数名错误(exp1_2_2.cpp)
  - 语法错误：
    - 域错误：初学者容易不加域名，最常见的错误是不加std::(exp2_1_1.cpp)
    - 函数调用错误：初学者在调用函数时，很容易传入类型不匹配的参数，尤其是在该函数为重载函数，或者参数为const型时(exp2_1_2.cpp)
    - 模板匹配错误：g++等编译器对模板匹配的报错比较晦涩难懂，常常一个简单的错误参数会影响十几个(互相依赖或有继承关系的)模板类，因此初学者很难弄明白错误在哪
    - 库引用错误：初学者没有引用函数所需要的库，例如在抛出exception时经常忘记引用stdexcept
- 链接错误：
  - 文件错误：因为初学者对命令行编译工具不熟悉，所以在命令行中输入的文件路径有错。这样时常会出现undefined reference to `function`，因为链接器没有找到该函数。
  - 重定义错误：初学者在引用.h文件时，时常忘记#ifndef保护或者#pragma once保护，这样会出现重定义错误。除此之外，因为初学者的疏忽，也可能无意中定义两个名字相同的函数
  - 主函数未定义错误：初学者尝尝不加主函数或者写错主函数，例如把main写成mian
- 运行时错误：
  - segfault错误：初学者写的程序在运行时尝尝会出现segfault意外退出，但因为部分系统下的debugger较难安装或者较难使用，所以初学者很难定位问题。常出现的原因是数组越界或者野指针。
  - 堆访问错误：初学者写的程序在运行时尝尝会出现堆访问错误，这样可能是因为初学者没有考虑到堆的分配和释放，或者没有考虑到堆的管理。虽然在部分系统上不会报错，但给程序留下的隐患。例如new的变量没有delete，或者访问了不存在的堆内存空间。
  - 与标准答案不符：OOP一课的Lab会给出与标准答案对比的评分脚本，学生可以看到自己的程序的输出与标准程序的输出是否相同。

编译错误和链接错误可以借由词法分析工具、语法分析工具和编译器报错信息来判断，规则较为明确，因此采用基于规则的推理系统。但是运行时错误可能的原因较多，较为复杂，因此采用基于模糊逻辑系统。

该系统的推理引擎及web后端均使用Python，前端使用React框架。为了省去初学者配置的困难，该项目将打包成docker镜像，并且提供一个web界面，用户可以在该界面上提交程序，并且查看程序的运行结果。

## 基于规则的推理系统

在本项目中，基于规则的推理系统不使用额外的推理引擎，使用Python自带的if-else语句来推理。
详见backend/engine.py，共15条规则


## 模糊逻辑系统

在本项目中，使用scikit-fuzzy库来实现模糊逻辑系统。
详见backend/runtime_error.py，共63条规则，模糊逻辑系统的拓扑图如下：
![](https://github.com/Outsider565/AICorrect/blob/main/imgs/fuzzy_system.png)

## 运行效果
![](https://github.com/Outsider565/AICorrect/blob/main/imgs/compile_error.jpg)
![](https://github.com/Outsider565/AICorrect/blob/main/imgs/link_error.jpg)
![](https://github.com/Outsider565/AICorrect/blob/main/imgs/runtime_error.jpg)

