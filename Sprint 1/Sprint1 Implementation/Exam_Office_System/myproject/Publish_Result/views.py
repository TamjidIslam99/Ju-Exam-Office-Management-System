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
    def get(self, request):
        departments = Department.objects.all()
        return render(request, 'Publish_Result/select_exam.html', {'departments': departments})

    def post(self, request):
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
    def get(self, request, exam_id):
        exam = get_object_or_404(Exam, id=exam_id)
        return render(request, 'Publish_Result/upload_results.html', {'exam': exam})

    def post(self, request, exam_id):
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
    template_name = 'Publish_Result/semester_yearly_result.html'

    def get(self, request):
        departments = Department.objects.all()
        return render(request, self.template_name, {'departments': departments})

    def post(self, request):
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
    def get(self, request, department_id, session):
        published_results = PublishedResult.objects.filter(department_id=department_id, session=session)
        return render(request, 'Publish_Result/published_results.html', {'published_results': published_results})

    def download_csv(self, request, department_id, session):
        published_results = PublishedResult.objects.filter(department_id=department_id, session=session)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="published_results_{department_id}_{session}.csv"'

        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Average Marks', 'Publish Date'])

        for result in published_results:
            writer.writerow([result.student.registration_number, result.average_marks, result.publish_date])

        return response
