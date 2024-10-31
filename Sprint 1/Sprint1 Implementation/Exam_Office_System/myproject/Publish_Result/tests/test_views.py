import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Exam_Office_System.models import Department, Exam, Student, Result
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

@pytest.fixture
def user(db):
    """Create a user for authentication."""
    return User.objects.create_user(username='testuser', password='testpassword')

@pytest.fixture
def department(db):
    """Create a department."""
    return Department.objects.create(name='Computer Science')

@pytest.fixture
def exam(department, db):
    """Create an exam associated with a department."""
    return Exam.objects.create(course_code='CS101', session='2024', department=department)

@pytest.fixture
def student(department, db):
    """Create a student associated with a department."""
    return Student.objects.create(registration_number='REG123', name='John Doe', department=department)

@pytest.fixture
def result(exam, student, db):
    """Create a result for a student in an exam."""
    return Result.objects.create(exam=exam, student=student, marks=85)

@pytest.mark.django_db
def test_select_exam_view_get(user, client, department):
    """Test the GET request of SelectExamView."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:select_exam')
    response = client.get(url)
    assert response.status_code == 200
    assert 'departments' in response.context

@pytest.mark.django_db
def test_select_exam_view_post_valid(user, client, exam, department):
    """Test the POST request of SelectExamView with valid data."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:select_exam')
    response = client.post(url, {
        'department_id': department.id,
        'session': exam.session,
        'course_code': exam.course_code
    })
    assert response.status_code == 302
    assert response.url == reverse('publish_result:upload_results', kwargs={'exam_id': exam.id})

@pytest.mark.django_db
def test_select_exam_view_post_invalid(user, client, department):
    """Test the POST request of SelectExamView with invalid data."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:select_exam')
    response = client.post(url, {
        'department_id': department.id,
        'session': 'Invalid Session',
        'course_code': 'Invalid Course'
    })
    assert response.status_code == 302
    assert 'No exam found for the selected criteria.' in response.wsgi_request._messages

@pytest.mark.django_db
def test_upload_results_view_get(user, client, exam):
    """Test the GET request of UploadResultsView."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:upload_results', kwargs={'exam_id': exam.id})
    response = client.get(url)
    assert response.status_code == 200
    assert 'exam' in response.context

@pytest.mark.django_db
def test_upload_results_view_post_valid(user, client, exam, student):
    """Test the POST request of UploadResultsView with valid XML data."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:upload_results', kwargs={'exam_id': exam.id})

    # Create XML file for upload
    xml_content = """<?xml version="1.0"?>
    <results>
        <result>
            <student>
                <id>REG123</id>
                <name>John Doe</name>
                <score>90</score>
            </student>
        </result>
    </results>"""
    xml_file = SimpleUploadedFile("results.xml", xml_content.encode(), content_type="text/xml")

    response = client.post(url, {'file': xml_file})
    assert response.status_code == 302
    assert Result.objects.filter(exam=exam, student=student, marks=90).exists()
    assert 'Uploaded 1 results successfully.' in response.wsgi_request._messages

@pytest.mark.django_db
def test_upload_results_view_post_invalid_xml(user, client, exam):
    """Test the POST request of UploadResultsView with invalid XML data."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:upload_results', kwargs={'exam_id': exam.id})

    # Create invalid XML file for upload
    invalid_xml_content = """<results><result></result></results>"""
    xml_file = SimpleUploadedFile("results.xml", invalid_xml_content.encode(), content_type="text/xml")

    response = client.post(url, {'file': xml_file})
    assert response.status_code == 302
    assert 'Error parsing XML file.' in response.wsgi_request._messages

@pytest.mark.django_db
def test_semester_yearly_result_view_get(user, client):
    """Test the GET request of SemesterYearlyResultView."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:semester_yearly_result')
    response = client.get(url)
    assert response.status_code == 200
    assert 'departments' in response.context

@pytest.mark.django_db
def test_published_results_view_get(user, client, exam, student):
    """Test the GET request of PublishedResultsView."""
    client.login(username='testuser', password='testpassword')
    url = reverse('publish_result:published_results', kwargs={'department_id': 1, 'session': '2024'})
    response = client.get(url)
    assert response.status_code == 200
    assert 'published_results' in response.context
