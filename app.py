from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Appointment
from forms import LoginForm, RegisterForm, AppointmentForm
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS') == 'True'

app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
mail = Mail(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            name=form.name.data,
            email=form.email.data, 
            password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        msg = Message(
            subject='Welcome to BookEase!',
            recipients=[new_user.email],
            body=f"""Hi {new_user.name},

Welcome to BookEase! Your account has been successfully created.

We're excited to help you manage your appointments easily.

Best regards,  
BookEase Team
"""
        )
        mail.send(msg)
        flash('Registration Successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login Successful!')
            if user.is_admin:
                return redirect(url_for('admin_panel'))  
            else:
                return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = AppointmentForm()
    if form.validate_on_submit():
        new_app = Appointment(
            date = form.date.data,
            time = form.time.data,
            user_id = current_user.id
        )
        db.session.add(new_app)
        db.session.commit()
        msg = Message('Appointment Confirmation',
              recipients=[current_user.email],
              body=f"Hi {current_user.email},\n\nYour appointment on {form.date.data} at {form.time.data} has been booked successfully.")
        mail.send(msg)
        flash('Appointment booked successfully!')
        return redirect(url_for('dashboard'))
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, appointments=appointments)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash("Unauthorized access.")
        return redirect(url_for('dashboard'))

    appointments = Appointment.query.all()

    if request.method == 'POST' and 'delete_id' not in request.form:
        updated = False
        for appt in appointments:
            new_status = request.form.get(f'status_{appt.id}')
            if new_status and new_status != appt.status:
                appt.status = new_status
                updated = True
        if updated:
            db.session.commit()
            flash('Appointment statuses updated.')
        else:
            flash('No changes made.')

    return render_template('admin_panel.html', appointments=appointments)

@app.route('/delete_appointment', methods=['POST'])
@login_required
def delete_appointment():
    if not current_user.is_admin:
        flash("Unauthorized access.")
        return redirect(url_for('dashboard'))
    appt_id = request.form.get('delete_id')
    if appt_id:
        appt = Appointment.query.get(int(appt_id))
        if appt:
            db.session.delete(appt)
            db.session.commit()
            flash('Appointment deleted.')
    return redirect(url_for('admin_panel'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)