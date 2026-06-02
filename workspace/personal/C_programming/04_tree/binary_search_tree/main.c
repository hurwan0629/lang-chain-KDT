// 이진 탐색 트리 만들어보기
//////////// [조건] ////////////
// 이진트리
// 크기가 [왼쪽자식] < [부모] < [오른쪽 자식] 고정
#include <stdio.h>
#include <stdlib.h>

// 노드 만들기
// [내 주소(기본)] [내 값] [왼쪽 자식 주소] [오른쪽 자식 주소]
struct Node{
    int value;
    struct Node *left;
    struct Node *right;
    int count; // 중복된 데이터 개수
};

typedef struct BinarySearchTree{
    int count;
    struct Node *root;
}BinarySearchTree;

// 자동정렬 하기 때문에 insertByIndex는 필요 없음

// insert(value) 만들기
int insert(BinarySearchTree *bst, int newVal) {
    // 비거나 이상한 트리의 경우 초기화해주기
    if((*bst).count <= 0) {
        (*bst).root = malloc(sizeof(struct Node));
        *(*bst).root = (struct Node){newVal, NULL, NULL, 1};
        (*bst).count = 1;
        return 0;
    }

    // 탐색 후 추가해주기
    struct Node *root = (*bst).root;
    struct Node *nextNode = NULL;
    if((*root).value < newVal) {
        if((*root).right == NULL) {
            (*root).right = malloc(sizeof(struct Node));
            *(*root).right = (struct Node){newVal, NULL, NULL, 1};
            (*bst).count += 1;
            return 0;
        }
        nextNode = (*root).right;
    }
    else if((*root).value > newVal) {
        if((*root).left == NULL) {
            (*root).left = malloc(sizeof(struct Node));
            *(*root).left = (struct Node){newVal, NULL, NULL, 1};
            (*bst).count += 1;
            return 0;
        }
        nextNode = (*root).left;
    }
    else if((*root).value == newVal) {
        (*root).count += 1;
        (*bst).count += 1;
        return 0;
    }
    while(1) {
        if((*nextNode).value < newVal) {
            if((*nextNode).right == NULL) {
                (*nextNode).right = malloc(sizeof(struct Node));
                *(*nextNode).right = (struct Node){newVal, NULL, NULL, 1};
                (*bst).count += 1;
                return 0;
            }
            nextNode = (*nextNode).right;
        }
        else if((*nextNode).value > newVal) {
            if((*nextNode).left == NULL) {
                (*nextNode).left = malloc(sizeof(struct Node));
                *(*nextNode).left = (struct Node){newVal, NULL, NULL, 1};
                (*bst).count += 1;
                return 0;
            }
            nextNode = (*nextNode).left;
        }
        else if((*nextNode).value == newVal) {
            (*nextNode).count += 1;
            (*bst).count += 1;
            return 0;
        }
    }
}

