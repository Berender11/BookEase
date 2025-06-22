from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from datetime import datetime

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=4, max=50)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')

class AppointmentForm(FlaskForm):
    date = DateField('Date', validators=[DataRequired()], default=datetime.today)
    time = SelectField('Time', choices=[
        ('09:00 AM - 10:00 AM', '09:00 AM - 10:00 AM'),
        ('10:00 AM - 11:00 AM', '10:00 AM - 11:00 AM'),
        ('11:00 AM - 12:00 PM', '11:00 AM - 12:00 PM'),
        ('02:00 PM - 03:00 PM', '02:00 PM - 03:00 PM'),
        ('03:00 PM - 04:00 PM', '03:00 PM - 04:00 PM'),
        ('04:00 PM - 05:00 PM', '04:00 PM - 05:00 PM')
    ], validators=[DataRequired()])
    submit = SubmitField('Book Appointment')