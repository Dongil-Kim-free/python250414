# demoForm.py
# demoForm.ui(화면단) + demoForm.py(로직단)
# PyQt5 선언
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

# 디자인한 파일을 로딩
form_class = uic.loadUiType("demoForm.ui")[0]

# 폼클래스를 정의
class DemoForm(QDialog, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # UI 설정
        self.label.setText("문자열을 출력~~")   # 레이블에 문자열 출력

# 직접 모듈을 실행했는지 진입점 체크
if __name__ == "__main__":
    app = QApplication(sys.argv)  # QApplication 객체 생성
    myWindow = DemoForm()         # DemoForm 객체 생성
    myWindow.show()               # 폼을 화면에 출력
    app.exec_()                   # 이벤트 루프 시작