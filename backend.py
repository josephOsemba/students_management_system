from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)

# SQL Server Connection
server = 'DESKTOP-GG3N3CR\\SQLEXPRESS' 
database = 'students'  
username = 'sa'  
password = 'Joseph13101'  
driver = 'ODBC Driver 17 for SQL Server'

# SQLAlchemy connection string
app.config['SQLALCHEMY_DATABASE_URI'] = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Student Model
class Student(db.Model):
    __tablename__ = 'student_records'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(10), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    second_name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    units = db.Column(db.Text, nullable=False)  # Stores subjects as comma-separated values

# Ensure database & table exist
with app.app_context():
    db.create_all()

# Validate Student Data
def validate_student_data(data):
    required_keys = ["title", "first_name", "second_name", "surname", "gender", "units"]
    missing_fields = [key for key in required_keys if key not in data or not data[key]]
    
    if missing_fields:
        return {"message": f"Missing required fields: {', '.join(missing_fields)}"}, 400
    return None

# Add Student
@app.route("/add_student", methods=["POST"])
def add_student():
    if not request.is_json:
        return jsonify({"message": "Invalid request, JSON data expected"}), 400

    data = request.get_json()
    error = validate_student_data(data)
    if error:
        return jsonify(error[0]), error[1]

    try:
        new_student = Student(
            title=data["title"],
            first_name=data["first_name"],
            second_name=data["second_name"],
            surname=data["surname"],
            gender=data["gender"],
            units=",".join(data["units"]),
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({"message": "Student added successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error adding student", "error": str(e)}), 500

# Delete Student
@app.route("/delete_student/<int:id>", methods=["DELETE"])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404

    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Student deleted successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error deleting student", "error": str(e)}), 500

# Search Student
@app.route("/search_student", methods=["GET"])
def search_student():
    query = request.args.get("name", "").strip().lower()
    if not query:
        return jsonify({"message": "Please provide a name to search."}), 400

    students = Student.query.filter(
        (Student.first_name.ilike(f"%{query}%")) |
        (Student.second_name.ilike(f"%{query}%")) |
        (Student.surname.ilike(f"%{query}%"))
    ).all()

    if not students:
        return jsonify({"message": "No students found."}), 404

    return jsonify([{
        "id": s.id, "first_name": s.first_name, "second_name": s.second_name, "surname": s.surname
    } for s in students])

# Update Student
@app.route("/update_student/<int:id>", methods=["PUT"])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found!"}), 404

    data = request.get_json()

    try:
        student.title = data.get("title", student.title)
        student.first_name = data.get("first_name", student.first_name)
        student.second_name = data.get("second_name", student.second_name)
        student.surname = data.get("surname", student.surname)
        student.gender = data.get("gender", student.gender)
        student.units = ",".join(data.get("units", student.units.split(","))) if "units" in data else student.units

        db.session.commit()
        return jsonify({"message": "Student updated successfully!"})

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error updating student", "error": str(e)}), 500

# Fetch All Students
@app.route("/get_students", methods=["GET"])
def get_students():
    students = Student.query.all()
    student_list = [{
        "id": s.id,
        "title": s.title,
        "first_name": s.first_name,
        "second_name": s.second_name,
        "surname": s.surname,
        "gender": s.gender,
        "units": s.units.split(","),
    } for s in students]
    
    return jsonify(student_list)

if __name__ == "__main__":
    app.run(debug=True)
