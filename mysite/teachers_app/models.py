from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)


    def __str__(self):
        return self.user.get_full_name() or self.user.username

