# BankAccount.py

#은행의 계정을 표현한 클래스 
class BankAccount:
    def __init__(self, id, name, balance):
        self.__id = id
        self.__name = name 
        self.__balance = balance 
    def deposit(self, amount):
        self.__balance += amount 
    def withdraw(self, amount):
        self.__balance -= amount
    def __str__(self):
        return "{0} , {1} , {2}".format(self.__id, \
            self.__name, self.__balance)

#인스턴스 객체를 생성
account1 = BankAccount(100, "전우치", 15000)
account1.deposit(5000)
account1.withdraw(3000)
print(account1)

#외부에서 접근(인스턴스) - 변수앞에 "__"가 없을 때 변경 가능, "__"가 있으면 변경 불가
account1.__balance = 15000000
print(account1)
#print(account1.__balance)   # 실행불가
#print(account1._BankAccount__balance)   # 외부에서 접근(테스트 용도로 규칙)
