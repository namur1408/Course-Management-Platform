# Django Courses Project

A simple Django web application that manages courses and members.
Users can register, log in, and enroll in available courses.


## Installation

1. Clone the repository:

```bash
    git clone https://github.com/namur1408/Django-Web-Application.git
    cd Django-Web-Application
```
2. Install dependencies:
```bash
  pip install -r requirements.txt
``` 
3. Apply migrations
```bash
  python manage.py makemigrations
  python manage.py migrate
``` 

4. Run the development server
```bash
  python manage.py runserver
``` 
5. Open in your browser
```bash
  http://127.0.0.1:8000/
``` 

## Features

 - User Registration

    Custom registration form with:

    - Username

    - First name, Last name

    - Email

    - Phone

    - Address

    - Password confirmation

- User Authentication:

    - Login / Logout using Django’s built-in system.

- Course Management:

    - Create new courses with title, description, start and end date.
 
    - Delete course.

    - Prevents duplicate course names using form validation.

    - Date validation ensures start < end date.

- Course Enrollment:

    - Authenticated users can enroll in courses.

    - Many-to-many relationship between Course and Member.
 
- Custom User

- Adding/Deleting comments under the course

##  Project Structure
```text
mysite/
│
├── courses_app/
│   ├── admins.py          
│   ├── models.py          
│   ├── apps.py            
│   ├── signals.py         
│   ├── views.py           
│   └── urls.py            
│   
│      
│
├── courses_app/
│   ├── admins.py          
│   ├── models.py          # Course model (many-to-many with Member)
│   ├── apps.py          
│   ├── forms.py           # Course creation form with validation
│   ├── views.py           # Course list, creation, and enrollment views
│   ├── urls.py            # Routes for course pages
│   └── templates/
│       └── courses/       # Templates for course list and forms
│
├── members_app/
│   ├── admins.py  
│   ├── models.py          # Member model linked to Django User
│   ├── apps.py    
│   ├── forms.py           # Registration and login forms
│   ├── views.py           # Registration and authentication logic
│   ├── urls.py            # Routes for user auth
│   └── templates/
│       └── registration/  # Login and register pages
├── teachers_app/
│   ├── admins.py  
│   ├── models.py          
│   ├── apps.py    
│   ├── forms.py           
│   ├── views.py           
│   └── urls.py            
│       
│
├── mysite/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
└── README.md      
```

## Technologies Used

- Python 3.13

- Django 5.2.7

- Django REST Framework 3.16

- SimpleJWT 5.5

- pillow 12.0

- django-extensions 4.1

- PostgreSQL (psycopg2-binary 2.9.11)
 
- Bootstrap 5 for styling forms


