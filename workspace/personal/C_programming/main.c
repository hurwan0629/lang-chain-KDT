#include <stdio.h>
#include <stdlib.h>
int a = 0;


// int *p = malloc(4);
// p = 12;
// printf("%d\n", p);
// free(p);
// p = NULL;

typedef struct {
    int value;
    void (*print)(int);
} Box;

void print_value(int x) {
    printf("value: %d", x);
}

int* something() {
    int *p = malloc(4);
    *p = 10;
    printf("%p\n", p);
    printf("%d\n", *p);
    // free(p);
    return p;
}

int main(void) {
    int *pp = something();
    // pp = 10;
    printf("%p\n", pp);
    printf("%d\n", *pp);
    free(pp);
    printf("%d\n", *pp);
    pp = NULL;
    return 0;
}