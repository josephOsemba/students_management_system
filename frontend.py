# -*- coding: utf-8 -*-
import sys
import requests
from PyQt5 import QtCore, QtGui, QtWidgets

API_URL = "http://127.0.0.1:5000"  # Flask backend URL

class StudentManager(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Student Management System")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        # Bio Data Group
        self.groupBox = QtWidgets.QGroupBox("Bio Data", self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(100, 30, 681, 131))

        self.titleLabel = QtWidgets.QLabel("Title:", self.groupBox)
        self.titleLabel.setGeometry(QtCore.QRect(40, 30, 50, 20))
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(40, 50, 91, 22))
        self.comboBox.addItems(["Mr.", "Ms.", "Dr.", "Prof.", "Eng."])

        self.firstNameLabel = QtWidgets.QLabel("First Name:", self.groupBox)
        self.firstNameLabel.setGeometry(QtCore.QRect(170, 30, 80, 20))
        self.firstNameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.firstNameEdit.setGeometry(QtCore.QRect(170, 50, 111, 21))

        self.secondNameLabel = QtWidgets.QLabel("Second Name:", self.groupBox)
        self.secondNameLabel.setGeometry(QtCore.QRect(330, 30, 100, 20))
        self.secondNameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.secondNameEdit.setGeometry(QtCore.QRect(330, 50, 141, 21))

        self.surnameLabel = QtWidgets.QLabel("Surname:", self.groupBox)
        self.surnameLabel.setGeometry(QtCore.QRect(540, 30, 80, 20))
        self.surnameEdit = QtWidgets.QLineEdit(self.groupBox)
        self.surnameEdit.setGeometry(QtCore.QRect(540, 50, 131, 21))

        # Gender Group
        self.genderGroup = QtWidgets.QGroupBox("Gender", self.centralwidget)
        self.genderGroup.setGeometry(QtCore.QRect(100, 180, 120, 111))

        self.maleRadio = QtWidgets.QRadioButton("Male", self.genderGroup)
        self.maleRadio.setGeometry(QtCore.QRect(10, 20, 100, 20))
        self.femaleRadio = QtWidgets.QRadioButton("Female", self.genderGroup)
        self.femaleRadio.setGeometry(QtCore.QRect(10, 50, 100, 20))
        self.otherRadio = QtWidgets.QRadioButton("Other", self.genderGroup)
        self.otherRadio.setGeometry(QtCore.QRect(10, 80, 100, 20))

        # Units Group
        self.unitsGroup = QtWidgets.QGroupBox("Select Your Units", self.centralwidget)
        self.unitsGroup.setGeometry(QtCore.QRect(300, 180, 181, 141))

        self.mathCheck = QtWidgets.QCheckBox("Mathematics", self.unitsGroup)
        self.mathCheck.setGeometry(QtCore.QRect(20, 20, 150, 20))
        self.chemCheck = QtWidgets.QCheckBox("Chemistry", self.unitsGroup)
        self.chemCheck.setGeometry(QtCore.QRect(20, 50, 150, 20))
        self.researchCheck = QtWidgets.QCheckBox("Research Methods", self.unitsGroup)
        self.researchCheck.setGeometry(QtCore.QRect(20, 80, 150, 20))
        self.calcCheck = QtWidgets.QCheckBox("Calculus", self.unitsGroup)
        self.calcCheck.setGeometry(QtCore.QRect(20, 110, 150, 20))

        # Buttons
        self.addButton = QtWidgets.QPushButton("ADD NEW", self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(120, 390, 100, 30))
        self.addButton.clicked.connect(self.add_student)

        self.updateButton = QtWidgets.QPushButton("UPDATE", self.centralwidget)
        self.updateButton.setGeometry(QtCore.QRect(560, 390, 100, 30))
        self.updateButton.clicked.connect(self.update_student)

        self.deleteButton = QtWidgets.QPushButton("DELETE", self.centralwidget)
        self.deleteButton.setGeometry(QtCore.QRect(230, 390, 100, 30))
        self.deleteButton.clicked.connect(self.delete_student)

        self.searchButton = QtWidgets.QPushButton("SEARCH", self.centralwidget)
        self.searchButton.setGeometry(QtCore.QRect(340, 390, 100, 30))
        self.searchButton.clicked.connect(self.search_student)

        self.showButton = QtWidgets.QPushButton("SAVE", self.centralwidget)
        self.showButton.setGeometry(QtCore.QRect(450, 390, 100, 30))
        self.showButton.clicked.connect(self.show_students)

       # Table Widget (Initially Hidden)
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(50, 450, 700, 150))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Title", "First Name", "Second Name", "Surname", "Gender"])
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setVisible(True)  # Hide initially


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
        """Clears all input fields after adding a student."""
        self.comboBox.setCurrentIndex(0)
        self.firstNameEdit.clear()
        self.secondNameEdit.clear()
        self.surnameEdit.clear()
        self.maleRadio.setChecked(False)
        self.femaleRadio.setChecked(False)
        self.otherRadio.setChecked(False)
        self.mathCheck.setChecked(False)
        self.chemCheck.setChecked(False)
        self.researchCheck.setChecked(False)
        self.calcCheck.setChecked(False)


    def add_student(self):
        student_data = {
            "title": self.comboBox.currentText(),
            "first_name": self.firstNameEdit.text().strip(),
            "second_name": self.secondNameEdit.text().strip(),
            "surname": self.surnameEdit.text().strip(),
            "gender": self.get_selected_gender(),
            "units": self.get_selected_units(),
        }

        response = requests.post(f"{API_URL}/add_student", json=student_data)
        if response.status_code == 200:
            QtWidgets.QMessageBox.information(self, "Success", response.json()["message"])
            self.clear_input_fields()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", response.json().get("message", "Failed to add student"))


    def delete_student(self):
        student_id, ok = QtWidgets.QInputDialog.getInt(self, "Delete Student", "Enter Student ID:")
        if ok:
            response = requests.delete(f"{API_URL}/delete_student/{student_id}")
            if response.status_code == 200:
                QtWidgets.QMessageBox.information(self, "Success", "Student deleted successfully!")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to delete student!")

    def search_student(self):
        query, ok = QtWidgets.QInputDialog.getText(self, "Search Student", "Enter Name:")
        if ok:
            response = requests.get(f"{API_URL}/search_student?name={query}")
            if response.status_code == 200:
                results = response.json()
                if results:
                    result_text = "\n".join([f"ID: {s['id']}, Name: {s['first_name']} {s['second_name']} {s['surname']}" for s in results])
                    QtWidgets.QMessageBox.information(self, "Search Results", result_text)
                else:
                    QtWidgets.QMessageBox.information(self, "No Results", "No student found.")
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to search students!")

    def update_student(self):
        student_id, ok = QtWidgets.QInputDialog.getInt(self, "Update Student", "Enter Student ID:")
        if not ok:
            return

        dialog = StudentEditDialog(student_id, self)
        dialog.exec_()  # Open pop-up


    def show_students(self):
        response = requests.get(f"{API_URL}/get_students")
        students = response.json()

        if not students:
            QtWidgets.QMessageBox.warning(self, "No Data", "No students found in the database!")
            return

        self.tableWidget.setRowCount(len(students))  # Set table row count

        for row, student in enumerate(students):
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(student["id"])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(student["title"]))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(student["first_name"]))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(student["second_name"]))
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem(student["surname"]))
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem(student["gender"]))


