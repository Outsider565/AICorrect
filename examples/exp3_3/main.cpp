#include "add1.h"
#include "add2.h"

// 错将main写成了mian
int mian(){
    int a = 0;
    add2(a);
    return a;
}