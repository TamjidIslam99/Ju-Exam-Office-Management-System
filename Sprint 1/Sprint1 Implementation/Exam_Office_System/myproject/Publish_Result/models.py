# Publish_Result/models.py

from django.db import models
from Exam_Office_System.models import Exam, Student, Result, Department

# models.py

class PublishedResult(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='published_results')
    session = models.CharField(max_length=50)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='published_results')
    average_marks = models.DecimalField(max_digits=5, decimal_places=2)  # Adjust as needed
    publish_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Published Result for {self.student.name} - {self.average_marks} marks"
