from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required, permission_required
from members_app.models import Member
from django.core.exceptions import ObjectDoesNotExist

@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.creator = request.user
            course.save()
            form.save_m2m()
            return redirect('course_list')
    else:
        form = CourseForm()
    return render(request, 'courses/create_course.html', {'form': form})

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.members.add(request.user)
    return redirect('course_list')

@login_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.creator != request.user and not request.user.has_perm('courses_app.can_delete_courses'):
        return redirect('course_list')
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'courses/course_confirm_delete.html', {'course': course})

