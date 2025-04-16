from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')  # 'admin' or 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<User {self.username}>'

class College(db.Model):
    __tablename__ = 'colleges'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Relationships
    departments = db.relationship('Department', backref='college', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('CollegeContact', backref='college', lazy=True, cascade='all, delete-orphan')
    faculties = db.relationship('Faculty', backref='college', lazy=True)
    
    def __repr__(self):
        return f'<College {self.name}>'

class CollegeContact(db.Model):
    __tablename__ = 'college_contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<CollegeContact {self.contact_number}>'

class Department(db.Model):
    __tablename__ = 'departments'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    head_of_department = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    
    # Relationships
    courses = db.relationship('Course', backref='department', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Department {self.name}>'

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    
    # Relationships
    faculty_courses = db.relationship('FacultyCourse', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.course_number} - {self.title}>'

class Faculty(db.Model):
    __tablename__ = 'faculties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    
    # Relationships
    faculty_courses = db.relationship('FacultyCourse', backref='faculty', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Faculty {self.name}>'

class FacultyCourse(db.Model):
    __tablename__ = 'faculty_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    def __repr__(self):
        return f'<FacultyCourse {self.faculty_id} - {self.course_id}>'

class Student(db.Model):
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    
    # Relationships
    progress_reports = db.relationship('ProgressReport', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Student {self.name}>'

# Look for the ProgressReport class definition
class ProgressReport(db.Model):
    __tablename__ = 'progress_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    # Check what the semester field is actually called
    semester = db.Column(db.Integer, nullable=False)  # It might be just 'semester'
    gpa = db.Column(db.String(10), nullable=False)
    remarks = db.Column(db.Text, nullable=True)
    
    # Relationships
    student = db.relationship('Student', backref=db.backref('progress_reports', lazy=True))
    grade = db.Column(db.String(2), nullable=False)  # A, B, C, D, F
    rank = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<ProgressReport {self.student_id} - Year {self.year}>'