class StudentEditDialog(QtWidgets.QDialog):
    def __init__(self, student_id, parent=None):
        super().__init__(parent)
        self.student_id = student_id
        self.setWindowTitle("Edit Student Details")
        self.setGeometry(400, 200, 400, 300)

        # Form Layout
        layout = QtWidgets.QVBoxLayout(self)

        self.firstNameLabel = QtWidgets.QLabel("First Name:")
        self.firstNameEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.firstNameLabel)
        layout.addWidget(self.firstNameEdit)

        self.secondNameLabel = QtWidgets.QLabel("Second Name:")
        self.secondNameEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.secondNameLabel)
        layout.addWidget(self.secondNameEdit)

        self.surnameLabel = QtWidgets.QLabel("Surname:")
        self.surnameEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.surnameLabel)
        layout.addWidget(self.surnameEdit)

        self.genderLabel = QtWidgets.QLabel("Gender:")
        self.genderCombo = QtWidgets.QComboBox()
        self.genderCombo.addItems(["Male", "Female", "Other"])
        layout.addWidget(self.genderLabel)
        layout.addWidget(self.genderCombo)

        self.unitsLabel = QtWidgets.QLabel("Units (comma separated):")
        self.unitsEdit = QtWidgets.QLineEdit()
        layout.addWidget(self.unitsLabel)
        layout.addWidget(self.unitsEdit)

        # Save Button
        self.saveButton = QtWidgets.QPushButton("Save Changes")
        self.saveButton.clicked.connect(self.save_changes)
        layout.addWidget(self.saveButton)

        self.load_student_data()  # Load existing data

    def load_student_data(self):
        response = requests.get(f"{API_URL}/get_students")
        students = response.json()
        student = next((s for s in students if s["id"] == self.student_id), None)

        if student:
            self.firstNameEdit.setText(student["first_name"])
            self.secondNameEdit.setText(student["second_name"])
            self.surnameEdit.setText(student["surname"])
            self.genderCombo.setCurrentText(student["gender"])
            self.unitsEdit.setText(", ".join(student["units"]))

    def save_changes(self):
        updated_data = {
            "first_name": self.firstNameEdit.text().strip(),
            "second_name": self.secondNameEdit.text().strip(),
            "surname": self.surnameEdit.text().strip(),
            "gender": self.genderCombo.currentText(),
            "units": self.unitsEdit.text().strip().split(", "),  # Convert back to list
        }

        response = requests.put(f"{API_URL}/update_student/{self.student_id}", json=updated_data)

        if response.status_code == 200:
            QtWidgets.QMessageBox.information(self, "Success", "Student updated successfully!")
            self.accept()  # Close the dialog
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to update student details!")



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = StudentManager()
    MainWindow.show()
    sys.exit(app.exec_())
