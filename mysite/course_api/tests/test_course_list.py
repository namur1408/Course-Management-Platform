import pytest
from django.urls import reverse
from course_api.tests.factories import UserFactory, SuperUserFactory, CourseFactory
from courses_app.models import Course
from django.test import RequestFactory
from rest_framework import status

pytestmark = pytest.mark.django_db

class TestCourseList:
    def test_course_list(self, client):
        user = UserFactory.create()
        user_courses = CourseFactory.create_batch(3, creator=user)
        other_courses = CourseFactory.create_batch(2)
        client.force_login(user)

        response = client.get(reverse('course_list'))

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

