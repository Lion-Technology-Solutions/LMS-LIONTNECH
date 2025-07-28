from flask import Blueprint, render_template, url_for, redirect, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from app import db, mail
from app.forms import RegistrationForm, LoginForm, ContactForm, CourseRegistrationForm
from app.models import User, Course, Registration
from flask_mail import Message
from datetime import datetime

main_routes = Blueprint('main_routes', __name__)

@main_routes.route('/')
def index():
    return render_template('index.html')

@main_routes.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        
        # Send welcome email
        msg = Message('Welcome to LionTech LMS',
                      sender='liontechacademy@gmail.com',
                      recipients=[user.email])
        msg.body = f'''Welcome {user.username}!
        
Thank you for registering with LionTech Learning Management System.
You can now login and browse our available courses.'''
        
        mail.send(msg)
        
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('main_routes.login'))
    return render_template('register.html', title='Register', form=form)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_routes.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main_routes.courses'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@main_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main_routes.index'))

@main_routes.route('/courses')
@login_required
def courses():
    courses = Course.query.all()
    form = CourseRegistrationForm()
    return render_template('courses.html', title='Courses', courses=courses, form=form)

@main_routes.route('/register_course', methods=['POST'])
@login_required
def register_course():
    form = CourseRegistrationForm()
    if form.validate_on_submit():
        registration = Registration(user_id=current_user.id, course_id=form.course.data)
        db.session.add(registration)
        db.session.commit()
        
        course = Course.query.get(form.course.data)
        
        # Send notification to admin
        msg = Message('New Course Registration',
                      sender='liontechacademy@gmail.com',
                      recipients=['liontechacademy@gmail.com'])
        msg.body = f'''New course registration:
        
Student: {current_user.username} ({current_user.email})
Course: {course.title}
Date: {datetime.utcnow()}'''
        
        mail.send(msg)
        
        flash('You have successfully registered for the course!', 'success')
    return redirect(url_for('main_routes.courses'))

@main_routes.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Send email
        msg = Message(form.subject.data,
                      sender='liontechacademy@gmail.com',
                      recipients=['liontechacademy@gmail.com'])
        msg.body = f'''From: {form.name.data} <{form.email.data}>
        
{form.message.data}'''
        
        mail.send(msg)
        
        flash('Your message has been sent! We will get back to you soon.', 'success')
        return redirect(url_for('main_routes.contact'))
    return render_template('contact.html', title='Contact Us', form=form)