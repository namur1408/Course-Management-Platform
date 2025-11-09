from django.shortcuts import render, redirect, get_object_or_404
from .models import Course, Comment
from .forms import CourseForm
from django.contrib.auth.decorators import login_required, permission_required
from django.views.generic import ListView, CreateView, DeleteView, UpdateView, DetailView
from members_app.models import Member
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from ActionLog.models import ActionLog


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

    def form_valid(self, form):
        form.instance.creator = self.request.user
        response = super().form_valid(form)
        ActionLog.objects.create(
            user=self.request.user,
            action_type='create_course',
            content_type=ContentType.objects.get_for_model(self.object),
            object_id=self.object.id,
        )
        return response

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.members.add(request.user)
    ActionLog.objects.create(
        user=request.user,
        action_type='enroll',
        content_type=ContentType.objects.get_for_model(course),
        object_id=course.id,
    )
    return redirect('course_list')

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    course.members.remove(request.user)
    ActionLog.objects.create(
        user=request.user,
        action_type='unenroll',
        content_type=ContentType.objects.get_for_model(course),
        object_id=course.id,
    )
    return redirect('course_list')

@login_required
def comment_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(course=course, user=request.user, content=content)
            ActionLog.objects.create(
                user=request.user,
                action_type='comment',
                content_type=ContentType.objects.get_for_model(comment),
                object_id=comment.id,
            )
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
                or self.request.user.has_perm('courses_app.can_delete_courses')
        )

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action_type='delete_course',
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        )
        return super().delete(request, *args, **kwargs)


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

    def form_valid(self, form):
        response = super().form_valid(form)
        ActionLog.objects.create(
            user=self.request.user,
            action_type='update_course',
            content_type=ContentType.objects.get_for_model(self.object),
            object_id=self.object.id,
        )
        return response

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

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        ActionLog.objects.create(
            user=request.user,
            action_type='delete_comment',
            content_type=ContentType.objects.get_for_model(obj),
            object_id=obj.id,
        )
        return super().delete(request, *args, **kwargs)

