from django import forms
from .models import ExaminerAssignment

class ExaminerAssignmentForm(forms.ModelForm):
    class Meta:
        model = ExaminerAssignment
        fields = ['first_examiner', 'second_examiner', 'third_examiner']
