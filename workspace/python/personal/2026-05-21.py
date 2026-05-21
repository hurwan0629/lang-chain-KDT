# 현재 파이썬의 이해도를 높이기 위해서 "dis" 라이브러리를 통해 파이썬 코드가 어떻게 컴파일되며 실행되는지 알아보려 합니다.

import dis

code = """
x = 10
y = x + 20
print(y)
"""
# compile(source, filename, mode)
# exec는 복수의 문장
compiled = compile(code, "<string>", "exec")
dis.dis(compiled)
print(compiled.co_code)   # 바이트코드
print(compiled.co_consts) # 상수테이블
print(compiled.co_names)  # 네임테이블

#   0           0 RESUME                   0     [상수테이블], [네임테이블]                                                        
#                                                                            
#   2           2 LOAD_CONST               0 (10) [10] []
#               4 STORE_NAME               0 (x) [10] [x]
#   
#   3           6 LOAD_NAME                0 (x) [10] [x]
#               8 LOAD_CONST               1 (20) [10, 20] [x]
#              10 BINARY_OP                0 (+) [10, 20] [x] *(`+`는 연산번호 0번)
#              14 STORE_NAME               1 (y) [10, 20] [x, y]
# 
#   4          16 PUSH_NULL
#              18 LOAD_NAME                2 (print) [10, 20] [x, y, print]
#              20 LOAD_NAME                1 (y) [10, 20] [x, y, print]
#              22 CALL                     1 [10, 20] [x, y, print]
#              30 POP_TOP
#              32 RETURN_CONST             2 (None) [10, 20, None] [x, y, print]

"""
0. RESUME: 최초 실행으로 추정
2. x = 10
- LOAD_CONST: 실행 스택에 10 올리기 
- STORE_NAME: 스택에서 값을 꺼내서 이름 x에 연결함 -> 현재 namespace에 x -> 10 연결

3. y = x + 20
- LOAD_NAME: x가 가리키는 값 10을 스택에 올림
- LOAD_CONST: 20을 실행 스택에 올리기
- BINANRY_OP: 이진 계산 실행 (30을 스택에 올림)
- STORE_NAME: 30을 꺼내 y에 바인딩하기

4. print(y)
- PUSH_NULL: 함수 호출을 위한 내부 준비값
- LOAD_NAME: print함수 객체를 스택에 올림
- LOAD_NAME: y가 가리키는 값 30을 스택에 올림
- CALL 1: 인자 1개로 print(30) 호출
- POP_TOP: print가 반환한 None을 버림
- RETURN_CONST: 코드 블록 전체가 None을 반환하고 종료
"""

# 명령어 별 의미와 숫자 열들의 의미
"""
결과를 기준으로 순서대로
[원본 코드의 줄 번호] [bytecode의 명령어 위치] [명령어 이름] [명령어 인자 벊] [사람이 보기 좋게 해석한 값]


---

상수테이블, 네임테이블, 바이트코드는 모두 Python 프로세스의 메모리에 존재합니다.



"""