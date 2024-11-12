# views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ApplyForCertificateForm
from Exam_Office_System.models import CertificateApplication, Student

@login_required
def apply_for_certificate(request):
    student = Student.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = ApplyForCertificateForm(request.POST)
        if form.is_valid():
            certificate_application = form.save(commit=False)
            certificate_application.student = student
            certificate_application.status = 'Pending'
            certificate_application.save()
            
            # Add selected exams to the application if needed
            form.save_m2m()
            
            return redirect('application_success')  # Redirect to a success page
    else:
        form = ApplyForCertificateForm()

    return render(request, 'apply_certificate/apply_for_certificate.html', {
        'form': form,
        'student': student
    })
