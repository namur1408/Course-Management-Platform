from django.contrib import admin
from .models import Course, Comment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'start_date', 'end_date', 'creator']
    list_filter = ['start_date', 'end_date']
    filter_horizontal = ('members',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'content', 'created_at')
    list_filter = ('course', 'user', 'created_at')
    search_fields = ('content',)

