# Publish_Result/forms.py

from django import forms

class ResultForm(forms.Form):
    exam_roll = forms.CharField(label='Exam Roll', max_length=50)
    score = forms.IntegerField(label='Score')

class BulkResultUploadForm(forms.Form):
    file = forms.FileField(label='Upload CSV or Excel File')
