import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QAction, QFileDialog, QMessageBox


class TextViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file_path = None
        self.init_ui()

    def init_ui(self):
        self.text_edit = QTextEdit(self)
        self.setCentralWidget(self.text_edit)

        # 파일 열기 액션
        open_file_action = QAction('Open File', self)
        open_file_action.triggered.connect(self.open_file)

        # 파일 저장 액션
        save_file_action = QAction('Save File', self)
        save_file_action.triggered.connect(self.save_file)

        # 메뉴바 설정
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)

        self.setWindowTitle('Text Viewer')
        self.setGeometry(100, 100, 800, 600)

    def open_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Text File', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    self.text_edit.setText(file.read())
                self.current_file_path = file_path
                self.setWindowTitle(f'Text Viewer - {file_path}')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to open file: {e}')

    def save_file(self):
        if self.current_file_path:
            try:
                with open(self.current_file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                QMessageBox.information(self, 'Success', 'File saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save file: {e}')
        else:
            self.save_file_as()

    def save_file_as(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Text File', '', 'Text Files (*.txt);;All Files (*)', options=options)
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(self.text_edit.toPlainText())
                self.current_file_path = file_path
                self.setWindowTitle(f'Text Viewer - {file_path}')
                QMessageBox.information(self, 'Success', 'File saved successfully.')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'Failed to save file: {e}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    viewer = TextViewer()
    viewer.show()
    sys.exit(app.exec_())