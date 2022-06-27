#include "add1.h"
#include "add2.h"
//因为add1.h和add2.h中均没有ifndef保护，因此会出现重定义错误
int main(){
    int a = 0;
    add2(a);
    return a;
}