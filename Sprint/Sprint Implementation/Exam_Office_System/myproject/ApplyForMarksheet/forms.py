# ApplyForMarksheet/forms.py

from django import forms
from Exam_Office_System.models import MarksheetApplication, Exam

class ExamSelectionForm(forms.Form):
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.all(),
        widget=forms.RadioSelect,
        label="Select Exam",
        empty_label=None,
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
