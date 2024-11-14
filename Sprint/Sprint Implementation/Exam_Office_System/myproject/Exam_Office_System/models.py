

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


# Custom User Manager
class UserManager(BaseUserManager):


    def create_user(self, username, email, password=None, role=None, **extra_fields):
        """
        Creates and saves a User with the given username, email, password, and role.

        :param username: str - Username for the user.
        :param email: str - Email address for the user. Must be unique.
        :param password: str - Password for the user.
        :param role: str - Role of the user. Must be one of the defined ROLE_CHOICES.
        :param extra_fields: dict - Additional fields for the user.
        :raises ValueError: If email or role is not provided.
        :return: User - The created user instance.
        """
        if not email:
            raise ValueError('The Email field must be set')
        if not role:
            raise ValueError('The Role field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, role='Exam_Office', **extra_fields):
        """
        Creates and saves a superuser with the given username, email, password, and role.

        :param username: str - Username for the superuser.
        :param email: str - Email address for the superuser.
        :param password: str - Password for the superuser.
        :param role: str - Role of the superuser. Defaults to 'Exam_Office'.
        :param extra_fields: dict - Additional fields for the superuser.
        :raises ValueError: If an invalid role is provided.
        :return: User - The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if role not in ['Exam_Office', 'Teacher', 'Department', 'Student']:
            raise ValueError('Superuser must have a valid role')
        return self.create_user(username, email, password, role, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with roles.

    Extends Django's AbstractBaseUser and PermissionsMixin to provide a flexible user system with multiple roles.
    """

    ROLE_CHOICES = [
        ('Exam_Office', 'Exam Office'),
        ('Department', 'Department'),
        ('Teacher', 'Teacher'),
        ('Student', 'Student'),
    ]

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # For admin site access

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role']

    def __str__(self):
        """
        Returns the string representation of the User.

        :return: str - The username of the user.
        """
        return self.username


# Department Model
class Department(models.Model):
    """
    Represents a department within the university.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_profile')
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the Department.

        :return: str - The name of the department.
        """
        return self.name


# Student Model
class Student(models.Model):
    """
    Represents a student.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    registration_number = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='students')
    session = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    hall_clearance = models.BooleanField(default=False, null=True)
    library_clearance = models.BooleanField(default=False, null=True)
    expelled = models.BooleanField(default=False, null=True)

    def __str__(self):
        """
        Returns the string representation of the Student.

        :return: str - The name of the student.
        """
        return self.name


# Teacher Model
class Teacher(models.Model):
    """
    Represents a teacher.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the Teacher.

        :return: str - The name of the teacher.
        """
        return self.name


# Exam Office or Admin Model
class ExamOfficeOrAdmin(models.Model):
    """
    Represents an exam office or an admin.
    """

    OFFICE_ROLE_CHOICES = [
        ('Exam_Office', 'Exam Office'),
        ('Admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='exam_office_profile')
    office_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        """
        Returns the string representation of the ExamOfficeOrAdmin.

        :return: str - The office name.
        """
        return self.office_name


# Course Model
class Course(models.Model):
    """
    Represents a course within a department.
    """

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=50, unique=True)
    course_title = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the Course.

        :return: str - The course code and title.
        """
        return f"{self.course_code} - {self.course_title}"


# Exam Model
class Exam(models.Model):
    """
    Represents an exam for a course.
    """

    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='exams')
    batch = models.CharField(max_length=50)
    session = models.CharField(max_length=50)
    exam_date = models.DateField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    invigilator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='invigilated_exams')
    examiner1 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='exam1_exams')
    examiner2 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='exam2_exams')
    examiner3 = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='exam3_exams')
    question_creator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='question_created_exams')
    moderator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='moderated_exams')
    translator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='translated_exams')

    def __str__(self):
        """
        Returns the string representation of the Exam.

        :return: str - A descriptive identifier for the exam.
        """
        return f"Exam {self.id} for {self.course.course_code} on {self.exam_date}"


# Exam Schedule Model
class ExamSchedule(models.Model):
    """
    Represents the schedule for an exam.
    """

    STATUS_CHOICES = [
        ('Published', 'Published'),
        ('Modified', 'Modified'),
    ]

    exam = models.OneToOneField(Exam, on_delete=models.CASCADE, related_name='schedule')
    published_date = models.DateField()
    modified_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def __str__(self):
        """
        Returns the string representation of the ExamSchedule.

        :return: str - A descriptive identifier for the schedule.
        """
        return f"Schedule for {self.exam}"


