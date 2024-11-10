# answer_script_management/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import AnswerScript, GradingAssignment, Discrepancy
from Exam_Office_System.models import Exam, Teacher

def select_exam(request):
    exams = Exam.objects.all()
    return render(request, 'answer_script_management/select_exam.html', {'exams': exams})

def list_answer_scripts(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    answer_scripts = exam.answer_scripts.all()
    return render(request, 'answer_script_management/list_answer_scripts.html', {
        'exam': exam,
        'answer_scripts': answer_scripts,
    })

def assign_examiner(request, script_id):
    answer_script = get_object_or_404(AnswerScript, id=script_id)
    teachers = Teacher.objects.all()
    if request.method == 'POST':
        examiner_id = request.POST.get('examiner_id')
        grading_round = request.POST.get('grading_round')
        examiner = get_object_or_404(Teacher, id=examiner_id)
        GradingAssignment.objects.create(
            answer_script=answer_script,
            examiner=examiner,
            grading_round=grading_round
        )
        answer_script.status = 'Assigned'
        answer_script.save()
        return redirect('list_answer_scripts', answer_script.exam.id)
    return render(request, 'answer_script_management/assign_examiner.html', {
        'answer_script': answer_script,
        'teachers': teachers,
    })

def review_discrepancies(request):
    discrepancies = Discrepancy.objects.filter(resolved=False)
    return render(request, 'answer_script_management/review_discrepancies.html', {'discrepancies': discrepancies})
