# ChatGPT로이미지해석하기.py

import sys
import base64
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QVBoxLayout, QWidget, QTextEdit, QSplitter
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

api_key = "AIP Key 입력"  # OpenAI API 키를 입력하세요

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("이미지 해석 애플리케이션")
        self.setGeometry(100, 100, 800, 800)  # 높이를 늘림

        # 스플리터 위젯 생성
        splitter = QSplitter(Qt.Vertical)

        # 이미지 표시 영역
        self.image_label = QLabel("이미지를 선택하세요")
        self.image_label.setStyleSheet("border: 1px solid black;")
        self.image_label.setFixedSize(600, 400)
        self.image_label.setScaledContents(True)

        # 결과 표시를 위한 QTextEdit
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)  # 읽기 전용으로 설정
        self.result_text.setMinimumHeight(200)  # 최소 높이 설정

        # 버튼들
        self.select_button = QPushButton("이미지 선택")
        self.select_button.clicked.connect(self.select_image)

        self.analyze_button = QPushButton("이미지 분석")
        self.analyze_button.clicked.connect(self.analyze_image)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.result_text)
        layout.addWidget(self.select_button)
        layout.addWidget(self.analyze_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 이미지 경로 저장 변수
        self.image_path = None

    def select_image(self):
        # 파일 선택 다이얼로그
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "이미지 선택", "", "Images (*.png *.jpg *.jpeg *.bmp)", options=options)
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.image_label.setPixmap(pixmap)

    def analyze_image(self):
        if not self.image_path:
            self.result_text.setText("이미지를 먼저 선택하세요.")
            return

        # 이미지 파일을 base64로 인코딩
        try:
            with open(self.image_path, "rb") as image_file:
                encoded_image = base64.b64encode(image_file.read()).decode('utf-8')

            # OpenAI API 호출
            response = self.send_to_openai(encoded_image)
            if response:
                self.result_text.setText(f"분석 결과:\n{response}")
            else:
                self.result_text.setText("분석 실패")
        except Exception as e:
            self.result_text.setText(f"오류 발생:\n{str(e)}")

    def send_to_openai(self, encoded_image):
        
        endpoint = "https://api.openai.com/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        data = {
            "model": "gpt-4o",  # 이미지 분석이 가능한 모델로 변경
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "이 이미지에 무엇이 있는지 한글로 설명해줘"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
        }

        try:
            response = requests.post(endpoint, headers=headers, json=data)
            if response.status_code == 200:
                # 응답에서 실제 텍스트 추출
                response_data = response.json()
                if 'choices' in response_data and len(response_data['choices']) > 0:
                    return response_data['choices'][0]['message']['content']
                return "결과를 찾을 수 없습니다."
            else:
                return f"API 오류: {response.status_code} - {response.text}"
        except Exception as e:
            return f"요청 실패: {str(e)}"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    sys.exit(app.exec_())

