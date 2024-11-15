from django import forms
from .models import ExamCalendar, Exam

class ExamCalendarForm(forms.ModelForm):
    class Meta:
        model = ExamCalendar
        fields = [
            'system_type',
            'class_start_date',
            'class_end_date',
            'exam_start_date',
            'exam_end_date'
        ]

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = [
            'session',  # session is in Exam model
            'batch',    # batch is in Exam model
        ]

class_start_date = forms.DateField(widget=forms.SelectDateWidget)
class_end_date = forms.DateField(widget=forms.SelectDateWidget)
exam_start_date = forms.DateField(widget=forms.SelectDateWidget)
exam_end_date = forms.DateField(widget=forms.SelectDateWidget)