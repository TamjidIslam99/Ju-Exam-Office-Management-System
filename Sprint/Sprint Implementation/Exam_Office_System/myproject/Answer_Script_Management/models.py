from django.db import models
from Exam_Office_System.models import Exam, Student, Teacher, Result

class AnswerScript(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='answer_scripts')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='answer_scripts')
    examiner1 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner1_scripts')
    examiner2 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner2_scripts')
    examiner3 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner3_scripts')
    marks_examiner1 = models.IntegerField(null=True, blank=True)
    marks_examiner2 = models.IntegerField(null=True, blank=True)
    marks_examiner3 = models.IntegerField(null=True, blank=True)
    evaluated = models.BooleanField(default=False)
    flagged_for_review = models.BooleanField(default=False)

    def __str__(self):
        return f"Answer Script for {self.student.name} in {self.exam.course.course_code}"

class ScriptEvaluationLog(models.Model):
    answer_script = models.ForeignKey(AnswerScript, on_delete=models.CASCADE, related_name='evaluation_logs')
    examiner = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    marks_given = models.IntegerField()
    evaluation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Evaluation Log for {self.answer_script} by {self.examiner.name}"