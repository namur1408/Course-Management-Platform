from django.db import models
from members_app.models import Member
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from ActionLog.models import ActionLog
from teachers_app.models import Teacher
User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null = True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=False, blank=False, related_name='courses')

    def __str__(self):
        return self.title

    action_logs = GenericRelation(ActionLog)

    class Meta:
        permissions = [
            ("can_delete_courses", "Can delete any course"),
            ("can_edit_courses", "Can edit any course"),
        ]


class Comment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.course.title}'

    action_logs = GenericRelation(ActionLog)

    class Meta:
        permissions = [
            ("can_delete_comments", "Can delete any comment"),
        ]
