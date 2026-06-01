// 이중 연결 리스트 만들기
#include <stdio.h>

// malloc/free를 위한 함수 가져오기
#include <stdlib.h>

// 기본 노드
// 20byte (+4)
typedef struct Node{
  // 앞의 노드 주소
  struct  Node *prev;  // 8byte
  // 내용물 (일단 편하게 int)
  int value;   // 4byte
  // 뒤의 노드 주소
  struct  Node *next;    // 8byte 
}Node;

// 노드 결합 구조체
// 20byte (+4)
typedef struct LinkedList{
  int length; // 4byte
  Node *first; // 8byte
  Node *last; // 8byte
} LinkedList;

// 자동으로 하나 만들어주는 함수
LinkedList createList() {
  return (LinkedList){0, NULL, NULL};
}

LinkedList initList(int value) {
  Node *n = malloc(sizeof(Node));

  *n = (Node){NULL, value, NULL};

  return (LinkedList){1, n, n};
}

int getLength(LinkedList ll) {
  return ll.length;
}

// 맨 앞에 노드를 붙여주는 함수 길이는 적당히 까지만 받아주기
int addFirst(LinkedList *ll, int value) {
  if((*ll).length > 999) {
    return 1;
  }
  Node *n = malloc(sizeof(Node));

  *n = (Node){NULL, value, NULL};
  if((*ll).length == 0) {
    (*ll).first = n;
    (*ll).last = n;
    (*ll).length += 1;
    return 0;
  }

  (*n).next = (*ll).first;
  (*(*ll).first).prev = n;
  (*ll).first = n;
  (*ll).length += 1;
  return 0;
}

// int insertNode(LinkedList ll, int value, int index) {

// }

int addLast(LinkedList *ll, int value) {
  if((*ll).length > 999) {
    return 1;
  }
  
  Node *n = malloc(sizeof(Node));

  *n = (Node){NULL, value, NULL};

  if((*ll).length == 0) {
    (*ll).first = n;
    (*ll).last = n;
    (*ll).length += 1;
    return 0;
  }

  (*n).prev = (*ll).last;
  (*(*ll).last).next = n;
  (*ll).last = n;
  (*ll).length += 1;
  return 0;
}

int removeFirst(LinkedList *ll) {
  // 0개일 때
  if((*ll).length <= 0) {
    return -1;
  }
  // 1개일 때
  else if((*ll).first == (*ll).last) {
    Node *old = (*ll).first;
    (*ll).first = NULL;
    (*ll).last = NULL;

    free(old);

    (*ll).length -= 1;
    return 0;
  }

  Node *old = (*ll).first;
  Node *tmp = (*(*ll).first).next;

  free(old);
  
  (*tmp).prev = NULL;
  (*ll).first = NULL;
  (*ll).first = tmp;
  (*ll).length -= 1;
  return 0;
}

void printLinkedList(LinkedList ll) {
  Node *n = ll.first;
  for(int i=0;i<ll.length;i++) {
    printf("%d ", (*n).value);
    n = (*n).next;
  }
}

int main() {

  LinkedList ll = createList();

  addFirst(&ll, 10);
  addFirst(&ll, 20);
  addFirst(&ll, 30);
  printLinkedList(ll);
  removeFirst(&ll);

  printLinkedList(ll);

  return 0;
}