import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from Exam_Office_System.models import Exam, Student, MarksheetApplication, Department, Course

User = get_user_model()

# Fixtures

@pytest.fixture
def exam_office_user(db):
    # Create an exam office user who can be associated with the department
    return User.objects.create_user(username="exam_office_user", password="password123", role="Exam_Office", email="office@example.com")

@pytest.fixture
def department(db, exam_office_user):
    # Associate the department with the exam office user
    return Department.objects.create(user=exam_office_user, name="Computer Science")

@pytest.fixture
def course(db, department):
    return Course.objects.create(department=department, course_code="CSE101", course_title="Intro to Computing")

@pytest.fixture
def exam(db, department, course):
    return Exam.objects.create(
        department=department,
        batch="2023",
        session="2023-24",
        exam_date="2023-05-01",
        course=course
    )

@pytest.fixture
def student_user(db, department):
    user = User.objects.create_user(username='Suraiya', password='qwerty123@', role='Student', email='suraiya@example.com')
    student_profile = Student.objects.create(
        user=user,
        registration_number="12345",
        department=department,
        session="2023-24",
        name="Suraiya",
        hall_clearance=True,
        library_clearance=True,
        expelled=False
    )
    return user

@pytest.fixture
def non_student_user(db):
    return User.objects.create_user(username='non_student', password='qwerty123@', role='Teacher', email='non_student@example.com')

# Test Cases

@pytest.mark.django_db
def test_apply_marksheet_view_access(client, student_user):
    """
    Test that a student user can access the apply_marksheet view.
    """
    client.force_login(student_user)
    url = reverse('apply_marksheet:apply_marksheet')
    response = client.get(url)

    # Check that the page loads successfully
    assert response.status_code == 200
    assert 'Select Exam for Marksheet Application' in response.content.decode()

@pytest.mark.django_db
def test_confirm_marksheet_incomplete_data(client, student_user):
    """
    Test confirm_marksheet when session data is incomplete (no exam_id).
    """
    client.force_login(student_user)
    url = reverse('apply_marksheet:confirm_marksheet')

    # Access confirm_marksheet without exam_id in session
    response = client.get(url)

    # Check for error message and redirect back to apply_marksheet
    messages = list(get_messages(response.wsgi_request))
    assert any("Incomplete registration data." in str(message) for message in messages)
    assert response.status_code == 302
    assert response.url == reverse('apply_marksheet:apply_marksheet')


    
def test_confirm_marksheet_ineligible_student(client,student_user,exam):
        # Store exam_id in session
        session = self.client.session
        session['exam_id'] = 1  # Assume an exam with ID 1 exists for simplicity
        session.save()

        response = self.client.post(reverse('apply_marksheet:confirm_marksheet'))

        # Check for the ineligibility messages
        messages = list(response.context['messages'])
        error_messages = [str(message) for message in messages]
        
        # Assertions to check for both Hall and Library clearance messages
        self.assertIn("Hall clearance not obtained.", error_messages)
        self.assertIn("Library clearance not obtained.", error_messages)


# @pytest.mark.django_db
# def test_apply_marksheet_non_student_redirect(client, non_student_user):
#     """
#     Test that a non-student user is redirected when trying to access the apply_marksheet view.
#     """
#     client.force_login(non_student_user)
    
#     url = reverse('apply_marksheet:apply_marksheet')
#     response = client.get(url)
    
#     assert response.status_code == 302
#     assert response.url == reverse('dashboard')


# @pytest.mark.django_db
# def test_apply_marksheet_post_valid_data(client, student_user, exam):
#     """
#     Test that submitting valid data to apply_marksheet view stores the exam ID in session and redirects.
#     """
#     client.force_login(student_user)
    
#     url = reverse('apply_marksheet:apply_marksheet')
#     response = client.post(url, {'exam': exam.id})

#     assert response.status_code == 302
#     assert response.url == reverse('apply_marksheet:confirm_marksheet')
#     assert client.session['exam_id'] == exam.id


# @pytest.mark.django_db
# def test_confirm_marksheet_incomplete_data(client, student_user):
#     """
#     Test that accessing confirm_marksheet view without exam data in session shows an error message.
#     """
#     client.force_login(student_user)
    
#     url = reverse('apply_marksheet:confirm_marksheet')
#     response = client.get(url)
    
#     messages = list(get_messages(response.wsgi_request))
#     assert any("Incomplete registration data" in str(message) for message in messages)


# @pytest.mark.django_db
# def test_confirm_marksheet_view_success(client, student_user, exam, mocker):
#     """
#     Test that confirm_marksheet view creates an application successfully if data is valid.
#     """
#     # Mock eligibility verification and payment processing
#     mocker.patch('ApplyForMarksheet.views.verify_student_eligibility', return_value=(True, ""))
#     mocker.patch('ApplyForMarksheet.views.handle_payment', return_value=True)
    
#     client.force_login(student_user)
#     client.session['exam_id'] = exam.id
#     client.session.save()

#     url = reverse('apply_marksheet:confirm_marksheet')
#     response = client.post(url, {'payment_method': 'CreditCard'})
    
#     # Check if application was created successfully
#     application = MarksheetApplication.objects.filter(student=student_user.student_profile, exam=exam).exists()
#     assert application is True

#     # Check success message
#     messages = list(get_messages(response.wsgi_request))
#     assert any("Your application has been recorded" in str(message) for message in messages)
