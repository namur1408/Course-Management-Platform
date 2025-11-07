from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Comment
from .forms import CourseForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
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
    course = get_object_or_404(Course, id=course_id)
    course.members.add(request.user)
    return redirect('course_list')

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.members.remove(request.user)
    return redirect('course_list')

@login_required
def comment_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(course=course, user=request.user, content=content)
    return redirect('course_detail', pk=course.pk)


class CourseDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses_app.can_delete_course'

    def has_permission(self):
        course = self.get_object()
        return (course.creator == self.request.user
                or self.request.user.has_perm('courses_app.can_delete_course')
        )

class CourseUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses_app.can_edit_course'

    def has_permission(self):
        course = self.get_object()
        return (course.creator == self.request.user
                or self.request.user.has_perm('courses_app.can_edit_course')
        )

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(course=self.object).order_by('-created_at')
        return context

class CommentDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Comment
    template_name = 'courses/comment_confirm_delete.html'
    context_object_name = 'comment'
    permission_required = 'courses_app.can_delete_comment'

    def has_permission(self):
        comment = self.get_object()
        return (comment.user == self.request.user
                or self.request.user.has_perm('courses_app.can_delete_comment')
                )
    def get_success_url(self):
        return reverse_lazy('course_detail', kwargs={'pk': self.object.course.pk})
