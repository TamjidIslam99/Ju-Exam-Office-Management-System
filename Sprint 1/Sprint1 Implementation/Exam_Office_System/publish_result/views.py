from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from Exam_Office.models import Result, Exam, Student, Attendance
from .forms import ResultInputForm, BulkUploadForm
import csv
from io import StringIO

def select_exam(request):
    """Allow exam office to select an exam to manage results."""
    exams = Exam.objects.all()
    return render(request, 'publish_result/select_exam.html', {'exams': exams})

def input_result(request, exam_id):
    """Input individual results for a selected exam or upload via CSV."""
    exam = get_object_or_404(Exam, id=exam_id)
    if request.method == 'POST':
        if 'upload' in request.POST:
            bulk_form = BulkUploadForm(request.POST, request.FILES)
            if bulk_form.is_valid():
                bulk_form.process_csv(exam_id)  # Handle bulk CSV upload
                messages.success(request, 'Results uploaded successfully.')
                return redirect('review_results', exam_id=exam.id)
        else:
            form = ResultInputForm(request.POST)
            if form.is_valid():
                result = form.save(commit=False)
                result.exam = exam
                result.save()
                messages.success(request, 'Result added successfully.')
                return redirect('review_results', exam_id=exam.id)
    else:
        form = ResultInputForm()
        bulk_form = BulkUploadForm()
    return render(request, 'publish_result/input_result.html', {'form': form, 'bulk_form': bulk_form, 'exam': exam})

def review_results(request, exam_id):
    """Review, validate, and flag results based on examiner discrepancies."""
    exam = get_object_or_404(Exam, id=exam_id)
    results = Result.objects.filter(exam=exam)
    threshold = 10  # Difference threshold for flagging
    flagged_results = []
    for result in results:
        if abs(result.examiner1 - result.examiner2) > threshold:
            flagged_results.append(result)
    return render(request, 'publish_result/review_results.html', {
        'exam': exam,
        'results': results,
        'flagged_results': flagged_results
    })

def publish_results(request, exam_id):
    """Finalize and publish results."""
    exam = get_object_or_404(Exam, id=exam_id)
    results = Result.objects.filter(exam=exam)
    results.update(status='Published')
    messages.success(request, 'Results published successfully.')
    return redirect('exam_office_dashboard')
