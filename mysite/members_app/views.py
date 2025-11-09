from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm
from ActionLog.models import ActionLog
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            ActionLog.objects.create(
                user=user,
                action_type='registration',
                content_type=ContentType.objects.get_for_model(user),
                object_id=user.id
            )
            return redirect('course_list')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            ActionLog.objects.create(
                user=user,
                action_type='login',
                content_type=ContentType.objects.get_for_model(user),
                object_id=user.id
            )
            return redirect('course_list')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    if request.user.is_authenticated:
        ActionLog.objects.create(
            user=request.user,
            action_type='logout',
            content_type=ContentType.objects.get_for_model(request.user),
            object_id=request.user.id
        )
    logout(request)
    return redirect('login_view')
