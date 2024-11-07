# Remunerate_Teachers/tests/test_views.py

import pytest
from django.urls import reverse
from django.test import Client
from django.contrib.messages import get_messages
from django.contrib.auth import get_user_model
from Exam_Office_System.models import (
    User,
    Department,
    Teacher,
    Course,
    Exam,
    TeacherRemuneration,
)
from Remunerate_Teachers.forms import RemunerationCreationForm, RemunerationUpdateForm

# Fixtures

@pytest.fixture
def client():
    """
    Provides a Django test client for making HTTP requests in tests.
    """
    return Client()

@pytest.fixture
def exam_office_user(db):
    """
    Creates a user with the role 'Exam_Office'.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="examofficeuser",
        email="examoffice@example.com",
        password="testpass123",
        role="Exam_Office"
    )

@pytest.fixture
def department_user(db):
    """
    Creates a user with the role 'Department'.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="departmentuser",
        email="department@example.com",
        password="testpass123",
        role="Department"
    )

@pytest.fixture
def teacher_user(db):
    """
    Creates a user with the role 'Teacher'.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="teacheruser",
        email="teacher@example.com",
        password="testpass123",
        role="Teacher"
    )

@pytest.fixture
def student_user(db):
    """
    Creates a user with the role 'Student'.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="studentuser",
        email="student@example.com",
        password="testpass123",
        role="Student"
    )

@pytest.fixture
def department(db, department_user):
    """
    Creates a Department associated with the department user.
    """
    return Department.objects.create(
        user=department_user,
        name="Computer Science"
    )

@pytest.fixture
def teacher(db, teacher_user, department):
    """
    Creates a Teacher associated with the teacher user and department.
    """
    return Teacher.objects.create(
        user=teacher_user,
        name="Jane Doe",
        department=department
    )

@pytest.fixture
def course(db, department):
    """
    Creates a Course associated with the department.
    """
    return Course.objects.create(
        department=department,
        course_code="CS101",
        course_title="Introduction to Computer Science"
    )

@pytest.fixture
def exam(db, department, teacher, course):
    """
    Creates an Exam associated with the department, teacher, and course.
    """
    return Exam.objects.create(
        department=department,
        batch="2021",
        session="2020-2021",
        exam_date="2024-11-01",
        course=course,
        invigilator=teacher,
        examiner1=teacher,
        examiner2=teacher,
        examiner3=teacher,
        question_creator=teacher,
        moderator=teacher,
        translator=teacher
    )

@pytest.fixture
def remuneration(db, teacher, exam):
    """
    Creates a TeacherRemuneration instance.
    """
    return TeacherRemuneration.objects.create(
        teacher=teacher,
        exam=exam,
        role='Invigilator',
        amount=500.00,
        status='Pending'
    )

# Helper Functions

def login_user(client, username, password):
    """
    Logs in a user using the test client.
    """
    return client.login(username=username, password=password)

# Test Cases

@pytest.mark.django_db
def test_exam_office_can_access_remuneration_creation_view(client, exam_office_user):
    """
    Test that an exam office user can access the remuneration creation view.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Access the remuneration creation view
    response = client.get(reverse('remunerate_teachers:create_remunerations'))

    # Check if the page is accessible and contains the form
    assert response.status_code == 200
    assert isinstance(response.context['form'], RemunerationCreationForm)

@pytest.mark.django_db
def test_non_exam_office_cannot_access_remuneration_creation_view(client, teacher_user):
    """
    Test that a non-exam office user cannot access the remuneration creation view.
    """
    # Log in as a teacher user
    assert login_user(client, "teacheruser", "testpass123") is True

    # Attempt to access the remuneration creation view
    response = client.get(reverse('remunerate_teachers:create_remunerations'))

    # Check that access is denied or redirected
    assert response.status_code == 302  # Redirect to dashboard

    # Follow the redirect and check for error message
    response_follow = client.get(response.url)
    messages = list(get_messages(response_follow.wsgi_request))
    assert any("Only exam office users can perform this action." in str(message) for message in messages)

@pytest.mark.django_db
def test_remuneration_created_correctly_with_amount_provided(client, exam_office_user, teacher, exam):
    """
    Test that the remuneration is correctly created for a teacher's role in an exam when amount is provided.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Post data to create remuneration with amount
    data = {
        'teacher': teacher.id,
        'exam': exam.id,
        'role': 'Invigilator',
        'amount': '500.00'
    }

    response = client.post(reverse('remunerate_teachers:create_remunerations'), data)

    # Check that the remuneration was created and user is redirected
    assert response.status_code == 302  # Redirect to remunerations_list
    assert response.url == reverse('remunerate_teachers:remunerations_list')

    # Check that the remuneration exists in the database
    remuneration = TeacherRemuneration.objects.get(teacher=teacher, exam=exam, role='Invigilator')
    assert remuneration.amount == 500.00
    assert remuneration.status == 'Pending'

