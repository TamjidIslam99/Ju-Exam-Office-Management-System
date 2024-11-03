# Register_Exam/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.core.mail import send_mail
from Exam_Office_System.models import Student, ExamRegistration, Exam
from .forms import ExamSelectionForm, PaymentForm
import uuid

class RegisterExamView(LoginRequiredMixin, View):
    """
    Handles the exam registration process for students.

    This view displays a form for students to select exams and proceed
    to the confirmation step if the selection is valid.
    """

    template_name = 'register_exam/register_exam.html'

    def get(self, request):
        """
        Renders the exam selection form for students.

        :param request: HTTP request object
        :return: Rendered HTML response for the exam selection page
        """
        if request.user.role != 'Student':
            messages.error(request, 'Only students can register for exams.')
            return redirect('auth:dashboard')

        try:
            student = request.user.student_profile
        except AttributeError:
            messages.error(request, 'Student profile not found.')
            return redirect('auth:dashboard')

        form = ExamSelectionForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Processes the selected exam from the form and stores data in session.

        :param request: HTTP request object
        :return: Redirects to the exam confirmation view on success,
                 re-renders the selection page on form error.
        """
        if request.user.role != 'Student':
            messages.error(request, 'Only students can register for exams.')
            return redirect('auth:dashboard')

        try:
            student = request.user.student_profile
        except AttributeError:
            messages.error(request, 'Student profile not found.')
            return redirect('auth:dashboard')

        form = ExamSelectionForm(request.POST)
        if form.is_valid():
            exam = form.cleaned_data['exams']
            registration_type = form.cleaned_data['registration_type']

            request.session['exam_id'] = exam.id
            request.session['registration_type'] = registration_type

            return redirect('register_exam:register_exam_confirm')

        return render(request, self.template_name, {'form': form})


class RegisterExamConfirmView(LoginRequiredMixin, View):
    """
    Handles exam registration confirmation, including payment and eligibility.

    This view verifies the student's eligibility and processes payment.
    On success, it generates an admit card and sends a confirmation email.
    """

    template_name = 'register_exam/register_exam_confirm.html'

    def get(self, request):
        """
        Renders the confirmation page with selected exam details.

        :param request: HTTP request object
        :return: Rendered HTML response for the confirmation page
        """
        exam_id = request.session.get('exam_id')
        registration_type = request.session.get('registration_type')

        if not exam_id or not registration_type:
            messages.error(request, 'Incomplete registration data.')
            return redirect('register_exam:register_exam')

        try:
            exam = Exam.objects.get(id=exam_id)
            student = request.user.student_profile
        except Exam.DoesNotExist:
            messages.error(request, 'Selected exam does not exist.')
            return redirect('register_exam:register_exam')
        except AttributeError:
            messages.error(request, 'Student profile not found.')
            return redirect('auth:dashboard')

        form = PaymentForm()

        context = {
            'exam': exam,
            'registration_type': registration_type,
            'student': student,
            'form': form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        """
        Processes the payment and verifies eligibility for exam registration.

        :param request: HTTP request object
        :return: Redirects to success or failure page based on verification and payment status.
        """
        exam_id = request.session.get('exam_id')
        registration_type = request.session.get('registration_type')

        if not exam_id or not registration_type:
            messages.error(request, 'Incomplete registration data.')
            return redirect('register_exam:register_exam')

        try:
            exam = Exam.objects.get(id=exam_id)
            student = request.user.student_profile
        except Exam.DoesNotExist:
            messages.error(request, 'Selected exam does not exist.')
            return redirect('register_exam:register_exam')
        except AttributeError:
            messages.error(request, 'Student profile not found.')
            return redirect('auth:dashboard')

        form = PaymentForm(request.POST)
        if form.is_valid():
            payment_method = form.cleaned_data['payment_method']

            verification_passed, ineligibility_reasons = self.verify_student_eligibility(student)

            if verification_passed:
                payment_success = self.handle_payment(payment_method)

                if payment_success:
                    exam_registration = ExamRegistration.objects.create(
                        student=student,
                        registration_type=registration_type,
                        payment_method=payment_method,
                        status='Verified',
                        payment_status='Completed',
                        admit_card_generated=True,
                        token=uuid.uuid4().hex[:10].upper()
                    )
                    exam_registration.exams.add(exam)
                    exam_registration.save()

                    self.send_confirmation_email(student, exam_registration)

                    request.session.flush()

                    messages.success(request, 'Registration successful! Admit card has been generated and sent to your email.')
                    return redirect(reverse('register_exam:registration_success'))
                else:
                    messages.error(request, 'Payment unsuccessful. Please try again.')
                    return redirect(reverse('register_exam:registration_failure'))
            else:
                messages.error(request, f'Registration rejected: {ineligibility_reasons}')
                return redirect(reverse('register_exam:registration_failure'))

        context = {
            'exam': exam,
            'registration_type': registration_type,
            'student': student,
            'form': form,
        }
        return render(request, self.template_name, context)

    def verify_student_eligibility(self, student):
        """
        Verifies student's eligibility based on clearance and disciplinary status.

        :param student: Student object
        :return: Tuple of (Boolean, String) indicating verification status and reasons for ineligibility
        """
        reasons = []
        if not student.hall_clearance:
            reasons.append("Hall clearance not obtained.")

        if not student.library_clearance:
            reasons.append("Library clearance not obtained.")

        if student.expelled:
            reasons.append("Student has been expelled from the university.")

        if reasons:
            return False, " ".join(reasons)
        return True, ""

    def handle_payment(self, payment_method):
        """
        Mock payment processing function. Replace with actual integration.

        :param payment_method: String indicating the payment method
        :return: Boolean indicating payment success status
        """
        return True

    def send_confirmation_email(self, student, exam_registration):
        """
        Sends a confirmation email to the student after successful registration.

        :param student: Student object
        :param exam_registration: ExamRegistration object
        """
        subject = 'Exam Registration Confirmation'
        message = f'Dear {student.name},\n\nYour registration for the following exam has been successfully completed:\n'
        for exam in exam_registration.exams.all():
            message += f'- {exam.course.course_code} - {exam.course.course_title} on {exam.exam_date}\n'
        message += f'\nYour registration token is: {exam_registration.token}\n\nThank you.'
        recipient_list = [student.user.email]
        send_mail(subject, message, 'noreply@ju.edu', recipient_list, fail_silently=True)


class RegistrationSuccessView(LoginRequiredMixin, View):
    """
    Displays a success page after exam registration is completed.
    """

    template_name = 'register_exam/registration_success.html'

    def get(self, request):
        """
        Renders the success page.

        :param request: HTTP request object
        :return: Rendered HTML response for the success page
        """
        return render(request, self.template_name)


class RegistrationFailureView(LoginRequiredMixin, View):
    """
    Displays a failure page when registration fails due to payment or eligibility issues.
    """

    template_name = 'register_exam/registration_failure.html'

    def get(self, request):
        """
        Renders the failure page with ineligibility reasons.

        :param request: HTTP request object
        :return: Rendered HTML response for the failure page
        """
        ineligibility_reasons = request.session.get('ineligibility_reasons', 'Unknown reasons.')
        context = {
            'reasons': ineligibility_reasons
        }
        return render(request, self.template_name, context)
