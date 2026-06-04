#include <stdio.h>
#include <stdlib.h>

// 메모리 영역에 대한 정리
// 메모모리의 형태
/* * * * * * * * * * * * 
[stack] - 지역 변수, 매개변수, 함수 호출 정보가 저장되는 공간
 ▼ ▼ stack메모리는 필요 시 아래로 확장 ▼ ▼
  [           유휴 공간 존재           ]
 ▲ ▲ heap메모리는 필요 시 위쪽으로 확장 ▲ ▲ 
[heap] - 동적으로 할당되는 변수나 객체가 저장됨
[bss] - 초기화되지 않은 전역 변수 및 정적 변수. 
        └ 초기화되어도 위치가 바뀌지 않음. 런타임 시점에 메모리 할당 후 0으로 채워 초기화
[data] - 초기화된 전역 변수 및 정적 변수
[code] - 프로그램의 실행 명령이 저장되는 읽기 전용 공간
* * * * * * * * * * * * */

// bss 영역으로 이동
int varBss1;
int varBss2 = 0;

// data 영역으로 이동
int a = 1;

// 현재 파일에서만 접근 가능한 변수로 이동 (/data)
static int varBss3 = 10;

int* counter() {
  printf("\n --- counter() --- \n");
  // bss 영역에 존재
  static int count = 0;

  printf("counter().count++ = %d\n", count++);
  // stack로 anchor 생성
  int anchor = 10;
  printf("counter().anchor = %d\n", anchor);
  printf("counter().anchor addr = %p\n", &anchor);
  
  return &anchor;
}

int* getIntArray(int size) {
  int* arr = malloc(sizeof(int) * size); // 4 * size

  return arr;
}

int main() {
  for(int i=0;i<10;i++){
    int *anchor = counter();
    printf("anchor addr: %p\n", anchor);
    // printf("anchor: %d\n", *anchor);

    printf("\n --- counter() return anchor --- \n");
  }

  int size = 10;
  int* arr = getIntArray(size);
  for(int i=0;i<size;i++) {
    *(arr + i) = i*10;
  }

  for(int i=0;i<size;i++) {
    printf("%d ", arr[i]);
  }
  printf("\n");

  free(arr);
  // printf("after free(arr); arr = %p", arr);
  arr = NULL;
  printf("after arr = NULL; arr = %p", arr);
  return 0;
}