// delete(value) 만들기
int delete(BinarySearchTree *bst, int delVal) {
    struct Node *node = (*bst).root;
    // 값이 없으면 그냥 -1 출력
    if(node == NULL) {
        return -1;
    }


    // 루트인 경우
    if((*node).value == delVal) {
        // 중복이 남아있으면 줄여주기
        if((*node).count > 1) {
            (*bst).count -= 1;
            (*node).count -= 1;
            return 0;
        }
        // 자식이 없으면 제거
        if((*node).left == NULL && (*node).right==NULL) {
            (*bst).root = NULL;
            (*bst).count = 0;
            free(node);
            return 0;  
        }
        // 1. 오른쪽 자식이 없는경우 
        // 왼쪽 트리 그냥 올려버리기
        else if((*node).right == NULL) {
            (*bst).root = (*node).left;
            (*bst).count -= 1;
            free(node);
            return 0;
        }
        // 2. 왼쪽 자식이 없는 경우
        else if((*node).left == NULL) {
            (*bst).root = (*node).right;
            (*bst).count -= 1;
            free(node);
            return 0;
        }
        // 3. 양쪽 자식이 있는 경우
        else {
            struct Node *subNode = (*node).right;
            
            // 바로 오른쪽 자식이 가장 작은값일 때
            if((*subNode).left == NULL) {
                (*bst).root=subNode;
                
                (*subNode).left = (*node).left;
                (*bst).count -= 1;
                free(node);
                return 0;
            }
            // 바로 오른쪽 자식이 가장 작은값이 아닐 때
            struct Node *prevSubNode = NULL;
            while((*subNode).left != NULL) {
                prevSubNode = subNode;
                subNode = (*subNode).left;
            }

            // subNode의 오른쪽에 값이 있을 수 있으므로 subNode > delNode를 할 때 
            // subNode의 오른쪽 자식을 이식해줘야함

            (*prevSubNode).left = (*subNode).right;
            (*bst).root = subNode;
            (*subNode).left = (*node).left;
            (*subNode).right = (*node).right;
            (*bst).count -= 1;
            free(node);
            return 0;
        }
         
    }

    // 삭제할 노드의 부모 저장용
    struct Node *prevNode = NULL;
    // 좌/우 중에 저장 (prevNode->n 을 하기 위해)
    // 0은 좌, 1은 우
    int lastMove = 0;
    // 삭제할 노드 저장용
    struct Node *delNode = NULL;

    // 위치를 찾을 때까지 탐색
    while(1) {
        if((*node).value == delVal) {
            delNode = node;
            break;
        }
        // 삭제할 노드 탐색 중 삭제할 값이 노드보다 작으면
        // 외쪽 노드로 내려가기
        else if((*node).value > delVal) {
            if((*node).left != NULL) {
                // 부모 저장
                prevNode = node;
                lastMove = 0;
                // 자식으로 이동
                node = (*node).left;
            }
            else {
                return -1;
            }
        }
        // 삭제할 노드 탐색 중 삭제할 값이 노드보다 작으면
        // 오른쪽 노드로 내려가기
        else {
            if((*node).right != NULL) {
                // 부모 저장
                prevNode = node;
                lastMove = 1;
                // 자식으로 이동
                node = (*node).right;
            }
            else {
                return -1;
            }
        }
    }

    // 노드의 중복수가 2 이상이면 줄이고 끝내기
    if((*delNode).count > 1) {
        (*delNode).count -= 1;
        (*bst).count -= 1;
        return 0;
    }

    // 0. 양쪽 자식이 없는경우
    else if((*delNode).left == NULL && (*delNode).right == NULL) {

        // 뭐 더 하지 않고 삭제.
        if(lastMove) {
            (*prevNode).right = NULL;
        }
        else {
            (*prevNode).left = NULL;
        }
        (*bst).count -= 1;
        // delNode의 
        free(delNode);
        return 0;
    }
    // 1. 오른쪽 자식이 없는경우 
    // 왼쪽 트리 그냥 올려버리기
    else if((*delNode).right == NULL) {
        if(lastMove) {
            (*prevNode).right = (*delNode).left;
        }
        else {
            (*prevNode).left = (*delNode).left;
        }
        (*bst).count -= 1;
        free(delNode);
        return 0;
    }
    // 2. 왼쪽 자식이 없는 경우
    else if((*delNode).left == NULL) {
        if(lastMove) {
            (*prevNode).right = (*delNode).right;
        }
        else {
            (*prevNode).left = (*delNode).right;
        }
        (*bst).count -= 1;
        free(delNode);
        return 0;
    }
    // 3. 양쪽 자식이 있는경우
    // 오른쪽에서 가장 작은 값 찾아서 대체시키기
    else {
        struct Node *prevSubNode = NULL;
        struct Node *subNode = (*delNode).right;

        // 바로 오른쪽 자식이 가장 작은값일 때
        if((*subNode).left == NULL) {
            if(lastMove) {
                (*prevNode).right = subNode;
            }
            else {
                (*prevNode).left = subNode;
            }
            (*subNode).left = (*delNode).left;
            (*bst).count -= 1;
            free(delNode);
            return 0;
        }
        // 바로 오른쪽 자식이 가장 작은값이 아닐 때
        while((*subNode).left != NULL) {
            prevSubNode = subNode;
            subNode = (*subNode).left;
        }

        // subNode의 오른쪽에 값이 있을 수 있으므로 subNode > delNode를 할 때 
        // subNode의 오른쪽 자식을 이식해줘야함

        (*prevSubNode).left = (*subNode).right;
        if(lastMove) {
            (*prevNode).right = subNode;
        }
        else {
            (*prevNode).left = subNode;
        }
        (*subNode).left = (*delNode).left;
        (*subNode).right = (*delNode).right;
        (*bst).count -= 1;
        free(delNode);
        return 0;
    }


}

// 유틸용 함수 구하기
// struct Node* getLeftNodeValue(struct Node *n){
//     if((*n).left != NULL) {
//         return (*n).left;
//     }
//     return NULL;
// }

// struct Node*  getRightNodeValue(struct Node *n){
//     if((*n).right != NULL) {
//         return (*n).right;
//     }
//     return NULL;
// }

// 중위 순위
void inorder(struct Node *node) {
    if(node == NULL) {
        return;
    }

    if((*node).left != NULL) {
        inorder((*node).left);
    }
    printf("%d: %d\n", (*node).value, (*node).count); // 중복 값들은 생략
    if((*node).right != NULL) {
        inorder((*node).right);
    }
}

// 전위순위
void preorder(struct Node *node) {
    if(node == NULL) {
        return;
    }

    printf("%d: %d\n", (*node).value, (*node).count); // 중복 값들은 생략
    if((*node).left != NULL) {
        preorder((*node).left);
    }
    if((*node).right != NULL) {
        preorder((*node).right);
    }
}

// 후위순위
void postorder(struct Node *node) {
    if(node == NULL) {
        return;
    }

    if((*node).left != NULL) {
        postorder((*node).left);
    }
    if((*node).right != NULL) {
        postorder((*node).right);
    }
    printf("%d: %d\n", (*node).value, (*node).count); // 중복 값들은 생략
}

int main() {
    BinarySearchTree bst =  {0, NULL};

    int values[] = {50, 30, 70, 20, 40, 60, 80, 30, 70};
    int size = sizeof(values) / sizeof(values[0]);

    for (int i = 0; i < size; i++) {
        insert(&bst, values[i]);
    }

    printf("=== init ===\n");
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== 30 discount 30 ===\n");
    delete(&bst, 30);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== 20 delete leaf ===\n");
    delete(&bst, 20);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== 70 delete: discount 70 ===\n");
    delete(&bst, 70);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== 70 delete again (fail) ===\n");
    delete(&bst, 70);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== 50 (root) delete ===\n");
    delete(&bst, 50);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    printf("\n=== non exist value 999 delete ===\n");
    int result = delete(&bst, 999);
    printf("result: %d\n", result);
    printf("count: %d\n", bst.count);
    inorder(bst.root);

    return 0;
}


