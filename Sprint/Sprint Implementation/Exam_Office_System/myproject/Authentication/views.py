from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import (
    UserForm, ExamOfficeRegisterForm, StudentRegisterForm, TeacherRegisterForm,
    DepartmentRegisterForm, ExamOfficeUserRegisterForm, StudentUserRegisterForm,
    TeacherUserRegisterForm, DepartmentUserRegisterForm, CustomAuthenticationForm
)
from Exam_Office_System.models import (
    User, Department, Student, Teacher, ExamOfficeOrAdmin, Course, Exam,
    ExamSchedule, ExamRegistration, Result, MarksheetApplication,
    CertificateApplication, TeacherRemuneration, ExamMaterials, Attendance
)
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import uuid

# Registration Views

class ExamOfficeRegisterView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = ExamOfficeRegisterForm()
        return render(request, 'Exam_Office/register_exam_office.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = ExamOfficeRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'Exam_Office'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Exam Office registered successfully!')
            return redirect('login')
        return render(request, 'Exam_Office/register_exam_office.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

class StudentRegisterView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = StudentRegisterForm()
        return render(request, 'Exam_Office/register_student.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = StudentRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'Student'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Student registered successfully!')
            return redirect('login')
        return render(request, 'Exam_Office/register_student.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

class TeacherRegisterView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = TeacherRegisterForm()
        return render(request, 'Exam_Office/register_teacher.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = TeacherRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'Teacher'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Teacher registered successfully!')
            return redirect('login')
        return render(request, 'Exam_Office/register_teacher.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

class DepartmentRegisterView(View):
    def get(self, request):
        user_form = UserForm()
        profile_form = DepartmentRegisterForm()
        return render(request, 'Exam_Office/register_department.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })
    
    def post(self, request):
        user_form = UserForm(request.POST)
        profile_form = DepartmentRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.role = 'Department'
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'Department registered successfully!')
            return redirect('login')
        return render(request, 'Exam_Office/register_department.html', {
            'user_form': user_form,
            'profile_form': profile_form
        })

# Login View
class CustomLoginView(View):
    def get(self, request):
        form = CustomAuthenticationForm()
        return render(request, 'Exam_Office/login.html', {'form': form})
    
    def post(self, request):
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'Exam_Office/login.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Dashboard View
@login_required
def dashboard(request):
    user = request.user
    if user.role == 'Exam_Office':
        return render(request, 'Exam_Office/exam_office_dashboard.html')
    elif user.role == 'Student':
        return render(request, 'Exam_Office/student_dashboard.html')
    elif user.role == 'Teacher':
        return render(request, 'Exam_Office/teacher_dashboard.html')
    elif user.role == 'Department':
        return render(request, 'Exam_Office/department_dashboard.html')
    else:
        return render(request, 'Exam_Office/dashboard.html')
