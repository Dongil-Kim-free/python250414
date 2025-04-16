import random
from openpyxl import Workbook

# 워크북 생성
wb = Workbook()
ws = wb.active
ws.title = "제품리스트"

# 헤더 추가
ws.append(["제품ID", "제품명", "수량", "가격"])

# 샘플 데이터
product_names = [
    "스마트폰", "노트북", "태블릿", "스마트워치", "헤드폰",
    "스피커", "키보드", "마우스", "모니터", "프린터"
]

# 데이터 생성
for i in range(1, 101):  # 100개의 데이터 생성
    product_id = f"P{i:03d}"  # 제품ID (P001, P002, ...)
    product_name = random.choice(product_names)  # 랜덤 제품명
    quantity = random.randint(1, 50)  # 수량 (1~50)
    price = random.randint(100, 10000)  # 가격 (100 ~ 10,000)
    ws.append([product_id, product_name, quantity, price])

# 엑셀 파일 저장
wb.save("products.xlsx")
print("products.xlsx 파일이 생성되었습니다.")