from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Length(1, 64), 
        Email('this is not email addresss.')])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('keeping login state')
    submit = SubmitField('Sign In')

class SignupForm(FlaskForm):        
    email = StringField('email', validators=[DataRequired('enter the email'), Length(1,64), 
        Email('this is not email.')])
    username = StringField('ID', validators=[
        DataRequired('enter the ID.'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        'ID can use of letter, number, dot, underline.')])
    password = PasswordField('password', validators=[
        DataRequired('enter the password.'), EqualTo('password2', message='not match password.')])
    password2 = PasswordField('password', validators=[DataRequired('check your password.')])
    submit = SubmitField('signup')
    
class Forgetpassword(FlaskForm):        
    email = StringField('email', validators=[DataRequired('enter the email'), Length(1,64), 
        Email('this is not email.')])
    username = StringField('ID', validators=[
        DataRequired('enter the ID.'), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 
        'ID can use of letter, number, dot, underline.')])
    submit = SubmitField('Find password')
