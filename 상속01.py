class Person:
    def __init__(self, name, phoneNumber):
        self.name = name
        self.phoneNumber = phoneNumber

    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1})".format(self.name, self.phoneNumber))

class Student(Person):
    # 덮어쓰기(재정의)
    def __init__(self, name, phoneNumber, subject, studentID):
        #self.name = name
        #self.phoneNumber = phoneNumber
        #명시적으로 부모 초기화 메서드 호출 (위에 두줄 삭제)
        Person.__init__(self, name, phoneNumber)
        self.subject = subject
        self.studentID = studentID

    # 메서드 재정의
    def printInfo(self):
        print("Info(Name:{0}, Phone Number: {1}, Subject: {2}, StudentID: {3})".format(self.name, self.phoneNumber, self.subject, self.studentID))


p = Person("전우치", "010-222-1234")
s = Student("이순신", "010-111-1234", "컴공", "991122")
#print(p.__dict__)
#print(s.__dict__)
p.printInfo()
s.printInfo()