# db2.py

import sqlite3

# 연결객체 리턴 (물리적인 파일에 저장)
con = sqlite3.connect(r"c:\work\sample.db")
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
print(cur.fetchall())   # commit 하지 않으면 메모리상에만 저장, 실제 파일에는 저장되지 않음

# 정상적 종료
con.commit()
