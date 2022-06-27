//例子2_1_1，语法错误-域错误
#include <iostream>

int max(int a, int b) { return a > b ? a : b; }

int main() {
    //找arr数组中的最大值
    int arr[] = {0, 1, 2, 3, 4, 5};
    int m = arr[0];
    for (int i = 1; i < 6; i++) {
        m = max(arr[i], m);
    }
    cout << m;
    return m;
}