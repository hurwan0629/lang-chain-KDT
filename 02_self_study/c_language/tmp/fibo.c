#include <stdio.h>
// 실행 시간 측정을 위한 time.h
#include <time.h>

// 반복적 피보나치수열 계산 함수
// 0부터 시작하는 인덱스 값을 기준으로 피보나치 수열의 인덱스값의 값을 반환
int fiboIter(int index) {
    // 정확한 시간 측정을 위해 로그는 출력하지 않음

    // 1 이하의 경우에는 그냥 반환 가능
    if(index <= 1) {
        return index;
    }

    // 0, 1 부터 시작해서 끝까지 더해가는 방식
    int prev1 = 0;
    int prev2 = 1;
    int tmp;
    for(int i=2;i<=index;i++) {
        tmp = prev2;
        prev2 = prev2 + prev1;
        prev1 = tmp;
        // 입출력 시간 없이
        // printf("%d\n", prev2);
    }
    return prev2;
}

int fiboRecurv(int index) {
    if(index <= 1) {
        return index;
    }
    return fiboRecurv(index-2) + fiboRecurv(index-1);
}

int main() {
    clock_t start = clock();

    // 1000,000번 반복
    for(int i=0;i<1000000;i++) {
        fiboRecurv(10);
    }

    clock_t end = clock();

    double elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("fiboRecurv exec time: %.6fsec\n", elapsed);

    /////////////////////////////////////////////////////////////

    start = clock();

    // 1000,000번 반복
    for(int i=0;i<1000000;i++) {
        fiboIter(10);
    }

    end = clock();

    elapsed = (double)(end - start) / CLOCKS_PER_SEC;

    printf("fibuIter exec time: %.6fsec\n", elapsed);
}

