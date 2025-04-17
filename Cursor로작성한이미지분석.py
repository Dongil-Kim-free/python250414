import sys
import os
import base64
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, 
                            QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QWidget)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import io
# from dotenv import load_dotenv

# OpenAI API 키를 환경 변수에서 로드
api_key = 'AIP Key 입력'
# load_dotenv()

class DemoForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.current_image_path = None
        
    def init_ui(self):
        # 메인 윈도우 설정
        self.setWindowTitle('이미지 분석 애플리케이션')
        self.setGeometry(100, 100, 800, 600)
        
        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 레이아웃 설정
        main_layout = QVBoxLayout(central_widget)
        
        # 버튼 영역
        button_layout = QHBoxLayout()
        
        # 이미지 선택 버튼
        self.select_button = QPushButton('이미지 선택')
        self.select_button.clicked.connect(self.select_image)
        button_layout.addWidget(self.select_button)
        
        # 분석 버튼
        self.analyze_button = QPushButton('이미지 분석')
        self.analyze_button.clicked.connect(self.analyze_image)
        self.analyze_button.setEnabled(False)
        button_layout.addWidget(self.analyze_button)
        
        main_layout.addLayout(button_layout)
        
        # 이미지 표시 영역
        self.image_label = QLabel('이미지가 여기에 표시됩니다')
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet('border: 1px solid #cccccc;')
        self.image_label.setMinimumHeight(300)
        main_layout.addWidget(self.image_label)
        
        # 분석 결과 표시 영역
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setPlaceholderText('분석 결과가 여기에 표시됩니다')
        main_layout.addWidget(self.result_text)
    
    def select_image(self):
        # 파일 다이얼로그를 통해 이미지 선택
        file_dialog = QFileDialog()
        image_path, _ = file_dialog.getOpenFileName(
            self, '이미지 선택', '', 'Images (*.png *.jpg *.jpeg)'
        )
        
        if image_path:
            self.current_image_path = image_path
            # 이미지 표시
            pixmap = QPixmap(image_path)
            # 이미지 크기 조정 (라벨 크기에 맞게)
            pixmap = pixmap.scaled(self.image_label.width(), self.image_label.height(), 
                                  Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.image_label.setPixmap(pixmap)
            # 분석 버튼 활성화
            self.analyze_button.setEnabled(True)
    
    def analyze_image(self):
        if not self.current_image_path:
            return
        
        # 이미지를 base64로 인코딩
        with open(self.current_image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
        
        # OpenAI API 호출
        self.result_text.setText("이미지 분석 중...")
        
        try:
            # api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                self.result_text.setText("OpenAI API 키가 설정되지 않았습니다. .env 파일에 OPENAI_API_KEY를 설정해주세요.")
                return
                
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            
            payload = {
                "model": "gpt-4o",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "이 이미지에 대해 자세히 설명해주세요."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 300
            }
            
            response = requests.post("https://api.openai.com/v1/chat/completions", 
                                    headers=headers, json=payload)
            
            if response.status_code == 200:
                result = response.json()
                analysis_text = result["choices"][0]["message"]["content"]
                self.result_text.setText(analysis_text)
            else:
                self.result_text.setText(f"API 오류: {response.status_code}\n{response.text}")
        
        except Exception as e:
            self.result_text.setText(f"오류 발생: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = DemoForm()
    demo.show()
    sys.exit(app.exec_())
