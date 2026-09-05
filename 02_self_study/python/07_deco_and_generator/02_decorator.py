import time


def log_and_block_zero(func):
    def wrapper(div_num):
        print("function start")
        result=None
        if div_num == 0:
            print("div_num cannot be 0")
        else:
            result = func(div_num)

        print("function end")
        return result
    return wrapper

@log_and_block_zero
def some_func(div_num):
    for i in range(9999):
        if i % div_num == 0:
            print(i)

# print("some_func(0)")
# some_func(0)
# time.sleep(3)
# print("some_func(99)")
# some_func(99)

def allow_only(allowed_div_num: list[int]):
    def decorator(func):
        def wrapper(div_num):
            if div_num not in allowed_div_num:
                print("you can only put allowed div num:", allowed_div_num)
                return
            else:
                func(div_num)
        return wrapper
    return decorator

@allow_only([1, 2, 3, 4])
def some_func2(div_num):
    s = 0
    for i in range(9999):
        if i % div_num == 0:
            # print(i)
            s += 1
    print(s)

print("some_func2(0)")
some_func2(0)

print("some_func2(123)")
some_func2(123)

print("some_func2(3)")
some_func2(3)