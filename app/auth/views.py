from flask import render_template, flash, redirect, url_for, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask.globals import request
from .. import db, mail
from . import auth
from .forms import SignupForm, LoginForm, Forgetpassword
from ..models import User
from sqlalchemy import exc
from flask_mail import Message


@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    data = request.get_json()

    # JSON으로부터 필요한 데이터 추출
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    password2 = data.get('password2')

    # 유효성 검사 등 필요한 로직 수행
    if not email or not username or not password or not password2:
        return jsonify({'error': 'All fields are required'}), 400

    if password != password2:
        return jsonify({'error': 'Passwords do not match'}), 400

    # 새로운 사용자 생성
    new_user = User(email=email, username=username, password=password)

    try:
        # 데이터베이스에 사용자 추가
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        # 데이터베이스 오류 발생 시
        db.session.rollback()
        return jsonify({'error': 'Failed to create user'}), 500

@auth.route('/forgetpassword/', methods=['GET', 'POST'])
def forgetpassword():
    form = Forgetpassword()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        user = User.query.filter_by(username=username, email=email).first()
        if user:
            # Generate a new password (you may want to use a more secure method)
            new_password = generate_new_password()  # You need to implement this function
            
            # Update the user's password in the database
            user.set_password(new_password)
            db.session.commit()
            
            # Send the new password to the user's email
            send_password_reset_email(user.email, new_password)
            
            flash('Your new password has been sent to your email.')
        else:
            flash('User not found.')
        return redirect(url_for('auth.login'))  # Redirect to login page after displaying password reset message
    return render_template('auth/forget_password.html', form=form)


def generate_new_password():
    # Implement your logic to generate a new password
    # For example, you can use the secrets module to generate a random password
    import secrets
    new_password = secrets.token_hex(8)  # Generate an 8-character random hexadecimal string
    return new_password

def send_password_reset_email(email, new_password):
    # Create a message object
    msg = Message('Password Reset', sender='dikwon79@gmail.com', recipients=[email])
    
    # Set the message body
    msg.body = f'Your new password is: {new_password}'
    
    # Send the email
    mail.send(msg)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    
    if current_user.is_authenticated:
        if current_user.username == 'admin':
            return redirect(url_for('main.admin'))
        else:
            return redirect(url_for('main.index'))
    
    form = LoginForm() 
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                # check the mail address starting with admin
                if user.email.startswith('admin'):
                    # redirection to admin page
                    return redirect(url_for('main.admin'))
                else:
                    next = url_for('main.index')  #user to main.index
            return redirect(next)
        flash('check your email or password.')   
    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logout completed.')
    return redirect(url_for('main.index'))  
