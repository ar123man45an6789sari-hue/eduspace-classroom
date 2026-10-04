# 🎓 EduSpace - Digital Classroom Management System

A modern, feature-rich digital classroom management platform built with Django. EduSpace provides a complete solution for teachers and students to manage classes, assignments, materials, and communication in one beautiful interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## ✨ Features

### 👨‍🏫 For Teachers
- **Classroom Management**: Create and manage unlimited virtual classrooms
- **Assignment System**: Create assignments with due dates, attachments, and grading
- **Material Sharing**: Upload and share study materials with students
- **Announcements**: Broadcast important updates to the entire class
- **Student Management**: View enrolled students and track their progress
- **Grading System**: Grade submissions and provide feedback

### 👨‍🎓 For Students
- **Easy Enrollment**: Join classes using unique class codes
- **Assignment Tracking**: View pending and completed assignments
- **Submission Portal**: Submit assignments with optional notes
- **Material Access**: Download shared study materials
- **Grade Tracking**: View grades and feedback from teachers
- **Class Feed**: Stay updated with announcements

## 🚀 Tech Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (Development) / PostgreSQL (Production Ready)
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Custom CSS with modern design system
- **Icons**: Font Awesome 6.5
- **Forms**: Django Crispy Forms with Bootstrap 5

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/eduspace.git
cd eduspace
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Database
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### 6. Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## 📁 Project Structure

```
Sem-4-project/
├── accounts/              # User authentication & profiles
│   ├── models.py         # UserProfile model
│   ├── views.py          # Login, register, profile views
│   ├── forms.py          # User forms
│   └── urls.py           # Account routes
├── classroom/            # Classroom management
│   ├── models.py         # Classroom, Enrollment, Announcement, Material
│   ├── views.py          # Classroom CRUD operations
│   ├── forms.py          # Classroom forms
│   └── urls.py           # Classroom routes
├── assignments/          # Assignment & submission system
│   ├── models.py         # Assignment, Submission models
│   ├── views.py          # Assignment operations
│   ├── forms.py          # Assignment forms
│   └── urls.py           # Assignment routes
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── home.html         # Landing page
│   ├── accounts/         # Auth templates
│   ├── classroom/        # Classroom templates
│   └── assignments/      # Assignment templates
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── forms.js      # Form interactions
│   └── images/           # Icons, illustrations, avatars
├── media/                # User uploaded files
│   ├── assignments/      # Assignment attachments
│   ├── materials/        # Study materials
│   └── submissions/      # Student submissions
├── classroom_clone/      # Django project settings
│   ├── settings.py       # Project configuration
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## 🎨 Key Models

### UserProfile
- Extends Django User model
- Roles: Teacher / Student
- Avatar and bio support

### Classroom
- Name, subject, description
- Unique join code generation
- Teacher ownership
- Cover color customization

### Assignment
- Title, description, due date
- File attachments
- Maximum marks
- Overdue tracking

### Submission
- Student file uploads
- Status tracking (submitted/graded/late)
- Marks and feedback
- Unique per student-assignment

## 🔐 User Roles

### Teacher
- Create and manage classrooms
- Post announcements
- Upload study materials
- Create assignments
- Grade submissions
- Manage enrolled students

### Student
- Join classrooms with code
- View announcements and materials
- Submit assignments
- Track grades and feedback
- View submission history

## 🎯 Usage

### Creating a Classroom (Teacher)
1. Register as a Teacher
2. Click "New Classroom" from dashboard
3. Fill in classroom details
4. Share the generated join code with students

### Joining a Classroom (Student)
1. Register as a Student
2. Click "Join Class"
3. Enter the class code provided by teacher
4. Access classroom materials and assignments

### Creating an Assignment (Teacher)
1. Open your classroom
2. Go to "Assignments" tab
3. Click "Create Assignment"
4. Set title, description, due date, and max marks
5. Optionally attach reference files

### Submitting an Assignment (Student)
1. Open the assignment from your class
2. Click "Submit Assignment"
3. Upload your work file
4. Add optional notes
5. Submit before due date

## 🔧 Configuration

### AI Features

The project includes a separate `ai_assistant` app with permission-scoped tools:

- Students can ask questions about materials in classrooms they are enrolled in.
- Teachers can generate assignment drafts, summarize PDF/DOCX/text materials, create revision quizzes, and request submission feedback suggestions.
- AI grading is advisory only. The teacher must edit and submit the existing grade form before marks or feedback are saved.

Install the AI dependencies and configure the provider on the server:

```powershell
pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-gemini-api-key"
$env:GEMINI_MODEL = "gemini-3.6-flash"  # optional
python manage.py migrate
python manage.py runserver
```

The key is read only by the server and is never exposed to templates or browser JavaScript. Supported material formats are `.pdf`, `.docx`, `.txt`, and `.md`. Copy `.env.example` to `.env` and add your key; the project loads this local ignored file on startup and never commits it.

AI routes are available under `/ai/`. Teachers can also reach the tools from the sidebar and the AI Review action in a submission list.

### Settings (classroom_clone/settings.py)

```python
# Change SECRET_KEY in production
SECRET_KEY = 'your-secret-key-here'

# Set DEBUG to False in production
DEBUG = False

# Configure allowed hosts
ALLOWED_HOSTS = ['yourdomain.com']

# Database configuration (PostgreSQL for production)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'eduspace_db',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 🚀 Deployment

### Heroku Deployment
```bash
# Install Heroku CLI and login
heroku login

# Create new app
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY='your-secret-key'
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser
```

## 📝 Environment Variables

Create a `.env` file for sensitive data:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
DATABASE_URL=your-database-url
ALLOWED_HOSTS=localhost,127.0.0.1
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 🐛 Known Issues

- File upload size limited to Django's default (2.5MB)
- No real-time notifications (planned for future)
- Email notifications not implemented yet

## 🔮 Future Enhancements

- [ ] Real-time chat between teachers and students
- [ ] Video conferencing integration
- [ ] Email notifications for assignments and announcements
- [ ] Mobile responsive design improvements
- [ ] Quiz and test creation module
- [ ] Attendance tracking system
- [ ] Grade analytics and reports
- [ ] Calendar view for assignments
- [ ] Dark mode support
- [ ] Multi-language support

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

## 🙏 Acknowledgments

- Django Documentation
- Font Awesome for icons
- Google Fonts (Inter)
- Inspiration from Google Classroom

## 📞 Support

For support, email your.email@example.com or open an issue in the GitHub repository.

---

⭐ If you find this project helpful, please give it a star!

**Made with ❤️ using Django**
