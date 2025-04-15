# ChatGPT로생성한클래스.py

# 클래스 정의 및 테스트 코드 통합

class Person:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def printInfo(self):
        #f-string 문법으로 변수명 바로 넘김
        print(f"ID: {self.id}, Name: {self.name}")

class Manager(Person):
    def __init__(self, id, name, title):
        #부모를 지칭하는 함수 :  super()
        super().__init__(id, name)
        self.title = title

    def printInfo(self):
        super().printInfo()
        print(f"Title: {self.title}")

class Employee(Person):
    def __init__(self, id, name, skill):
        super().__init__(id, name)
        self.skill = skill

    def printInfo(self):
        super().printInfo()
        print(f"Skill: {self.skill}")

def run_tests():
    print("Test 1: 기본 Person 객체")
    p1 = Person(1, "Alice")
    p1.printInfo()

    print("\nTest 2: Manager 객체")
    m1 = Manager(2, "Bob", "Team Lead")
    m1.printInfo()

    print("\nTest 3: Employee 객체")
    e1 = Employee(3, "Charlie", "Python")
    e1.printInfo()

    print("\nTest 4: Manager 객체 다른 타이틀")
    m2 = Manager(4, "David", "Project Manager")
    m2.printInfo()

    print("\nTest 5: Employee 객체 다른 스킬")
    e2 = Employee(5, "Eve", "Data Analysis")
    e2.printInfo()

    print("\nTest 6: Person 이름 변경 테스트")
    p2 = Person(6, "Frank")
    p2.name = "Franklin"
    p2.printInfo()

    print("\nTest 7: Manager 타이틀 변경 테스트")
    m1.title = "Senior Team Lead"
    m1.printInfo()

    print("\nTest 8: Employee 스킬 변경 테스트")
    e1.skill = "Java"
    e1.printInfo()

    print("\nTest 9: 다형성 테스트 (Person 타입 리스트)")
    people = [p1, m1, e1]
    for person in people:
        person.printInfo()
        print("---")

    print("\nTest 10: 잘못된 값으로 생성된 객체")
    try:
        bad = Employee(None, "", "")
        bad.printInfo()
    except Exception as e:
        print("Error:", e)

# 테스트 실행
run_tests()
