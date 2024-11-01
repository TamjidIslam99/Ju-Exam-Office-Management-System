# view_result/views.py

from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from Exam_Office_System.models import Result
from .forms import ResultLookupForm

class ViewResultView(LoginRequiredMixin, View):
    """
    Handles viewing of exam results for students.

    This view allows students to view their exam results by selecting a particular exam registration.
    Only students with the role 'Student' can access this view, and access is restricted through
    `LoginRequiredMixin`.

    Attributes:
        template_name (str): The name of the template used for rendering the result lookup page.
    """
    template_name = 'view_result/view_result.html'

    def get(self, request):
        """
        Handles GET requests to display the result lookup form.

        Checks if the user has the 'Student' role and then displays the form for
        selecting an exam registration. Redirects non-student users to the dashboard with an error message.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered HTML response with the result lookup form for students.
        """
        if request.user.role != 'Student':
            messages.error(request, 'Only students can view results.')
            return redirect('dashboard')  # Replace 'dashboard' with your actual dashboard URL name

        form = ResultLookupForm(student=request.user.student_profile)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handles POST requests for submitting the result lookup form.

        Checks if the user has the 'Student' role and validates the form data.
        After validation, it retrieves the requested result based on the selected exam registration
        and displays it. If the result does not exist, an informational message is shown.

        Args:
            request (HttpRequest): The HTTP request object containing form data.

        Returns:
            HttpResponse: The rendered HTML response with the result if available,
                          otherwise re-renders the form with messages indicating issues.
        """
        if request.user.role != 'Student':
            messages.error(request, 'Only students can view results.')
            return redirect('dashboard')

        form = ResultLookupForm(request.POST, student=request.user.student_profile)
        if form.is_valid():
            exam_registration = form.cleaned_data['exam_registration']
            registration_type = form.cleaned_data['registration_type']

            # Verify that the registration type matches
            if exam_registration.registration_type != registration_type:
                messages.error(request, 'Selected registration type does not match the exam registration.')
                return render(request, self.template_name, {'form': form})

            try:
                result = Result.objects.get(registration=exam_registration)
                context = {
                    'result': result,
                    'exam_registration': exam_registration
                }
                return render(request, 'view_result/result_display.html', context)
            except Result.DoesNotExist:
                messages.info(request, 'Result for the selected exam is not yet available.')
                return render(request, self.template_name, {'form': form})

        return render(request, self.template_name, {'form': form})
