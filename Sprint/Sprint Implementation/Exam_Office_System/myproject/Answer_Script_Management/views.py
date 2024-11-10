# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.models import User
# from .models import AnswerScript, ExaminerAssignment, Discrepancy, EvaluationLog
# from .forms import ExaminerAssignmentForm
# from Exam_Office_System.models import Exam

# # View for selecting an exam to manage
# def select_exam(request):
#     exams = Exam.objects.all()
#     return render(request, 'select_exam.html', {'exams': exams})


# # View for assigning examiners to an answer script
# def assign_examiners(request, script_id):
#     answer_script = get_object_or_404(AnswerScript, id=script_id)
#     if request.method == "POST":
#         first_examiner_id = request.POST.get("first_examiner")
#         second_examiner_id = request.POST.get("second_examiner")
#         third_examiner_id = request.POST.get("third_examiner")
        
#         # Assign examiners
#         examiner_assignment = ExaminerAssignment.objects.create(
#             answer_script=answer_script,
#             first_examiner_id=first_examiner_id,
#             second_examiner_id=second_examiner_id,
#             third_examiner_id=third_examiner_id
#         )
        
#         # Log the assignment action
#         log_message = f"Examiners assigned to {answer_script.student.name} for {answer_script.exam.name}"
#         EvaluationLog.objects.create(examiner=request.user, action=log_message)

#         return redirect('track_evaluation_status')
    
#     # Provide form with available examiners
#     users = User.objects.all()
#     return render(request, 'assign_examiners.html', {'answer_script': answer_script, 'users': users})


# # View for tracking the evaluation status of answer scripts
# def track_evaluation_status(request):
#     assignments = ExaminerAssignment.objects.all()
#     incomplete_assignments = assignments.filter(status='Not Evaluated')
    
#     # Sending reminders for incomplete evaluations (can be handled with celery/task scheduler in real scenario)
#     for assignment in incomplete_assignments:
#         if not assignment.first_examiner_marks or not assignment.second_examiner_marks:
#             # Send reminder logic can go here
#             log_message = f"Reminder: Evaluation for {assignment.answer_script.student.name} is incomplete."
#             EvaluationLog.objects.create(examiner=request.user, action=log_message)
    
#     return render(request, 'track_status.html', {'assignments': assignments})


# # View for flagging discrepancies between examiners' grades
# def flag_discrepancies(request):
#     assignments = ExaminerAssignment.objects.filter(
#         first_examiner_marks__isnull=False, second_examiner_marks__isnull=False
#     )
#     discrepancies = []
    
#     for assignment in assignments:
#         diff = abs(assignment.first_examiner_marks - assignment.second_examiner_marks)
#         if diff > 5.0:  # Threshold for discrepancy
#             discrepancy = Discrepancy.objects.create(
#                 assignment=assignment,
#                 difference=diff
#             )
#             discrepancies.append(discrepancy)
    
#     return render(request, 'flag_discrepancies.html', {'discrepancies': discrepancies})


# # View for reviewing the status of all answer scripts (ensuring all scripts are processed)
# def review_evaluation_status(request):
#     scripts = AnswerScript.objects.filter(status='Not Graded')
#     return render(request, 'review_evaluation_status.html', {'scripts': scripts})


# # View for finalizing evaluation and archiving the graded answer scripts
# def finalize_and_archive(request):
#     completed_scripts = AnswerScript.objects.filter(status='Evaluated')
    
#     # Logic for archiving the completed scripts
#     for script in completed_scripts:
#         # Archive logic can be implemented here (e.g., saving to a specific archive location)
#         script.status = 'Archived'
#         script.save()

#         # Log the action
#         log_message = f"Answer script for {script.student.name} has been archived."
#         EvaluationLog.objects.create(examiner=request.user, action=log_message)

#     return render(request, 'finalize_and_archive.html', {'completed_scripts': completed_scripts})
# Answer_Script_Management/views.py
from django.shortcuts import render, redirect
from django.http import Http404
from .models import AnswerScript, GradingDiscrepancy, FinalizedAnswerScript
from Exam_Office_System.models import Exam, Teacher, Student

# Constants for grading statuses
NOT_GRADED = 'Not Graded'
GRADED = 'Graded'
FINALIZED = 'Finalized'

def assign_answer_script(request, exam_id):
    try:
        exam = Exam.objects.get(id=exam_id)
    except Exam.DoesNotExist:
        raise Http404("Exam not found")

    if request.method == 'POST':
        student_id = request.POST.get('student_id')
        examiner_id = request.POST.get('examiner_id')

        try:
            student = Student.objects.get(id=student_id)
            examiner = Teacher.objects.get(id=examiner_id)
        except (Student.DoesNotExist, Teacher.DoesNotExist):
            raise Http404("Student or Examiner not found")

        answer_script = AnswerScript.objects.create(
            exam=exam,
            student=student,
            examiner=examiner,
            grading_status=NOT_GRADED
        )
        return redirect('assign_answer_script', exam_id=exam_id)

    students = Student.objects.filter(examregistration__exams=exam)
    examiners = Teacher.objects.filter(exam=exam)
    return render(request, 'answer_script_management/assign_answer_script.html', {
        'exam': exam,
        'students': students,
        'examiners': examiners
    })

def grade_answer_script(request, answer_script_id):
    try:
        answer_script = AnswerScript.objects.get(id=answer_script_id)
    except AnswerScript.DoesNotExist:
        raise Http404("Answer script not found")

    if request.method == 'POST':
        marks = request.POST.get('marks')
        remarks = request.POST.get('remarks')

        if marks is not None and not marks.isdigit():
            # Handle invalid marks input (e.g., non-numeric marks)
            return render(request, 'answer_script_management/grade_answer_script.html', {
                'answer_script': answer_script,
                'error': 'Marks must be a valid number'
            })

        # Update grading status and remarks
        answer_script.grading_status = GRADED
        answer_script.remarks = remarks
        answer_script.save()

        # Create a grading discrepancy if marks are not matching (you can add logic here for examiner comparisons)
        GradingDiscrepancy.objects.create(answer_script=answer_script, examiner1_marks=int(marks))

        return redirect('answer_script_detail', answer_script_id=answer_script.id)
    
    return render(request, 'answer_script_management/grade_answer_script.html', {
        'answer_script': answer_script
    })

def finalize_answer_script(request, answer_script_id):
    try:
        answer_script = AnswerScript.objects.get(id=answer_script_id)
    except AnswerScript.DoesNotExist:
        raise Http404("Answer script not found")

    if request.method == 'POST':
        total_marks = request.POST.get('total_marks')

        if total_marks is None or not total_marks.isdigit():
            # Handle invalid total_marks input
            return render(request, 'answer_script_management/finalize_answer_script.html', {
                'answer_script': answer_script,
                'error': 'Total marks must be a valid number'
            })

        FinalizedAnswerScript.objects.create(
            answer_script=answer_script,
            total_marks=int(total_marks),
            status=FINALIZED
        )
        return redirect('answer_script_detail', answer_script_id=answer_script.id)
    
    return render(request, 'answer_script_management/finalize_answer_script.html', {
        'answer_script': answer_script
    })
