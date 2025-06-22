from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from models import db, User, Appointment
from forms import LoginForm, RegisterForm, AppointmentForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appointments.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'berendery1@gmail.com'
app.config['MAIL_PASSWORD'] = 'ipwr wepn qemp jvup'
app.config['MAIL_DEFAULT_SENDER'] = 'berendery1@gmail.com'
mail = Mail(app)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @app.before_first_request
# def create_tables():
#     db.create_all()

@app.route('/')
def home():
    return redirect(url_for('login'))

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

    if request.method == 'POST':
        appt_id = request.form.get('appt_id')
        new_status = request.form.get('status')
        appt = Appointment.query.get(int(appt_id))
        if appt:
            appt.status = new_status
            db.session.commit()
            flash('Appointment status updated.')

    return render_template('admin_panel.html', appointments=appointments)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)