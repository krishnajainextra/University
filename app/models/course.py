from app import db

class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    course_number = db.Column(db.String(20), nullable=False, unique=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    credits = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'), nullable=False)
    
    # Add this relationship
    department = db.relationship('Department', backref='courses', lazy=True)
    
    # Existing relationships
    faculty_courses = db.relationship('FacultyCourse', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Course {self.course_number} - {self.title}>'

class FacultyCourse(db.Model):
    __tablename__ = 'faculty_courses'
    
    id = db.Column(db.Integer, primary_key=True)
    faculty_id = db.Column(db.Integer, db.ForeignKey('faculties.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    
    def __repr__(self):
        return f'<FacultyCourse {self.faculty_id} - {self.course_id}>'