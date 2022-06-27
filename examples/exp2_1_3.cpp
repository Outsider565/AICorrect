//例子2_1_3 语法错误-模板匹配错误
#include <iostream>
#include <algorithm>
#include <list>
using namespace std;

int main(){
    std::list<int> l{1,2,3,4,5};
    l.sort(); //正确sort list的方式
    sort(l.begin(), l.end()); //该sort需要Random Access Iterator，因此在这里会模板匹配错误
}