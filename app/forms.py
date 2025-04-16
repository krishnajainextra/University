from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SelectField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional, NumberRange

class FacultyForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    designation = StringField('Designation', validators=[DataRequired(), Length(max=100)])
    qualification = StringField('Qualification', validators=[DataRequired(), Length(max=100)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    college_id = SelectField('College', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class CollegeForm(FlaskForm):
    name = StringField('College Name', validators=[DataRequired(), Length(min=2, max=100)])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Save')

class CollegeContactForm(FlaskForm):
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    college_id = SelectField('College', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class DepartmentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    head_of_department = StringField('Head of Department', validators=[DataRequired(), Length(max=100)])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    college_id = SelectField('College', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class CourseForm(FlaskForm):
    course_number = StringField('Course Number', validators=[DataRequired(), Length(max=20)])
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional()])
    credits = IntegerField('Credits', validators=[DataRequired(), NumberRange(min=1)])
    year = SelectField('Year', choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], 
                      coerce=int, validators=[DataRequired()])
    department_id = SelectField('Department', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class FacultyCourseForm(FlaskForm):
    faculty_id = SelectField('Faculty', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

class StudentForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(max=100)])
    year = SelectField('Year', choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], 
                      coerce=int, validators=[DataRequired()])
    contact_number = StringField('Contact Number', validators=[DataRequired(), Length(max=20)])
    address = TextAreaField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ProgressReportForm(FlaskForm):
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    year = SelectField('Year', choices=[(1, '1st Year'), (2, '2nd Year'), (3, '3rd Year'), (4, '4th Year')], 
                      coerce=int, validators=[DataRequired()])
    # You need to update your ProgressReportForm to remove the semester field requirement
    # or update your model to include the semester field
    semester = SelectField('Semester', choices=[(1, 'Semester 1'), (2, 'Semester 2')], 
                         coerce=int, validators=[DataRequired()])
    gpa = StringField('GPA', validators=[DataRequired()])
    remarks = TextAreaField('Remarks', validators=[Optional()])
    submit = SubmitField('Submit')

class UserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Add LoginForm class
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
