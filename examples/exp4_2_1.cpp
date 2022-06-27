#include <iostream>
//该程序为计算斐波那契数列的程序
using namespace std;

int fib(int n){
    //因为没有设置递归中止条件，所以无限递归了
    return fib(n-1)+fib(n-2);
}

int main(){
    cout << fib(5);
}