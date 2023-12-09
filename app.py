from flask import Flask, render_template, request, redirect, url_for, session, flash,g
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy import LargeBinary
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from sqlalchemy import or_,and_
from easygui import *

app = Flask(__name__, template_folder='templates', static_url_path='/static')
app.secret_key = '034c426c843d013262dd0d4292ba9d55'  # Replace with a secure secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ta_app.db'
app.config['UPLOAD_FOLDER'] = 'static/applications'
app.config['UPLOAD_FOLDER2'] = 'static/assignments'
app.config['UPLOAD_FOLDER3'] = 'static/Submitted_assignments'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class TAApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    z_number = db.Column(db.String(10), unique=True)
    current_fau_gpa = db.Column(db.Float)
    phone_number = db.Column(db.String(15))
    department = db.Column(db.String(100))
    level = db.Column(db.String(20))
    password = db.Column(db.String(100), nullable=False)
    enrollment_status = db.Column(db.String(50))
    expected_graduated_year = db.Column(db.Integer)
    citizenship_status = db.Column(db.String(50))
    graduate_program_major = db.Column(db.String(100))

class DepartmentStaff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(100))

class TACommitteMember(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(100))

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    phone_number = db.Column(db.String(20))
    password = db.Column(db.String(100))

class InstructorRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    z_number = db.Column(db.String(10),  nullable=False)
    current_fau_gpa = db.Column(db.Float)
    spring_2024_undergrad_courses = db.Column(db.String(200))
    feedback=db.Column(db.String(200))

class TASelection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    z_number = db.Column(db.String(255), nullable=False) 
    status=db.Column(db.String(255), nullable=False,default="Pending")
     
