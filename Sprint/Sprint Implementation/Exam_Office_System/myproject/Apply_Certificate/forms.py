# forms.py

from django import forms
from Exam_Office_System.models import CertificateApplication, Exam

class ApplyForCertificateForm(forms.ModelForm):
    exams = forms.ModelMultipleChoiceField(
        queryset=Exam.objects.all(),  # Filter by department or student if needed
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    payment_method = forms.ChoiceField(choices=CertificateApplication.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = CertificateApplication
        fields = ['degree', 'exams', 'payment_method']
