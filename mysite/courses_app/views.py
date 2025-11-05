from django.shortcuts import render, redirect, get_object_or_404
from .models import Course
from .forms import CourseForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, DeleteView
from members_app.models import Member
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'
    context_object_name = 'courses'
    success_url = reverse_lazy('course_list')
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

@login_required
def enroll_course(request, course_id):
    course = Course.objects.get(id=course_id)
    course.members.add(request.user)
    return redirect('course_list')

class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses_app.can_delete_course'

    def has_permission(self):
        course = self.get_object()
        return (course.creator == self.request.user or self.request.user.has_perm('courses_app.can_delete_course'))
