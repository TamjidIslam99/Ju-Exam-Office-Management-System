from django.db import models
from Exam_Office_System.models import Exam, Teacher, Student

# Constants for grading status
NOT_GRADED = 'Not Graded'
GRADED = 'Graded'

# Constants for discrepancy status
PENDING = 'Pending'
RESOLVED = 'Resolved'

class AnswerScript(models.Model):
    """
    Model representing an answer script submitted by a student for an exam.
    Includes metadata about the script file, its grading status, and examiner assignments.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answer_scripts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answer_scripts')
    examiner = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='assigned_answer_scripts')
    script_file = models.FileField(upload_to='answer_scripts/')
    grading_status = models.CharField(
        max_length=20, choices=[(NOT_GRADED, 'Not Graded'), (GRADED, 'Graded')], default=NOT_GRADED
    )
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Answer Script for {self.student.name} in {self.exam.course.course_code}"

class GradingDiscrepancy(models.Model):
    """
    Model representing grading discrepancies between different examiners for a student's answer script.
    Tracks marks assigned by multiple examiners and the resolution status of the discrepancy.
    """
    answer_script = models.ForeignKey(AnswerScript, on_delete=models.CASCADE, related_name='grading_discrepancies')
    examiner1_marks = models.IntegerField(null=True)
    examiner2_marks = models.IntegerField(null=True)
    examiner3_marks = models.IntegerField(null=True)
    discrepancy_status = models.CharField(
        max_length=20, choices=[(PENDING, 'Pending'), (RESOLVED, 'Resolved')], default=PENDING
    )
    
    def __str__(self):
        return f"Discrepancy for {self.answer_script.student.name} in {self.answer_script.exam.course.course_code}"

class FinalizedAnswerScript(models.Model):
    """
    Model representing the finalized version of an answer script, with total marks and final status.
    This model ensures that answer scripts are marked as finalized after grading discrepancies are resolved.
    """
    answer_script = models.OneToOneField(AnswerScript, on_delete=models.CASCADE, related_name='finalized_script')
    total_marks = models.IntegerField()
    status = models.CharField(
        max_length=20, choices=[('Finalized', 'Finalized'), ('Not Finalized', 'Not Finalized')], default='Not Finalized'
    )

    def __str__(self):
        return f"Finalized script for {self.answer_script.student.name}"
