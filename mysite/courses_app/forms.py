from django import forms
from django.core.exceptions import ValidationError
from .models import Course
from django.utils import timezone

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter course name', 'class': "form-control"}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter course description', 'class': 'form-control'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    def clean_title(self):
        title = self.cleaned_data['title']
        if Course.objects.filter(title=title).exists():
            raise ValidationError("Course with this title is already taken!")
        return title

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            if start_date > end_date:
                raise ValidationError("Start date must be before end date!")
            if start_date < timezone.now():
                raise ValidationError("Start date cannot be in the past!")

        return cleaned_data