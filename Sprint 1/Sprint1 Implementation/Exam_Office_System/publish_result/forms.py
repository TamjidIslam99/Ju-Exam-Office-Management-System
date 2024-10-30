from django import forms
from Exam_Office.models import Result, Student
import csv
from io import StringIO

class ResultInputForm(forms.ModelForm):
    """Form for entering individual results."""
    class Meta:
        model = Result
        fields = ['student', 'examiner1', 'examiner2', 'examiner3', 'marks']

class BulkUploadForm(forms.Form):
    """Form for bulk uploading results via CSV."""
    file = forms.FileField()

    def process_csv(self, exam_id):
        csv_file = self.cleaned_data['file']
        file_data = csv_file.read().decode("utf-8")
        csv_data = StringIO(file_data)
        reader = csv.reader(csv_data)
        for row in reader:
            # Example row processing; adapt according to CSV structure
            student_id, examiner1, examiner2, examiner3, marks = row
            Result.objects.create(
                student=Student.objects.get(id=student_id),
                exam_id=exam_id,
                examiner1=examiner1,
                examiner2=examiner2,
                examiner3=examiner3,
                marks=marks
            )
