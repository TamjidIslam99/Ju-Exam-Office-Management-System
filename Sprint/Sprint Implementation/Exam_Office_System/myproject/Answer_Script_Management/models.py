from django.db import models
from Exam_Office_System.models import Exam, Student, Teacher

class AnswerScript(models.Model):
    """
    Model representing an answer script submitted by a student for an exam.

    Attributes:
        exam (ForeignKey): The exam associated with this answer script.
        student (ForeignKey): The student who submitted the answer script.
        examiner1 (ForeignKey): The first examiner assigned to evaluate the script.
        examiner2 (ForeignKey): The second examiner assigned to evaluate the script.
        examiner3 (ForeignKey): The third examiner assigned to evaluate the script.
        marks_examiner1 (IntegerField): Marks given by the first examiner.
        marks_examiner2 (IntegerField): Marks given by the second examiner.
        marks_examiner3 (IntegerField): Marks given by the third examiner.
        evaluated (BooleanField): Indicates whether the script has been evaluated.
        flagged_for_review (BooleanField): Indicates whether the script has been flagged for review.
    """

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
        """
        String representation of the AnswerScript model.

        Returns:
            str: A string representing the answer script, including the student's name and the exam course code.
        """
        return f"Answer Script for {self.student.name} in {self.exam.course.course_code}"


class ScriptEvaluationLog(models.Model):
    """
    Model representing the evaluation log for an answer script.

    Attributes:
        answer_script (ForeignKey): The answer script associated with this evaluation log.
        examiner (ForeignKey): The examiner who evaluated the answer script.
        marks_given (IntegerField): The marks given by the examiner.
        evaluation_date (DateField): The date when the evaluation was made, automatically set to the current date.
    """

    answer_script = models.ForeignKey(AnswerScript, on_delete=models.CASCADE, related_name='evaluation_logs')
    examiner = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    marks_given = models.IntegerField()
    evaluation_date = models.DateField(auto_now_add=True)

    def __str__(self):
        """
        String representation of the ScriptEvaluationLog model.

        Returns:
            str: A string representing the evaluation log, including the answer script and examiner's name.
        """
        return f"Evaluation Log for {self.answer_script} by {self.examiner.name}"