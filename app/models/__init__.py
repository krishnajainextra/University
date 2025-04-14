from app import db
from app.models.user import User
from app.models.college import College, CollegeContact
from app.models.department import Department
from app.models.course import Course, FacultyCourse
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.progress_report import ProgressReport

# Export all models
__all__ = [
    'db',
    'User', 
    'College', 
    'CollegeContact', 
    'Department', 
    'Course', 
    'FacultyCourse', 
    'Faculty', 
    'Student', 
    'ProgressReport'
]