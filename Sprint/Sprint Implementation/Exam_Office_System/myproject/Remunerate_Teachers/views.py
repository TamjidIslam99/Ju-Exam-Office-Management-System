# Remunerate_Teachers/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import RemunerationCreationForm, RemunerationUpdateForm
from Exam_Office_System.models import TeacherRemuneration


class ExamOfficeRequiredMixin(UserPassesTestMixin):
    """
    Mixin to ensure that the user has the 'Exam_Office' role.

    This mixin restricts access to views so that only users with the
    'Exam_Office' role can interact with certain functionalities.

    :ivar str error_message: The error message displayed when permission is denied.
    """
    error_message = 'Only exam office users can perform this action.'

    def test_func(self):
        """
        Check if the current user has the 'Exam_Office' role.

        :return: True if the user has the 'Exam_Office' role, False otherwise.
        :rtype: bool
        """
        return self.request.user.role == 'Exam_Office'

    def handle_no_permission(self):
        """
        Handle the scenario where a user does not have the required permissions.

        This method adds an error message and redirects the user to the dashboard.

        :return: An HTTP redirect response to the 'dashboard' URL.
        :rtype: HttpResponseRedirect
        """
        messages.error(self.request, self.error_message)
        return redirect('dashboard')  # Ensure 'dashboard' URL exists


class CreateRemunerationsView(LoginRequiredMixin, ExamOfficeRequiredMixin, View):
    """
    View to handle the creation of teacher remunerations by exam office users.

    This view allows users with the 'Exam_Office' role to create new remuneration
    entries for teachers based on their roles in exams.

    :ivar str template_name: The path to the template used for rendering the remuneration creation form.
    :ivar dict ROLE_AMOUNT_MAPPING: A mapping of teacher roles to their corresponding remuneration amounts.
    """
    template_name = 'remunerate_teachers/create_remunerations.html'

    ROLE_AMOUNT_MAPPING = {
        'Invigilator': 1000.00,
        'Examiner': 2000.00,
        'QuestionSetter': 1200.00,
        'Moderator': 800.00,
        'Translator': 500.00,
    }

    def get(self, request):
        """
        Handle GET requests to display the remuneration creation form.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: Rendered HTML page with the remuneration creation form.
        :rtype: HttpResponse
        """
        form = RemunerationCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """
        Handle POST requests to create a new remuneration entry.

        This method processes the submitted form data, validates it, and saves a new
        TeacherRemuneration instance. If the amount is not provided, it is automatically
        calculated based on the teacher's role.

        :param request: The HTTP request object containing form data.
        :type request: HttpRequest
        :return: Redirects to the remunerations list view upon successful creation,
                 or re-renders the form with errors if validation fails.
        :rtype: HttpResponseRedirect or HttpResponse
        """
        form = RemunerationCreationForm(request.POST)
        if form.is_valid():
            remuneration = form.save(commit=False)
            # If amount is not provided, calculate based on role
            if not remuneration.amount:
                remuneration.amount = self.ROLE_AMOUNT_MAPPING.get(remuneration.role, 0.00)
            remuneration.save()
            messages.success(request, 'Remuneration created successfully.')
            return redirect('remunerate_teachers:remunerations_list')
        return render(request, self.template_name, {'form': form})


class RemunerationsListView(LoginRequiredMixin, ExamOfficeRequiredMixin, View):
    """
    View to list all remunerations.

    This view displays a comprehensive list of all TeacherRemuneration entries
    within the system, accessible only to users with the 'Exam_Office' role.

    :ivar str template_name: The path to the template used for rendering the remunerations list.
    """
    template_name = 'remunerate_teachers/remunerations_list.html'

    def get(self, request):
        """
        Handle GET requests to display all remunerations.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: Rendered HTML page with a list of all remunerations.
        :rtype: HttpResponse
        """
        remunerations = TeacherRemuneration.objects.all()
        return render(request, self.template_name, {'remunerations': remunerations})


class PendingRemunerationsView(LoginRequiredMixin, ExamOfficeRequiredMixin, View):
    """
    View to list all pending remunerations for exam office users.

    This view displays only those TeacherRemuneration entries that have a status of 'Pending',
    allowing exam office users to review and update their statuses.

    :ivar str template_name: The path to the template used for rendering the pending remunerations list.
    """
    template_name = 'remunerate_teachers/pending_remunerations.html'

    def get(self, request):
        """
        Handle GET requests to display pending remunerations.

        :param request: The HTTP request object.
        :type request: HttpRequest
        :return: Rendered HTML page with a list of pending remunerations.
        :rtype: HttpResponse
        """
        remunerations = TeacherRemuneration.objects.filter(status='Pending')
        return render(request, self.template_name, {'remunerations': remunerations})


class UpdateRemunerationStatusView(LoginRequiredMixin, ExamOfficeRequiredMixin, View):
    """
    View to update the status of a remuneration to 'Paid'.

    This view processes the submitted form data to update the status of a specific
    TeacherRemuneration entry. Only users with the 'Exam_Office' role can perform this action.

    :ivar str template_name: The path to the template used for rendering the remuneration status update form.
    """
    template_name = 'remunerate_teachers/update_remuneration_status.html'

    def post(self, request):
        """
        Handle POST requests to update remuneration status.

        This method validates the submitted form data and updates the status of the specified
        TeacherRemuneration instance. If the data is invalid, it redirects back with an error message.

        :param request: The HTTP request object containing form data.
        :type request: HttpRequest
        :return: Redirects to the pending remunerations view upon successful update,
                 or redirects back with an error message if validation fails.
        :rtype: HttpResponseRedirect
        """
        form = RemunerationUpdateForm(request.POST)
        if form.is_valid():
            remuneration_id = form.cleaned_data['remuneration_id']
            status = form.cleaned_data['status']
            remuneration = get_object_or_404(TeacherRemuneration, id=remuneration_id)
            remuneration.status = status
            remuneration.save()
            messages.success(request, 'Remuneration status updated successfully.')
            return redirect('remunerate_teachers:pending_remunerations')
        messages.error(request, 'Invalid data submitted.')
        return redirect('remunerate_teachers:pending_remunerations')
