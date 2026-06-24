import MySQLdb

# 데코레이터
def my_decorator(func):
  def wrapper(name):
    func(name)

  return wrapper



if __name__ == "__main__":