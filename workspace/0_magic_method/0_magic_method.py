# --- 제너레이터 ---
class Counter:
    # 생성자
    def __init__(self, max):
        self.max = max
        self.current = 0
    
    # iterator의 사용 함수
    def __iter__(self):
        return self
    
    # iterator의 다음 함수
    def __next__(self):
        if self.current < self.max:
            self.current += 1
            return self.current
        else:
            raise StopIteration

counter = Counter(5)
for num in counter:
    print(num)
# 1
# 2
# 3
# 4
# 5

def counter(max):
    current = 0
    while current < max:
        print(f"현재: ${current}")
        current += 1
        yield current

for num in counter(10):
    print(num)