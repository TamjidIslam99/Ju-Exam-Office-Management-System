from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from .models import ExamCalendar
from .forms import ExamCalendarForm, ExamForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
class ExamCalendarListView(View):
    """
    View to list all the exam calendars.
    
    This view fetches all the exam calendar records from the database and renders 
    them in the `exam_calendar_list.html` template.
    """
    def get(self, request):
        """
        Handles GET requests to fetch all the exam calendars.
        
        Arguments:
            request (HttpRequest): The HTTP request object.
        
        Returns:
            HttpResponse: Renders the `exam_calendar_list.html` template with all the 
                           exam calendars.
        """
        exam_calendars = ExamCalendar.objects.all()
        return render(request, 'Publish_Exam_Calendar/exam_calendar_list.html', {'exam_calendars': exam_calendars})

class CreateExamCalendarView(View):
    """
    View to create a new exam calendar and associated exams.
    
    This view handles the GET and POST requests to display and process the form to 
    create a new exam calendar, along with the related exams.
    """
    def get(self, request):
        """
        Handles GET requests to display the form for creating a new exam calendar 
        and related exams.
        
        Arguments:
            request (HttpRequest): The HTTP request object.
        
        Returns:
            HttpResponse: Renders the form for creating a new exam calendar.
        """
        form_calendar = ExamCalendarForm()
        form_exam = ExamForm()
        return render(request, 'Publish_Exam_Calendar/create_exam_calendar.html', {'form_calendar': form_calendar, 'form_exam': form_exam})

    def post(self, request):
        """
        Handles POST requests to process the form data and create a new exam calendar 
        and associated exams.
        
        Arguments:
            request (HttpRequest): The HTTP request object containing form data.
        
        Returns:
            HttpResponse: Redirects to the `exam_calendar_list` view if successful, 
                           or re-renders the form with errors if the form is invalid.
        """
        form_calendar = ExamCalendarForm(request.POST)
        form_exam = ExamForm(request.POST)
        
        if form_calendar.is_valid() and form_exam.is_valid():
            # Save ExamCalendar form
            exam_calendar = form_calendar.save(commit=False)
            exam_calendar.save()
            
            # Save Exam form, linking to the created ExamCalendar instance
            exam = form_exam.save(commit=False)
            exam.exam_calendar = exam_calendar  # Linking the Exam to the ExamCalendar
            exam.save()

            return redirect('exam_calendar_list')
        
        return render(request, 'Publish_Exam_Calendar/create_exam_calendar.html', {'form_calendar': form_calendar, 'form_exam': form_exam})

class ExamCalendarDetailView(View):
    """
    View to display the details of a specific exam calendar.
    
    This view fetches the details of a specific exam calendar and renders them 
    in the `exam_calendar_detail.html` template.
    """
    def get(self, request, pk):
        """
        Handles GET requests to display the details of a specific exam calendar.
        
        Arguments:
            request (HttpRequest): The HTTP request object.
            pk (int): The primary key (ID) of the exam calendar to display.
        
        Returns:
            HttpResponse: Renders the `exam_calendar_detail.html` template with the 
                           details of the specified exam calendar.
        """
        exam_calendar = get_object_or_404(ExamCalendar, pk=pk)
        return render(request, 'Publish_Exam_Calendar/exam_calendar_detail.html', {'exam_calendar': exam_calendar})
