import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5 import uic
import sqlite3
import os.path

# 데이터베이스 처리 클래스
class DatabaseManager:
    def __init__(self, db_name="ProductList.db"):
        self.db_name = db_name
        self.con = None
        self.cur = None
        self.connect()

    def connect(self):
        if not os.path.exists(self.db_name):
            self.con = sqlite3.connect(self.db_name)
            self.cur = self.con.cursor()
            self.cur.execute(
                "CREATE TABLE Products (id INTEGER PRIMARY KEY AUTOINCREMENT, Name TEXT, Price INTEGER);"
            )
        else:
            self.con = sqlite3.connect(self.db_name)
            self.cur = self.con.cursor()

    def execute(self, query, params=()):
        self.cur.execute(query, params)

    def fetchall(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def commit(self):
        self.con.commit()

    def __del__(self):
        if self.con:
            self.con.close()

# 디자인 파일 로딩
form_class = uic.loadUiType("ProductList.ui")[0]

class DemoForm(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 데이터베이스 매니저 초기화
        self.db = DatabaseManager()

        # 초기값 셋팅
        self.id = 0
        self.name = ""
        self.price = 0

        # QTableWidget 설정
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 150)
        self.tableWidget.setColumnWidth(2, 100)
        self.tableWidget.setHorizontalHeaderLabels(["제품ID", "제품명", "가격"])
        self.tableWidget.setTabKeyNavigation(False)

        # 엔터키로 다음 컨트롤로 이동
        self.prodID.returnPressed.connect(lambda: self.focusNextChild())
        self.prodName.returnPressed.connect(lambda: self.focusNextChild())
        self.prodPrice.returnPressed.connect(lambda: self.focusNextChild())

        # 더블클릭 시그널 처리
        self.tableWidget.doubleClicked.connect(self.doubleClick)

        # 초기 데이터 로드
        self.getProduct()

    def addProduct(self):
        self.name = self.prodName.text().strip()
        self.price = self.prodPrice.text().strip()

        # 입력값 검증
        if not self.name or not self.price:
            QMessageBox.warning(self, "입력 오류", "제품명과 가격을 모두 입력하세요.")
            return

        if not self.price.isdigit():
            QMessageBox.warning(self, "입력 오류", "가격은 숫자만 입력해야 합니다.")
            return

        self.db.execute("INSERT INTO Products (Name, Price) VALUES (?, ?);", (self.name, int(self.price)))
        self.db.commit()
        self.getProduct()

    def updateProduct(self):
        self.id = self.prodID.text().strip()
        self.name = self.prodName.text().strip()
        self.price = self.prodPrice.text().strip()

        # 입력값 검증
        if not self.id or not self.name or not self.price:
            QMessageBox.warning(self, "입력 오류", "제품 ID, 제품명, 가격을 모두 입력하세요.")
            return

        if not self.price.isdigit():
            QMessageBox.warning(self, "입력 오류", "가격은 숫자만 입력해야 합니다.")
            return

        self.db.execute("UPDATE Products SET Name = ?, Price = ? WHERE id = ?;", (self.name, int(self.price), self.id))
        self.db.commit()
        self.getProduct()

    def removeProduct(self):
        self.id = self.prodID.text()
        self.db.execute("DELETE FROM Products WHERE id = ?;", (self.id,))
        self.db.commit()
        self.getProduct()

    def getProduct(self):
        self.tableWidget.clearContents()
        products = self.db.fetchall("SELECT * FROM Products;")
        self.tableWidget.setRowCount(len(products))

        for row, item in enumerate(products):
            self.tableWidget.setItem(row, 0, self.createTableItem(item[0], Qt.AlignRight))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(item[1]))
            self.tableWidget.setItem(row, 2, self.createTableItem(item[2], Qt.AlignRight))

    def createTableItem(self, value, alignment):
        item = QTableWidgetItem(str(value))
        item.setTextAlignment(alignment)
        return item

    def doubleClick(self):
        self.prodID.setText(self.tableWidget.item(self.tableWidget.currentRow(), 0).text())
        self.prodName.setText(self.tableWidget.item(self.tableWidget.currentRow(), 1).text())
        self.prodPrice.setText(self.tableWidget.item(self.tableWidget.currentRow(), 2).text())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demoForm = DemoForm()
    demoForm.show()
    app.exec_()