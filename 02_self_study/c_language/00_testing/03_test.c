#include <stdio.h>
#include <stdlib.h>

// bss 위치의 초기화되지 않은 데이터
int bssVar;

int a = 10;

void first() {
  printf("%p\n", &bssVar);
  printf("%d\n", bssVar);
  bssVar = 10;
  printf("%d\n", bssVar);
  printf("%p\n", &bssVar);
}

void counter() {
  static long c = 0;
  printf("counter called [%d]\n", c++);
}

void execute1() {
  // stack
  int s = 10;

  for(int i=0;i<10;i++){
    counter();
  }
}

void execute2() {
  printf("sizeof(int): %lld\n", sizeof(int));
  printf("sizeof(long long): %lld\n", sizeof(long));

  struct Box{
    int a;
    long b;
    long long c;
  };

  printf("sizeof(char): %lld\n", sizeof(char));
  printf("sizeof(Box[int + long + long long]): %lld\n", sizeof(struct Box));
}

void execute3() {
  int *p = malloc(sizeof(int) * 5);
  printf("sizeof(p): %zu\n", sizeof(p));
  printf("sizeof(*p): %zu\n", sizeof(*p));
  printf("\n");
  printf("p: %p\n", p);
  printf("p[0]: %p\n", &p[0]);
  printf("p[1]: %p\n", &p[1]);
  printf("p[2]: %p\n", &p[2]);
  printf("p[3]: %p\n", &p[3]);
  printf("p[4]: %p\n", &p[4]);
  printf("p[5]: %p\n", &p[5]);

  printf("&p[5] - &p[2] = %p\n", (&p[5] - &p[2]));

  char *c = malloc(1);
  *c = 'c';
  printf("c: %p\n", c);
  printf("&p[5] - c = %p\n", (c));

  for(int i=0;i<20;i++){
    printf("(p-%d): %d\n", i, *(p-i));
  }

  *(4+p) = 10;
  printf("*(p+4) = 10; %p\n", p+4);
  printf("p[4] = %d\n", p[4]);
  free(c);
  free(p);
}

int main() {
  execute3();
}