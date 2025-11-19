from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    CommentsViewSet,
    TeachersViewSet,
    CourseRefreshView,
    CourseTokenObtainPairView,
)

router = DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'teacher', TeachersViewSet)
router.register(r'comment', CommentsViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('course-token/', CourseTokenObtainPairView.as_view(), name='course_obtain_token_pair'),
    path('course-token/refresh/', CourseRefreshView.as_view(), name='course_refresh_token'),
]