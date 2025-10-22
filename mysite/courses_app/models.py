from django.db import models
from members_app.models import Member
from django.contrib.auth.models import User

class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    start_date = models.DateTimeField(null=True, blank=False)
    end_date = models.DateTimeField(null=True, blank=False)
    members = models.ManyToManyField(Member, related_name='courses')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses', null = True)

    def __str__(self):
        return self.title

