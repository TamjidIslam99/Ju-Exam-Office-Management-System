import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from Exam_Office_System.models import Attendance, StudentAttendance, TeacherAttendance, Exam, Student, Teacher, Department, Course

User = get_user_model()

@pytest.fixture
def exam_office_user(db):
    # Create an exam office user
    return User.objects.create_user(
        username="exam_office_user", password="password123", role="Exam_Office", email="office@example.com"
    )

@pytest.fixture
def department(db, exam_office_user):
    # Create and associate a department with the exam office user
    return Department.objects.create(user=exam_office_user, name="Computer Science")

@pytest.fixture
def course(db, department):
    # Create a course linked to the department
    return Course.objects.create(department=department, course_code="CSE101", course_title="Intro to Computing")

@pytest.fixture
def exam(db, department, course):
    # Create an exam and link it to the department
    exam_instance = Exam.objects.create(
        department=department,
        batch="2023",
        session="2023-24",
        exam_date="2023-05-01"
    )
    # Add the course to the ManyToMany field after the instance is created
    exam_instance.courses.add(course)
    return exam_instance

@pytest.fixture
def student_user(db, department):
    # Create a student user and student profile
    user = User.objects.create_user(
        username='Suraiya', password='qwerty123@', role='Student', email='suraiya@example.com'
    )
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
    return student_profile  # Return the Student profile

@pytest.fixture
def teacher_user(db, department):
    # Create a teacher user and teacher profile
    user = User.objects.create_user(
        username='Mr_Smith', password='password123', role='Teacher', email='smith@example.com'
    )
    teacher_profile = Teacher.objects.create(
        user=user,
        department=department,
        name="Mr. Smith"
    )
    return teacher_profile  # Return the Teacher profile


@pytest.fixture
def login_exam_office_user(client, exam_office_user):
    client.login(username='exam_office', password='password')
    return client


@pytest.fixture
def login_student_user(client, student_user):
    client.login(username='student', password='password')
    return client


@pytest.mark.django_db
def test_record_attendance(client, exam, student_user, teacher_user, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Prepare POST data to record attendance
    post_data = {
        'exam': exam.id,  # Ensure field name matches form
        'attendance_date': '2023-05-01',
        'students': [student_user.id],  # Corrected to access student profile ID
        'teachers': [teacher_user.id],  # Corrected to access teacher profile ID
    }

    # Send POST request to record attendance
    response = client.post(reverse('exam:record_attendance'), post_data)

    # Check that the attendance was recorded successfully and redirected
    assert response.status_code == 302  # Check for redirect
    assert Attendance.objects.count() == 1
    assert StudentAttendance.objects.count() == 1
    assert TeacherAttendance.objects.count() == 1

    # Check the attendance record
    attendance = Attendance.objects.first()
    assert attendance.exam == exam
    assert str(attendance.attendance_date) == '2023-05-01'
    assert StudentAttendance.objects.first().student == student_user
    assert TeacherAttendance.objects.first().teacher == teacher_user

# Test case for attendance_statistics view
@pytest.mark.django_db
def test_attendance_statistics(client, exam, student_user, teacher_user, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Create attendance record
    attendance = Attendance.objects.create(
        exam=exam,
        attendance_date='2023-05-01'
    )

    # Create student and teacher attendance records
    StudentAttendance.objects.create(attendance=attendance, student=student_user, is_present=True)
    TeacherAttendance.objects.create(attendance=attendance, teacher=teacher_user, is_present=True)

    # Send GET request to attendance statistics page
    response = client.get(reverse('exam:attendance_statistics', args=[attendance.id]))

    # Check if the statistics are displayed correctly
    assert response.status_code == 200
    assert 'Attendance Statistics' in response.content.decode()  # Check for page content


@pytest.mark.django_db
def test_multiple_students_teachers_attendance(client, exam, student_user, teacher_user, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Prepare POST data with multiple students and teachers
    student_user2 = Student.objects.create(
        user=User.objects.create_user(username="Ravi", password="password123", role="Student", email="ravi@example.com"),
        registration_number="12346",
        department=exam.department,
        session="2023-24",
        name="Ravi",
        hall_clearance=True,
        library_clearance=True,
        expelled=False
    )
    teacher_user2 = Teacher.objects.create(
        user=User.objects.create_user(username="Mr_Jones", password="password123", role="Teacher", email="jones@example.com"),
        department=exam.department,
        name="Mr. Jones"
    )

    post_data = {
        'exam': exam.id,
        'attendance_date': '2023-05-01',
        'students': [student_user.id, student_user2.id],
        'teachers': [teacher_user.id, teacher_user2.id],
    }

    # Send POST request to record attendance
    response = client.post(reverse('exam:record_attendance'), post_data)

    # Check that the attendance was recorded successfully
    assert response.status_code == 302
    assert Attendance.objects.count() == 1
    assert StudentAttendance.objects.count() == 2
    assert TeacherAttendance.objects.count() == 2

    # Check the attendance records
    attendance = Attendance.objects.first()
    assert str(attendance.attendance_date) == '2023-05-01'
    assert StudentAttendance.objects.count() == 2
    assert TeacherAttendance.objects.count() == 2



@pytest.mark.django_db
def test_attendance_for_absent_students_teachers(client, exam, student_user, teacher_user, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Create attendance record
    attendance = Attendance.objects.create(
        exam=exam,
        attendance_date='2023-05-01'
    )

    # Create student and teacher attendance records with absence marked
    StudentAttendance.objects.create(attendance=attendance, student=student_user, is_present=False)
    TeacherAttendance.objects.create(attendance=attendance, teacher=teacher_user, is_present=False)

    # Send GET request to attendance statistics page
    response = client.get(reverse('exam:attendance_statistics', args=[attendance.id]))

    # Check if the statistics are displayed correctly
    assert response.status_code == 200
    assert 'Present: 0 students' in response.content.decode()
    assert 'Absent: 1 students' in response.content.decode()
    assert 'Present: 0 teachers' in response.content.decode()
    assert 'Absent: 1 teachers' in response.content.decode()



@pytest.mark.django_db
def test_no_attendance_data(client, exam, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Send GET request to attendance statistics page with no attendance records
    response = client.get(reverse('exam:attendance_statistics', args=[exam.id]))

    # Check that the page returns with no attendance data
    assert response.status_code == 302

@pytest.mark.django_db
def test_non_existing_attendance_id(client, exam, exam_office_user):
    # Login as Exam Officer
    client.login(username='exam_office_user', password='password123')

    # Send GET request to attendance statistics page with a non-existing attendance ID
    response = client.get(reverse('exam:attendance_statistics', args=[999999]))  # Non-existing ID

    # Check if the appropriate error message is shown
    assert response.status_code == 302  # Redirect due to error


def test_record_attendance_unauthorized_user(client, login_student_user):
    """
    Test that a non-Exam Office user is redirected to the dashboard.
    """
    response = client.get(reverse('exam:record_attendance'))
    assert response.status_code == 302  # Should be redirected




def test_record_attendance_url(client):
    """
    Test that the 'attendance/record/' URL resolves to the correct view.
    """
    url = reverse('exam:record_attendance')
    response = client.get(url)  # Use 'client' directly here
    assert response.status_code == 302  # Ensure the page redirect 


def test_attendance_statistics_url(client):
    """
    Test that the 'attendance/statistics/<attendance_id>/' URL resolves to the correct view.
    """
    url = reverse('exam:attendance_statistics', kwargs={'attendance_id': 1})
    response = client.get(url)  # Use 'client' directly here
    assert response.status_code == 302  # Ensure the page redirect 