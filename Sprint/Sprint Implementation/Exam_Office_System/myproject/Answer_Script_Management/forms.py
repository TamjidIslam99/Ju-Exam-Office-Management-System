from django import forms
from .models import AnswerScript

class EvaluateScriptForm(forms.ModelForm):
    class Meta:
        model = AnswerScript
        fields = ['marks_examiner1', 'marks_examiner2', 'marks_examiner3']