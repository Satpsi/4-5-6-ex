import sys
import sqlite3
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem


class CoffeeApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()
        conn.close()

        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())