# Exam Registration Model
class ExamRegistration(models.Model):
    """
    Represents a student's registration for exams.
    """

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobilePayment', 'Mobile Payment'),
    ]

    REGISTRATION_TYPE_CHOICES = [
        ('Regular', 'Regular'),
        ('Retake', 'Retake'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_registrations')
    exams = models.ManyToManyField(Exam, related_name='registrations')
    registration_type = models.CharField(
        max_length=20,
        choices=REGISTRATION_TYPE_CHOICES,
        help_text="Type of registration: Regular or Retake."
    )
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    ineligibility_reasons = models.TextField(null=True, blank=True)
    admit_card_generated = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the string representation of the ExamRegistration.

        :return: str - A descriptive identifier for the registration.
        """
        return f"Registration {self.id} by {self.student.name}"


# Results Model
class Result(models.Model):
    """
    Represents the result of a student for an exam.
    """

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    marks = models.IntegerField()

    class Meta:
        """
        Meta options for the Result model.

        Ensures that each student has only one result per exam.
        """
        unique_together = ('exam', 'student')

    def __str__(self):
        """
        Returns the string representation of the Result.

        :return: str - A descriptive identifier for the result.
        """
        return f"Result {self.id} - {self.student.name}: {self.marks} marks"


# Marksheet Application Model
class MarksheetApplication(models.Model):
    """
    Represents an application for a marksheet by a student.
    """

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobilePayment', 'Mobile Payment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    token = models.CharField(max_length=10, unique=True, null=True)

    def __str__(self):
        """
        Returns the string representation of the MarksheetApplication.

        :return: str - A descriptive identifier for the marksheet application.
        """
        return f"MarksheetApplication {self.token} by {self.student.name}"


# Certificate Application Model
class CertificateApplication(models.Model):
    """
    Represents an application for a certificate by a student.
    """

    DEGREE_CHOICES = [
        ('Honours', 'Honours'),
        ('Regular Masters', 'Regular Masters'),
        ('Professional Masters', 'Professional Masters'),
        ('PhD', 'PhD'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Failed', 'Failed'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('CreditCard', 'Credit Card'),
        ('BankTransfer', 'Bank Transfer'),
        ('MobilePayment', 'Mobile Payment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='certificate_applications')
    degree = models.CharField(max_length=30, choices=DEGREE_CHOICES)
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    token = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """
        Returns the string representation of the CertificateApplication.

        :return: str - A descriptive identifier for the certificate application.
        """
        return f"Certificate Application {self.id} by {self.student.name}"


# Teacher Remuneration Model
class TeacherRemuneration(models.Model):
    """
    Represents remuneration details for a teacher based on their role in an exam.
    """

    ROLE_CHOICES = [
        ('Invigilator', 'Invigilator'),
        ('Examiner', 'Examiner'),
        ('QuestionSetter', 'Question Setter'),
        ('Moderator', 'Moderator'),
        ('Translator', 'Translator'),
    ]

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
    ]

    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='remunerations')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='remunerations')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        """
        Returns the string representation of the TeacherRemuneration.

        :return: str - A descriptive identifier for the remuneration.
        """
        return f"Remuneration {self.id} for {self.teacher.name} as {self.role}"


# Exam Materials Model
class ExamMaterials(models.Model):
    """
    Represents materials required for an exam.
    """

    MATERIAL_TYPE_CHOICES = [
        ('AnswerScripts', 'Answer Scripts'),
        ('Pens', 'Pens'),
        ('QuestionPapers', 'Question Papers'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE_CHOICES)
    quantity = models.IntegerField()

    def __str__(self):
        """
        Returns the string representation of the ExamMaterials.

        :return: str - A descriptive identifier for the exam material.
        """
        return f"{self.material_type} for {self.exam}"


# Attendance Model
class Attendance(models.Model):
    """
    Represents attendance records for exams.
    """

    ROLE_CHOICES = [
        ('Student', 'Student'),
        ('Invigilator', 'Invigilator'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendances', null=True, blank=True)
    attendance_date = models.DateField()
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        """
        Returns the string representation of the Attendance.

        :return: str - A descriptive identifier for the attendance record.
        """
        if self.role == 'Student':
            return f"Attendance {self.id} - {self.student.name} as {self.role} on {self.attendance_date}"
        else:
            return f"Attendance {self.id} - {self.teacher.name} as {self.role} on {self.attendance_date}"


class Sickbed(models.Model):

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='sick_student', null=True, blank=True)
    reason = models.TextField()


