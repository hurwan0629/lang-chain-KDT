from app.server.service.service import Service
from app.view.page_interface import Page
from app.view.component.get_menu_number import get_menu_number
from app.view.component.print_product_default import print_product_table
from app.view.component.get_menu_number import get_menu_number

# 주문 하기
# 1. 
class OrderPage(Page):
  def __init__(self, service: Service, user_id):
    self.__user_id = user_id
    self.__service = service

  def run_page(self) -> bool:
    while True:
      print("==========================")
      print(f"  상품 주문")
      print(f"  *나가시고 싶으시면 '0'을 입력해주세요")
      print("==========================")
      exit_flag = False
      # 상품 선택하기
      product_data = None
      while True:
        try: 
          user_input = int(input("원하는 상품의 ID를 입력하세요: "))

          if user_input == 0:
            exit_flag = True
            break

          if self.__service.check_product_by_id(user_input):
            product_data = self.__service.get_product_by_id_to_print(user_input)
            print_product_table((product_data, ))
            break
          else:
            raise ValueError
        except ValueError:
          print("해당 ID의 상품이 존재하지 않습니다.")
          continue
        except TypeError:
          print("올바른 수를 입력해주세요")
          continue
      
      if exit_flag == True:
        input("아무 키를 눌러서 메인 메뉴로 나가기: ")
        return False
      
      # 상품 재고 0개면 바로 나가기
      if product_data[3] == "품절":
        input("품절된 상품입니다. 아무키를 눌러 나가기")
        return False
      
      # 상품 수량 선택하기
      product_count = 0
      while True:
        try: 
          user_input = int(input("원하는 상품의 개수를 입력하세요 (0은 메인 메뉴입니다.): "))

          if user_input == 0:
            exit_flag = True
            break
          
          stock = 0 if product_data[3] == "품절" else int(product_data[3])
          if 1<= user_input <= stock:
            product_count = user_input
            break
        except ValueError:
          print("")
          continue
        except TypeError:
          print("올바른 수를 입력해주세요")
          continue
      
      if exit_flag == True:
        input("아무 키를 눌러서 메인 메뉴로 나가기: ")
        return False
      
      # 최종 주문 선택
      final_check = 0
      while True:
        try:
          print(f"총 금액은 {product_data[2]*product_count}원입니다. 주문 하시겠습니까?")
          print("1. 네")
          print("2. 아니오")
          final_check = int(input("입력: "))
          if final_check not in (0, 1, 2):
            raise Exception
          break
        except Exception:
          continue
      
      if final_check != 1:
        print("메인 메뉴로 돌아갑니다.")
        input("아무키를 눌러서 나가기")
        return False
    
      # 상품 수량 점유 후 주문하기 (중간에 사라질 수 있으니 한번 더 확인하고 결제)
      order_id = self.__service.order_product_by_user(product_data[0], product_count, self.__user_id, product_data[2])
      if order_id is None:
        print("주문에 실패하였습니다. 메인 메뉴로 돌아갑니다.")
        return False
      print("주문이 완료되었습니다! 메인 메뉴로 돌아갑니다.")
      return False
