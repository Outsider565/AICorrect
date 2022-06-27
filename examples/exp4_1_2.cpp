//OOP的作业之一，写一个链表，这里是示意的简化版
//运行时错误-segfault错误-堆访问错误
#include <iostream>

using namespace std;
struct Node{
    int val;
    Node* next;
};

Node* init_link_list(){
    //哨兵节点
    Node* n = new Node;
    n->val = 0;
    n->next = nullptr;
    return n;
}

Node* push_back_val(Node* head, int val){
    auto p = head;
    while(p->next!=nullptr){
        p = p->next;
    }
    auto n = new Node;
    n->val = val;
    n->next = nullptr;
    p->next = n;
}

int get_ith(Node* head, int i){
    auto p = head;
    while(i-- > 0){
        p = p->next;
    }
    return p->val;
}

int main(){
    auto n = init_link_list();
    push_back_val(n, 1);
    push_back_val(n, 2);
    push_back_val(n, 3);
    push_back_val(n, 4);
    get_ith(n,1);
    get_ith(n,5);
}