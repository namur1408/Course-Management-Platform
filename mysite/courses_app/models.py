from django.db import models
from members_app.models import Member
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=False)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='courses')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null = True)

    def __str__(self):
        return self.title

    class Meta:
        permissions = [
            ("can_delete_courses", "Can delete any course"),
        ]
