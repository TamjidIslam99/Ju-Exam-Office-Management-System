from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from Exam_Office_System.models import Attendance, StudentAttendance, TeacherAttendance, Exam, Student, Teacher
from .forms import AttendanceForm

@login_required
def record_attendance(request):
    """
    View for recording attendance for students and teachers in a given exam.

    This view allows an Exam Office user to record attendance for students and teachers
    during an exam. The user must be authorized to access this view (role: 'Exam_Office').

    **POST**:
    The view processes the submitted form data which includes:
        - The selected exam.
        - The attendance date.
        - The list of selected students and teachers.

    It records the attendance for all students and teachers associated with the exam
    and marks them present or absent based on form selection.

    **GET**:
    Displays a form to record attendance.

    :param request: HttpRequest
        The HTTP request object.
    :return: HttpResponse
        A response rendering the attendance form or the success/error message.
    """
    # Check if the user is an Exam Office
    if request.user.role != 'Exam_Office':
        messages.error(request, "You are not authorized to access this page.")
        return redirect('dashboard')  # Redirect non-Exam Office users to dashboard

    # Handle form submission
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            # Get the exam and attendance date from the form
            exam = form.cleaned_data['exam']
            attendance_date = form.cleaned_data['attendance_date']

            # Create the attendance record for the exam
            attendance = Attendance.objects.create(
                exam=exam,
                attendance_date=attendance_date
            )

            # Get the list of all students and teachers linked to the exam
            students = form.cleaned_data['students']
            teachers = form.cleaned_data['teachers']

            # Record student attendance
            all_students = Student.objects.filter(department=exam.department)  # Fetch all students in the exam's department
            all_teachers = Teacher.objects.filter(department=exam.department)  # Fetch all teachers in the exam's department

            for student in all_students:
                # If the student is selected in the form, mark as present, otherwise absent
                is_present = student in students
                StudentAttendance.objects.create(attendance=attendance, student=student, is_present=is_present)

            # Record teacher attendance
            for teacher in all_teachers:
                # If the teacher is selected in the form, mark as present, otherwise absent
                is_present = teacher in teachers
                TeacherAttendance.objects.create(attendance=attendance, teacher=teacher, is_present=is_present)

            # Success message
            messages.success(request, 'Attendance recorded successfully.')
            return redirect('office:dashboard')

        # If form is not valid, show error messages
        else:
            messages.error(request, 'There was an error in the form. Please try again.')

    else:
        form = AttendanceForm()  # Initialize the form for GET request

    return render(request, 'Exam_Office1/record_attendance.html', {'form': form})


@login_required
def attendance_statistics(request, attendance_id):
    """
    View for displaying attendance statistics for a specific exam attendance.

    This view fetches the attendance record for a specific exam and calculates 
    the attendance statistics for students and teachers.

    It provides a count of the number of students and teachers present and absent 
    for the exam.

    :param request: HttpRequest
        The HTTP request object.
    :param attendance_id: int
        The ID of the attendance record.
    :return: HttpResponse
        A response rendering the attendance statistics.
    """
    try:
        # Fetch the attendance record
        attendance = Attendance.objects.get(id=attendance_id)

        # Get attendance data for students and teachers
        student_attendance = StudentAttendance.objects.filter(attendance=attendance)
        teacher_attendance = TeacherAttendance.objects.filter(attendance=attendance)

        # Calculate statistics for students
        student_present = student_attendance.filter(is_present=True).count()
        student_absent = student_attendance.filter(is_present=False).count()

        # Calculate statistics for teachers
        teacher_present = teacher_attendance.filter(is_present=True).count()
        teacher_absent = teacher_attendance.filter(is_present=False).count()

        # Render the statistics in the template
        return render(request, 'Exam_Office1/attendance_statistics.html', {
            'attendance': attendance,
            'student_present': student_present,
            'student_absent': student_absent,
            'teacher_present': teacher_present,
            'teacher_absent': teacher_absent,
        })
    except Attendance.DoesNotExist:
        messages.error(request, 'Attendance record not found.')
        return redirect('office:dashboard')
