# 📹 ZoomingCLS — Django Classroom Management System

A complete, full-stack classroom management system built with Django.
Teachers can create classrooms, post announcements, assign work, and schedule meetings.
Students can join classes, submit assignments, and interact with their teachers.

---

## 📁 Project Structure

```
zooming-cls/
├── classroom/          # Core classroom app
│   ├── models.py       # Classroom, Post, Comment, Assignment, Submission, Meeting
│   ├── views.py        # All views (CRUD for all features)
│   ├── forms.py        # All forms
│   ├── urls.py         # URL routing
│   └── admin.py        # Admin panel config
│
├── profiles/           # User profiles app
│   ├── models.py       # Profile model (Teacher / Student roles)
│   ├── views.py        # Register, profile view, profile edit
│   ├── forms.py        # RegisterForm, ProfileUpdateForm
│   └── urls.py
│
├── templates/
│   ├── base.html                          # Main layout (sidebar + topbar)
│   ├── registration/login.html            # Login page
│   ├── classroom/
│   │   ├── dashboard.html                 # Home page with classroom cards
│   │   ├── classroom_detail.html          # Stream (posts + class info)
│   │   ├── classroom_form.html            # Create / Edit classroom
│   │   ├── classroom_join.html            # Join by code
│   │   ├── classroom_members.html         # Student list
│   │   ├── assignment_list.html
│   │   ├── assignment_detail.html         # Submit + Grade
│   │   ├── assignment_form.html
│   │   ├── meeting_list.html
│   │   └── meeting_form.html
│   └── profiles/
│       ├── register.html
│       ├── profile.html
│       └── profile_edit.html
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── static/             # CSS, JS, images
├── media/              # User uploaded files
├── manage.py
└── requirements.txt
```

---

## 🚀 Setup & Run

```bash
# 1. Clone / unzip the project
cd zooming-cls

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env

# 5. Run migrations (creates the database)
python manage.py migrate

# 6. Create a superuser (for admin panel)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver

# App → http://127.0.0.1:8000
# Admin → http://127.0.0.1:8000/admin
```

---

## ✨ Features

### 👩‍🏫 Teachers can:
- Create classrooms with a unique join code
- Post announcements, materials, and questions
- Create assignments with due dates and file attachments
- View, grade, and give feedback on student submissions
- Schedule meetings with a Zoom/Google Meet link
- Manage students (view + remove from class)

### 🎓 Students can:
- Join classrooms using a code
- View the class stream (posts and announcements)
- Comment on posts
- View and submit assignments (text or file)
- See their grades and teacher feedback
- View scheduled meetings with join links
- Leave classrooms

---

## 🔑 Default URLs

| Page | URL |
|---|---|
| Login | `/accounts/login/` |
| Register | `/profiles/register/` |
| Dashboard | `/dashboard/` |
| Create Classroom | `/classrooms/create/` |
| Join Classroom | `/classrooms/join/` |
| Admin Panel | `/admin/` |
