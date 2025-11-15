from django.shortcuts import redirect, get_object_or_404
from .models import Course, Comment
from .forms import CourseForm
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView, CreateView, DeleteView, UpdateView, DetailView)
from .mixins import (
    FormCreatorAssignMixin,
    LogActionMixin,
    OwnerOrPermissionMixin,
    SuccessUrlMixin,
    UpdateTimestampMixin
)
from members_app.models import Member
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from ActionLog.models import ActionLog


class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/course_list.html'
    context_object_name = 'courses'

class CourseCreateView(
    LoginRequiredMixin,
    FormCreatorAssignMixin,
    LogActionMixin,
    CreateView
):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'
    context_object_name = 'courses'
    success_url = reverse_lazy('course_list')
    action_type = 'create_course'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action(self.object)
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

class CourseDeleteView(
    LoginRequiredMixin,
    OwnerOrPermissionMixin,
    LogActionMixin,
    DeleteView
):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses_app.can_delete_course'
    action_type = 'delete_course'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.log_action(obj)
        return super().delete(request, *args, **kwargs)

class CourseUpdateView(
    LoginRequiredMixin,
    LogActionMixin,
    UpdateTimestampMixin,
    OwnerOrPermissionMixin,
    UpdateView
):
    model = Course
    form_class = CourseForm
    template_name = 'courses/create_course.html'
    context_object_name = 'course'
    success_url = reverse_lazy('course_list')
    permission_required = 'courses_app.can_edit_course'
    action_type = 'update_course'

    def form_valid(self, form):
        response = super().form_valid(form)
        self.log_action(self.object)
        return response

class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    context_object_name = 'course'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(course=self.object).order_by('-created_at')
        return context

class CommentDeleteView(
    LoginRequiredMixin,
    OwnerOrPermissionMixin,
    LogActionMixin,
    SuccessUrlMixin,
    DeleteView
):
    model = Comment
    template_name = 'courses/comment_confirm_delete.html'
    context_object_name = 'comment'
    permission_required = 'courses_app.can_delete_comment'
    action_type = 'delete_comment'
    related_field = 'course'
    owner_field = 'user'

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        self.log_action(obj)
        return super().delete(request, *args, **kwargs)
