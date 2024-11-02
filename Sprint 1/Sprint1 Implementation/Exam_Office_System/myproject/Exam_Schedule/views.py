from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin  # For handling authentication in class-based views
from .forms import ExamForm  # Ensure ExamForm is properly defined in forms.py

class CreateExamView(LoginRequiredMixin, View):
    """
    View to handle the creation of new exams by a teacher.
    
    Attributes:
        template_name (str): The HTML template used to render the form.
    """
    template_name = 'schedule/create_exam.html'
    login_url = reverse_lazy('login')  # Redirect to 'login' if user is not authenticated

    def get(self, request):
        """
        Handles GET requests to display the exam creation form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the form for creating a new exam.
        """
        form = ExamForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        """
        Handles POST requests to process exam creation form data.

        Args:
            request (HttpRequest): The HTTP request object containing form data.

        Returns:
            HttpResponseRedirect: Redirects to the dashboard upon successful form submission.
            HttpResponse: Renders the form with error messages if form validation fails.
        """
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new exam
            return redirect('dashboard')  # Redirect to the teacher dashboard or other appropriate page
        return render(request, self.template_name, {'form': form})