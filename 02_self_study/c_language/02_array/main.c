#include <stdio.h>

int main() {

  // 일단 배열 생성
  char str[] = "hello";
  
  long a = 1;

  // 
  printf("%lld\n", sizeof(a));
  // long = 4byte

  printf("%lld\n", sizeof(str));
  // 6 - h + e + l + l + o + \0
  // char = 1byte

  printf("%p\n", &a);
  
  long b = 1030;
  int c = 1;

  printf("%p\n", &a);
  printf("%p\n", &b);
  printf("%p\n", &c);
  printf("%lld\n", sizeof(&c));


  void *obj[] = {&a, &b, &c, str };

  printf("\n --- \n");
  for (int i = 0; i < 4; i++) {
    printf("%p\n", obj[i]);
  }
  
  printf("%c\n", *((char *)obj[3]));
  printf("%s\n", (char *)obj[3]);

  printf("%p\n", str);
  printf("%p\n", &str[0]);
  printf("%p\n", &str[1]);
  printf("%p\n", &str[2]);
  printf("--- end ---\n");

  for(int i=0;i<10;i++) {
    printf("%c, ", *(&str[0] + i));
  }
  printf("\n");

  printf("--- end2 ---\n");

  str[3] = '\0';

  printf("%s\n", (char *)str);

  printf("--- end3 ---\n");

  for(int i=0;i<10;i++) {
    printf("%c, ", *(&str[0] + i));
  }
  printf("\n");

  return 0; 
}