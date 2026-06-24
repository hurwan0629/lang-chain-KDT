from tabulate import tabulate

_headers = ["ID", "상품명", "가격", "재고"]

def print_product_table(data: tuple[tuple[int, str, int, int]]):
  if data is None or len(data) <= 0:
    print("""
            +------+----------+--------+--------+
            | ID   | 상품명    | 가격    | 재고  |
            +======+==========+========+========+
            |           검색 결과 없음           |
            +------+----------+--------+--------+
            """)
    return
  print(tabulate(data, headers=_headers, tablefmt="grid"))