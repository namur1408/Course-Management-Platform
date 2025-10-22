from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'creator']
    list_filter = ['start_date', 'end_date']
    filter_horizontal = ('members',)