class AcceptOrDecline(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    z_number = db.Column(db.String(255), nullable=False) 
    name=db.Column(db.String(255), nullable=False) 
    status=db.Column(db.String(255), nullable=False,default="Pending")

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    crn=db.Column(db.String(100), nullable=False)
    course_number = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    term = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.Date, nullable=True)

    

    def __init__(self, subject, crn,course_number, title,term,deadline):
        self.subject = subject
        self.crn=crn
        self.course_number = course_number
        self.title = title
        self.term=term
        self.deadline=deadline


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(200), nullable=False)
    sender_id = db.Column(db.Integer, nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)
    usertype=db.Column(db.String(200), nullable=False)
    usertype2=db.Column(db.String(200), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    z_number=db.Column(db.String(255), nullable=False) 

class ApplicationForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    z_number = db.Column(db.String(10),  nullable=False)
    enrollment_status = db.Column(db.String(50))
    expected_graduated_year = db.Column(db.Integer)
    citizenship_status = db.Column(db.String(50))
    graduate_program_major = db.Column(db.String(100))
    credits_completed_at_fau = db.Column(db.Integer)
    credits_plan_to_register = db.Column(db.Integer)
    current_fau_gpa = db.Column(db.Float)
    undergraduate_major = db.Column(db.String(100))
    courses_served_as_ta = db.Column(db.String(200))
    graduate_courses_completed_at_fau = db.Column(db.String(200))
    undergraduate_courses_completed_at_fau = db.Column(db.String(200))
    spring_2024_undergrad_courses = db.Column(db.String(200))
    is_phd_or_ms_thesis_student = db.Column(db.Boolean)
    document = db.Column(db.String(100))

    def __init__(self, username,z_number, enrollment_status, expected_graduated_year, citizenship_status, graduate_program_major,
                 credits_completed_at_fau, credits_plan_to_register, current_fau_gpa, undergraduate_major,
                 courses_served_as_ta, graduate_courses_completed_at_fau, undergraduate_courses_completed_at_fau,
                 spring_2024_undergrad_courses, is_phd_or_ms_thesis_student,document):
        self.username=username
        self.z_number = z_number
        self.enrollment_status = enrollment_status
        self.expected_graduated_year = expected_graduated_year
        self.citizenship_status = citizenship_status
        self.graduate_program_major = graduate_program_major
        self.credits_completed_at_fau = credits_completed_at_fau
        self.credits_plan_to_register = credits_plan_to_register
        self.current_fau_gpa = current_fau_gpa
        self.undergraduate_major = undergraduate_major
        self.courses_served_as_ta = courses_served_as_ta
        self.graduate_courses_completed_at_fau = graduate_courses_completed_at_fau
        self.undergraduate_courses_completed_at_fau = undergraduate_courses_completed_at_fau
        self.spring_2024_undergrad_courses = spring_2024_undergrad_courses
        self.is_phd_or_ms_thesis_student = is_phd_or_ms_thesis_student
        self.document=document
#-----------------------Home Page-----------------------------------------------#
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        login_as = request.form['login_as']
        if login_as=='TA Applicant':
            return redirect('/login')
        if login_as=="Department Staff":
            return redirect('/deptstafflogin')
        if login_as=='TA Committee':
            return redirect('/tacommittelogin')
        if login_as=='Instructor':
            return redirect('/instructorlogin')
       
    return render_template('index.html')


    

#-----------------------------------TA Applicant--------------------------------------------#
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        z_number = request.form['z_number']
        phone_number = request.form['phone_number']
        department = request.form['department']
        level = request.form['level']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        ta_application = TAApplication(name=name, email=email, z_number=z_number, phone_number=phone_number, department=department, level=level, password=hashed_password)

        try:
            db.session.add(ta_application)
            db.session.commit()
            flash('TA application created successfully!', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('An error occurred while creating the TA application. Please try again.', 'danger')

    return render_template('create.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        ta_application = TAApplication.query.filter_by(email=email).first()

        if ta_application and bcrypt.check_password_hash(ta_application.password, password):
            session['user_id'] = ta_application.id
            flash('Logged in successfully!', 'success')
           
            session['username'] = ta_application.name  # Set the username in the session
            return redirect(url_for('userpage'))
            #return redirect(url_for('userpage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('login.html')
@app.route('/userpage', methods=['GET', 'POST'])
def userpage():
    coursedetails=Course.query.all()
    courses=[]
    for i in coursedetails:
        courses.append(i.subject)
    if 'user_id' in session:
        ta_application = TAApplication.query.get(session['user_id'])
        return render_template('tauser.html', username=ta_application.name,courses=courses)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('login'))
@app.route('/profile')
def profile():
    if 'user_id' in session:
        ta_application = TAApplication.query.get(session['user_id'])
        return render_template('profile.html', username=ta_application.name, email=ta_application.email, z_number=ta_application.z_number, phone_number=ta_application.phone_number, department=ta_application.department, level=ta_application.level)
    else:
        flash('You need to log in to access your profile.', 'danger')
        return redirect(url_for('login'))
@app.route('/edit_profile')
def edit_profile():
    user = TAApplication.query.get(session['user_id'])
    return render_template("edit_profile.html", user=user)

@app.route('/editprofile', methods=['POST'])
def editprofile():
    user = TAApplication.query.get(session['user_id'])
    if user:
        user.current_fau_gpa = request.form['current_fau_gpa']
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        user.department = request.form['department']
        user.level = request.form['level']
        user.enrollment_status = request.form['enrollment_status']
        user.expected_graduated_year = request.form['expected_graduated_year']
        user.citizenship_status = request.form['citizenship_status']
        user.graduate_program_major = request.form['graduate_program_major']

        # Save the changes to the database
        db.session.commit()
        return redirect(url_for('profile'))
    else:
        return "User not found", 404

@app.route('/taApplication/<course>')
def taApplication(course):
    username=session.get('username')
    coursedetails=Course.query.all()
    courses=[]
    data=""
    for i in coursedetails:
        courses.append(i.subject)
        if i.subject==course:
            data+=i.term
    
    return render_template('create_form.html',course=course,courses=courses,term=data,username=username)

@app.route('/submit_form/<course>', methods=['POST'])
def submit_form(course):
    name = session.get('username')
    
    data=TAApplication.query.all()
    z_number = ""
    current_fau_gpa=""
    enrollment_status = ""
    expected_graduated_year = ""
    citizenship_status =""
    graduate_program_major = ""
    for d in data:
        if d.name==name:

            z_number = d.z_number
            current_fau_gpa=d.current_fau_gpa
            enrollment_status = d.enrollment_status
            expected_graduated_year = d.expected_graduated_year
            citizenship_status =d.citizenship_status
            graduate_program_major = d.graduate_program_major
    credits_completed_at_fau = request.form['credits_completed_at_fau']
    credits_plan_to_register = request.form['credits_plan_to_register']
    undergraduate_major = request.form['undergraduate_major']
    courses_served_as_ta = request.form['courses_served_as_ta']
    graduate_courses_completed_at_fau = request.form['graduate_courses_completed_at_fau']
    undergraduate_courses_completed_at_fau = request.form['undergraduate_courses_completed_at_fau']
    spring_2024_undergrad_courses = course
    is_phd_or_ms_thesis_student = request.form.get('is_phd_or_ms_thesis_student') == 'on'
    
    document=request.files['document']

    if document:
        filename = secure_filename(document.filename)
        document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    new_application = ApplicationForm(username=name,
        z_number=z_number,
        current_fau_gpa=current_fau_gpa,
        enrollment_status=enrollment_status,
        expected_graduated_year=expected_graduated_year,
        citizenship_status=citizenship_status,
        graduate_program_major=graduate_program_major,
        credits_completed_at_fau=credits_completed_at_fau,
        credits_plan_to_register=credits_plan_to_register,
        undergraduate_major=undergraduate_major,
        courses_served_as_ta=courses_served_as_ta,
        graduate_courses_completed_at_fau=graduate_courses_completed_at_fau,
        undergraduate_courses_completed_at_fau=undergraduate_courses_completed_at_fau,
        spring_2024_undergrad_courses=spring_2024_undergrad_courses,
        is_phd_or_ms_thesis_student=is_phd_or_ms_thesis_student,
        document=document.filename
    )

    db.session.add(new_application)
    db.session.commit()

    return redirect('/userpage')
@app.route('/application_details')
def application_details():
    coursedetails=Course.query.all()
    courses=[]
    for i in coursedetails:
        courses.append(i.subject)
    username = session.get('username')  
    application = ApplicationForm.query.filter_by(username=username)
    return render_template('application_details.html', application=application,courses=courses,username=username)
@app.route('/edit/<z_number>', methods=['GET', 'POST'])
def edit_application(z_number):
    application = ApplicationForm.query.get(z_number)
    if request.method == 'POST':
        application.username = request.form['username']
        application.enrollment_status = request.form['enrollment_status']
        application.expected_graduated_year = request.form['expected_graduated_year']
        application.citizenship_status = request.form['citizenship_status']
        application.graduate_program_major = request.form['graduate_program_major']
        application.credits_completed_at_fau = request.form['credits_completed_at_fau']
        application.credits_plan_to_register = int(request.form['credits_plan_to_register'])
        application.current_fau_gpa = float(request.form['current_fau_gpa'])
        application.undergraduate_major = request.form['undergraduate_major']
        application.courses_served_as_ta = request.form['courses_served_as_ta']
        application.graduate_courses_completed_at_fau = request.form['graduate_courses_completed_at_fau']
        application.undergraduate_courses_completed_at_fau = request.form['undergraduate_courses_completed_at_fau']
        application.spring_2024_undergrad_courses = request.form['spring_2024_undergrad_courses']
        application.is_phd_or_ms_thesis_student = bool(request.form.get('is_phd_or_ms_thesis_student'))
        document=request.files['document']

        if document:
            filename = secure_filename(document.filename)
            document.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        application.document=document.filename
        db.session.commit()
        return redirect(url_for('userpage'))

    return render_template('edit_application.html', application=application)

@app.route('/delete/<z_number>', methods=['GET'])
def delete_application(z_number):
    application = ApplicationForm.query.get(z_number)
    if application:
        db.session.delete(application)
        db.session.commit()
    return redirect(url_for('userpage'))

@app.route('/acceptordecline', methods=['GET'])
def acceptordecline():
    coursedetails=Course.query.all()
    courses=[]
    for i in coursedetails:
        courses.append(i.subject)
    username = session.get('username')  
    znumber=TAApplication.query.filter_by(name=username).first()
    subjects=TASelection.query.filter_by(z_number=znumber.z_number).all()
    data=[]
    status=[]
    subject=[]
    accept_status=[]
    accept_subject=[]
    accept_znumber=[]
    reject_status=[]
    reject_subject=[]
    reject_znumber=[]
    for s in subjects:
       
        found=AcceptOrDecline.query.filter_by(z_number=znumber.z_number ,subject=s.subject).all()
       
        if found:
            for found in found:
                subject.append(found.subject)
                if found.status=="Accepted":
                    accept_status.append("Accepted")
                    accept_subject.append(found.subject)
                    accept_znumber.append(found.z_number)
                else:
                    reject_status.append("Rejected")
                    reject_subject.append(found.subject)
                    reject_znumber.append(found.z_number)
                
        else:
            if subject:
                #for sub in subject:
                data = TASelection.query.filter(TASelection.z_number == znumber.z_number, TASelection.subject.notin_(subject)).all()
            else:
                data = TASelection.query.filter(TASelection.z_number == znumber.z_number).all()
   
    return render_template('acceptordecline.html',data=data,status_sub=list(zip(accept_status,accept_subject,accept_znumber)),courses=courses,status_sub2=list(zip(reject_status,reject_subject,reject_znumber)),username=username)

@app.route('/accept/<subject>/<znumber>', methods=['GET'])
def accept(subject,znumber):
    username = session.get('username') 
    add_status=AcceptOrDecline(subject=subject,z_number=znumber,name=username,status='Accepted') 
    db.session.add(add_status)
    db.session.commit()
    return redirect(url_for('acceptordecline'))

@app.route('/decline/<subject>/<znumber>', methods=['GET'])
def decline(subject,znumber):
    username = session.get('username') 
    add_status=AcceptOrDecline(subject=subject,z_number=znumber,name=username,status='Declined') 
    db.session.add(add_status)
    db.session.commit()
    return redirect(url_for('acceptordecline'))

@app.route('/accept1/<subject>/<znumber>', methods=['GET'])
def accept1(subject, znumber):
    username = session.get('username')

    # Assuming AcceptOrDecline has composite primary key (subject, z_number)
    add_status = AcceptOrDecline.query.filter_by(z_number=znumber, subject=subject).first()

    if add_status:
        add_status.status = 'Accepted'
        db.session.commit()
        return redirect(url_for('acceptordecline'))
    else:
        # Handle case where no record is found
        return "No record found for provided subject and znumber"


@app.route('/decline1/<subject>/<znumber>', methods=['GET'])
def decline1(subject,znumber):
    username = session.get('username') 
    add_status = AcceptOrDecline.query.filter_by(z_number=znumber, subject=subject).first()

    if add_status:
        add_status.status = 'Declined'
        db.session.commit()
        return redirect(url_for('acceptordecline'))
    else:
        # Handle case where no record is found
        return "No record found for provided subject and znumber"
@app.route('/application_status')
def application_status():
    coursedetails=Course.query.all()
    courses1=[]
    for i in coursedetails:
        courses1.append(i.subject)
    username = session.get('username') 
    #print(username)
    znumber=TAApplication.query.filter_by(name=username).first()
    courses=[]
    
    
    sub=ApplicationForm.query.filter_by(z_number=znumber.z_number).all()
    for subject in sub:
        selection=AcceptOrDecline.query.filter_by(subject=subject.spring_2024_undergrad_courses,z_number=znumber.z_number).all()
        print(subject.spring_2024_undergrad_courses)
        if selection:
            
            
            for j in selection:
                
                
                courses.append((j.subject,j.status+"  by You"))
            
            
        else:
            status=TASelection.query.filter_by(subject=subject.spring_2024_undergrad_courses,z_number=znumber.z_number).all()
            
            if status:
                courses.append((subject.spring_2024_undergrad_courses,"Selected by TA Committe Member"))
            
            else:
                courses.append((subject.spring_2024_undergrad_courses,"Application Processing"))
    
    return render_template('application_status.html', data=courses,username=username,courses1=courses1)

@app.route('/Applicationview/<course>')
def Applicationview(course):
    username = session.get('username') 
    application_details = ApplicationForm.query.filter_by(username=username,spring_2024_undergrad_courses=course).all()
    columns = ApplicationForm.__table__.columns.keys()

    data = []
    for i in application_details:
        if i.spring_2024_undergrad_courses == course:
            row_data = []
            for column in columns:
                value = getattr(i, column)
                row_data.append(f"{value}")
            data.append(row_data)
    
    return render_template('taApplication.html', columns=columns, data=data,course=course,username=username)

#----------------------------Department Staff--------------------------------------------------------------#
@app.route('/deptstaffsignup', methods=['GET', 'POST'])
def deptstaffsignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #z_number = request.form['z_number']
        phone_number = request.form['phone_number']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        deptstaff = DepartmentStaff(name=name, email=email,  phone_number=phone_number, password=hashed_password)

        try:
            db.session.add(deptstaff)
            db.session.commit()
            #flash('TA application created successfully!', 'success')
            return redirect(url_for('deptstafflogin'))
        except Exception as e:
            flash('An error occurred while creating the TA application. Please try again.', 'danger')

    return render_template('deptstaffsignup.html')

@app.route('/deptstafflogin', methods=['GET', 'POST'])
def deptstafflogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        deptstaff = DepartmentStaff.query.filter_by(email=email).first()

        if  deptstaff and bcrypt.check_password_hash( deptstaff.password, password):
            session['user_id'] =  deptstaff.id
            flash('Logged in successfully!', 'success')
           
            session['username'] =  deptstaff.name  # Set the username in the session
            return redirect(url_for('deptstaff'))
            #return redirect(url_for('userpage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('deptstafflogin.html')
@app.route('/deptstaff', methods=['GET', 'POST'])
def deptstaff():
    if 'user_id' in session:
        deptstaff_user = DepartmentStaff.query.get(session['user_id'])
        return render_template('deptstaff.html', username=deptstaff_user.name)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('deptstafflogin'))
    
@app.route('/dept_profile')
def dept_profile():
    if 'user_id' in session:
        dept_data = DepartmentStaff.query.get(session['user_id'])
        return render_template('dept_profile.html', username=dept_data.name, email=dept_data.email, phone_number=dept_data.phone_number, password=dept_data.password)
    else:
        flash('You need to log in to access your profile.', 'danger')
        return redirect(url_for('login'))
@app.route('/edit_dept_profile')
def edit_dept_profile():
    user = DepartmentStaff.query.get(session['user_id'])
    return render_template("edit_dept_profile.html", user=user)

@app.route('/editdeptprofile', methods=['POST'])
def editdeptprofile():
    user = DepartmentStaff.query.get(session['user_id'])
    if user:
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        # Save the changes to the database
        db.session.commit()
        return redirect(url_for('dept_profile'))
    else:
        return "User not found", 404

@app.route('/create_course', methods=['GET', 'POST'])
def create_course():
    dept_data = DepartmentStaff.query.get(session['user_id'])
    if request.method == 'POST':
        subject = request.form.get('subject')
        crn = request.form.get('crn')
        course_number = request.form.get('course_number')
        title = request.form.get('title')
        term=request.form.get('term')
        deadline=request.form.get('deadline')
        deadline=datetime.strptime(deadline, '%Y-%m-%d').date()
        

        if subject and crn and course_number and title:
            new_course = Course(subject=subject, crn=crn,course_number=course_number, title=title,term=term,deadline=deadline)
            db.session.add(new_course)
            db.session.commit()
            return redirect('/courses')
    
    return render_template('create_course.html',username=dept_data.name)
@app.route('/courses')
def list_courses():
    
    dept_data = DepartmentStaff.query.get(session['user_id'])
    courses = Course.query.all()
    
    return render_template('courses.html', courses=courses,username=dept_data.name)

@app.route('/edit_course/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get(course_id)
    
    if course is None:
        return "Course not found", 404  # Return a 404 error if the course doesn't exist
    
    if request.method == 'POST':
        course.subject = request.form.get('subject')
        course.crn=request.form.get('crn')
        course.course_number = request.form.get('course_number')
        course.title = request.form.get('title')
        course.term=request.form.get('term')
        course.deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d').date()
        
        db.session.commit()
        return redirect('/courses')
    
    return render_template('edit_course.html', course=course)
@app.route('/delete_course/<int:course_id>', methods=['GET', 'POST'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    
    if course is None:
        return "Course not found", 404  # Return a 404 error if the course doesn't exist
    
    if course:
        db.session.delete(course)
        db.session.commit()

        return redirect('/courses')
    
@app.route('/depttaApplicationreview')
def depttaApplicationreview():
    deptstaff = DepartmentStaff.query.get(session['user_id'])
    coursedetails=Course.query.all()
    courses=[]
    data=""
    for i in coursedetails:
        courses.append(i.subject)
    
    return render_template('depttaApplicationreview.html',courses=courses,username= deptstaff.name)

@app.route('/depttaApplicationdata/<course>')
def depttaApplicationdata(course):
    deptstaff = DepartmentStaff.query.get(session['user_id'])
    application_details = ApplicationForm.query.filter_by(spring_2024_undergrad_courses=course).all()
    columns = ApplicationForm.__table__.columns.keys()

    data = []
    for i in application_details:
        if i.spring_2024_undergrad_courses == course:
            row_data = []
            for column in columns:
                value = getattr(i, column)
                row_data.append(f"{value}")
            data.append(row_data)
    
    return render_template('depttaApplicationData.html', columns=columns, data=data,course=course,username=deptstaff.name)

@app.route('/taselctionstatus')
def taselctionstatus():
    coursedetails=Course.query.all()
    deptstaff = DepartmentStaff.query.get(session['user_id'])
    courses=[]
    
    for i in coursedetails:
        selection=AcceptOrDecline.query.filter_by(subject=i.subject).all()
        if selection:
            
            
            for j in selection:
                
                courses.append((j.subject,j.z_number,j.name,j.status))
            
            
        else:
            courses.append((i.subject,"","","Pending"))
    
    return render_template('taselctionstatus.html', data=courses,username=deptstaff.name)
@app.route('/show_data/<z_number>')
def show_data(z_number):
    data=TAApplication.query.filter_by(z_number=z_number).first()
    deptstaff = DepartmentStaff.query.get(session['user_id'])
    return render_template('tashowdata.html',user=data,username=deptstaff.name)

import random
@app.route('/tamatching', methods=['GET', 'POST'])
def tamatching():
    deptstaff = DepartmentStaff.query.get(session['user_id'])

    if request.method == 'POST':
        subject_id = request.form['subjectId']
        selected_z_number = request.form[f'znumber']
        subject_name = Course.query.get(subject_id).subject  # Get subject name from the database
        r=Recommendation.query.filter_by(id=random.randint(0,9)).first()
        if r:

        # Save the recommendation to the database
            recommendation = Recommendation(id=random.randint(100,1000), name=deptstaff.name,subject=subject_name,z_number=selected_z_number)
            db.session.add(recommendation)
            db.session.commit()
            msgbox("Your Recommandation is Done!", "Success", "OK" )
            return redirect('/tamatching')
        else:
            recommendation = Recommendation(id=random.randint(0,9), name=deptstaff.name,subject=subject_name,z_number=selected_z_number)
            db.session.add(recommendation)
            db.session.commit()
            msgbox("Your Recommandation is Done!", "Success", "OK" )

            return redirect('/tamatching')

    subjects = Course.query.all()
    znumbers = TAApplication.query.all()
    
    return render_template('tamatching.html', subjects=subjects, znumbers=znumbers, username=deptstaff.name)



#---------------------------TA Committee----------------------------------------------------------------#

@app.route('/tacommittesignup', methods=['GET', 'POST'])
def tacommittesignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #z_number = request.form['z_number']
        phone_number = request.form['phone_number']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        tacommitte = TACommitteMember(name=name, email=email,  phone_number=phone_number, password=hashed_password)

        try:
            db.session.add(tacommitte)
            db.session.commit()
            return redirect(url_for('tacommittelogin'))
        except Exception as e:
            flash('An error occurred while creating the tacommitte signup. Please try again.', 'danger')

    return render_template('tacommittesignup.html')

@app.route('/tacommittelogin', methods=['GET', 'POST'])
def tacommittelogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        tacommitte = TACommitteMember.query.filter_by(email=email).first()

        if  tacommitte and bcrypt.check_password_hash( tacommitte.password, password):
            session['user_id'] =  tacommitte.id
            flash('Logged in successfully!', 'success')
           
            session['username'] =  tacommitte.name  # Set the username in the session
            return redirect(url_for('tacommitte'))
            #return redirect(url_for('userpage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('tacommittelogin.html')
@app.route('/tacommitte', methods=['GET', 'POST'])
def tacommitte():
    if 'user_id' in session:
        tacommitte = TACommitteMember.query.get(session['user_id'])
        return render_template('tacommitte.html', username=tacommitte.name)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('tacommittelogin'))
    
@app.route('/tacommitte_profile')
def tacommitte_profile():
    if 'user_id' in session:
        tacommitte = TACommitteMember.query.get(session['user_id'])
        return render_template('tacommitte_profile.html', username=tacommitte.name, email=tacommitte.email, phone_number=tacommitte.phone_number, password=tacommitte.password)
    else:
        flash('You need to log in to access your profile.', 'danger')
        return redirect(url_for('login'))
@app.route('/edit_tacommitte_profile')
def edit_tacommitte_profile():
    user = TACommitteMember.query.get(session['user_id'])
    return render_template("edit_tacommitte_profile.html", user=user)

@app.route('/edittacommitteprofile', methods=['POST'])
def edittacommitteprofile():
    user = TACommitteMember.query.get(session['user_id'])
    if user:
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        # Save the changes to the database
        db.session.commit()
        return redirect(url_for('tacommitte_profile'))
    else:
        return "User not found", 404
    
@app.route('/taApplicationreview')
def taApplicationreview():
    tacommitte = TACommitteMember.query.get(session['user_id'])
    coursedetails=Course.query.all()
    courses=[]
    data=""
    for i in coursedetails:
        courses.append(i.subject)
    
    return render_template('taApplicationreview.html',courses=courses,username=tacommitte.name)

@app.route('/taApplicationdata/<course>')
def taApplicationdata(course):
    tacommitte = TACommitteMember.query.get(session['user_id'])
    application_details = ApplicationForm.query.filter_by(spring_2024_undergrad_courses=course).all()
    columns = ApplicationForm.__table__.columns.keys()

    # Print the column names
    print("Column Names:", columns)

    data = []
    for i in application_details:
        if i.spring_2024_undergrad_courses == course:
            row_data = []
            for column in columns:
                value = getattr(i, column)
                row_data.append(f"{value}")
            print(row_data)
            data.append(row_data)
    
    return render_template('taApplicationData.html', columns=columns, data=data,course=course,username=tacommitte.name)
@app.route('/taselection')
def taselection():
    coursedetails=Course.query.all()
    # selection=TASelection.query.all()
    courses=[]
    for i in coursedetails:
        selection=TASelection.query.filter_by(subject=i.subject).first()
        if selection:
            courses.append((i.subject,selection.status))
        else:
            courses.append((i.subject,"Pending"))

    return render_template('taselection.html', courses=courses)
@app.route('/selection/<course>', methods=['GET', 'POST'])
def selection(course):
    z_number=[]
    znumbers=TAApplication.query.all()
    for i in znumbers:
        z_number.append(i.z_number)
    if request.method == 'POST':
        z_number = request.form['znumber']
        status="Selected"
        taselected=TASelection(z_number=z_number,subject=course,status=status)
        db.session.add(taselected)
        db.session.commit()
        return redirect(url_for('taselection'))
    return render_template('selection.html',z_number=z_number)

@app.route('/finalise/<course1>', methods=['GET', 'POST'])
def finalise(course1):
    taselected=TASelection.query.filter_by(subject=course1).all()
    for select in taselected:
        select.status="Finalised"
        db.session.commit()
    return redirect(url_for('taselection'))
        
@app.route('/viewdetails/<course>', methods=['GET', 'POST'])
def viewdetails(course):
    znumber=TASelection.query.filter_by(subject=course).all()
    data=[]
    for i in znumber:
        data.append(TAApplication.query.filter_by(z_number=i.z_number).all())
        
    
    
    return render_template('viewdetails.html',data=data)
@app.route('/delete_data/<znumber>', methods=['GET', 'POST'])
def delete_data(znumber):
    record_to_delete = TASelection.query.filter_by(z_number=znumber).first()
    
    if record_to_delete:
        db.session.delete(record_to_delete)
        db.session.commit()
        return redirect(url_for('taselection')) # Or redirect to another endpoint
    else:
        return "Record not found"  
@app.route('/tadecision')
def tadecision():
    coursedetails=Course.query.all()
    # selection=TASelection.query.all()
    courses=[]
    
    for i in coursedetails:
        selection=AcceptOrDecline.query.filter_by(subject=i.subject).all()
        if selection:
            
            
            for j in selection:
                
                courses.append((j.subject,j.z_number,j.name,j.status))
            
            
        else:
            courses.append((i.subject,"","","Pending"))
    
    return render_template('tadecision.html', data=courses)


@app.route('/notifications')
def notifications():
    user = TACommitteMember.query.get(session['user_id'])
    data=AcceptOrDecline.query.all()
    recommand=Recommendation.query.all()
    return render_template('notifications.html',data=data,recommand=recommand,username=user.name)



#---------------------------instructor----------------------------------------------------------------#

@app.route('/instructorsignup', methods=['GET', 'POST'])
def instructorsignup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        #z_number = request.form['z_number']
        phone_number = request.form['phone_number']
        password = request.form['password']

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        instructor = Instructor(name=name, email=email,  phone_number=phone_number, password=hashed_password)

        try:
            db.session.add(instructor)
            db.session.commit()
            return redirect(url_for('instructorlogin'))
        except Exception as e:
            flash('An error occurred while creating the tacommitte signup. Please try again.', 'danger')

    return render_template('instructorsignup.html')

@app.route('/instructorlogin', methods=['GET', 'POST'])
def instructorlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        instructor = Instructor.query.filter_by(email=email).first()

        if  instructor and bcrypt.check_password_hash( instructor.password, password):
            session['user_id'] =  instructor.id
            flash('Logged in successfully!', 'success')
           
            session['username'] =  instructor.name  # Set the username in the session
            return redirect(url_for('instructor'))
            #return redirect(url_for('userpage'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

    return render_template('instructorlogin.html')
@app.route('/instructor', methods=['GET', 'POST'])
def instructor():
    if 'user_id' in session:
        instructor = Instructor.query.get(session['user_id'])
        return render_template('instructor.html', username=instructor.name)
    else:
        flash('You need to log in to access this page.', 'danger')
        return redirect(url_for('instructorlogin'))
    
@app.route('/instructor_profile')
def instructor_profile():
    if 'user_id' in session:
        instructor = Instructor.query.get(session['user_id'])
        return render_template('instructor_profile.html', username=instructor.name, email=instructor.email, phone_number=instructor.phone_number, password=instructor.password)
    else:
        flash('You need to log in to access your profile.', 'danger')
        return redirect(url_for('login'))
@app.route('/edit_instructor_profile')
def edit_instructor_profile():
    user = Instructor.query.get(session['user_id'])
    return render_template("edit_instructor_profile.html", user=user)

@app.route('/editinstructorprofile', methods=['POST'])
def editinstructorprofile():
    user = Instructor.query.get(session['user_id'])
    if user:
        user.email = request.form['email']
        user.phone_number = request.form['phone_number']
        # Save the changes to the database
        db.session.commit()
        return redirect(url_for('instructor_profile'))
    else:
        return "User not found", 404
@app.route('/student_records')
def student_records():
    user = Instructor.query.get(session['user_id'])
    return render_template("student_records.html", username=user.name)
@app.route('/student_data/<sub>')
def student_data(sub):
    username = session.get('username') 
    data=Course.query.filter_by(term=sub).all()
    
    z=[]
    unique_z_numbers = set()
    filtered_data = []

    for i in data:
        znumber=AcceptOrDecline.query.filter_by(subject=i.subject,status='Accepted').all()
       
        if znumber:
            for j in znumber:
                if j.z_number not in unique_z_numbers:
                    unique_z_numbers.add(j.z_number)
                    z.append((j.z_number,j.subject,j.name))
    print(z)         
    return render_template("student_data.html", z=list(set(z)),username=username,sub=sub)




@app.route('/feedback/<znumber>/<subject>/<sub>/', methods=['GET', 'POST'])
def feedback(znumber,subject,sub):
    username = session.get('username')
    record=InstructorRecord.query.filter_by(z_number=znumber).all()
    data = AcceptOrDecline.query.filter_by(z_number=znumber, subject=subject,status='Accepted').all()
    applicants=ApplicationForm.query.filter_by(z_number=znumber,spring_2024_undergrad_courses=subject).all()
    if request.method == 'POST':
        feedback_data = request.form.getlist('feedback')  # Retrieve multiple feedback values
        
        for idx, applicant in enumerate(applicants):
            if idx < len(feedback_data):
                feedback = feedback_data[idx]
                application = InstructorRecord(
                    username=applicant.username,
                    z_number=applicant.z_number,
                    current_fau_gpa=applicant.current_fau_gpa,
                    spring_2024_undergrad_courses=applicant.spring_2024_undergrad_courses,
                    feedback=feedback  # Add feedback field based on your InstructorRecord model
                )
                db.session.add(application)
                db.session.commit()

        return redirect(url_for('feedback',znumber=znumber,subject=subject,sub=sub))  # Redirect to the records page after adding feedback

    return render_template("records.html", sub=sub,applicants=data, username=username,znumber=znumber,subject=subject,record=record)
@app.route('/edit_feedback/<subject>/<znumber>/<sub>/' , methods=['GET', 'POST'])
def edit_feedback(subject,znumber,sub):
    username = session.get('username') 
    record=InstructorRecord.query.filter_by(spring_2024_undergrad_courses=subject,z_number=znumber).first()
    if request.method == 'POST':
        feedback_data = request.form['feedback']
        record.feedback=feedback_data
        db.session.commit()
        
        return redirect(url_for('feedback',znumber=znumber,subject=subject,sub=sub))
    return render_template("records_edit.html", sub=sub,subject=subject,username=username,znumber=znumber,record=record)
@app.route('/records/<znumber>/<subject>/<sub>')
def records(znumber,subject,sub):
    username = session.get('username') 
    user_records = InstructorRecord.query.filter_by(z_number=znumber).all()
    subject_feedback = {}
    if user_records:
        subject_feedback = {}
        for record in user_records:
            subject = record.spring_2024_undergrad_courses
            feedback = record.feedback
            subject_feedback[subject] = feedback
    else:
        user_records=[[]]
    return render_template("showrecords.html", sub=sub,user_records=user_records, subject_feedback=subject_feedback, username=username)
@app.route('/notifications2')
def notifications2():
    user = Instructor.query.get(session['user_id'])
    recommand=Recommendation.query.all()
    return render_template('notifications2.html',recommand=recommand,username=user.name)


@app.route('/tarecords', methods=['GET', 'POST'])
def tarecords():
    username = session.get('username')
    user_records = [[]]
    subject_feedback = {}

    if request.method == 'POST':
        znumber = request.form.get('znumber', '')
        user_records = InstructorRecord.query.filter_by(z_number=znumber.upper()).all()

        if user_records:
            subject_feedback = {record.spring_2024_undergrad_courses: record.feedback for record in user_records}
        else:
            user_records = [[]]
        print(subject_feedback)
        return render_template("tarecords.html", user_records=user_records, subject_feedback=subject_feedback, username=username)

    return render_template("tarecords.html", user_records=user_records, subject_feedback=subject_feedback, username=username)
@app.route('/tarecords2', methods=['GET', 'POST'])
def tarecords2():
    username = session.get('username')
    user_records = [[]]
    subject_feedback = {}

    if request.method == 'POST':
        znumber = request.form.get('znumber', '')
        user_records = InstructorRecord.query.filter_by(z_number=znumber.upper()).all()

        if user_records:
            subject_feedback = {record.spring_2024_undergrad_courses: record.feedback for record in user_records}
        else:
            user_records = [[]]
        print(subject_feedback)
        return render_template("tarecords2.html", user_records=user_records, subject_feedback=subject_feedback, username=username)

    return render_template("tarecords2.html", user_records=user_records, subject_feedback=subject_feedback, username=username)

#---------------------------------Chat operations--------------------------------------------------#



              ###############################Deptstaff chat###############################

@app.route('/deptchat')
def deptchat():
    ta_names = TAApplication.query.all()
    ta_committe_names=TACommitteMember.query.all()
    instructor_names=Instructor.query.all()
    
    deptstaff = DepartmentStaff.query.get(session['user_id'])
    return render_template('deptchat.html', ta_names=ta_names, teacher=deptstaff.name,ta_committe_names=ta_committe_names,instructor_names=instructor_names)



@app.route('/chat/<int:receiver_id>/<type>', methods=['GET', 'POST'])
def chat(receiver_id,type):
    deptstaff = DepartmentStaff.query.get(session['user_id'])
   
    if request.method == 'POST':
        sender_id = request.form.get('sender_id')
        content = request.form.get('content')

        name = DepartmentStaff.query.filter_by(id=sender_id).first()
        
        new_message = Message(name=deptstaff.name, sender_id=deptstaff.id, receiver_id=receiver_id, usertype="Dept Staff",usertype2=type,content=content)
        db.session.add(new_message)
        db.session.commit()

        # Redirect to the same route to prevent form resubmission on page refresh
        return redirect(url_for('chat', receiver_id=receiver_id,type=type))
    name1=[]
    messages = Message.query.filter(
                    or_(
                        and_(
                        Message.sender_id == deptstaff.id,  # Assuming Siva's ID is 2
                        Message.receiver_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.usertype == 'Dept Staff',
                        Message.usertype2 == type
                    ),
                    and_(
                        Message.sender_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.receiver_id == deptstaff.id,  # Assuming Siva's ID is 2
                        Message.usertype == type,
                        Message.usertype2 == 'Dept Staff'
                    )
                )
            ).order_by(Message.timestamp).all()
    for i in messages:
       
        if i.sender_id==deptstaff.id:
            
            name1.append(i.name)
    if len(name1)>0:
        name1=name1[0]
    else:
        name1=""
    print(name1)
    return render_template('chat.html', receiver_id=receiver_id,type=type, messages=messages,name=name1)




    
     ###############################Ta Applicant chat###############################

@app.route('/taapplicantchat')
def  taapplicantchat():
    
    dept_names = DepartmentStaff.query.all()
   
    ta_committe_names=TACommitteMember.query.all()
    instructor_names=Instructor.query.all()
    ta_name = TAApplication.query.get(session['user_id'])
    return render_template('taapplicantchat.html', dept_names=dept_names,ta_committe_names=ta_committe_names,instructor_names=instructor_names, taname=ta_name.name)

@app.route('/tachat/<int:receiver_id>/<type>',methods=['GET', 'POST'])
def tachat(receiver_id,type):
    ta_name = TAApplication.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Get sender, receiver, and content from the form
        sender_id = request.form.get('sender_id')
        content = request.form.get('content')
       
        
        name=TAApplication.query.filter_by(id=sender_id).first()
        # Create a new message and add it to the database
        new_message = Message(sender_id=ta_name.id, name=ta_name.name,receiver_id=receiver_id, usertype="TA",usertype2=type,content=content)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('tachat',receiver_id=receiver_id,type=type))
    name2=[]
    # Retrieve messages between the sender and receiver from the database
    #messages = Message.query.filter_by(receiver_id=receiver_id,sender_id=ta_name.id ,usertype.in_(['TA',type]),usertype2=type).all()
    

    messages = Message.query.filter(
                    or_(
                        and_(
                        Message.sender_id == ta_name.id,  # Assuming Siva's ID is 2
                        Message.receiver_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.usertype == 'TA',
                        Message.usertype2 == type
                    ),
                    and_(
                        Message.sender_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.receiver_id == ta_name.id,  # Assuming Siva's ID is 2
                        Message.usertype == type,
                        Message.usertype2 == 'TA'
                    )
                )
            ).order_by(Message.timestamp).all()

    for i in messages:
        
        if i.sender_id==ta_name.id:
            name2.append(i.name)   
    if len(name2)>0:
        name2=name2[0]
    else:
        name2="" 
    #print(name1)
    return render_template('tachat.html',receiver_id=receiver_id,type=type, messages=messages,name=name2)

           ###############################instructor chat###############################

@app.route('/instructorchat')
def instructorchat():
    ta_names = TAApplication.query.all()
    ta_committe_names=TACommitteMember.query.all()
    deptstaff_names=DepartmentStaff.query.all()
    
    instructor = Instructor.query.get(session['user_id'])
    return render_template('instructorchat.html', ta_names=ta_names, teacher=instructor.name,ta_committe_names=ta_committe_names,deptstaff_names=deptstaff_names)



@app.route('/ichat/<int:receiver_id>/<type>', methods=['GET', 'POST'])
def ichat(receiver_id,type):
    instructor = Instructor.query.get(session['user_id'])
    if request.method == 'POST':
        sender_id = request.form.get('sender_id')
        content = request.form.get('content')

        name = Instructor.query.filter_by(id=sender_id).first()
        
        new_message = Message(name=instructor.name, sender_id=instructor.id, receiver_id=receiver_id, usertype="Instructor",usertype2=type,content=content)
        db.session.add(new_message)
        db.session.commit()

        # Redirect to the same route to prevent form resubmission on page refresh
        return redirect(url_for('ichat', receiver_id=receiver_id,type=type))
    name1=[]
   
    messages = Message.query.filter(
                    or_(
                        and_(
                        Message.sender_id == instructor.id,  # Assuming Siva's ID is 2
                        Message.receiver_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.usertype == 'Instructor',
                        Message.usertype2 == type
                    ),
                    and_(
                        Message.sender_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.receiver_id == instructor.id,  # Assuming Siva's ID is 2
                        Message.usertype == type,
                        Message.usertype2 == 'Instructor'
                    )
                )
            ).order_by(Message.timestamp).all()
    if messages:
        for i in messages:
            
            if i.sender_id==instructor.id:
                print(i.name)
                name1.append(i.name)
        if len(name1)>0:
            name1=name1[0]
        else:
            name1=""
    return render_template('ichat.html', receiver_id=receiver_id, type=type,messages=messages,name=name1)

 ###############################TA COmmitte chat###############################

@app.route('/tacommittechat')
def tacommittechat():
    ta_names = TAApplication.query.all()
    deptstaff_names=DepartmentStaff.query.all()
    instructor_names=Instructor.query.all()
    tacommitte = TACommitteMember.query.get(session['user_id'])
    return render_template('tacommittechat.html', ta_names=ta_names, teacher=tacommitte.name,instructor_names=instructor_names,dept_names=deptstaff_names)



@app.route('/tchat/<int:receiver_id>/<type>', methods=['GET', 'POST'])
def tchat(receiver_id,type):
    tacommitte = TACommitteMember.query.get(session['user_id'])
    if request.method == 'POST':
        sender_id = request.form.get('sender_id')
        content = request.form.get('content')

        
        
        new_message = Message(name=tacommitte.name, sender_id=tacommitte.id, receiver_id=receiver_id, usertype="TA Committe",usertype2=type,content=content)
        db.session.add(new_message)
        db.session.commit()

        # Redirect to the same route to prevent form resubmission on page refresh
        return redirect(url_for('tchat', receiver_id=receiver_id,type=type))
    name1=[]
   
    messages = Message.query.filter(
                    or_(
                        and_(
                        Message.sender_id == tacommitte.id,  # Assuming Siva's ID is 2
                        Message.receiver_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.usertype == 'TA Committe',
                        Message.usertype2 == type
                    ),
                    and_(
                        Message.sender_id == receiver_id,  # Assuming Anvika's ID is 1
                        Message.receiver_id == tacommitte.id,  # Assuming Siva's ID is 2
                        Message.usertype == type,
                        Message.usertype2 == 'TA Committe'
                    )
                )
            ).order_by(Message.timestamp).all()
    
    if messages:
        for i in messages:
           
            if i.sender_id==tacommitte.id:
                
                name1.append(i.name)
        if len(name1)>0:
            name1=name1[0]
        else:
            name1=""
    return render_template('tchat.html', receiver_id=receiver_id, type=type,messages=messages,name=name1)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
