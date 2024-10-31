from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from Exam_Office_System.models import Exam, Department  # Ensure these are imported

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
            return render(request, 'Publish_Result/select_exam.html', {
                'departments': Department.objects.all(),
                'error': 'No exam found for the selected criteria.'
            })

class UploadResultsView(LoginRequiredMixin, View):
    def get(self, request, exam_id):
        exam = Exam.objects.get(id=exam_id)
        return render(request, 'Publish_Result/upload_results.html', {'exam': exam})

    def post(self, request, exam_id):
        if 'file' in request.FILES:
            uploaded_file = request.FILES['file']
            # Process the file (e.g., save it, parse XML/CSV, etc.)
            return redirect('some_success_page')  # Redirect after processing
        else:
            return render(request, 'Publish_Result/upload_results.html', {
                'exam_id': exam_id,
                'error': 'No file uploaded.'
            })
