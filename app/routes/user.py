from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.models import db, College, Department, Course, Faculty, Student, ProgressReport, User
from flask import render_template
from app.models import Faculty

user = Blueprint('user', __name__)

@user.route('/')
@login_required
def dashboard():
    colleges = College.query.all()
    departments = Department.query.all()
    courses = Course.query.all()
    students = Student.query.all()
    
    return render_template('user/dashboard.html', 
                          colleges=colleges,
                          departments=departments,
                          courses=courses,
                          students=students)

@user.route('/colleges')
@login_required
def colleges():
    colleges = College.query.all()
    return render_template('user/colleges.html', colleges=colleges)

@user.route('/departments')
@login_required
def departments():
    departments = Department.query.all()
    return render_template('user/departments.html', departments=departments)

@user.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    return render_template('user/courses.html', courses=courses)

@user.route('/faculties')
@login_required
def faculties():
    # Fetch all faculty members with their related data
    faculties = Faculty.query.all()
    return render_template('user/faculties.html', faculties=faculties)

@user.route('/students')
@login_required
def students():
    students = Student.query.all()
    return render_template('user/students.html', students=students)

@user.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html')

@user.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Check if username already exists (excluding current user)
        user_by_username = User.query.filter(User.username == username, User.id != current_user.id).first()
        if user_by_username:
            flash('Username already exists.', 'danger')
            return redirect(url_for('user.edit_profile'))
            
        # Check if email already exists (excluding current user)
        user_by_email = User.query.filter(User.email == email, User.id != current_user.id).first()
        if user_by_email:
            flash('Email already exists.', 'danger')
            return redirect(url_for('user.edit_profile'))
            
        # Update user profile
        current_user.username = username
        current_user.email = email
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('user.profile'))
        
    return render_template('user/edit_profile.html')