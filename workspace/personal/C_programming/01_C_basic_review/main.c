#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// bss
int a1;
int a2 = 0;
// data
int b = 10;

// data에 존재하는 structure
struct Box {
  char name[20];
  int value;
};

// 파일 안에서만 쓰일 수 있는 (private한) 함수
static void helloBasic() {
  // bss로 시작해서 값이 추가되는 시점에 data영역으로
  static int called = 0;

  called++;

  printf("helloBasic called: %d\n", called);
  return;
}

int main() {
  helloBasic();
  helloBasic();
  helloBasic();
  helloBasic();

  struct Box box = {
    "first box", 20
  };

  printf("name: %s\nvalue: %d\n", box.name, box.value);

  struct Box *bp = &box;

  printf("pb-name: %s\npb-value: %d\n", bp->name, bp->value);

  strcpy(box.name, "pointed box");

  printf("name: %s\nvalue: %d\n", box.name, box.value);
  printf("pb-name: %s\npb-value: %d\n", bp->name, bp->value);

  printf("%p\n", &box);

  return 0;
}