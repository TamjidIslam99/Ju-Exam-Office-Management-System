from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Avg
from django.utils import timezone
from .models import PublishedResult
from Exam_Office_System.models import Exam, Department, Student, Result
import xml.etree.ElementTree as ET
import csv

class SelectExamView(LoginRequiredMixin, View):
    """
    View to select an exam based on department and session.

    This view allows users to select an exam by specifying a department, session,
    and course code. If an exam matching the criteria is found, it redirects 
    to the upload results view.

    Attributes:
        None
    """

    def get(self, request):
        """
        Handle GET requests to display the exam selection form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the exam selection template with available departments.
        """
        departments = Department.objects.all()
        return render(request, 'Publish_Result/select_exam.html', {'departments': departments})

    def post(self, request):
        """
        Handle POST requests to process the selected exam.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to the upload results view if an exam is found,
            or displays an error message if no exam matches the criteria.
        """
        department_id = request.POST.get('department_id')
        session = request.POST.get('session')
        course_code = request.POST.get('course_code')
        
        exams = Exam.objects.filter(department_id=department_id, session=session, course__course_code=course_code)
        
        if exams.exists():
            return redirect('publish_result:upload_results', exam_id=exams.first().id)
        else:
            messages.error(request, 'No exam found for the selected criteria.')
            return redirect('publish_result:select_exam')


class UploadResultsView(LoginRequiredMixin, View):
    """
    View to upload exam results in XML format.

    This view handles the uploading of exam results from an XML file,
    validating student data and saving results to the database.

    Attributes:
        None
    """

    def get(self, request, exam_id):
        """
        Handle GET requests to display the upload results form.

        Args:
            request (HttpRequest): The HTTP request object.
            exam_id (int): The ID of the exam to upload results for.

        Returns:
            HttpResponse: Renders the upload results template for the specified exam.
        """
        exam = get_object_or_404(Exam, id=exam_id)
        return render(request, 'Publish_Result/upload_results.html', {'exam': exam})

    def post(self, request, exam_id):
        """
        Handle POST requests to upload exam results from an XML file.

        Args:
            request (HttpRequest): The HTTP request object.
            exam_id (int): The ID of the exam for which results are uploaded.

        Returns:
            HttpResponse: Redirects to the exam selection page, displaying success or error messages.
        """
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            try:
                tree = ET.parse(uploaded_file)
                root = tree.getroot()
                results = []
                
                for result in root.findall('result'):
                    student_registration_number = result.find('student/id').text
                    student_name = result.find('student/name').text
                    score = result.find('student/score').text
                    
                    try:
                        student = Student.objects.get(registration_number=student_registration_number)
                        score = int(score)
                        exam_result = Result(exam_id=exam_id, student=student, marks=score)
                        exam_result.save()
                        results.append(exam_result)
                    except (Student.DoesNotExist, ValueError):
                        messages.error(request, f"Invalid data for student: {student_name}")
                
                messages.success(request, f"Uploaded {len(results)} results successfully.")
            except ET.ParseError:
                messages.error(request, "Error parsing XML file.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "No file uploaded.")
        
        return redirect('publish_result:select_exam')


class SemesterYearlyResultView(LoginRequiredMixin, View):
    """
    View to calculate and publish semester yearly results.

    This view checks if all exam results are uploaded for a specified department
    and session, calculates the average marks for each student, and allows
    publishing the results.

    Attributes:
        template_name (str): The template for rendering the results view.
    """

    template_name = 'Publish_Result/semester_yearly_result.html'

    def get(self, request):
        """
        Handle GET requests to display the results calculation form.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Renders the form to select department and session for result calculation.
        """
        departments = Department.objects.all()
        return render(request, self.template_name, {'departments': departments})

    def post(self, request):
        """
        Handle POST requests to calculate and publish semester yearly results.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: Redirects to published results view if successful, or re-renders the form with context.
        """
        department_id = request.POST.get('department_id')
        session = request.POST.get('session')
        selected_department = get_object_or_404(Department, id=department_id)

        exams = Exam.objects.filter(department=selected_department, session=session).select_related('course')
        exam_results = []
        all_results_uploaded = True

        for exam in exams:
            has_results_uploaded = Result.objects.filter(exam=exam).exists()
            exam_results.append({
                'exam': exam,
                'has_results_uploaded': has_results_uploaded
            })
            if not has_results_uploaded:
                all_results_uploaded = False

        context = {
            'departments': Department.objects.all(),
            'selected_department': selected_department,
            'selected_session': session,
            'exam_results': exam_results,
            'all_results_uploaded': all_results_uploaded
        }

        if request.POST.get('publish_results') and all_results_uploaded:
            students = Student.objects.filter(department=selected_department)

            for student in students:
                average_marks = Result.objects.filter(student=student, exam__in=exams).aggregate(average_marks=Avg('marks'))['average_marks']
                PublishedResult.objects.update_or_create(
                    department=selected_department,
                    session=session,
                    student=student,
                    defaults={'average_marks': average_marks, 'publish_date': timezone.now()}
                )

            return redirect('publish_result:published_results', department_id=selected_department.id, session=session)

        return render(request, self.template_name, context)


class PublishedResultsView(LoginRequiredMixin, View):
    """
    View to display published results for a department and session.

    This view retrieves and displays the published results for the specified
    department and session, allowing users to download the results as a CSV file.

    Attributes:
        None
    """

    def get(self, request, department_id, session):
        """
        Handle GET requests to display the published results.

        Args:
            request (HttpRequest): The HTTP request object.
            department_id (int): The ID of the department for which results are published.
            session (str): The session for which results are published.

        Returns:
            HttpResponse: Renders the published results template.
        """
        published_results = PublishedResult.objects.filter(department_id=department_id, session=session)
        return render(request, 'Publish_Result/published_results.html', {'published_results': published_results})

    def download_csv(self, request, department_id, session):
        """
        Handle requests to download published results as a CSV file.

        Args:
            request (HttpRequest): The HTTP request object.
            department_id (int): The ID of the department for which results are published.
            session (str): The session for which results are published.

        Returns:
            HttpResponse: CSV file containing published results for the specified department and session.
        """
        published_results = PublishedResult.objects.filter(department_id=department_id, session=session)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="published_results_{department_id}_{session}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Average Marks', 'Publish Date'])

        for result in published_results:
            writer.writerow([result.student.registration_number, result.average_marks, result.publish_date])

        return response
