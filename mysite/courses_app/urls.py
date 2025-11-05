from django.urls import path
from .views import (
    CourseListView,
    CourseCreateView,
    CourseDeleteView,
    CourseUpdateView,
    CourseDetailView,
    enroll_course,
    unenroll_course,
    comment_course
)

urlpatterns = [
    path('', CourseListView.as_view(), name='course_list'),
    path('create/', CourseCreateView.as_view(), name='create_course'),
    path('<int:course_id>/enroll/', enroll_course, name='enroll_course'),
    path('<int:course_id>/unenroll/', unenroll_course, name='unenroll_course'),
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='delete_course'),
    path('<int:pk>/update/', CourseUpdateView.as_view(), name='update_course'),
    path('<int:pk>/courses', CourseDetailView.as_view(), name='course_detail'),
    path('<int:pk>/comments/', comment_course, name='comment_course'),
]
