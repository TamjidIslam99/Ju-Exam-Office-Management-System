# Authentication/views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.views import View
from .forms import (
    ExamOfficeRegistrationForm,
    DepartmentRegistrationForm,
    TeacherRegistrationForm,
    StudentRegistrationForm,
)
from Exam_Office.models import User, Department, Teacher, Student, ExamOfficeOrAdmin
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    """View for the homepage."""
    template_name = 'authentication/home.html'


class RegisterExamOfficeView(View):
    """View for registering Exam Office or Admin users."""

    def get(self, request):
        form = ExamOfficeRegistrationForm()
        return render(request, 'authentication/register_exam_office.html', {'form': form})

    def post(self, request):
        form = ExamOfficeRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Exam_Office'  # Set the role explicitly
            user.save()
            ExamOfficeOrAdmin.objects.create(
                user=user,
                office_name=form.cleaned_data['office_name'],
                contact_number=form.cleaned_data['contact_number'],
                address=form.cleaned_data['address']
            )
            messages.success(request, 'Exam Office registered successfully.')
            return redirect('login')
        return render(request, 'authentication/register_exam_office.html', {'form': form})


class RegisterDepartmentView(View):
    """View for registering Department users."""

    def get(self, request):
        form = DepartmentRegistrationForm()
        return render(request, 'authentication/register_department.html', {'form': form})

    def post(self, request):
        form = DepartmentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Department'  # Set the role explicitly
            user.save()
            Department.objects.create(
                user=user,
                name=form.cleaned_data['name']
            )
            messages.success(request, 'Department user registered successfully.')
            return redirect('login')
        return render(request, 'authentication/register_department.html', {'form': form})


class RegisterTeacherView(View):
    """View for registering Teacher users."""

    def get(self, request):
        form = TeacherRegistrationForm()
        return render(request, 'authentication/register_teacher.html', {'form': form})

    def post(self, request):
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Teacher'  # Set the role explicitly
            user.save()
            Teacher.objects.create(
                user=user,
                department=form.cleaned_data['department'],
                name=form.cleaned_data['name']
            )
            messages.success(request, 'Teacher registered successfully.')
            return redirect('login')
        return render(request, 'authentication/register_teacher.html', {'form': form})


class RegisterStudentView(View):
    """View for registering Student users."""

    def get(self, request):
        form = StudentRegistrationForm()
        return render(request, 'authentication/register_student.html', {'form': form})

    def post(self, request):
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'Student'  # Set the role explicitly
            user.save()
            Student.objects.create(
                user=user,
                registration_number=form.cleaned_data['registration_number'],
                department=form.cleaned_data['department'],
                session=form.cleaned_data['session'],
                name=form.cleaned_data['name']
            )
            messages.success(request, 'Student registered successfully.')
            return redirect('login')
        return render(request, 'authentication/register_student.html', {'form': form})





