# Remunerate_Teachers/forms.py
from django import forms
from Exam_Office_System.models import TeacherRemuneration

class RemunerationCreationForm(forms.ModelForm):
    """
    Form for creating a new TeacherRemuneration.
    """
    class Meta:
        model = TeacherRemuneration
        fields = ['teacher', 'exam', 'role', 'amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount < 0:
            raise forms.ValidationError("Amount must be a positive value.")
        return amount

class RemunerationUpdateForm(forms.Form):
    """
    Form for updating the status of a TeacherRemuneration.
    """
    remuneration_id = forms.IntegerField(widget=forms.HiddenInput)
    status = forms.ChoiceField(choices=TeacherRemuneration.STATUS_CHOICES)
