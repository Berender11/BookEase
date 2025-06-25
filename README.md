# 🗓️ BookEase – Appointment Booking System

**BookEase** is a full-featured, production-ready **Flask web application** that allows users to register, log in, and book appointments through an intuitive interface. It supports **role-based access control** with separate dashboards for users and admins. Admins can view all appointments and update their status in real-time. The system integrates **email notifications**, secure authentication, and a clean UI — making it ideal for small clinics, salons, or consultancy services.

---

## 🚀 Features

- 🔐 **User Authentication** – Secure registration and login using `Flask-Login`
- 👥 **Role-Based Access** – Different views for users and admins
- 📅 **Appointment Booking** – Book by selecting date and time slots
- 🛠 **Admin Panel** – View all appointments and update statuses (Pending, Confirmed, Cancelled)
- 📬 **Email Alerts** – SMTP-based email notifications on registration and booking
- 🎨 **Clean UI** – Built with HTML, CSS, and Jinja2 templating
- ☁️ **Live Deployed** – Hosted on Render with Gunicorn and environment-based configuration

---

## 🧰 Tech Stack

- **Backend:** Python, Flask, SQLite, SQLAlchemy
- **Authentication:** Flask-Login, Werkzeug security
- **Forms & Validation:** Flask-WTF
- **Email Integration:** Flask-Mail with SMTP (Gmail App Password)
- **Templating & UI:** Jinja2, HTML5, CSS3
- **Deployment:** Gunicorn + Render

---

## 🌐 Live Demo

👉 [https://bookease-oxuh.onrender.com](https://bookease-oxuh.onrender.com)

---

<!-- ## 📸 Screenshots (optional)

_Add screenshots of login page, dashboard, booking form, and admin panel here for better presentation._

--- -->

## 📂 How to Run Locally

```bash
git clone https://github.com/Berender11/BookEase.git
cd BookEase
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Configure these variables in `app.py`:

```env
SECRET_KEY=your_secret_key
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your_email@gmail.com
MAIL_PASSWORD=your_app_password
MAIL_DEFAULT_SENDER=your_email@gmail.com
```

Finally:

```bash
python app.py
```

---

## 💡 Future Enhancements

- [ ] Google Calendar integration
- [ ] Email appointment reminders
- [ ] Rescheduling and cancellation by users
- [ ] Pagination and filters in admin panel
- [ ] SMS notifications via Twilio

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
