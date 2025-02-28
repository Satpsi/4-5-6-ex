import sys
import sqlite3
from PyQt6 import QtWidgets, uic


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.load_data()
        self.addButton = self.findChild(QtWidgets.QPushButton, "addButton")
        self.editButton = self.findChild(QtWidgets.QPushButton, "editButton")

        if self.addButton:
            self.addButton.clicked.connect(self.open_add_edit_form)
        if self.editButton:
            self.editButton.clicked.connect(self.open_add_edit_form)

    def load_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()
        connection.close()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(len(rows[0]))
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Сорт", "Обжарка", "Форма", "Описание", "Цена", "Объем"])

        for row_idx, row in enumerate(rows):
            for col_idx, cell in enumerate(row):
                self.tableWidget.setItem(row_idx, col_idx, QtWidgets.QTableWidgetItem(str(cell)))

    def open_add_edit_form(self):
        self.add_edit_window = AddEditCoffeeForm(self)
        self.add_edit_window.show()


class AddEditCoffeeForm(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):
        connection = sqlite3.connect("coffee.sqlite")
        cursor = connection.cursor()
        sort = self.sortInput.text()
        roast_level = self.roastInput.text()
        form = self.formInput.text()
        description = self.descInput.toPlainText()
        price = float(self.priceInput.text())
        volume = int(self.volumeInput.text())

        cursor.execute(
            "INSERT INTO coffee (sort, roast_level, form, description, price, volume) VALUES (?, ?, ?, ?, ?, ?)",
            (sort, roast_level, form, description, price, volume))
        connection.commit()
        connection.close()
        self.parent().load_data()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec())