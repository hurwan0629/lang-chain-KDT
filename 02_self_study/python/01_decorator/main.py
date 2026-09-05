from my_decorator import my_decorator_factory

@my_decorator_factory(10, 20, "a", "b", c=10, d=20)
def print_and_return_str(s: str):
  print("\n --- print_and_return_str 진입 ---")
  print(f"기본 함수 출력: {s}")
  return s

print_and_return_str("기본 함수 출력!")