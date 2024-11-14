import pytest
from django.contrib.auth.models import User
from .models import Student, AccommodationRequest, DepartmentReview
from django.core.exceptions import ValidationError
import tempfile

@pytest.fixture
def create_user():
    """Fixture to create a user."""
    return User.objects.create_user(username='student', password='password')


@pytest.fixture
def create_student(create_user):
    """Fixture to create a student."""
    return Student.objects.create(
        user=create_user,
        registration_number='12345',
        department='Computer Science',
        session='2024-2025',
        exam_name='Final Exam'
    )


@pytest.fixture
def create_accommodation_request(create_student):
    """Fixture to create an accommodation request."""
    return AccommodationRequest.objects.create(
        student=create_student,
        special_needs='Need scriber',
        medical_documents='path/to/document.pdf'
    )


@pytest.fixture
def create_department_review(create_accommodation_request):
    """Fixture to create a department review."""
    return DepartmentReview.objects.create(
        accommodation_request=create_accommodation_request,
        department_input='Approved for scriber.',
    )


@pytest.mark.django_db
def test_create_student_success(create_user):
    """Test creating a student with valid data."""
    student = Student.objects.create(
        user=create_user,
        registration_number='12345',
        department='Computer Science',
        session='2024-2025',
        exam_name='Final Exam'
    )
    
    # Check that the student object is created successfully
    assert student.user.username == 'student'
    assert student.registration_number == '12345'
    assert student.department == 'Computer Science'
    assert student.session == '2024-2025'
    assert student.exam_name == 'Final Exam'


@pytest.mark.django_db
def test_create_student_duplicate_registration_number(create_user):
    """Test creating a student with a duplicate registration number (failure)."""
    Student.objects.create(
        user=create_user,
        registration_number='12345',
        department='Computer Science',
        session='2024-2025',
        exam_name='Final Exam'
    )
    
    # Try to create a student with the same registration number (should raise error)
    with pytest.raises(ValidationError):
        Student.objects.create(
            user=create_user,
            registration_number='12345',
            department='Maths',
            session='2024-2025',
            exam_name='Final Exam'
        )


@pytest.mark.django_db
def test_create_accommodation_request_success(create_accommodation_request):
    """Test creating an accommodation request with valid data."""
    accommodation_request = create_accommodation_request
    
    # Check that the accommodation request is created successfully
    assert accommodation_request.student.registration_number == '12345'
    assert accommodation_request.special_needs == 'Need scriber'
    assert accommodation_request.medical_documents == 'path/to/document.pdf'
    assert accommodation_request.is_approved is False


@pytest.mark.django_db
def test_create_accommodation_request_without_special_needs(create_student):
    """Test creating an accommodation request without special needs (failure)."""
    with pytest.raises(ValidationError):
        AccommodationRequest.objects.create(
            student=create_student,
            special_needs='',
            medical_documents='path/to/document.pdf'
        )


@pytest.mark.django_db
def test_create_accommodation_request_without_medical_documents(create_student):
    """Test creating an accommodation request without medical documents (failure)."""
    with pytest.raises(ValidationError):
        AccommodationRequest.objects.create(
            student=create_student,
            special_needs='Need scriber',
            medical_documents=''
        )


@pytest.mark.django_db
def test_create_department_review_success(create_department_review):
    """Test creating a department review for an accommodation request."""
    department_review = create_department_review
    
    # Check that the department review is created successfully
    assert department_review.accommodation_request.special_needs == 'Need scriber'
    assert department_review.department_input == 'Approved for scriber.'


@pytest.mark.django_db
def test_create_department_review_without_input(create_accommodation_request):
    """Test creating a department review without input (failure)."""
    with pytest.raises(ValidationError):
        DepartmentReview.objects.create(
            accommodation_request=create_accommodation_request,
            department_input='',
        )


@pytest.mark.django_db
def test_accommodation_request_str_method(create_accommodation_request):
    """Test the string representation of an accommodation request."""
    accommodation_request = create_accommodation_request
    
    # Check the string representation of the accommodation request
    assert str(accommodation_request) == 'Request by student - Need scriber - Pending'


@pytest.mark.django_db
def test_department_review_str_method(create_department_review):
    """Test the string representation of a department review."""
    department_review = create_department_review
    
    # Check the string representation of the department review
    assert str(department_review) == f'Review for student - {department_review.reviewed_at}'


@pytest.mark.django_db
def test_create_accommodation_request_invalid_document(create_student):
    """Test creating an accommodation request with an invalid file (failure)."""
    # Create a temporary invalid file (e.g., not a PDF)
    invalid_file = tempfile.NamedTemporaryFile(delete=False)
    invalid_file.write(b'Not a valid PDF document.')
    invalid_file.close()
    
    # Try to create an accommodation request with an invalid document (should fail)
    with pytest.raises(ValidationError):
        AccommodationRequest.objects.create(
            student=create_student,
            special_needs='Need scriber',
            medical_documents=invalid_file.name
        )
