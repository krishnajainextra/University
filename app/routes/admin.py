from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user  # Add current_user here
from functools import wraps
from app.models import (
    College, CollegeContact, Department, Course, 
    Faculty, FacultyCourse, Student, ProgressReport, User, db
)
from app.forms import (
    CollegeForm, CollegeContactForm, DepartmentForm, CourseForm,
    FacultyForm, FacultyCourseForm, StudentForm, ProgressReportForm, UserForm
)

admin = Blueprint('admin', __name__, url_prefix='/admin')

# Decorator for admin-only routes
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        # Check if user is admin
        if not current_user.role == 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

# Add a dashboard route
@admin.route('/')
@admin.route('/dashboard')
@admin_required
def dashboard():
    # Count of each model for dashboard statistics
    stats = {
        'colleges': College.query.count(),
        'departments': Department.query.count(),
        'courses': Course.query.count(),
        'faculty': Faculty.query.count(),
        'students': Student.query.count(),
        'reports': ProgressReport.query.count(),
        'users': User.query.count()
    }
    return render_template('admin/dashboard.html', stats=stats)

# College CRUD
@admin.route('/colleges')
@admin_required
def colleges():
    colleges = College.query.all()
    return render_template('admin/colleges/index.html', colleges=colleges)

@admin.route('/colleges/create', methods=['GET', 'POST'])
@admin_required
def create_college():
    form = CollegeForm()
    if request.method == 'POST':
        print("College form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("College form validated successfully!")
            college = College(
                name=form.name.data,
                address=form.address.data
            )
            db.session.add(college)
            db.session.commit()
            
            # Handle contact numbers
            contact_numbers = request.form.getlist('contact_numbers[]')
            for number in contact_numbers:
                if number.strip():  # Only add non-empty contact numbers
                    contact = CollegeContact(college_id=college.id, contact_number=number.strip())
                    db.session.add(contact)
            
            db.session.commit()
            flash('College created successfully!', 'success')
            return redirect(url_for('admin.colleges'))
        else:
            print(f"College form validation errors: {form.errors}")
    
    return render_template('admin/colleges/create.html', form=form)

@admin.route('/colleges/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_college(id):
    college = College.query.get_or_404(id)
    form = CollegeForm(obj=college)
    
    if form.validate_on_submit():
        # Update college details
        form.populate_obj(college)
        
        # Handle contact numbers
        contact_numbers = request.form.getlist('contact_numbers')
        
        # Delete existing contacts
        for contact in college.contacts:
            db.session.delete(contact)
        
        # Add new contacts
        for number in contact_numbers:
            if number.strip():  # Only add non-empty contact numbers
                contact = CollegeContact(college_id=college.id, contact_number=number.strip())
                db.session.add(contact)
        
        db.session.commit()
        flash('College updated successfully!', 'success')
        return redirect(url_for('admin.colleges'))

@admin.route('/colleges/delete/<int:id>', methods=['POST'])
@admin_required
def delete_college(id):
    college = College.query.get_or_404(id)
    
    # Check if there are any departments associated with this college
    departments = Department.query.filter_by(college_id=id).all()
    if departments:
        flash('Cannot delete college because it has associated departments. Delete the departments first.', 'danger')
        return redirect(url_for('admin.colleges'))
    
    # If no departments, proceed with deletion
    db.session.delete(college)
    
    try:
        db.session.commit()
        flash('College deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting college: {str(e)}', 'danger')
    
    return redirect(url_for('admin.colleges'))

# Department CRUD
@admin.route('/departments')
@admin_required
def departments():
    departments = Department.query.all()
    return render_template('admin/departments/index.html', departments=departments)

@admin.route('/departments/create', methods=['GET', 'POST'])
@admin_required
def create_department():
    form = DepartmentForm()
    # Set the choices for the college_id field
    form.college_id.choices = [(c.id, c.name) for c in College.query.all()]
    
    if request.method == 'POST':
        print("Form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("Form validated successfully!")
            department = Department(
                name=form.name.data,
                head_of_department=form.head_of_department.data,
                contact_number=form.contact_number.data,
                college_id=form.college_id.data
            )
            db.session.add(department)
            db.session.commit()
            flash('Department created successfully!', 'success')
            return redirect(url_for('admin.departments'))
        else:
            print(f"Form validation errors: {form.errors}")
    
    return render_template('admin/departments/create.html', form=form)

@admin.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_department(id):
    department = Department.query.get_or_404(id)
    form = DepartmentForm(obj=department)
    form.college_id.choices = [(c.id, c.name) for c in College.query.all()]
    if form.validate_on_submit():
        form.populate_obj(department)
        db.session.commit()
        flash('Department updated successfully!', 'success')
        return redirect(url_for('admin.departments'))
    return render_template('admin/departments/edit.html', form=form, department=department)

@admin.route('/departments/delete/<int:id>', methods=['POST'])
@admin_required
def delete_department(id):
    department = Department.query.get_or_404(id)
    
    # Check if there are any courses associated with this department
    courses = Course.query.filter_by(department_id=id).all()
    if courses:
        # Option 1: Prevent deletion
        flash('Cannot delete department because it has associated courses. Delete the courses first.', 'danger')
        return redirect(url_for('admin.departments'))
        
        # Option 2 (alternative): Delete all associated courses
        # for course in courses:
        #     db.session.delete(course)
    
    # If no courses, proceed with deletion
    db.session.delete(department)
    
    try:
        db.session.commit()
        flash('Department deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting department: {str(e)}', 'danger')
    
    return redirect(url_for('admin.departments'))

# Course CRUD
@admin.route('/courses')
@admin_required
def courses():
    courses = Course.query.all()
    return render_template('admin/courses/index.html', courses=courses)

@admin.route('/courses/create', methods=['GET', 'POST'])
@admin_required
def create_course():
    form = CourseForm()
    departments = Department.query.all()
    
    # Check if there are any departments
    if not departments:
        flash('Please create at least one department before adding courses.', 'warning')
        return redirect(url_for('admin.departments'))
        
    form.department_id.choices = [(d.id, d.name) for d in departments]
    
    if request.method == 'POST':
        print("Course form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("Course form validated successfully!")
            course = Course(
                course_number=form.course_number.data,
                title=form.title.data,
                description=form.description.data,
                credits=form.credits.data,
                year=form.year.data,
                department_id=form.department_id.data
            )
            db.session.add(course)
            db.session.commit()
            flash('Course created successfully!', 'success')
            return redirect(url_for('admin.courses'))
        else:
            print(f"Course form validation errors: {form.errors}")
    
    return render_template('admin/courses/create.html', form=form, departments=departments)

@admin.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_course(id):
    course = Course.query.get_or_404(id)
    form = CourseForm(obj=course)
    form.department_id.choices = [(d.id, d.name) for d in Department.query.all()]
    if form.validate_on_submit():
        form.populate_obj(course)
        db.session.commit()
        flash('Course updated successfully!', 'success')
        return redirect(url_for('admin.courses'))
    return render_template('admin/courses/edit.html', form=form, course=course)

@admin.route('/courses/delete/<int:id>', methods=['POST'])
@admin_required
def delete_course(id):
    course = Course.query.get_or_404(id)
    db.session.delete(course)
    db.session.commit()
    flash('Course deleted successfully!', 'success')
    return redirect(url_for('admin.courses'))

# Faculty CRUD
@admin.route('/faculties')
@admin_required
def faculties():
    faculties = Faculty.query.all()
    # Create an empty form for CSRF protection
    form = FacultyForm()
    return render_template('admin/faculties/index.html', faculties=faculties, form=form)

@admin.route('/faculties/create', methods=['GET', 'POST'])
@admin_required
def create_faculty():
    form = FacultyForm()
    colleges = College.query.all()
    
    # Check if there are any colleges
    if not colleges:
        flash('Please create at least one college before adding faculty.', 'warning')
        return redirect(url_for('admin.colleges'))
        
    form.college_id.choices = [(c.id, c.name) for c in colleges]
    
    if request.method == 'POST':
        print("Faculty form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("Faculty form validated successfully!")
            faculty = Faculty(
                name=form.name.data,
                designation=form.designation.data,
                qualification=form.qualification.data,
                contact_number=form.contact_number.data,
                address=form.address.data,
                college_id=form.college_id.data
            )
            db.session.add(faculty)
            db.session.commit()
            flash('Faculty created successfully!', 'success')
            return redirect(url_for('admin.faculties'))
        else:
            print(f"Faculty form validation errors: {form.errors}")
    
    return render_template('admin/faculties/create.html', form=form)

@admin.route('/faculties/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    form = FacultyForm(obj=faculty)
    form.college_id.choices = [(c.id, c.name) for c in College.query.all()]
    if form.validate_on_submit():
        form.populate_obj(faculty)
        db.session.commit()
        flash('Faculty updated successfully!', 'success')
        return redirect(url_for('admin.faculties'))
    return render_template('admin/faculties/edit.html', form=form, faculty=faculty)

@admin.route('/faculties/delete/<int:id>', methods=['POST'])
@admin_required
def delete_faculty(id):
    faculty = Faculty.query.get_or_404(id)
    db.session.delete(faculty)
    
    try:
        db.session.commit()
        flash('Faculty deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting faculty: {str(e)}', 'danger')
    
    return redirect(url_for('admin.faculties'))

# Student CRUD
@admin.route('/students')
@admin_required
def students():
    students = Student.query.all()
    # Create an empty form for CSRF protection
    form = StudentForm()
    return render_template('admin/students/index.html', students=students, form=form)

@admin.route('/students/create', methods=['GET', 'POST'])
@admin_required
def create_student():
    form = StudentForm()
    
    if request.method == 'POST':
        print("Student form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("Student form validated successfully!")
            student = Student(
                name=form.name.data,
                year=form.year.data,
                contact_number=form.contact_number.data,
                address=form.address.data
            )
            db.session.add(student)
            db.session.commit()
            flash('Student created successfully!', 'success')
            return redirect(url_for('admin.students'))
        else:
            print(f"Student form validation errors: {form.errors}")
    
    return render_template('admin/students/create.html', form=form)

@admin.route('/students/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_student(id):
    student = Student.query.get_or_404(id)
    form = StudentForm(obj=student)
    if form.validate_on_submit():
        form.populate_obj(student)
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect(url_for('admin.students'))
    return render_template('admin/students/edit.html', form=form, student=student)

@admin.route('/students/delete/<int:id>', methods=['POST'])
@admin_required
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect(url_for('admin.students'))

# Progress Report CRUD
@admin.route('/progress-reports')
@admin_required
def progress_reports():
    reports = ProgressReport.query.all()
    # Create an empty form for CSRF protection
    form = ProgressReportForm()
    return render_template('admin/progress_reports/index.html', reports=reports, form=form)

@admin.route('/progress-reports/create', methods=['GET', 'POST'])
@admin_required
def create_progress_report():
    form = ProgressReportForm()
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    
    if request.method == 'POST':
        print("Progress report form submitted!")
        print(f"Form data: {request.form}")
        
        if form.validate_on_submit():
            print("Progress report form validated successfully!")
            # Create report with the fields that actually exist in the model
            report = ProgressReport(
                student_id=form.student_id.data,
                year=form.year.data,
                grade=form.gpa.data,  # Using gpa field from form for grade
                rank=0,  # Providing a default value for rank
                # Note: semester field is not in the model, so we don't include it
            )
            db.session.add(report)
            db.session.commit()
            flash('Progress Report created successfully!', 'success')
            return redirect(url_for('admin.progress_reports'))
        else:
            print(f"Progress report form validation errors: {form.errors}")
    
    return render_template('admin/progress_reports/create.html', form=form)

@admin.route('/progress-reports/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_progress_report(id):
    report = ProgressReport.query.get_or_404(id)
    form = ProgressReportForm(obj=report)
    form.student_id.choices = [(s.id, s.name) for s in Student.query.all()]
    
    # Map the grade field to gpa in the form
    if request.method == 'GET':
        form.gpa.data = report.grade
    
    if form.validate_on_submit():
        report.student_id = form.student_id.data
        report.year = form.year.data
        report.grade = form.gpa.data  # Map gpa from form to grade in model
        report.remarks = form.remarks.data
        # If your form has a rank field, update it here
        # report.rank = form.rank.data
        db.session.commit()
        flash('Progress Report updated successfully!', 'success')
        return redirect(url_for('admin.progress_reports'))
    else:
        # Print form errors for debugging
        print(f"Form validation errors: {form.errors}")
    
    return render_template('admin/progress_reports/edit.html', form=form, report=report)

@admin.route('/progress-reports/delete/<int:id>', methods=['POST'])
@admin_required
def delete_progress_report(id):
    report = ProgressReport.query.get_or_404(id)
    db.session.delete(report)
    db.session.commit()
    flash('Progress Report deleted successfully!', 'success')
    return redirect(url_for('admin.progress_reports'))

# User CRUD
@admin.route('/users')
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users/index.html', users=users)

@admin.route('/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # You should hash this password
            role=form.role.data
        )
        db.session.add(user)
        db.session.commit()
        flash('User created successfully!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/users/create.html', form=form)

@admin.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    # Don't require password for edit
    form.password.validators = []
    form.confirm_password.validators = []
    
    # Remove password fields from form
    delattr(form, 'password')
    delattr(form, 'confirm_password')
    
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.role = form.role.data
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin.users'))
    return render_template('admin/users/edit.html', form=form, user=user)

@admin.route('/users/delete/<int:id>', methods=['POST'])
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    
    # Don't allow deleting the current user
    if current_user.id == user.id:
        flash('You cannot delete your own account.', 'danger')
        return redirect(url_for('admin.users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'danger')
    
    return redirect(url_for('admin.users'))
