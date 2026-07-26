import time
from typing import Generator, Literal, Any


def hello() -> Generator[Literal[10, 20], str, str]:
    print("a")
    x = yield 10
    print("b")
    print("x:", x)
    y = yield 20
    print("c")
    print("y:", y)

    return "custom stop iterator"

k = hello()
print("first next:", next(k))
print("first send:", k.send("k-first"))
time.sleep(1)
# print(next(k))
print("second send:", k.send("k-second"))
time.sleep(1)
# next(k)

# for i in hello():
#     print("i:", i)

