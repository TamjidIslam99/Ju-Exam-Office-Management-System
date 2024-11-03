"""
ApplyForMarksheet/views.py

This module contains Django views for handling the marksheet application process by students.
"""

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ExamSelectionForm, PaymentForm
from Exam_Office_System.models import MarksheetApplication, Exam
import uuid


@login_required
def apply_marksheet(request):
    """
    Handles the initial marksheet application by a student.

    This view allows a logged-in student to select an exam for which they want to apply for a marksheet.
    It presents a form to select the exam , validates the input, and stores the
    selected exam in the session before redirecting to the confirmation page.

    :param request: HttpRequest - The incoming HTTP request.
    :return: HttpResponse - The rendered template or a redirect response.
    """
    user = request.user
    if user.role != 'Student':
        messages.error(request, 'Only students can apply for marksheets.')
        return redirect('dashboard')  # Adjust namespace as per your project

    try:
        student = user.student_profile
    except AttributeError:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = ExamSelectionForm(request.POST)
        if form.is_valid():
            # Get selected data
            exam = form.cleaned_data['exam']

            # Store data in session
            request.session['exam_id'] = exam.id

            return redirect('apply_marksheet:confirm_marksheet')
    else:
        form = ExamSelectionForm()

    return render(request, 'marksheet/apply_marksheet.html', {'form': form})


@login_required
def confirm_marksheet(request):
    """
    Handles the confirmation and payment process for a marksheet application.

    This view retrieves the selected exam from the session, displays a payment form,
    verifies the student's eligibility, processes the payment, and creates a MarksheetApplication record
    upon successful payment. It also handles various error scenarios and provides appropriate feedback
    to the user.

    :param request: HttpRequest - The incoming HTTP request.
    :return: HttpResponse - The rendered template or a redirect response.
    """
    user = request.user
    if user.role != 'Student':
        messages.error(request, 'Only students can apply for marksheets.')
        return redirect('dashboard')

    try:
        student = user.student_profile
    except AttributeError:
        messages.error(request, 'Student profile not found.')
        return redirect('dashboard')

    exam_id = request.session.get('exam_id')

    if not exam_id:
        messages.error(request, 'Incomplete registration data.')
        return redirect('apply_marksheet:apply_marksheet')

    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        messages.error(request, 'Selected exam does not exist.')
        return redirect('apply_marksheet:apply_marksheet')

    success_message = None  # Initialize success message

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']

            # Perform eligibility check
            verification_passed, ineligibility_reasons = verify_student_eligibility(student)

            if verification_passed:
                # Handle payment
                payment_success = handle_payment(payment_method)

                if payment_success:
                    # Create MarksheetApplication
                    application = MarksheetApplication.objects.create(
                        student=student,
                        exam=exam,
                        payment_method=payment_method,
                        status='Verified',
                        payment_status='Completed',
                    )

                    # Clear session data
                    request.session.flush()

                    # Set success message
                    success_message = 'Your application has been recorded. You can collect your marksheet after three days from the exam office.'
                else:
                    # Payment failed
                    messages.error(request, 'Payment unsuccessful. Please try again.')
            else:
                # Verification failed
                messages.error(request, f'Registration rejected: {ineligibility_reasons}')
    else:
        form = PaymentForm()

    context = {
        'student': student,
        'exam': exam,
        'form': form,
        'success_message': success_message,  # Pass success message to template
    }

    return render(request, 'marksheet/confirm_marksheet.html', context)


# Helper Functions

def verify_student_eligibility(student):
    """
    Verifies if the student is eligible to apply for a marksheet.

    This function checks various conditions such as hall clearance, library clearance,
    and expulsion status to determine the student's eligibility. It aggregates any
    ineligibility reasons and returns a tuple indicating the verification status
    and the reasons for ineligibility, if any.

    :param student: Student - The student instance to verify.
    :return: tuple(bool, str) - A tuple containing a boolean indicating if the verification
             passed and a string with reasons for ineligibility.
    """
    reasons = []
    # Check Hall Clearance
    if not student.hall_clearance:
        reasons.append("Hall clearance not obtained.")

    # Check Library Clearance
    if not student.library_clearance:
        reasons.append("Library clearance not obtained.")

    # Check Expulsion Status
    if student.expelled:
        reasons.append("Student has been expelled from the university.")

    if reasons:
        return False, " ".join(reasons)
    return True, ""


def handle_payment(payment_method):
    """
    Handles the payment process for the marksheet application.

    This is a mock function simulating payment processing. In a real-world scenario,
    this function should integrate with an actual payment gateway to process the payment.
    For demonstration purposes, it assumes that the payment is always successful.

    :param payment_method: str - The method of payment chosen by the student.
    :return: bool - Returns True if payment is successful, False otherwise.
    """
    # Mock payment processing
    # Replace this with actual payment gateway integration
    # For demonstration, we'll assume payment is always successful
    # To simulate failure, you can randomly return False
    return True
