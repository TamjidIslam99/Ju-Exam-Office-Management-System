# view_result/tests/test_views.py

import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.auth import get_user_model
from Exam_Office_System.models import Student, Department

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def student_user():
    User = get_user_model()
    return User.objects.create_user(
        username="studentuser",
        email="student@example.com",
        password="testpass123",
        role="Student"
    )

@pytest.fixture
def department(student_user):
    return Department.objects.create(user=student_user, name="Computer Science")

@pytest.fixture
def student(student_user, department):
    return Student.objects.create(
        user=student_user,
        registration_number="12345",
        name="John Doe",
        department=department,
        session="2023"
    )

# view_result/tests/test_views.py

@pytest.mark.django_db
def test_view_result_get_method_for_student(client, student_user, student):
    # Log in as the student user
    client.login(username="studentuser", password="testpass123")

    # Access the view using the namespaced URL pattern
    response = client.get(reverse('view_result:view_result'))

    # Check if the page is accessible and the form is in context
    assert response.status_code == 200
    assert 'form' in response.context