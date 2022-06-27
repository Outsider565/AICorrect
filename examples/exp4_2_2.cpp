#include <iostream>
#include <vector>
using namespace std;

int main(){
    vector<int> vec{1,2,3};
    auto sz = vec.size();
    auto sum = 0;
    while(--sz >= 0){ //问题在sz是size_type型变量，即是uint32_t的别名，因此永远不可能小于0；
        sum += vec[sz];
    }
}