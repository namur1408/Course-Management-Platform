from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, CommentsViewSet, TeachersViewSet

router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'teacher', TeachersViewSet)
router.register(r'comment', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]