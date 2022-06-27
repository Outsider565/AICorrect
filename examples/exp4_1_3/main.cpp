#include "arr.h"

int main(){
    //对数组arr求和
    int sum = 0;
    for(int i = 0; i <= 10; i++){
        sum += arr[i]; //arr的大小是10，但这里访问了第11个元素
    }
    std::cout << sum;
    return 0;
}