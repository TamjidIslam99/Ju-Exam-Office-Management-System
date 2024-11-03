import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()


# view_result/tests/conftest.py

import pytest
from django.contrib.auth import get_user_model
from Exam_Office_System.models import (
    Department, Student, Teacher, Exam, Course, ExamRegistration, Result
)

User = get_user_model()

@pytest.fixture
def department_user(db):
    user = User.objects.create_user(
        username="departmentuser",
        email="dept@example.com",
        password="testpass123",
        role="Department"
    )
    return user

@pytest.fixture
def department(db, department_user):
    department = Department.objects.create(
        user=department_user,
        name="Computer Science"
    )
    return department

@pytest.fixture
def student_user(db):
    user = User.objects.create_user(
        username="studentuser",
        email="student@example.com",
        password="testpass123",
        role="Student"
    )
    return user

@pytest.fixture
def student_profile(db, student_user, department):
    student_profile = Student.objects.create(
        user=student_user,
        registration_number="202101",
        department=department,
        session="2020-2021",
        name="John Doe"
    )
    return student_profile

@pytest.fixture
def teacher_user(db):
    user = User.objects.create_user(
        username="teacheruser",
        email="teacher@example.com",
        password="testpass123",
        role="Teacher"
    )
    return user

@pytest.fixture
def teacher_profile(db, teacher_user, department):
    teacher_profile = Teacher.objects.create(
        user=teacher_user,
        department=department,
        name="Jane Smith"
    )
    return teacher_profile

@pytest.fixture
def course(db, department):
    course = Course.objects.create(
        department=department,
        course_code="CS101",
        course_title="Introduction to Computer Science"
    )
    return course

@pytest.fixture
def exam(db, department, course, teacher_profile):
    exam = Exam.objects.create(
        department=department,
        batch="2021",
        session="2020-2021",
        exam_date="2024-11-01",
        course=course,
        invigilator=teacher_profile,
        examiner1=teacher_profile,
        examiner2=teacher_profile,
        examiner3=teacher_profile,
        question_creator=teacher_profile,
        moderator=teacher_profile,
        translator=teacher_profile
    )
    return exam

@pytest.fixture
def exam_registration(db, student_profile, exam):
    exam_registration = ExamRegistration.objects.create(
        student=student_profile,
        exam=exam,
        registration_type="Regular",
        status="Verified"
    )
    return exam_registration

@pytest.fixture
def result(db, exam_registration):
    result = Result.objects.create(
        registration=exam_registration,
        marks=85
    )
    return result
