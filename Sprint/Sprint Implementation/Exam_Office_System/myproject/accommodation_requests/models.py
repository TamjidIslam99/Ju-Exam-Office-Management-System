# accommodation_requests/models.py
from django.db import models
from Exam_Office_System.models import*
from django.contrib.auth.models import User

class Student(models.Model):
    """
    This model represents a student in the system.

    Attributes
    ----------
    user : OneToOneField
        A one-to-one relationship with Django's User model.
    registration_number : CharField
        A unique identifier for the student.
    department : CharField
        The department the student belongs to.
    session : CharField
        The session the student is enrolled in.
    exam_name : CharField
        The name of the exam the student is registered for.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100)
    session = models.CharField(max_length=100)
    exam_name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.registration_number}"


class AccommodationRequest(models.Model):
    """
    This model represents the request for special accommodations from a student.

    Attributes
    ----------
    student : ForeignKey
        A foreign key relationship to the Student model.
    special_needs : TextField
        A description of the specific accommodations being requested (e.g., scriber, sickbed).
    medical_documents : FileField
        A file upload field for medical documentation supporting the accommodation request.
    is_approved : BooleanField
        Indicates whether the request has been approved (default is False).
    approval_notes : TextField
        Notes added by the Exam Office regarding the approval (optional).
    created_at : DateTimeField
        Timestamp of when the request was created.
    updated_at : DateTimeField
        Timestamp of the most recent update to the request.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    special_needs = models.TextField(help_text="Describe your special accommodation request (e.g. scriber, sickbed, medical aid).")
    medical_documents = models.FileField(upload_to='medical_documents/', help_text="Upload any medical documentation supporting your request.")
    is_approved = models.BooleanField(default=False)
    approval_notes = models.TextField(blank=True, null=True, help_text="Approval notes from the Exam Office.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Request by {self.student.user.username} for {self.special_needs} - {'Approved' if self.is_approved else 'Pending'}"
    

class DepartmentReview(models.Model):
    """
    This model represents the department's input on a student's accommodation request.

    Attributes
    ----------
    accommodation_request : ForeignKey
        A foreign key relationship to the AccommodationRequest model.
    department_input : TextField
        The department's comments or input on the requested accommodations.
    reviewed_at : DateTimeField
        Timestamp of when the department review was created.
    """
    accommodation_request = models.ForeignKey(AccommodationRequest, on_delete=models.CASCADE)
    department_input = models.TextField(help_text="Department's input on the requested accommodations.")
    reviewed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review for {self.accommodation_request.student.user.username} - {self.reviewed_at}"
