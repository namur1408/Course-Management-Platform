from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

User = get_user_model()

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': "form-control"}),
        label="Password"
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password', 'class': "form-control"}),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 'address', 'password', 'confirm_password', 'preffered_language']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address', 'class': "form-control"}),
            'phone': forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': "form-control"}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name', 'class': "form-control"}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name', 'class': "form-control"}),
            'address': forms.TextInput(attrs={'placeholder': 'Enter your address', 'class': "form-control"}),
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': "form-control"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email', 'class': "form-control"}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password', 'class': "form-control"}),
        label="Password"
    )
