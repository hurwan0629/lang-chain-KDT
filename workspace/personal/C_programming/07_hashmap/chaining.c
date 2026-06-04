// 체이닝 방식으로 연결 리스트 구현하기 
#include <stdio.h>
#include <stdlib.h>

// 유연한 자료구조 삽입을 위한 구조체 
// 키, 값을 모두 int로 설정
struct Box {
    int key;
    int value;
    struct Box *next;
};

// 해시맵 (일반 맵을 가지는 구조체)
struct HashMap{
    // 사용률을 나타내기 위한 변수
    int length;
    int used;

    // 실제로 들어가게 될 객체의 리스트.
    // (Box *)의 리스트 공간을 만들어주는 방식
    struct Box **box;
};

// 해시맵을 만들어주는 함수
struct HashMap* getMap(int length) {
    // HashMap의 공간 할당
    struct HashMap *map = malloc(sizeof(struct HashMap));

    (*map).length = length;
    (*map).used = 0;
    // 초기화와 함께 Box의 포인터 배열 저장
    (*map).box = calloc(length, sizeof(struct Box*));

    return map;
};

// 해싱은 간단하게 나눈 나머지
int hash(int key, int length) {
    return key%length;
}

// 해시맵에 자료를 추가하는 함수
int insertHashMap(struct HashMap *map, int key, int value) {
    int index = hash(key, (*map).length);

    // 추가할 공간
    // (충돌 가능성 남아있는 상태)
    struct Box *first = (*map).box[index];

    // 없을 때까지 오른쪽으로 이동 (같은 값인 경우에는 패스)
    while(first != NULL) {
        // 이미 있는 키라면 값 변경
        if((*first).key == key) {
            // 값 변경
            (*first).value = value;
            return 0;
        }
        // 다음 체인으로 이동
        first = (*first).next;
    }

    // 연결 리스트의 맨 앞에 넣기
    struct Box *new = malloc(sizeof(struct Box));
    (*new).key = key;
    (*new).next = (*map).box[index];
    (*new).value = value;

    (*map).box[index] = new;
    (*map).used++;
    return 0;
}

int deleteElement(struct HashMap *map, int key) {
    int index = hash(key, (*map).length);
    // 처음부터 탐색
    struct Box *first = (*map).box[index];

    if(first == NULL) {
        // 존재하지 않는 키값
        // 에러는 아니지만 그냥 -1 반환
        return -1;
    }
    // 찾거나 끝까지 갈때까지 반복
    struct Box *prev = NULL;
    while(first != NULL && (*first).key != key) {
        // 다음으로 이동
        prev = first;
        first = (*first).next;
    }

    if(first == NULL) {
        return -1;
    }
    // 찾았는지 확인
    if((*first).key == key) {
        // 찾았으면 첫번째인 경우
        if(prev == NULL) {
            (*map).box[index] = (*first).next;
            free(first);
            (*map).used--;
            return 0;
        }
        // 뒤에꺼 연결해줘야 하는 경우
        (*prev).next = (*first).next;
        free(first);
        (*map).used--;
        return 0;
    }

    // 못찾았으면
    return -1;
}

// 삭제와 매우 유사 (삭제할 값 찾기이므로)
int getElement(struct HashMap *map, int key) {
    int index = hash(key, (*map).length);
    // 처음부터 탐색
    struct Box *first = (*map).box[index];

    if(first == NULL) {
        // 존재하지 않는 키값
        // 에러는 아니지만 그냥 -1 반환
        return -1;
    }
    // 찾거나 끝까지 갈때까지 반복
    while(first != NULL && (*first).key != key) {
        first = (*first).next;
    }
    if(first == NULL) {
        return -99999;
    }
    // 찾았는지 확인
    if((*first).key == key) {
        // 찾았으면 반환
        return (*first).value;
    }
    // 찾지 못했으면 -99999 반환
    return -99999;
}

int main() {
    struct HashMap *map = getMap(8);

    insertHashMap(map, 9, 10);
    insertHashMap(map, 17, 20);
    insertHashMap(map, 25, 30);

    printf("9  = %d\n", getElement(map, 9));
    printf("17 = %d\n", getElement(map, 17));
    printf("25 = %d\n", getElement(map, 25));

    deleteElement(map, 17);
    printf("17 after delete = %d\n", getElement(map, 17));

    return 0;
}