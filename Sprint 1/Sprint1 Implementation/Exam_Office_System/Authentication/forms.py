# Authentication/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from Exam_Office.models import User, Department
from django.contrib.auth import get_user_model

User = get_user_model()

class ExamOfficeRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    office_name = forms.CharField(max_length=100)
    contact_number = forms.CharField(max_length=15)
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'office_name', 'contact_number', 'address', 'password1', 'password2')


class DepartmentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'name', 'password1', 'password2')


class TeacherRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'department', 'name', 'password1', 'password2')


class StudentRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    registration_number = forms.CharField(max_length=100)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    session = forms.CharField(max_length=20)
    name = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ('username', 'email', 'registration_number', 'department', 'session', 'name', 'password1', 'password2')



