from app import db
from datetime import datetime

class Faculty(db.Model):
    __tablename__ = 'faculties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(50), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    
    college_id = db.Column(db.Integer, db.ForeignKey('colleges.id'), nullable=False)
    
    # Relationships
    faculty_courses = db.relationship('FacultyCourse', backref='faculty', lazy=True, cascade='all, delete-orphan')
    
    # Add this relationship to your Faculty model
    college = db.relationship('College', backref='faculties', lazy=True)
    
    def __repr__(self):
        return f'<Faculty {self.name}>'

# Remove the FacultyCourse class from here since it's already defined in course.py