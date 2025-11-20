from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from .models import Member, BillingAdress

admin.site.register(BillingAdress)
admin.site.register(Permission)
admin.site.register(ContentType)
class DateInput(forms.DateInput):
    input_type = 'date'

class BillingAdressInLine(admin.StackedInline):
    model = BillingAdress
    extra = 1
    max_num = 2
    fields = ('city', 'street', 'postal_code')

class MemberChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label='Current password', help_text='Encrypted password')
    new_password1 = forms.CharField(
        label='New password',
        widget=forms.PasswordInput,
        required=False,
        help_text="Left empty if you don't want to change password"
    )
    new_password2 = forms.CharField(
        label='confirm new password',
        widget=forms.PasswordInput,
        required=False
    )
    class Meta:
        model = Member
        fields = '__all__'
        widgets = {
            'date_of_birth': DateInput
        }


@admin.register(Member)
class TaskUserAdmin(UserAdmin):
    inlines = [BillingAdressInLine]
    list_display = ('email', 'phone', 'first_name', 'last_name', 'phone', 'is_active')
    ordering = ['-date_joined',]
    form = MemberChangeForm

    fieldsets = (
        ('Personal Data', {'fields': ('email', 'first_name', 'last_name', 'is_active', 'phone', 'date_of_birth')}),
        ('Password Change', {'fields': ('new_password1', 'new_password2'), 'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'user_permissions'), 'classes': ('collapse',)}),
    )