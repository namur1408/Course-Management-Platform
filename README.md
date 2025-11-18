# Django Courses Project

A Django web application designed for managing courses, teachers, and user interactions.
The platform allows users to register, authenticate, enroll in courses, leave comments, and interact with dynamic course content.
The project demonstrates practical implementation of Django basics, advanced features, and backend architecture patterns.

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

- Custom registration
      
- Custom User System
  
    - Custom user model
      
    - JWT authentication
 
    - login/logout flows
 
    - Role-based permissions for admins and content creators

- Course Management:

    - Create, update, and delete courses
 
    - Each course includes
      
       - Title, description
     
       - Start and end dates
     
       - Assigned teacher
     
       - Creator
     
       - Many-to-many student enrollment

    - Prevents duplicate course names using form validation

    - Date validation ensures start < end date

- Course Enrollment

    - Authenticated users can enroll in courses

    - Many-to-many relationship between Course and Member

- Comment System

    - Users can leave comments under each course

    - Delete/edit permissions: users can delete only their own comments; admins can delete any

    - GenericRelation for attaching action logs

- Action Log System

    - ActionLog model tracks:

    - User actions (create/delete courses, enroll, comment, login/logout, etc.)

    - Timestamp and user info

    - Lcustom pre_delete signal safely nullifies content_type and object_id


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
├── courses_api/      
│   ├── apps.py          
│   ├── auth.py           
│   └──  views.py        
│
├── courses_app/
│   ├── admins.py          
│   ├── models.py          
│   ├── apps.py          
│   ├── forms.py           
│   ├── views.py           
│   ├── urls.py            
│   └── templates/
│       └── courses/       
│
├── members_app/
│   ├── admins.py  
│   ├── models.py          
│   ├── apps.py    
│   ├── forms.py           
│   ├── views.py           
│   ├── urls.py           
│   └── templates/
│       └── registration/  
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


