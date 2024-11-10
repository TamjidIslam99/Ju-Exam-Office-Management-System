# answer_script_management/models.py

from django.db import models
from Exam_Office_System.models import Exam, Student, Teacher

class AnswerScript(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answer_scripts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answer_scripts')
    status = models.CharField(max_length=20, default='Pending', choices=[
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned'),
        ('Evaluated', 'Evaluated'),
    ])
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"AnswerScript of {self.student.name} for {self.exam.course.course_code}"

class GradingAssignment(models.Model):
    answer_script = models.ForeignKey(AnswerScript, on_delete=models.CASCADE, related_name='assignments')
    examiner = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='assigned_grades')
    grading_round = models.IntegerField()  # 1, 2, or 3 for different examiner rounds
    marks = models.IntegerField(null=True, blank=True)
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_graded = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Grading for {self.answer_script} by {self.examiner.name}"

class Discrepancy(models.Model):
    answer_script = models.OneToOneField(AnswerScript, on_delete=models.CASCADE, related_name='discrepancy')
    examiner_1_marks = models.IntegerField()
    examiner_2_marks = models.IntegerField()
    discrepancy_threshold = models.IntegerField()
    examiner_3_marks = models.IntegerField(null=True, blank=True)
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Discrepancy for {self.answer_script}"
