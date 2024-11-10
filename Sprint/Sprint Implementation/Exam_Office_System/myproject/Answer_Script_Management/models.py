from django.db import models
from django.contrib.auth.models import User

class AnswerScript(models.Model):
    exam = models.ForeignKey('Exam', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    department = models.CharField(max_length=255)
    session = models.CharField(max_length=255)
    script_file = models.FileField(upload_to='answer_scripts/')
    status = models.CharField(max_length=255, default="Not Graded")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer Script for {self.student.name} - {self.exam.name}"
class ExaminerAssignment(models.Model):
    answer_script = models.ForeignKey(AnswerScript, on_delete=models.CASCADE)
    first_examiner = models.ForeignKey(User, related_name='first_examiner', on_delete=models.SET_NULL, null=True)
    second_examiner = models.ForeignKey(User, related_name='second_examiner', on_delete=models.SET_NULL, null=True)
    third_examiner = models.ForeignKey(User, related_name='third_examiner', on_delete=models.SET_NULL, null=True)
    
    first_examiner_marks = models.FloatField(null=True, blank=True)
    second_examiner_marks = models.FloatField(null=True, blank=True)
    third_examiner_marks = models.FloatField(null=True, blank=True)
    
    status = models.CharField(max_length=255, default="Not Evaluated")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Assignment for {self.answer_script}"
class Discrepancy(models.Model):
    assignment = models.ForeignKey(ExaminerAssignment, on_delete=models.CASCADE)
    difference = models.FloatField()
    resolved = models.BooleanField(default=False)
    flagged_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Discrepancy for {self.assignment.answer_script}"
class EvaluationLog(models.Model):
    examiner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log for {self.examiner.username} at {self.timestamp}"
