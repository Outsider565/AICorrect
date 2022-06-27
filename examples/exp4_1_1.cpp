//运行时错误-segfault错误-栈访问错误
#include <iostream>
#include <vector>

int main(){
    //对数组arr求和
    int arr[10]= {0,1,2,3};
    int sum = 0;
    for(int i = 0; i <= 10; i++){
        sum += arr[i];
    }
    std::cout << sum;
    return 0;
}