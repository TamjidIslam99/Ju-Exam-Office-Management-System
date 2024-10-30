# Authentication/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User model extending Django's AbstractUser."""
    ROLE_CHOICES = [
        ('Exam_Office', 'Exam Office'),
        ('Department', 'Department'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student')
    ]
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )
    email = models.EmailField(unique=False)  # Ensure email uniqueness

    def __str__(self):
        return self.username


class Department(models.Model):
    """Model for storing department information."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_profile',default=1)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Student(models.Model):
    """Model for storing student details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Model for storing teacher details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExamOfficeOrAdmin(models.Model):
    """Model for exam office or administrative details."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='exam_office_profile')
    office_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.office_name


class Course(models.Model):
    """Model for storing course details."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=100)

    def __str__(self):
        return self.course_title


class Exam(models.Model):
    """Model for storing exam information."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    batch = models.CharField(max_length=20)
    session = models.CharField(max_length=20)
    exam_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    invigilator = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='invigilator_exams'
    )
    examiner1 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner1_exams'
    )
    examiner2 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner2_exams'
    )
    examiner3 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner3_exams'
    )

    def __str__(self):
        return f"Exam for {self.course.course_title} on {self.exam_date}"


class ExamSchedule(models.Model):
    """Model for managing exam schedules."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    published_date = models.DateField(auto_now_add=True)
    modified_date = models.DateField(auto_now=True)
    STATUS_CHOICES = [
        ('Published', 'Published'),
        ('Modified', 'Modified')
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES
    )

    def __str__(self):
        return f"Schedule for {self.exam}"


class ExamRegistration(models.Model):
    """Model for managing exam registrations."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    registration_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobilePayment', 'Mobile Payment')
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.student} - {self.exam}"


class Result(models.Model):
    """Model for storing exam results."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField()

    def __str__(self):
        return f"Result of {self.student} for {self.exam}"


class MarksheetApplication(models.Model):
    """Model for handling marksheet applications."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    application_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    token = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Marksheet Application of {self.student} for {self.exam}"


class CertificateApplication(models.Model):
    """Model for handling certificate applications."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    DEGREE_CHOICES = [
        ('Honours', 'Honours'),
        ('Masters', 'Masters'),
        ('PhD', 'PhD')
    ]
    degree = models.CharField(
        max_length=50,
        choices=DEGREE_CHOICES
    )
    application_date = models.DateField(auto_now_add=True)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected')
    ]
    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed')
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    payment_status = models.CharField(
        max_length=50,
        choices=PAYMENT_STATUS_CHOICES,
        default='Pending'
    )
    token = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"Certificate Application of {self.student} for {self.degree}"


class TeacherRemuneration(models.Model):
    """Model for handling teacher remunerations."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    ROLE_CHOICES = [
        ('Invigilator', 'Invigilator'),
        ('Examiner', 'Examiner'),
        ('QuestionSetter', 'Question Setter'),
        ('Moderator', 'Moderator'),
        ('Translator', 'Translator')
    ]
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid')
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.role} - {self.teacher} for {self.exam}"


class ExamMaterial(models.Model):
    """Model for managing exam materials."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    MATERIAL_TYPE_CHOICES = [
        ('AnswerScripts', 'Answer Scripts'),
        ('Pens', 'Pens'),
        ('QuestionPapers', 'Question Papers')
    ]
    material_type = models.CharField(
        max_length=50,
        choices=MATERIAL_TYPE_CHOICES
    )
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.material_type} for {self.exam}"


class Attendance(models.Model):
    """Model for tracking attendance."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    attendance_date = models.DateField()
    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Invigilator', 'Invigilator')
    ]
    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )

    def __str__(self):
        return f"{self.role} Attendance for {self.exam} on {self.attendance_date}"
