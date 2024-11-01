import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Exam_Office_System.models import Student, Exam, Department

User = get_user_model()

@pytest.mark.django_db
class TestRegisterExamView:
    @pytest.fixture
    def create_user(self):
        """Creates a test user with 'Student' role."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='Student'
        )
        return user

    @pytest.fixture
    def create_department(self, create_user):
        """Creates a test department linked to the user."""
        return Department.objects.create(user=create_user, name='Test Department')

    @pytest.fixture
    def create_student(self, create_user, create_department):
        """Creates a test student linked to the user and department."""
        return Student.objects.create(
            user=create_user,
            registration_number='REG123',
            department=create_department,  # Use the created department
            session='2023',
            name='Test Student'
        )

    @pytest.fixture
    def create_exam(self):
        """Creates a test exam."""
        return Exam.objects.create(
            department=None,  # Adjust as necessary for your test
            batch='2023',
            session='2023',
            exam_date='2024-01-01',
            course=None  # Ensure to link this if course is required
        )

    def test_get_exam_selection_form(self, client, create_student):
        """Tests the GET request for exam selection form."""
        client.login(username='testuser', password='testpassword')
        response = client.get(reverse('register_exam:register_exam'))
        assert response.status_code == 200  # Check if the form is displayed
        assert 'form' in response.context  # Ensure the form is in the context

    # Add more tests here as necessary...
