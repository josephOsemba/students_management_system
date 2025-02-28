# -*- coding: utf-8 -*-
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

API_URL = "http://127.0.0.1:5000"

class StudentManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Student Management System")
        self.resize(900, 700)
        self.setStyleSheet("""
            QWidget {
                background-color: #f4f4f4;
                font-family: Arial;
                font-size: 12pt;
            }
            QPushButton {
                background-color: #007BFF;
                color: white;
                border-radius: 8px;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QLineEdit, QComboBox, QTextEdit {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 5px;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 10px;
            }
            QLabel {
                font-weight: bold;
            }
        """)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        layout = QtWidgets.QVBoxLayout(central_widget)

        # Tabs for better navigation
        self.tabs = QtWidgets.QTabWidget()
        layout.addWidget(self.tabs)

        self.bio_data_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.bio_data_tab, "Bio Data")

        self.records_tab = QtWidgets.QWidget()
        self.tabs.addTab(self.records_tab, "Student Records")

        # Bio Data Form
        bio_layout = QtWidgets.QGridLayout(self.bio_data_tab)

        self.titleCombo = QtWidgets.QComboBox()
        self.titleCombo.addItems(["Mr.", "Ms.", "Dr.", "Prof.", "Eng."])
        bio_layout.addWidget(QtWidgets.QLabel("Title:"), 0, 0)
        bio_layout.addWidget(self.titleCombo, 0, 1)

        self.firstNameEdit = QtWidgets.QLineEdit()
        self.firstNameEdit.setPlaceholderText("First Name")
        bio_layout.addWidget(QtWidgets.QLabel("First Name:"), 1, 0)
        bio_layout.addWidget(self.firstNameEdit, 1, 1)

        self.secondNameEdit = QtWidgets.QLineEdit()
        self.secondNameEdit.setPlaceholderText("Second Name")
        bio_layout.addWidget(QtWidgets.QLabel("Second Name:"), 2, 0)
        bio_layout.addWidget(self.secondNameEdit, 2, 1)

        self.surnameEdit = QtWidgets.QLineEdit()
        self.surnameEdit.setPlaceholderText("Surname")
        bio_layout.addWidget(QtWidgets.QLabel("Surname:"), 3, 0)
        bio_layout.addWidget(self.surnameEdit, 3, 1)

        # Gender
        self.genderGroup = QtWidgets.QGroupBox("Gender")
        gender_layout = QtWidgets.QHBoxLayout(self.genderGroup)
        self.maleRadio = QtWidgets.QRadioButton("Male")
        self.femaleRadio = QtWidgets.QRadioButton("Female")
        self.otherRadio = QtWidgets.QRadioButton("Other")
        gender_layout.addWidget(self.maleRadio)
        gender_layout.addWidget(self.femaleRadio)
        gender_layout.addWidget(self.otherRadio)
        bio_layout.addWidget(self.genderGroup, 4, 0, 1, 2)

        # Units
        self.unitsGroup = QtWidgets.QGroupBox("Select Your Units")
        units_layout = QtWidgets.QVBoxLayout(self.unitsGroup)
        self.mathCheck = QtWidgets.QCheckBox("Mathematics")
        self.chemCheck = QtWidgets.QCheckBox("Chemistry")
        self.researchCheck = QtWidgets.QCheckBox("Research Methods")
        self.calcCheck = QtWidgets.QCheckBox("Calculus")
        for check in [self.mathCheck, self.chemCheck, self.researchCheck, self.calcCheck]:
            units_layout.addWidget(check)
        bio_layout.addWidget(self.unitsGroup, 5, 0, 1, 2)

        # Buttons
        button_layout = QtWidgets.QHBoxLayout()
        self.addButton = QtWidgets.QPushButton("Add Student")
        self.addButton.clicked.connect(self.add_student)
        button_layout.addWidget(self.addButton)

        self.clearButton = QtWidgets.QPushButton("Clear Fields")
        self.clearButton.clicked.connect(self.clear_input_fields)
        button_layout.addWidget(self.clearButton)

        bio_layout.addLayout(button_layout, 6, 0, 1, 2)

        # Student Records Table
        records_layout = QtWidgets.QVBoxLayout(self.records_tab)
        self.tableWidget = QtWidgets.QTableWidget()
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Title", "First Name", "Second Name", "Surname", "Gender"])
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        records_layout.addWidget(self.tableWidget)

        # Load records button
        self.loadButton = QtWidgets.QPushButton("Load Student Records")
        self.loadButton.clicked.connect(self.show_students)
        records_layout.addWidget(self.loadButton)

    def add_student(self):
        student_data = {
            "title": self.titleCombo.currentText(),
            "first_name": self.firstNameEdit.text().strip(),
            "second_name": self.secondNameEdit.text().strip(),
            "surname": self.surnameEdit.text().strip(),
            "gender": self.get_selected_gender(),
            "units": self.get_selected_units(),
        }

        response = requests.post(f"{API_URL}/add_student", json=student_data)
        if response.status_code == 200:
            QtWidgets.QMessageBox.information(self, "Success", "Student added successfully!")
            self.clear_input_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to add student")

    def get_selected_gender(self):
        if self.maleRadio.isChecked():
            return "Male"
        elif self.femaleRadio.isChecked():
            return "Female"
        elif self.otherRadio.isChecked():
            return "Other"
        return ""

    def get_selected_units(self):
        units = []
        if self.mathCheck.isChecked():
            units.append("Mathematics")
        if self.chemCheck.isChecked():
            units.append("Chemistry")
        if self.researchCheck.isChecked():
            units.append("Research Methods")
        if self.calcCheck.isChecked():
            units.append("Calculus")
        return units

    def clear_input_fields(self):
        self.titleCombo.setCurrentIndex(0)
        self.firstNameEdit.clear()
        self.secondNameEdit.clear()
        self.surnameEdit.clear()
        self.maleRadio.setChecked(False)
        self.femaleRadio.setChecked(False)
        self.otherRadio.setChecked(False)
        for check in [self.mathCheck, self.chemCheck, self.researchCheck, self.calcCheck]:
            check.setChecked(False)

    def show_students(self):
        response = requests.get(f"{API_URL}/get_students")
        students = response.json()
        self.tableWidget.setRowCount(len(students))
        for row, student in enumerate(students):
            for col, key in enumerate(["id", "title", "first_name", "second_name", "surname", "gender"]):
                self.tableWidget.setItem(row, col, QtWidgets.QTableWidgetItem(str(student[key])))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = StudentManager()
    MainWindow.show()
    sys.exit(app.exec_())
