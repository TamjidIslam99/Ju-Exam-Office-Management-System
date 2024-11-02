from django import forms
from Exam_Office_System.models import Exam  # Adjust if necessary based on your setup

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = ['department', 'batch', 'session', 'exam_date', 'course', 'invigilator', 'examiner1', 'examiner2', 'examiner3', 'question_creator', 'moderator', 'translator']
