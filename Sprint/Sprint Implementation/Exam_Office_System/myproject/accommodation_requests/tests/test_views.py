import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from .models import AccommodationRequest, DepartmentReview, Student


# Fixtures
@pytest.fixture
def student_user():
    """Create and return a student user."""
    user = User.objects.create_user(username='student', password='password')
    student = Student.objects.create(user=user)
    return user, student


@pytest.fixture
def department_user():
    """Create and return a department user."""
    user = User.objects.create_user(username='department', password='password')
    return user


@pytest.fixture
def accommodation_request(student_user):
    """Create and return an accommodation request."""
    user, student = student_user
    return AccommodationRequest.objects.create(
        student=student,
        request_type='scriber',
        medical_document='path/to/document.pdf',
        status='pending'
    )


# Test cases using fixtures

@pytest.mark.django_db
def test_request_accommodation_success(client, student_user):
    """Test submitting an accommodation request successfully."""
    user, student = student_user
    
    # Log in as the student
    client.login(username='student', password='password')
    
    # Post valid data to the accommodation request form
    response = client.post(reverse('accommodation_requests:request_accommodation'), {
        'request_type': 'scriber',
        'medical_document': 'path/to/document.pdf',
    })
    
    # Check the response status and redirect location
    assert response.status_code == 302  # Redirect to status page
    assert 'accommodation_requests:status' in response.url
    
    # Check that the accommodation request was created
    accommodation_request = AccommodationRequest.objects.last()
    assert accommodation_request.student == student
    assert accommodation_request.status == 'pending'


@pytest.mark.django_db
def test_request_accommodation_missing_document(client, student_user):
    """Test submitting an accommodation request with missing medical document (failure)."""
    user, student = student_user
    
    # Log in as the student
    client.login(username='student', password='password')
    
    # Post invalid data to the accommodation request form (missing document)
    response = client.post(reverse('accommodation_requests:request_accommodation'), {
        'request_type': 'scriber',
        'medical_document': '',
    })
    
    # Check that the form is invalid
    assert response.status_code == 200  # Form page should be re-rendered
    assert 'This field is required.' in response.content.decode()


@pytest.mark.django_db
def test_review_accommodation_success(client, accommodation_request, department_user):
    """Test the department reviewing the accommodation request successfully."""
    # Log in as the department user
    client.login(username='department', password='password')
    
    # Post valid review data
    response = client.post(reverse('accommodation_requests:review_accommodation', kwargs={'pk': accommodation_request.pk}), {
        'feasibility': 'approved',
        'comments': 'Accommodation is feasible.',
    })
    
    # Check that the department review was successfully submitted
    assert response.status_code == 302  # Redirect to status page
    accommodation_request.refresh_from_db()
    assert accommodation_request.is_approved is True


@pytest.mark.django_db
def test_review_accommodation_missing_comments(client, accommodation_request, department_user):
    """Test the department reviewing the accommodation request with missing comments (failure)."""
    # Log in as the department user
    client.login(username='department', password='password')
    
    # Post invalid review data (missing comments)
    response = client.post(reverse('accommodation_requests:review_accommodation', kwargs={'pk': accommodation_request.pk}), {
        'feasibility': 'approved',
        'comments': '',
    })
    
    # Check that the form is invalid
    assert response.status_code == 200  # Form page should be re-rendered
    assert 'This field is required.' in response.content.decode()


@pytest.mark.django_db
def test_accommodation_status_page(client, accommodation_request, student_user):
    """Test viewing the accommodation status page."""
    user, student = student_user
    
    # Log in as the student
    client.login(username='student', password='password')
    
    # Visit the status page
    response = client.get(reverse('accommodation_requests:status', kwargs={'pk': accommodation_request.pk}))
    
    # Check that the status page is rendered
    assert response.status_code == 200
    assert 'Accommodation Request Status' in response.content.decode()


@pytest.mark.django_db
def test_accommodation_status_page_not_found(client):
    """Test accessing a non-existing accommodation status page (failure)."""
    # Log in as a student
    user = User.objects.create_user(username='student', password='password')
    client.login(username='student', password='password')
    
    # Try to visit a non-existent status page
    response = client.get(reverse('accommodation_requests:status', kwargs={'pk': 999}))
    
    # Check that a 404 page is returned
    assert response.status_code == 404


@pytest.mark.django_db
def test_review_accommodation_access_by_non_department_user(client, accommodation_request, student_user):
    """Test that a non-department user cannot access the review page (failure)."""
    user, student = student_user
    
    # Log in as the student (not a department user)
    client.login(username='student', password='password')
    
    # Try to access the review page
    response = client.get(reverse('accommodation_requests:review_accommodation', kwargs={'pk': accommodation_request.pk}))
    
    # Check that the response is a 403 Forbidden error
    assert response.status_code == 403


@pytest.mark.django_db
def test_request_accommodation_logged_out(client):
    """Test that a logged-out user cannot submit an accommodation request (failure)."""
    # Try to access the request accommodation page without logging in
    response = client.get(reverse('accommodation_requests:request_accommodation'))
    
    # Check that the user is redirected to the login page
    assert response.status_code == 302  # Redirect to login
    assert 'login' in response.url


@pytest.mark.django_db
def test_department_review_logged_out(client, accommodation_request):
    """Test that a logged-out department user cannot review an accommodation request (failure)."""
    # Try to access the review page without logging in
    response = client.get(reverse('accommodation_requests:review_accommodation', kwargs={'pk': accommodation_request.pk}))
    
    # Check that the user is redirected to the login page
    assert response.status_code == 302  # Redirect to login
    assert 'login' in response.url
