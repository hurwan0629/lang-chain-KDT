class Person:
  # 정적(클래스) 변수
  __person_define = {
    "eye": 2,
    "brain": 1,
    "hand": 2
  }

  def __init__(self, name: str, age: int):
    print("Person.__init__() 호출!")
    self.name = name
    self.ag = age
  
  def __repr__(self):
    return f"Person(name={self.name}, age={self.ag}), person_define={self.__person_define}"

  def __str__(self):
    return f"저는 {self.name}입니당"

  ## 은닉화
  @property
  def name(self):
    return self.__name
  
  @name.setter
  def name(self, name):
    self.__name = name
  
  @property
  def ag(self):
    return self.__age
  
  @ag.setter
  def ag(self, age):
    self.__age = age

class Me(Person):
  def __init__(self, name, age, hobby, strong):
    super().__init__(name, age)
    self.hobby = hobby
    self.strong = strong

p = Person("hong", 21)

print(p.ag)