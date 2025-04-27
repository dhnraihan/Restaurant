# 🍽️ Tasty Restaurant Management System

A complete restaurant management system built with Django, featuring online ordering, menu management, user profiles, reservations, and invoice generation.

![Restaurant Management System](demo.gif)

---

## ✨ Features

### 🧑‍🍳 Customer-Facing Features
- 🧒 **Interactive Menu**: Browse food items by categories with search functionality
- 🔐 **User Authentication**: Register, login, and maintain profile information
- 🛒 **Shopping Cart**: Add/remove items and adjust quantities
- 🛕️ **Online Ordering**: Complete checkout process with delivery information
- 🗕️ **Reservation System**: Book tables specifying date, time, and party size
- 📩 **Contact Form**: Submit inquiries directly through the website

### 🛠️ Administrative Features
- 🍴 **Menu Management**: Add, edit, and categorize menu items
- 🪑 **Reservation Management**: View and manage table reservations
- 🚚 **Order Processing**: Track orders from pending to completion
- 🧳️ **Invoice Generation**: Automatic PDF invoice creation for orders
- 🧑‍💻 **User Management**: Manage customer accounts and profiles

---

## 🧰 Tech Stack

- 🖥️ **Backend**: Django 5.2
- 🎨 **Frontend**: HTML, CSS (Tailwind CSS v4), JavaScript
- 💄️ **Database**: SQLite (development), PostgreSQL (recommended for production)
- 📄 **PDF Generation**: ReportLab
- ✨ **UI Enhancements**: Alpine.js, Font Awesome

---

## 📁 Project Structure

```
├── home/                   # Main app for website content
│   ├── models.py           # Menu and reservation models
│   ├── views.py            # Core website views
│   ├── forms.py            # Reservation and contact forms
│   └── admin.py            # Admin configurations
│
├── user/                   # User management app
│   ├── models.py           # User profile, order, and invoice models
│   ├── views.py            # User account and order views
│   ├── forms.py            # User related forms
│   └── signals.py          # Signals for profile and invoice creation
│
├── templates/              # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── home/               # Home app templates
│   └── user/               # User app templates
│
└── media/                  # User uploaded content
    ├── menu_items/         # Food images
    ├── categories/         # Category images
    ├── profiles/           # User profile pictures
    └── invoices/           # Generated PDF invoices
```

---

## 🚀 Installation and Setup

### 📋 Prerequisites
- Python 3.10 or higher 🐍
- pip (Python package manager) 📦
- Virtual environment (recommended) 🌐

### ⚙️ Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/dhnraihan/Restaurant.git
   cd Restaurant
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv

   # On Windows
   venv\Scripts\activate

   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the website**
   - 🌐 Website: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   - 🔑 Admin panel: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## ⚙️ Configuration

### 🖼️ Media Files
Configure your `settings.py` to handle media uploads:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

### 📧 Email Settings
Set up email settings for order confirmations and contact forms:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.your-email-provider.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-password'
```

---

## 🚢 Deployment

For production deployment:

- 🔒 Set `DEBUG = False` in settings.py
- 📄️ Use PostgreSQL as your production database
- 🌐 Serve static and media files properly (e.g., Nginx)
- 🏎️ Use Gunicorn or uWSGI as the WSGI server
- 🛡️ Secure your app with HTTPS (SSL certificate)

---

## 🤝 Contributing

1. Fork the repository 🍴
2. Create your feature branch (`git checkout -b feature/amazing-feature`) 🌟
3. Commit your changes (`git commit -m 'Add some amazing feature'`) ✍️
4. Push to the branch (`git push origin feature/amazing-feature`) 🚀
5. Open a Pull Request 🔥

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgements

- 🐍 Django framework and community
- 🎨 Tailwind CSS for the responsive design
- ⭐ Font Awesome for the icons
- ❤️ All contributors who have helped with development

---

