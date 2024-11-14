# Publish_Result/models.py

from django.db import models
from Exam_Office_System.models import Exam, Student, Result, Department


# models.py
class PublishedResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='published_results')
    session = models.CharField(max_length=50)
    average_marks = models.FloatField()

    def __str__(self):
        return f"Published Result for {self.student.name} in {self.session}: {self.average_marks}"
