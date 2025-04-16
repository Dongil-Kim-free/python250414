import requests
from bs4 import BeautifulSoup
from openpyxl import Workbook
import urllib.parse

# 크롤링할 URL
query = '반도체'
encoded_query = urllib.parse.quote(query)
url = f"https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query={encoded_query}"

# HTTP 요청
response = requests.get(url)
response.raise_for_status()  # 요청 실패 시 예외 발생

# BeautifulSoup 객체 생성
soup = BeautifulSoup(response.text, 'html.parser')

# 신문기사 제목과 링크 크롤링
titles = soup.select('.news_tit')  # 네이버 뉴스 제목 클래스 선택자

# 제목과 링크 리스트 생성
news_data = [(title.get_text(), title['href']) for title in titles]

# 결과를 엑셀 파일로 저장
wb = Workbook()
ws = wb.active
ws.title = "News Titles"

# 헤더 추가
ws.append(["번호", "제목", "링크"])

# 데이터 추가
for idx, (title, link) in enumerate(news_data, start=1):
    ws.append([idx, title, link])

# 엑셀 파일 저장
wb.save("results.xlsx")

print("크롤링 및 저장 완료: results.xlsx")