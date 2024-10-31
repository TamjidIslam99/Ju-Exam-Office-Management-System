from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Exam_Office_System.models import Exam, Department, Student, Result  # Ensure models are imported
import xml.etree.ElementTree as ET
from django.contrib import messages
from django.db.models import Exists, OuterRef

from django.db.models import Avg, F, Q
from django.shortcuts import redirect
from django.utils import timezone
from .models import PublishedResult

class SelectExamView(LoginRequiredMixin, View):
    def get(self, request):
        departments = Department.objects.all()  # Get all departments
        return render(request, 'Publish_Result/select_exam.html', {'departments': departments})

    def post(self, request):
        department_id = request.POST.get('department_id')
        session = request.POST.get('session')
        course_code = request.POST.get('course_code')

        # Debugging prints
        print(f"Department ID: {department_id}, Session: {session}, Course Code: {course_code}")

        # Find the exam based on provided criteria
        exams = Exam.objects.filter(
            department_id=department_id,
            session=session,
            course__course_code=course_code
        )

        if exams.exists():
            print(f"Found exam ID: {exams.first().id}")  # Debugging
            return redirect('publish_result:upload_results', exam_id=exams.first().id)
        else:
            print("No exam found.")  # Debugging
            messages.error(request, 'No exam found for the selected criteria.')
            return render(request, 'Publish_Result/select_exam.html', {
                'departments': Department.objects.all(),
            })

class UploadResultsView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'Publish_Result/upload_results.html', {'exam': exam})

    def post(self, request, exam_id):
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']

            # Parse the uploaded XML file
            try:
                tree = ET.parse(uploaded_file)
                root = tree.getroot()

                results = []
                for result in root.findall('result'):
                    student_registration_number = result.find('student/id').text
                    student_name = result.find('student/name').text
                    course_code = result.find('student/course_code').text
                    score = result.find('student/score').text

                    # Example of validation
                    if not student_registration_number or not student_name or not score:
                        messages.error(request, f"Invalid data for student: {student_name}")
                        continue  # Skip invalid entries

                    # Attempt to find the student by registration number
                    try:
                        student = Student.objects.get(registration_number=student_registration_number)
                    except Student.DoesNotExist:
                        messages.error(request, f"Student with registration number {student_registration_number} does not exist.")
                        continue

                    # Ensure score is a valid integer
                    try:
                        score = int(score)
                    except ValueError:
                        messages.error(request, f"Invalid score for student: {student_name}")
                        continue  # Skip invalid scores

                    # Assuming you have a model to save these results
                    exam_result = Result(
                        exam_id=exam_id,
                        student=student,
                        marks=score
                    )
                    exam_result.save()
                    results.append(exam_result)

                # Provide success feedback
                messages.success(request, f"Uploaded {len(results)} results successfully.")
                
            except ET.ParseError:
                messages.error(request, "Error parsing XML file. Please check the file format.")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")

        else:
            messages.error(request, "No file uploaded.")

        return redirect('publish_result:select_exam')  # Redirect to select exam or a success page


class SemesterYearlyResultView(LoginRequiredMixin, View):
    template_name = 'Publish_Result/semester_yearly_result.html'

    def get(self, request):
        departments = Department.objects.all()
        return render(request, self.template_name, {'departments': departments})

    def post(self, request):
        department_id = request.POST.get('department_id')
        session = request.POST.get('session')
        selected_department = Department.objects.get(id=department_id)
        
        exams = Exam.objects.filter(department_id=department_id, session=session).select_related('course')
        
        # Fetch results status for each exam
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

        # If "Publish Result" button was clicked and all results are uploaded
        if request.POST.get('publish_results') and all_results_uploaded:
            students = Student.objects.filter(department=selected_department, session=session)

            for student in students:
                # Calculate the average marks for the student
                average_marks = Result.objects.filter(
                    student=student,
                    exam__in=exams
                ).aggregate(average_marks=Avg('marks'))['average_marks']

                # Save the published result
                PublishedResult.objects.update_or_create(
                    department=selected_department,
                    session=session,
                    student=student,
                    defaults={'average_marks': average_marks, 'publish_date': timezone.now()}
                )

            # Redirect after publishing results
            return redirect('publish_result_success')  # Define a success URL

        return render(request, self.template_name, context)