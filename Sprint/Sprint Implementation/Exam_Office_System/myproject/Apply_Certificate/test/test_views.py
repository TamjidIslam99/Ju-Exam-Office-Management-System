import pytest
from django.urls import reverse
from Exam_Office_System.models import CertificateApplication, Student, Department
from django.contrib.auth import get_user_model

@pytest.fixture
def create_department_user(db):
    """
    Fixture to create a user for the department.
    """
    User = get_user_model()
    return User.objects.create_user(username='deptuser', email='deptuser@example.com', password='password', role='Department')

@pytest.fixture
def create_department(db, create_department_user):
    """
    Fixture to create a test department and associate it with the created department user.
    """
    return Department.objects.create(user=create_department_user, name='Computer Science')

@pytest.fixture
def create_student(db, django_user_model, create_department):
    """
    Fixture to create a test student and associate with a department.
    """
    user = django_user_model.objects.create_user(username='testuser', email='testuser@example.com', password='password', role='Student')
    student = Student.objects.create(
        user=user,
        registration_number='2023REG001',
        name='Test Student',
        session='2023-24',
        department=create_department,  # Assign the created department
    )
    return student

@pytest.fixture
def login_client(client, create_student):
    """
    Fixture to log in the client with the test student user.
    """
    client.login(username='testuser', password='password')
    return client

def test_apply_for_certificate_get_request(login_client, create_student):
    """
    Test apply_for_certificate view with a GET request.
    """
    url = reverse('apply_for_certificate')
    response = login_client.get(url)
    
    assert response.status_code == 200
    assert 'form' in response.context
    assert response.context['student'] == create_student
    assert 'apply_certificate/apply_for_certificate.html' in [t.name for t in response.templates]

def test_apply_for_certificate_post_request(login_client, create_student):
    """
    Test apply_for_certificate view with a POST request to create an application.
    """
    url = reverse('apply_for_certificate')
    post_data = {
        'degree': 'Honours',
        'payment_method': 'CreditCard',
    }
    response = login_client.post(url, post_data)
    
    # Check for redirect after successful form submission
    assert response.status_code == 302
    assert response.url == reverse('application_success')

    # Verify that a CertificateApplication was created with the expected data
    application = CertificateApplication.objects.filter(student=create_student, degree='Honours').first()
    assert application is not None
    assert application.status == 'Pending'
    assert application.payment_method == 'CreditCard'
    assert application.token is not None  # Ensures token was generated
