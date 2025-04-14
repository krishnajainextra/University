from app import db
from datetime import datetime

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    address = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress_reports = db.relationship('ProgressReport', backref='student', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Student {self.name}>'