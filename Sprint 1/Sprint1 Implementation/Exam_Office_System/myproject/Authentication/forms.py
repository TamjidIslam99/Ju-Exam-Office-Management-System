from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from Exam_Office_System.models import (
    User, Department, Student, Teacher, ExamOfficeOrAdmin, Course, Exam,
    ExamSchedule, ExamRegistration, Result, MarksheetApplication,
    CertificateApplication, TeacherRemuneration, ExamMaterials, Attendance
)
from django.forms import ModelForm

# Base User Registration Form
class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

# Exam Office Registration Form
class ExamOfficeRegisterForm(forms.ModelForm):
    class Meta:
        model = ExamOfficeOrAdmin
        fields = ['office_name', 'contact_number', 'address']

# Student Registration Form
class StudentRegisterForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'registration_number',
            'department',
            'session',
            'name',
        ]

# Teacher Registration Form
class TeacherRegisterForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['department', 'name']

# Department Registration Form
class DepartmentRegisterForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

# Combined Registration Forms

class ExamOfficeUserRegisterForm(forms.Form):
    user = UserForm()
    profile = ExamOfficeRegisterForm()

class StudentUserRegisterForm(forms.Form):
    user = UserForm()
    profile = StudentRegisterForm()

class TeacherUserRegisterForm(forms.Form):
    user = UserForm()
    profile = TeacherRegisterForm()

class DepartmentUserRegisterForm(forms.Form):
    user = UserForm()
    profile = DepartmentRegisterForm()

# Custom Authentication Form (Optional Enhancement)
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password'}), required=True)
