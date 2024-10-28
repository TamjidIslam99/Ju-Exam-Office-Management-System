from django.db import models


class User(models.Model):
    """Model for storing user information."""
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(
        max_length=50,
        choices=[
            ('Exam_Office', 'Exam Office'),
            ('Department', 'Department'),
            ('Teacher', 'Teacher'),
            ('Student', 'Student')
        ]
    )
    email = models.EmailField()

    def __str__(self):
        return self.username


class Department(models.Model):
    """Model for storing department information."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    """Model for storing student details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    registration_number = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    session = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    """Model for storing teacher details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ExamOfficeOrAdmin(models.Model):
    """Model for exam office or administrative details."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    office_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.office_name


class Course(models.Model):
    """Model for storing course details."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_code = models.CharField(max_length=20)
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
        Teacher, on_delete=models.SET_NULL, null=True, related_name='invigilator'
    )
    examiner1 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner1'
    )
    examiner2 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner2'
    )
    examiner3 = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, related_name='examiner3'
    )

    def __str__(self):
        return f"Exam for {self.course.course_title}"


class ExamSchedule(models.Model):
    """Model for managing exam schedules."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    published_date = models.DateField()
    modified_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Published', 'Published'),
            ('Modified', 'Modified')
        ]
    )


class ExamRegistration(models.Model):
    """Model for managing exam registrations."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    registration_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Verified', 'Verified'),
            ('Rejected', 'Rejected')
        ]
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ]
    )
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('CreditCard', 'Credit Card'),
            ('BankTransfer', 'Bank Transfer'),
            ('MobilePayment', 'Mobile Payment')
        ]
    )


class Result(models.Model):
    """Model for storing exam results."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    marks = models.IntegerField()


class MarksheetApplication(models.Model):
    """Model for handling marksheet applications."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    application_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ]
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ]
    )
    token = models.CharField(max_length=50)


class CertificateApplication(models.Model):
    """Model for handling certificate applications."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    degree = models.CharField(
        max_length=50,
        choices=[
            ('Honours', 'Honours'),
            ('Masters', 'Masters'),
            ('PhD', 'PhD')
        ]
    )
    application_date = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ]
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Failed', 'Failed')
        ]
    )
    token = models.CharField(max_length=50)


class TeacherRemuneration(models.Model):
    """Model for handling teacher remunerations."""
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=50,
        choices=[
            ('Invigilator', 'Invigilator'),
            ('Examiner', 'Examiner'),
            ('QuestionSetter', 'Question Setter'),
            ('Moderator', 'Moderator'),
            ('Translator', 'Translator')
        ]
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[
            ('Pending', 'Pending'),
            ('Paid', 'Paid')
        ]
    )


class ExamMaterial(models.Model):
    """Model for managing exam materials."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    material_type = models.CharField(
        max_length=50,
        choices=[
            ('AnswerScripts', 'Answer Scripts'),
            ('Pens', 'Pens'),
            ('QuestionPapers', 'Question Papers')
        ]
    )
    quantity = models.IntegerField()


class Attendance(models.Model):
    """Model for tracking attendance."""
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True, blank=True)
    attendance_date = models.DateField()
    role = models.CharField(
        max_length=50,
        choices=[
            ('Student', 'Student'),
            ('Invigilator', 'Invigilator')
        ]
    )

