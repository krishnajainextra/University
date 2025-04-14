from app import create_app, db
from app.models.user import User
from app.models.college import College, CollegeContact
from app.models.department import Department
from app.models.course import Course, FacultyCourse
from app.models.faculty import Faculty
from app.models.student import Student
from app.models.progress_report import ProgressReport
from werkzeug.security import generate_password_hash

app = create_app()

# Create admin user and sample data for development
@app.cli.command('create-admin')
def create_admin():
    """Create an admin user."""
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@example.com',
            password=generate_password_hash('admin123', method='sha256'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created!')
    else:
        print('Admin user already exists!')

@app.cli.command('create-sample-data')
def create_sample_data():
    """Create sample data for development."""
    # Create colleges
    college1 = College(name='Engineering College', address='123 Main St, City')
    college2 = College(name='Arts College', address='456 Park Ave, City')
    db.session.add_all([college1, college2])
    db.session.flush()
    
    # Create college contacts
    contact1 = CollegeContact(college_id=college1.id, contact_number='123-456-7890')
    contact2 = CollegeContact(college_id=college1.id, contact_number='123-456-7891')
    contact3 = CollegeContact(college_id=college2.id, contact_number='123-456-7892')
    db.session.add_all([contact1, contact2, contact3])
    
    # Create departments
    dept1 = Department(name='Computer Science', college_id=college1.id, head_of_department='Dr. Smith', contact_number='123-456-7893')
    dept2 = Department(name='Electrical Engineering', college_id=college1.id, head_of_department='Dr. Johnson', contact_number='123-456-7894')
    dept3 = Department(name='English', college_id=college2.id, head_of_department='Dr. Williams', contact_number='123-456-7895')
    db.session.add_all([dept1, dept2, dept3])
    db.session.flush()
    
    # Create courses
    course1 = Course(course_number='CS101', title='Introduction to Programming', description='Basic programming concepts', credits=3, year=1, department_id=dept1.id)
    course2 = Course(course_number='CS201', title='Data Structures', description='Advanced data structures', credits=4, year=2, department_id=dept1.id)
    course3 = Course(course_number='EE101', title='Circuit Theory', description='Basic electrical circuits', credits=3, year=1, department_id=dept2.id)
    course4 = Course(course_number='ENG101', title='English Composition', description='Basic writing skills', credits=3, year=1, department_id=dept3.id)
    db.session.add_all([course1, course2, course3, course4])
    db.session.flush()
    
    # Create faculty
    faculty1 = Faculty(name='Prof. Anderson', designation='Assistant Professor', qualification='PhD', contact_number='123-456-7896', address='789 Oak St, City', college_id=college1.id)
    faculty2 = Faculty(name='Prof. Brown', designation='Associate Professor', qualification='PhD', contact_number='123-456-7897', address='101 Pine St, City', college_id=college1.id)
    faculty3 = Faculty(name='Prof. Davis', designation='Professor', qualification='PhD', contact_number='123-456-7898', address='202 Maple St, City', college_id=college2.id)
    db.session.add_all([faculty1, faculty2, faculty3])
    db.session.flush()
    
    # Create faculty-course relationships
    fc1 = FacultyCourse(faculty_id=faculty1.id, course_id=course1.id)
    fc2 = FacultyCourse(faculty_id=faculty1.id, course_id=course2.id)
    fc3 = FacultyCourse(faculty_id=faculty2.id, course_id=course3.id)
    fc4 = FacultyCourse(faculty_id=faculty3.id, course_id=course4.id)
    db.session.add_all([fc1, fc2, fc3, fc4])
    
    # Create students
    student1 = Student(name='John Doe', year=1, contact_number='123-456-7899', address='303 Cedar St, City')
    student2 = Student(name='Jane Smith', year=2, contact_number='123-456-7900', address='404 Birch St, City')
    student3 = Student(name='Bob Johnson', year=3, contact_number='123-456-7901', address='505 Elm St, City')
    student4 = Student(name='Alice Williams', year=4, contact_number='123-456-7902', address='606 Walnut St, City')
    db.session.add_all([student1, student2, student3, student4])
    db.session.flush()
    
    # Create progress reports
    pr1 = ProgressReport(student_id=student1.id, year=1, grade='A', rank=1)
    pr2 = ProgressReport(student_id=student2.id, year=1, grade='B', rank=2)
    pr3 = ProgressReport(student_id=student2.id, year=2, grade='A', rank=1)
    pr4 = ProgressReport(student_id=student3.id, year=1, grade='C', rank=3)
    pr5 = ProgressReport(student_id=student3.id, year=2, grade='B', rank=2)
    pr6 = ProgressReport(student_id=student3.id, year=3, grade='A', rank=1)
    pr7 = ProgressReport(student_id=student4.id, year=1, grade='B', rank=2)
    pr8 = ProgressReport(student_id=student4.id, year=2, grade='B', rank=2)
    pr9 = ProgressReport(student_id=student4.id, year=3, grade='A', rank=1)
    pr10 = ProgressReport(student_id=student4.id, year=4, grade='A', rank=1)
    db.session.add_all([pr1, pr2, pr3, pr4, pr5, pr6, pr7, pr8, pr9, pr10])
    
    db.session.commit()
    print('Sample data created!')

if __name__ == '__main__':
    app.run(debug=True)