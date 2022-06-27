//例子1_2_1，名错误-变量名错误
#include <iostream>
using namespace std;

int max(int a, int b) { return a > b ? a : b; }

int main() {
    //找arr数组中的最大值
    int arr[] = {0, 1, 2, 3, 4, 5};
    int m = arr[0];
    for (int i = 1; i < 6; i++) {
        m = max(ar[i], m);
    }
    return m;
}