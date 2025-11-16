from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from .models import ActionLog
from courses_app.models import Course, Comment

def clear_logs_for_instance(instance):
    content_type = ContentType.objects.get_for_model(instance.__class__)
    ActionLog.objects.filter(
        content_type=content_type,
        object_id=instance.id
    ).update(content_type=None, object_id=None)

@receiver(pre_delete, sender=Course)
def course_pre_delete(sender, instance, **kwargs):
    clear_logs_for_instance(instance)

@receiver(pre_delete, sender=Comment)
def comment_pre_delete(sender, instance, **kwargs):
    clear_logs_for_instance(instance)
