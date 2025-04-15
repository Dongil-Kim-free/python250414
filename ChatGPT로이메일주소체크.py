import re

# 이메일 유효성 검사 함수
def is_valid_email(email):
    # 정규표현식 설명:
    # ^                          : 문자열의 시작을 의미
    # [a-zA-Z0-9._%+-]+          : 사용자 이름 부분 (영문 대소문자, 숫자, 점, 밑줄, %, +, - 허용 / 한 글자 이상)
    # @                          : 반드시 @ 기호가 있어야 함
    # [a-zA-Z0-9.-]+             : 도메인 이름 (영문 대소문자, 숫자, 점, - 허용 / 한 글자 이상)
    # \.                         : 실제 점(.)을 의미함
    # [a-zA-Z]{2,}               : 최상위 도메인 (영문 2자 이상, 예: com, net, kr 등)
    # $                          : 문자열의 끝을 의미

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# 샘플 이메일 리스트 (10개)
sample_emails = [
    "user@example.com",         # ✅ 유효
    "john.doe123@gmail.com",    # ✅ 유효
    "jane-doe@company.co.uk",   # ✅ 유효
    "admin@site.",              # ❌ 도메인 끝 오류
    "no_at_symbol.com",         # ❌ @ 없음
    "@missinguser.com",         # ❌ 사용자 없음
    "space in@email.com",       # ❌ 공백 포함
    "user@@doubleat.com",       # ❌ @ 두 개
    "user@.com",                # ❌ 도메인 이름 없음
    "valid_email@domain.org"    # ✅ 유효
]

# 검사 실행
def run_email_tests():
    print("이메일 유효성 검사 결과:\n")
    for email in sample_emails:
        result = "✅ 유효" if is_valid_email(email) else "❌ 유효하지 않음"
        print(f"{email:30} → {result}")

# 실행
run_email_tests()