@pytest.mark.django_db
def test_remuneration_created_correctly_with_amount_auto_calculated(client, exam_office_user, teacher, exam):
    """
    Test that the remuneration amount is automatically calculated based on the role when amount is not provided.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Post data to create remuneration without amount
    data = {
        'teacher': teacher.id,
        'exam': exam.id,
        'role': 'Examiner',
        # 'amount' is omitted
    }

    response = client.post(reverse('remunerate_teachers:create_remunerations'), data)

    # Check that the remuneration was created and user is redirected
    assert response.status_code == 302  # Redirect to remunerations_list
    assert response.url == reverse('remunerate_teachers:remunerations_list')

    # Check that the remuneration exists in the database with auto-calculated amount
    remuneration = TeacherRemuneration.objects.get(teacher=teacher, exam=exam, role='Examiner')
    assert remuneration.amount == 1000.00  # As per ROLE_AMOUNT_MAPPING
    assert remuneration.status == 'Pending'

@pytest.mark.django_db
def test_remunerations_list_view_accessible_to_exam_office(client, exam_office_user, remuneration):
    """
    Test that the remunerations list view is accessible to exam office users and displays remunerations.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Access the remunerations list view
    response = client.get(reverse('remunerate_teachers:remunerations_list'))

    # Check if the page is accessible and contains remunerations
    assert response.status_code == 200
    assert 'remunerations' in response.context
    assert remuneration in response.context['remunerations']

@pytest.mark.django_db
def test_remunerations_list_view_not_accessible_to_non_exam_office(client, teacher_user, remuneration):
    """
    Test that the remunerations list view is not accessible to non-exam office users.
    """
    # Log in as a teacher user
    assert login_user(client, "teacheruser", "testpass123") is True

    # Attempt to access the remunerations list view
    response = client.get(reverse('remunerate_teachers:remunerations_list'))

    # Check that access is denied or redirected
    assert response.status_code == 302  # Redirect to dashboard

    # Follow the redirect and check for error message
    response_follow = client.get(response.url)
    messages = list(get_messages(response_follow.wsgi_request))
    assert any("Only exam office users can perform this action." in str(message) for message in messages)

@pytest.mark.django_db
def test_pending_remunerations_view_accessible_and_filters_correctly(client, exam_office_user, remuneration):
    """
    Test that the pending remunerations view lists only remunerations with status 'Pending'.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Create another remuneration with status 'Paid'
    TeacherRemuneration.objects.create(
        teacher=remuneration.teacher,
        exam=remuneration.exam,
        role='Translator',
        amount=600.00,
        status='Paid'
    )

    # Access the pending remunerations view
    response = client.get(reverse('remunerate_teachers:pending_remunerations'))

    # Check if the page is accessible and contains only pending remunerations
    assert response.status_code == 200
    assert 'remunerations' in response.context
    pending_remunerations = response.context['remunerations']
    assert len(pending_remunerations) == 1
    assert pending_remunerations[0] == remuneration

@pytest.mark.django_db
def test_pending_remunerations_view_not_accessible_to_non_exam_office(client, teacher_user):
    """
    Test that the pending remunerations view is not accessible to non-exam office users.
    """
    # Log in as a teacher user
    assert login_user(client, "teacheruser", "testpass123") is True

    # Attempt to access the pending remunerations view
    response = client.get(reverse('remunerate_teachers:pending_remunerations'))

    # Check that access is denied or redirected
    assert response.status_code == 302  # Redirect to dashboard

    # Follow the redirect and check for error message
    response_follow = client.get(response.url)
    messages = list(get_messages(response_follow.wsgi_request))
    assert any("Only exam office users can perform this action." in str(message) for message in messages)

@pytest.mark.django_db
def test_update_remuneration_status_as_paid(client, exam_office_user, remuneration):
    """
    Test that the exam office can mark a remuneration as 'Paid'.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Post data to update remuneration status
    data = {
        'remuneration_id': remuneration.id,
        'status': 'Paid'
    }

    response = client.post(reverse('remunerate_teachers:update_remuneration_status'), data)

    # Check redirect after update
    assert response.status_code == 302  # Redirect to pending_remunerations
    assert response.url == reverse('remunerate_teachers:pending_remunerations')

    # Refresh the remuneration from the database
    remuneration.refresh_from_db()
    assert remuneration.status == 'Paid'

@pytest.mark.django_db
def test_update_remuneration_status_invalid_data(client, exam_office_user):
    """
    Test that updating remuneration status with invalid data does not change any remuneration.
    """
    # Log in as the exam office user
    assert login_user(client, "examofficeuser", "testpass123") is True

    # Attempt to update with invalid remuneration_id
    data = {
        'remuneration_id': 9999,  # Assuming this ID does not exist
        'status': 'Paid'
    }

    response = client.post(reverse('remunerate_teachers:update_remuneration_status'), data)

    # Check redirect after failed update
    assert response.status_code == 302  # Redirect to pending_remunerations
    assert response.url == reverse('remunerate_teachers:pending_remunerations')

    # Check for error message
    response_follow = client.get(response.url)
    messages = list(get_messages(response_follow.wsgi_request))
    assert any("Invalid data submitted." in str(message) for message in messages)

@pytest.mark.django_db
def test_update_remuneration_status_not_accessible_to_non_exam_office(client, teacher_user, remuneration):
    """
    Test that non-exam office users cannot update remuneration status.
    """
    # Log in as a teacher user
    assert login_user(client, "teacheruser", "testpass123") is True

    # Attempt to update remuneration status
    data = {
        'remuneration_id': remuneration.id,
        'status': 'Paid'
    }

    response = client.post(reverse('remunerate_teachers:update_remuneration_status'), data)

    # Check that access is denied or redirected
    assert response.status_code == 302  # Redirect to dashboard

    # Refresh the remuneration to ensure it was not updated
    remuneration.refresh_from_db()
    assert remuneration.status == 'Pending'

    # Follow the redirect and check for error message
    response_follow = client.get(response.url)
    messages = list(get_messages(response_follow.wsgi_request))
    assert any("Only exam office users can perform this action." in str(message) for message in messages)
