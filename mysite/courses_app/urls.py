from django.urls import path
from .views import enroll_course, CourseListView, CourseCreateView, CourseDeleteView

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path('<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='delete_course'),
]
