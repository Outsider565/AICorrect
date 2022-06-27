//例子2_1_2，语法错误-函数调用错误
#include <iostream>

int max(int a, int b) { return a > b ? a : b; }

void swap(int& a, int &b) {
    int temp = a;
    a = b;
    b = temp;
}

int main() {
    const int a = 5;
    int b = 6;
    swap(a, b);
    return m;
}