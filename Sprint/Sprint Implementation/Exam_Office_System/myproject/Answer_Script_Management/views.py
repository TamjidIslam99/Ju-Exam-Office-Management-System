from django.shortcuts import render, redirect
from .models import AnswerScript, ScriptEvaluationLog
from Exam_Office_System.models import Exam, Student
from django.contrib.auth.decorators import login_required

@login_required
def manage_answer_scripts(request):
    """
    Manage answer scripts by displaying available exams and handling form submissions.

    This view allows users to assign answer scripts to examiners. If the request method is POST,
    it processes the form submission for assigning scripts.

    :param request: The HTTP request object.
    :return: Rendered template for managing answer scripts.
    """
    if request.method == 'POST':
        # Handle form submission for assigning scripts to examiners
        # Implement logic to assign and save answer scripts
        pass

    exams = Exam.objects.all()
    return render(request, 'manage_answer_scripts.html', {'exams': exams})


@login_required
def view_attendance_and_scripts(request, exam_id):
    """
    View attendance and answer scripts for a specific exam.

    This view retrieves the exam, its associated students, and answer scripts, 
    then renders the attendance and scripts template.

    :param request: The HTTP request object.
    :param exam_id: The ID of the exam to view.
    :return: Rendered template for attendance and scripts.
    """
    exam = Exam.objects.get(id=exam_id)
    students = Student.objects.filter(attendances__exam=exam).distinct()
    answer_scripts = AnswerScript.objects.filter(exam=exam)

    return render(request, 'attendance_and_scripts.html', {
        'exam': exam,
        'students': students,
        'answer_scripts': answer_scripts,
    })


@login_required
def evaluate_script(request, script_id):
    """
    Evaluate a specific answer script.

    This view retrieves the answer script based on its ID. If the request method is POST,
    it processes the marks submission from examiners.

    :param request: The HTTP request object.
    :param script_id: The ID of the answer script to evaluate.
    :return: Rendered template for evaluating the answer script.
    """
    answer_script = AnswerScript.objects.get(id=script_id)
    if request.method == 'POST':
        # Handle marks submission from examiners
        # Implement logic to evaluate the answer script
        pass

    return render(request, 'evaluate_script.html', {'answer_script': answer_script})


@login_required
def finalize_management(request):
    """
    Finalize the management of answer scripts.

    This view checks all answer scripts that have not been evaluated and marks them as evaluated 
    if all evaluations are complete. If the request method is POST, it processes the finalization.

    :param request: The HTTP request object.
    :return: Redirect to manage answer scripts or render the finalize management template.
    """
    if request.method == 'POST':
        # Logic to finalize and archive answer scripts
        answer_scripts = AnswerScript.objects.filter(evaluated=False)
        for script in answer_scripts:
            # Check if all evaluations are complete
            if script.marks_examiner1 is not None and script.marks_examiner2 is not None:
                # Calculate average if needed and mark as evaluated
                script.evaluated = True
                script.save()
        return redirect('manage_answer_scripts')

    return render(request, 'finalize_management.html')