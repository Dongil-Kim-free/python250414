# db1.py

import sqlite3

# 연결객체 리턴 (메모리에서 작업)
con = sqlite3.connect(":memory:")
# 커서객체 리턴
cur = con.cursor()

# 테이블 구조 생성
cur.execute("CREATE TABLE PhoneBook(name text, phoneNum text);")

# 1건 입력
cur.execute("INSERT INTO PhoneBook VALUES ('derick', '010-222');")

# 입력 파라메터 처리
name = "홍길동"
phoneNumber = "010-333"
cur.execute("INSERT INTO PhoneBook VALUES (?,?);", (name, phoneNumber))

# 다중의 레코드(행데이터 입력)
datalist = (("전우치","010-123"), ("이순신","010-555"))
cur.executemany("INSERT INTO PhoneBook VALUES (?,?);", datalist)

# 검색
cur.execute("SELECT * FROM PhoneBook;")
# fetchone, fetchmany, fetchall 실행 시 레코드포인터가 다음 레코드로 이동
print("---fetchone---")
print(cur.fetchone())   # 레코드포인터 0 -> 1
print("---fetchmany(2)---")
print(cur.fetchmany(2)) # 레코드포인터 1 -> 3
print("---fetchall---")
print(cur.fetchall()) # 레코드포인터 3 -> 4