from tabulate import tabulate
from datetime import datetime

_headers = ["ID", "총 가격", "상태", "생성일"]

def print_order_table(data: tuple[tuple[int, int, str, datetime]]):
  if data is None or len(data) <= 0:
    print("""
            +------+----------+--------+--------+
            | ID   | 총 가격    | 상태    | 생성일  |
            +======+==========+========+========+
            |           주문 기록 없음           |
            +------+----------+--------+--------+
            """)
    return
  print(tabulate(data, headers=_headers, tablefmt="grid"))