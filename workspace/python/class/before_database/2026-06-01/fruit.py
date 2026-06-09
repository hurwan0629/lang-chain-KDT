# fruit.py

PI = 3.14

def print_fruit(name):
    print(f"{name}입니다.")

def add_quantity(quantity, amount):
    return quantity + amount

class Fruit:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def print_info(self):
        print(f"과일 이름: {self.name}")
        print(f"수량: {self.quantity}")

print(__name__)

if __name__ == "__main__":
    print("hello fruit")
    print(__name__)