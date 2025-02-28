# Student Management System

This is a simple Student Management System built with Python and PyQt5. The application provides an intuitive graphical user interface (GUI) to manage student records, including adding, updating, deleting, and viewing student details.

## Features

- **Add Student:** Register new students with their details.
- **Update Student:** Modify existing student information.
- **Delete Student:** Remove a student record.
- **View Students:** Display a list of all students.

## Project Structure

```
PyQT5 Projects/
|-- frontend.py             # Main application GUI
|-- backend.py              # Database operations (if separate)
|-- requirements.txt        # Project dependencies
|-- README.md               # Project documentation
```

## Prerequisites

Make sure you have the following installed:

- Python 3.8+
- PyQt5 library

## Setup and Installation

1. Clone the repository:

```
git clone https://github.com/josephOsemba/students_management_system.git
```

2. Navigate to the project directory:

```
cd PyQT5 Projects
```

3. Set up a virtual environment (optional but recommended):

```
python -m venv venv
source venv/bin/activate    # For Linux/Mac
venv\Scripts\activate       # For Windows
```

4. Install dependencies:

```
pip install -r requirements.txt
```

## Usage

Run the application with the following command:

```
python frontend.py
```
```
python backend.py
```
## Troubleshooting

**Error:** `AttributeError: 'StudentManager' object has no attribute 'update_student'`

**Solution:**

- Ensure the `update_student` method is defined in the `StudentManager` class in `frontend.py`.
- Confirm proper indentation and spelling.

Example method definition:

```python
def update_student(self):
    student_id, ok = QtWidgets.QInputDialog.getInt(self, "Update Student", "Enter Student ID:")
    if not ok:
        return

    dialog = StudentEditDialog(student_id, self)
    dialog.exec_()
```

## Contributing

Feel free to fork this repository and submit pull requests. Any contributions, whether bug fixes, feature additions, or documentation improvements, are welcome.


