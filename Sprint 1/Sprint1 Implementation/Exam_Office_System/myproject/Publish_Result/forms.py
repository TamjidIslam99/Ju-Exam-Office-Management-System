from django import forms

class ResultForm(forms.Form):
    """
    Form for submitting individual exam results.

    This form allows users to input an exam roll number and the corresponding score.

    Attributes:
        exam_roll (CharField): The exam roll number of the student.
        score (IntegerField): The score obtained by the student in the exam.
    """

    exam_roll = forms.CharField(label='Exam Roll', max_length=50)
    score = forms.IntegerField(label='Score')


class BulkResultUploadForm(forms.Form):
    """
    Form for bulk uploading exam results.

    This form allows users to upload a CSV or Excel file containing exam results.

    Attributes:
        file (FileField): The file field for uploading the CSV or Excel file.
    """

    file = forms.FileField(label='Upload CSV or Excel File')
