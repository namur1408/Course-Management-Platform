from django.contrib import admin
from .models import Teacher


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'specialization')
    list_display_links = ('id', 'user')

    fieldsets = (
        ("Main information", {"fields": ("user", "specialization", "bio")}),
    )

    def get_courses(self, obj):
        return ", ".join(course.title for course in obj.courses.all())
    get_courses.short_description = "Courses"
