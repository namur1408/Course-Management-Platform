from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.conf import settings
from django.utils import timezone

class ActionLog(models.Model):
    ACTION_CHOICES = [
        ('create_course', 'Creation course'),
        ('update_course', 'Updation of the course'),
        ('delete_course', 'Deleting course'),
        ('admin_delete_course', "Banning someone's course as an admin"),
        ('login', 'Login'),
        ('logout', 'Logout'),
        ('comment', 'Comment'),
        ('enroll', 'Course Enrollment'),
        ('unenroll', 'Course Unenrollment'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='action_logs'
    )
    action_type = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    content_type = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        obj_str = str(self.content_object) if self.content_object else "deleted object"
        return f"{self.user.email} - {self.get_action_type_display()} - {obj_str} - {self.timestamp:%Y-%m-%d %H:%M}"