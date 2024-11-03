# view_result/forms.py

from django import forms
from Exam_Office_System.models import ExamRegistration

class ResultLookupForm(forms.Form):
    """
    Form for selecting an exam registration and registration type
    to view the associated result.

    This form filters `ExamRegistration` entries based on the logged-in
    student's profile and only includes registrations with a 'Verified' status.

    Attributes:
        exam_registration (ModelChoiceField): A dropdown for selecting the specific exam registration.
        registration_type (ChoiceField): Radio buttons for selecting the registration type (Regular or Retake).
        REGISTRATION_TYPE_CHOICES (list): Choice options for the registration type field.
    """

    exam_registration = forms.ModelChoiceField(
        queryset=ExamRegistration.objects.none(),
        label="Select Exam"
    )
    
    REGISTRATION_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Retake', 'Retake'),
    ]

    registration_type = forms.ChoiceField(
        choices=REGISTRATION_TYPE_CHOICES,
        widget=forms.RadioSelect,
        label="Registration Type"
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the `ResultLookupForm` with a filtered queryset
        of `ExamRegistration` objects for the given student.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments, including:
                - student (Student): The student instance whose exam registrations are queried.
        """
        student = kwargs.pop('student', None)
        super(ResultLookupForm, self).__init__(*args, **kwargs)
        if student:
            # Filter ExamRegistrations by the logged-in student and verified status
            self.fields['exam_registration'].queryset = ExamRegistration.objects.filter(
                student=student,
                status='Verified'
            )
            self.fields['exam_registration'].label_from_instance = lambda obj: (
                f"{obj.exam.course.course_code} - {obj.exam.course.course_title} on {obj.exam.exam_date} "
                f"({obj.registration_type})"
            )
