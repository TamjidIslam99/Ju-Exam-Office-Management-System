# Publish_Result/models.py

from django.db import models
from Exam_Office_System.models import Exam, Student, Result

class ResultUpload(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='result_uploads')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='uploads/results/')  # for bulk uploads
    processed = models.BooleanField(default=False)

    def __str__(self):
        return f"Result upload for {self.exam.course.course_code} on {self.uploaded_at}"
