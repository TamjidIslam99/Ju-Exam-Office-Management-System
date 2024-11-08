from django import forms
from Exam_Office_System.models import Exam, Student, Teacher

class AttendanceForm(forms.Form):
    exam = forms.ModelChoiceField(queryset=Exam.objects.all(), label="Exam", required=True)
    attendance_date = forms.DateField(widget=forms.SelectDateWidget, label="Attendance Date", required=True)
    students = forms.ModelMultipleChoiceField(queryset=Student.objects.all(), widget=forms.CheckboxSelectMultiple, label="Students", required=False)
    teachers = forms.ModelMultipleChoiceField(queryset=Teacher.objects.all(), widget=forms.CheckboxSelectMultiple, label="Teachers", required=False)

    class Meta:
        fields = ['exam', 'attendance_date', 'students', 'teachers']
