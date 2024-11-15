# Publish_Exam_Calendar/tests/test_views.py
import django
django.setup()

import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client
from Publish_Exam_Calendar.models import ExamCalendar, Exam

# This is the setup for the test case
@pytest.fixture
def user():
    User = get_user_model()
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def client(user):
    # Log in the user with the test client
    client = Client()
    client.login(username='testuser', password='testpassword')
    return client

@pytest.fixture
def valid_exam_calendar_data_1():
    return {
        'system_type': 'Semester',
        'class_start_date': '2024-01-01',
        'class_end_date': '2024-04-15',
        'exam_start_date': '2024-05-01',
        'exam_end_date': '2024-06-30',
        'remarks': 'Semester 1 Exam'
    }

@pytest.fixture
def valid_exam_data_1():
    return {
        'session': '2023-2024',
        'batch': '101'
    }

@pytest.fixture
def valid_exam_calendar_data_2():
    return {
        'system_type': 'Semester',
        'class_start_date': '2024-08-01',
        'class_end_date': '2024-12-15',
        'exam_start_date': '2025-01-10',
        'exam_end_date': '2025-02-28',
        'remarks': 'Semester 2 Exam'
    }

@pytest.fixture
def valid_exam_data_2():
    return {
        'session': '2024-2025',
        'batch': '102'
    }

@pytest.fixture
def valid_exam_calendar_data_3():
    return {
        'system_type': 'Yearly',
        'class_start_date': '2024-06-01',
        'class_end_date': '2025-05-31',
        'exam_start_date': '2025-06-01',
        'exam_end_date': '2025-06-30',
        'remarks': 'Annual Exam'
    }

@pytest.fixture
def valid_exam_data_3():
    return {
        'session': '2024-2025',
        'batch': '103'
    }

@pytest.fixture
def valid_exam_calendar_data_4():
    return {
        'system_type': 'Yearly',
        'class_start_date': '2024-01-01',
        'class_end_date': '2024-12-31',
        'exam_start_date': '2025-01-01',
        'exam_end_date': '2025-01-31',
        'remarks': 'Yearly Exam'
    }

@pytest.fixture
def valid_exam_data_4():
    return {
        'session': '2024-2025',
        'batch': '104'
    }

@pytest.fixture
def valid_exam_calendar_data_5():
    return {
        'system_type': 'Semester',
        'class_start_date': '2024-02-01',
        'class_end_date': '2024-05-30',
        'exam_start_date': '2024-06-10',
        'exam_end_date': '2024-07-15',
        'remarks': 'Mid Year Exam'
    }

@pytest.fixture
def valid_exam_data_5():
    return {
        'session': '2023-2024',
        'batch': '105'
    }

@pytest.fixture
def valid_exam_calendar_data_6():
    return {
        'system_type': 'Yearly',
        'class_start_date': '2023-08-01',
        'class_end_date': '2024-07-31',
        'exam_start_date': '2024-08-01',
        'exam_end_date': '2024-08-31',
        'remarks': 'Year End Exam'
    }

@pytest.fixture
def valid_exam_data_6():
    return {
        'session': '2023-2024',
        'batch': '106'
    }

@pytest.fixture
def valid_exam_calendar_data_7():
    return {
        'system_type': 'Semester',
        'class_start_date': '2024-03-01',
        'class_end_date': '2024-06-30',
        'exam_start_date': '2024-07-01',
        'exam_end_date': '2024-07-30',
        'remarks': 'Summer Semester Exam'
    }

@pytest.fixture
def valid_exam_data_7():
    return {
        'session': '2024-2025',
        'batch': '107'
    }

@pytest.fixture
def valid_exam_calendar_data_8():
    return {
        'system_type': 'Yearly',
        'class_start_date': '2024-09-01',
        'class_end_date': '2025-08-31',
        'exam_start_date': '2025-09-01',
        'exam_end_date': '2025-09-30',
        'remarks': 'Full Year Exam'
    }

@pytest.fixture
def valid_exam_data_8():
    return {
        'session': '2024-2025',
        'batch': '108'
    }

@pytest.fixture
def valid_exam_calendar_data_9():
    return {
        'system_type': 'Semester',
        'class_start_date': '2024-11-01',
        'class_end_date': '2025-02-28',
        'exam_start_date': '2025-03-01',
        'exam_end_date': '2025-03-31',
        'remarks': 'End of Year Semester Exam'
    }

@pytest.fixture
def valid_exam_data_9():
    return {
        'session': '2024-2025',
        'batch': '109'
    }

@pytest.fixture
def valid_exam_calendar_data_10():
    return {
        'system_type': 'Yearly',
        'class_start_date': '2024-01-01',
        'class_end_date': '2024-12-31',
        'exam_start_date': '2025-01-01',
        'exam_end_date': '2025-01-31',
        'remarks': 'Annual Final Exam'
    }

@pytest.fixture
def valid_exam_data_10():
    return {
        'session': '2024-2025',
        'batch': '110'
    }

# Test case for the valid POST request to create an exam calendar and exam
@pytest.mark.django_db
def test_create_exam_calendar(client, valid_exam_calendar_data_1, valid_exam_data_1):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_1, **valid_exam_data_1}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_2(client, valid_exam_calendar_data_2, valid_exam_data_2):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_2, **valid_exam_data_2}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_3(client, valid_exam_calendar_data_3, valid_exam_data_3):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_3, **valid_exam_data_3}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_4(client, valid_exam_calendar_data_4, valid_exam_data_4):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_4, **valid_exam_data_4}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_5(client, valid_exam_calendar_data_5, valid_exam_data_5):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_5, **valid_exam_data_5}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_6(client, valid_exam_calendar_data_6, valid_exam_data_6):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_6, **valid_exam_data_6}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_7(client, valid_exam_calendar_data_7, valid_exam_data_7):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_7, **valid_exam_data_7}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_8(client, valid_exam_calendar_data_8, valid_exam_data_8):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_8, **valid_exam_data_8}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_9(client, valid_exam_calendar_data_9, valid_exam_data_9):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_9, **valid_exam_data_9}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1

@pytest.mark.django_db
def test_create_exam_calendar_10(client, valid_exam_calendar_data_10, valid_exam_data_10):
    url = reverse('create_exam_calendar')
    data = {**valid_exam_calendar_data_10, **valid_exam_data_10}
    response = client.post(url, data)
    assert response.status_code == 302
    assert response.url == reverse('exam_calendar_list')
    assert ExamCalendar.objects.count() == 1
    assert Exam.objects.count() == 1
