class Student:

    def __init__(self, name):
        self.__name = name

    @property
    def name(self):
        return self.__name

class StudentList:
    def __init__(self):
        self.data: list[Student] = []
    
    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value

    
    
    def __delitem__(self, index):
        del self.data[index]


s1 = Student("허완")
s2 = Student("홍길동")
s3 = Student("길삼이")

print(s1.name)