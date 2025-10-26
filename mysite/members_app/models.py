from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, UserManager
from django.utils import timezone

class TaskUserManager(BaseUserManager):
    def create_user(self, email, phone, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not phone:
            raise ValueError('User must have phone number')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have "is_staff=True"')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have "is_staff=True"')

        return self.create_user(email, phone,password, **extra_fields)

class Member(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True, verbose_name='Username')
    email = models.EmailField(unique=True, verbose_name='email address', null=True)
    phone = models.CharField(max_length=20, unique=True, verbose_name='Phone number')
    first_name = models.CharField(max_length=30, verbose_name='First name', blank=True)
    date_of_birth = models.DateField(null=True, verbose_name='Date of birth', blank=True)
    address = models.CharField(max_length=255, verbose_name='Address')
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name='Active')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    date_joined = models.DateTimeField(default=timezone.now, verbose_name='Date joined')
    preffered_language = models.CharField(max_length=10, verbose_name='Preffered language', choices=[
        ('en', 'English'),
        ('uk', 'Ukrainian'),
    ], default='en')

    objects = TaskUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()