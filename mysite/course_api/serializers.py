from rest_framework import serializers
from courses_app.models import Course, Comment
from teachers_app.models import Teacher
from django.contrib.auth import get_user_model
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'phone']


class TeachersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', 'user', 'bio', 'specialization']


class CourseSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    teacher = TeachersSerializer(read_only=True)
    teacher_id = serializers.PrimaryKeyRelatedField(
        queryset=Teacher.objects.all(), source='teacher',
        write_only=True
    )
    members = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=User.objects.all(),
        required=False
    )
    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'creator', 'teacher', 'teacher_id', 'start_date', 'end_date', 'members']


class CommentsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'course', 'user', 'content', 'created_at']