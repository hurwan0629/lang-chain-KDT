# 데코레이터 팩토리 만들어보기

# my_decorator_factory의 인자는 어노테이션 옆에 있는 인자를 받음
# @my_decorator_factory(a=10, b=20) 하면 그대로 받아짐
def my_decorator_factory(x: int, y: int, *p_args, **p_kwargs):
  print("\n --- my_decorator_factory 진입 ---")
  # 실제로 실행되는 함수를 받아줌
  def my_decorator(func):
    print("\n --- my_decorator 진입 ---")
    default = "기본값"
    # 함수 옆에 들어온 인자를 wrapper가 가져감
    def wrapper(*args, **kwargs):
      print("\n --- wrapper 진입 ---")
      print(f"데코레이터 인자: {x}, {y}, {p_args}, {p_kwargs}")
      print(f"인자들(args): {args}")
      print(f"인자들(kwargs): {kwargs}")

      return default + func(*args, **kwargs)
    return wrapper
  return my_decorator