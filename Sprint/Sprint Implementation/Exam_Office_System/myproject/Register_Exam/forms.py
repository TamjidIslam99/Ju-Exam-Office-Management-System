# Register_Exam/forms.py

from django import forms
from Exam_Office_System.models import Exam

class ExamSelectionForm(forms.Form):
    exams = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.RadioSelect,
        label="Select Exam",
        empty_label=None,
    )
    REGISTRATION_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Retake', 'Retake'),
    ]
    registration_type = forms.ChoiceField(
        choices=REGISTRATION_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Registration Type"
    )

class PaymentForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobilePayment', 'Mobile Payment'),
    ]
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Payment Method",
    )
