from flask import render_template, flash, redirect, url_for, session
from flask_login import login_user, logout_user, login_required, current_user
from flask.globals import request
from .. import db
from . import auth
from .forms import SignupForm, LoginForm
from ..models import User
from sqlalchemy import exc

@auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(email=form.email.data,
                username=form.username.data,
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
