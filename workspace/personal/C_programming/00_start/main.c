#include <stdio.h>
#include <stdlib.h>

// BSS 영역에서 존재하는 0 또는 NULL같이 초기화 되지 않은 변수의 영역
// 0
// 초기화 되지 않은 전역 변수
// 초기화 되지 않은 정적 변수
/*
왜 초기화되지 않은 변수를 위한 공간이 따로 있는 것일까?

예를 들어서 `int arr[99999999]; 와 같은 초기화가 존재할 때 0으로 매워진 공간이 매우 많아지기
때문에 이를 채우지 않고 일단 임시 저장 해놓기 위해 BSS라는 공간을 활용한다.

이는 C에만 있는 개념은 아니지만 일반적으로 고급 언어에서는 사용자가 느끼기 어려운 특징을 가지고있다.
*/
// BSS 영역에 존재하게 될 a 변수
int a = 0;

// data 영역으로 가게 될 전역 변수 c=10
int c = 10;

// 실제로 메모리의 구조상으로는 보통 [code] > [data] > [BSS] > [Heap] > [Stack]
// 과 같은형태로 설명합니다.
// 이 때문에 그림상으로는 비슷해 보일 수 있어도 성격은 완전히 다르게 됩니다.

typedef struct
{
  int value;
  void (*print)(int);
} Box;

void print_value(int x)
{
  printf("value: %d", x);
}

int *something()
{
  static int count = 0;
  count++;
  printf("count: %d\n", count);
  int *p = malloc(4);
  *p = 10;
  printf("%p\n", p);
  printf("%d\n", *p);
  free(p);
  return 0;
}

int main(void)
{
  // int *pp = something();
  // pp = 10;
  // printf("%p\n", pp);
  // printf("%d\n", *pp);
  // free(pp);
  // printf("%d\n", *pp);
  // printf("%d\n", pp);
  // pp = NULL;
  something();
  something();
  something();
  something();
  return 0;
}