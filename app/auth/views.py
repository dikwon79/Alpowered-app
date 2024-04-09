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
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(email=form.email.data,
                username=form.username.data,
                role = 1,
                password=form.password.data)
                
            try:    
                db.session.add(user)
                db.session.commit()
                flash('you have got member. please login.')                
                return redirect(url_for('main.index'))
            except exc.IntegrityError:
                db.session.rollback()
                flash('already used mail.')
        else:
            flash('already enrolled.')        
    return render_template('auth/signup.html', form=form)

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

@auth.route('/docs', methods=['GET', 'POST'])
def docs():
    # Your code to render a template or return a response
    return render_template('docs.html')
