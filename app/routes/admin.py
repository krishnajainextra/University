from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app.models import db, College, Department, Course, Faculty, Student, ProgressReport, CollegeContact, User
from functools import wraps
from app.models.course import Course
from app.models.department import Department

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Admin required decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('You need to be an admin to view this page.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/')
@login_required
@admin_required
def dashboard():
    colleges_count = College.query.count()
    departments_count = Department.query.count()
    courses_count = Course.query.count()
    faculties_count = Faculty.query.count()
    students_count = Student.query.count()
    users_count = db.session.execute(db.select(db.func.count()).select_from(db.text('users'))).scalar()
    
    return render_template('admin/dashboard.html', 
                          colleges_count=colleges_count,
                          departments_count=departments_count,
                          courses_count=courses_count,
                          faculties_count=faculties_count,
                          students_count=students_count,
                          users_count=users_count)

@admin.route('/student-progress-data')
@login_required
@admin_required
def student_progress_data():
    # Get student progress data for chart
    year_1_count = Student.query.filter_by(year=1).count()
    year_2_count = Student.query.filter_by(year=2).count()
    year_3_count = Student.query.filter_by(year=3).count()
    year_4_count = Student.query.filter_by(year=4).count()
    
    data = {
        'labels': ['Year 1', 'Year 2', 'Year 3', 'Year 4'],
        'datasets': [{
            'label': 'Number of Students',
            'data': [year_1_count, year_2_count, year_3_count, year_4_count],
            'backgroundColor': [
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            'borderColor': [
                'rgba(75, 192, 192, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            'borderWidth': 1
        }]
    }
    
    return jsonify(data)

@admin.route('/college-departments-data')
@login_required
@admin_required
def college_departments_data():
    # Get college departments data for chart
    colleges = College.query.all()
    
    labels = [college.name for college in colleges]
    data = [len(college.departments) for college in colleges]
    
    chart_data = {
        'labels': labels,
        'datasets': [{
            'label': 'Number of Departments',
            'data': data,
            'backgroundColor': [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            'borderColor': [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            'borderWidth': 1
        }]
    }
    
    return jsonify(chart_data)

# College routes
@admin.route('/colleges')
@login_required
@admin_required
def colleges():
    colleges = College.query.all()
    return render_template('admin/colleges/index.html', colleges=colleges)

@admin.route('/colleges/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_college():
    if request.method == 'POST':
        name = request.form.get('name')
        address = request.form.get('address')
        contact_numbers = request.form.getlist('contact_numbers[]')
        
        # Create new college
        new_college = College(name=name, address=address)
        db.session.add(new_college)
        db.session.flush()  # Flush to get the college ID
        
        # Add contact numbers
        for contact_number in contact_numbers:
            if contact_number:  # Only add non-empty contact numbers
                new_contact = CollegeContact(college_id=new_college.id, contact_number=contact_number)
                db.session.add(new_contact)
        
        db.session.commit()
        flash('College created successfully!', 'success')
        return redirect(url_for('admin.colleges'))
        
    return render_template('admin/colleges/create.html')

@admin.route('/colleges/<int:id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_college(id):
    college = College.query.get_or_404(id)
    
    if request.method == 'POST':
        college.name = request.form.get('name')
        college.address = request.form.get('address')
        
        # Update contact numbers
        # First, remove all existing contacts
        for contact in college.contacts:
            db.session.delete(contact)
        
        # Then add the new ones
        contact_numbers = request.form.getlist('contact_numbers')
        for contact_number in contact_numbers:
            if contact_number:  # Only add non-empty contact numbers
                new_contact = CollegeContact(college_id=college.id, contact_number=contact_number)
                db.session.add(new_contact)
        
        db.session.commit()
        flash('College updated successfully!', 'success')
        return redirect(url_for('admin.colleges'))
        
    return render_template('admin/colleges/edit.html', college=college)

@admin.route('/colleges/<int:id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_college(id):
    college = College.query.get_or_404(id)
    
    # Check if college has departments
    if college.departments:
        flash('Cannot delete college with departments. Delete departments first.', 'danger')
        return redirect(url_for('admin.colleges'))
    
    # Delete all contacts first
    for contact in college.contacts:
        db.session.delete(contact)
    
    # Delete the college
    db.session.delete(college)
    db.session.commit()
    
    flash('College deleted successfully!', 'success')
    return redirect(url_for('admin.colleges'))

# Department routes
@admin.route('/departments')
@login_required
@admin_required
def departments():
    departments = Department.query.all()
    return render_template('admin/departments/index.html', departments=departments)

@admin.route('/departments/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_department():
    if request.method == 'POST':
        name = request.form.get('name')
        college_id = request.form.get('college_id')
        head_of_department = request.form.get('head_of_department')
        contact_number = request.form.get('contact_number')
        
        # Create new department
        new_department = Department(
            name=name,
            college_id=college_id,
            head_of_department=head_of_department,
            contact_number=contact_number
        )
        
        db.session.add(new_department)
        db.session.commit()
        
        flash('Department created successfully!', 'success')
        return redirect(url_for('admin.departments'))
    
    colleges = College.query.all()
    return render_template('admin/departments/create.html', colleges=colleges)
@admin.route('/courses')
@login_required
@admin_required
def courses():
    courses = Course.query.all()
    return render_template('admin/courses/index.html', courses=courses)

@admin.route('/faculties')
@login_required
@admin_required
def faculties():
    faculties = Faculty.query.all()
    return render_template('admin/faculties/index.html', faculties=faculties)

@admin.route('/students')
@login_required
@admin_required
def students():
    students = Student.query.all()
    return render_template('admin/students/index.html', students=students)

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)

@admin.route('/courses/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_course():
    if request.method == 'POST':
        course_number = request.form.get('course_number')
        title = request.form.get('title')
        credits = request.form.get('credits')
        year = request.form.get('year')
        department_id = request.form.get('department_id')
        description = request.form.get('description', '')
        
        # Create new course
        new_course = Course(
            course_number=course_number,
            title=title,
            description=description,
            credits=credits,
            year=year,
            department_id=department_id
        )
        
        db.session.add(new_course)
        db.session.commit()
        
        flash('Course created successfully!', 'success')
        return redirect(url_for('admin.courses'))
    
    departments = Department.query.all()
    return render_template('admin/courses/create.html', departments=departments)

@admin.route('/faculties/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_faculty():
    if request.method == 'POST':
        name = request.form.get('name')
        designation = request.form.get('designation')
        qualification = request.form.get('qualification')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        college_id = request.form.get('college_id') or None
        
        # Create new faculty with all fields
        new_faculty = Faculty(
            name=name,
            designation=designation,
            qualification=qualification,
            contact_number=contact_number,
            address=address,
            college_id=college_id
        )
        
        db.session.add(new_faculty)
        db.session.commit()
        
        flash('Faculty member added successfully!', 'success')
        return redirect(url_for('admin.faculties'))
    
    colleges = College.query.all()
    return render_template('admin/faculties/create.html', colleges=colleges)

@admin.route('/students/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_student():
    if request.method == 'POST':
        name = request.form.get('name')
        contact_number = request.form.get('contact_number')
        year = request.form.get('year')
        address = request.form.get('address')
        
        # Create new student with only valid fields
        new_student = Student(
            name=name,
            contact_number=contact_number,
            year=year,
            address=address
        )
        
        db.session.add(new_student)
        db.session.commit()
        
        flash('Student added successfully!', 'success')
        return redirect(url_for('admin.students'))
    
    return render_template('admin/students/create.html')
