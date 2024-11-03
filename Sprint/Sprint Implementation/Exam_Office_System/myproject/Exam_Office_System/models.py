from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

class UserManager(BaseUserManager):
    """
    Custom manager for the ``User`` model with methods for creating users and superusers.
    """
    def create_user(self, username, email, password=None, role=None, **extra_fields):
        """
        Creates and saves a regular user with the given username, email, password, and role.

        Args:
            username (str): The username of the user.
            email (str): The email address of the user.
            password (str, optional): The password for the user.
            role (str): The role of the user.
            **extra_fields: Additional fields for the user.

        Raises:
            ValueError: If email or role is not provided.

        Returns:
            User: The created user instance.
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

        Args:
            username (str): The username of the superuser.
            email (str): The email address of the superuser.
            password (str): The password for the superuser.
            role (str, optional): The role of the superuser, default is 'Exam_Office'.
            **extra_fields: Additional fields for the superuser.

        Raises:
            ValueError: If the role is invalid.

        Returns:
            User: The created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if role not in ['Exam_Office', 'Teacher', 'Department', 'Student']:
            raise ValueError('Superuser must have a valid role')
        return self.create_user(username, email, password, role, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that supports different roles in the system.

    Attributes:
        ROLE_CHOICES (list of tuples): Available roles for the user.
        username (CharField): Unique username for the user.
        email (EmailField): Unique email address for the user.
        role (CharField): Role of the user.
        is_active (BooleanField): Indicates if the user account is active.
        is_staff (BooleanField): Indicates if the user can access the admin site.
        objects (UserManager): Custom manager for the ``User`` model.
        USERNAME_FIELD (str): Field used for authentication.
        REQUIRED_FIELDS (list): Fields required when creating a superuser.
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
        Returns the string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username

class Department(models.Model):
    """
    Model representing a department in the system.

    Attributes:
        user (OneToOneField): One-to-one relationship with a ``User``.
        name (CharField): The name of the department.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_profile')
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the department.

        Returns:
            str: The name of the department.
        """
        return self.name

class Student(models.Model):
    """
    Model representing a student in the system.

    Attributes:
        user (OneToOneField): One-to-one relationship with a ``User``.
        registration_number (CharField): Unique registration number for the student.
        department (ForeignKey): Relationship to a ``Department``.
        session (CharField): Academic session for the student.
        name (CharField): Name of the student.
        hall_clearance (BooleanField): Indicates hall clearance status.
        library_clearance (BooleanField): Indicates library clearance status.
        expelled (BooleanField): Indicates if the student is expelled.
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
        Returns the string representation of the student.

        Returns:
            str: The name of the student.
        """
        return self.name

class Teacher(models.Model):
    """
    Model representing a teacher in the system.

    Attributes:
        user (OneToOneField): One-to-one relationship with a ``User``.
        department (ForeignKey): Relationship to a ``Department``.
        name (CharField): Name of the teacher.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the teacher.

        Returns:
            str: The name of the teacher.
        """
        return self.name

class ExamOfficeOrAdmin(models.Model):
    """
    Model representing an exam office or admin role in the system.

    Attributes:
        OFFICE_ROLE_CHOICES (list of tuples): Available roles (Exam Office or Admin).
        user (OneToOneField): One-to-one relationship with a ``User``.
        office_name (CharField): The name of the office.
        contact_number (CharField): Contact number of the office.
        address (TextField): Address of the office.
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
        Returns the string representation of the exam office or admin.

        Returns:
            str: The office name.
        """
        return self.office_name

class Course(models.Model):
    """
    Model representing a course in a department.

    Attributes:
        department (ForeignKey): Relationship to a ``Department``.
        course_code (CharField): Unique code of the course.
        course_title (CharField): Title of the course.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=50, unique=True)
    course_title = models.CharField(max_length=255)

    def __str__(self):
        """
        Returns the string representation of the course.

        Returns:
            str: The course code and title.
        """
        return f"{self.course_code} - {self.course_title}"

class Exam(models.Model):
    """
    Model representing an exam for a specific course.

    Attributes:
        department (ForeignKey): Relationship to a ``Department``.
        batch (CharField): Batch for which the exam is conducted.
        session (CharField): Academic session of the exam.
        exam_date (DateField): Date of the exam.
        course (ForeignKey): Relationship to a ``Course``.
        invigilator (ForeignKey): Teacher invigilating the exam.
        examiner1 (ForeignKey): Teacher assigned as examiner 1.
        examiner2 (ForeignKey): Teacher assigned as examiner 2.
        examiner3 (ForeignKey): Teacher assigned as examiner 3.
        question_creator (ForeignKey): Teacher who created the questions.
        moderator (ForeignKey): Teacher who moderated the exam.
        translator (ForeignKey): Teacher who translated the exam.
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
        Returns the string representation of the exam.

        Returns:
            str: Details of the exam including course code and date.
        """
        return f"Exam {self.id} for {self.course.course_code} on {self.exam_date}"

class ExamSchedule(models.Model):
    """
    Model representing a schedule for an exam.

    Attributes:
        STATUS_CHOICES (list of tuples): Status options for the schedule.
        exam (OneToOneField): Relationship to an ``Exam``.
        published_date (DateField): Date the schedule was published.
        modified_date (DateField): Date the schedule was last modified.
        status (CharField): Status of the schedule (Published or Modified).
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
        Returns the string representation of the exam schedule.

        Returns:
            str: Details of the schedule including associated exam.
        """
        return f"Schedule for {self.exam}"

class ExamRegistration(models.Model):
    """
    Model representing a student's registration for an exam.

    Attributes:
        STATUS_CHOICES (list of tuples): Status options for the registration.
        PAYMENT_STATUS_CHOICES (list of tuples): Payment status options.
        PAYMENT_METHOD_CHOICES (list of tuples): Payment method options.
        REGISTRATION_TYPE_CHOICES (list of tuples): Registration type options.
        student (ForeignKey): Relationship to a ``Student``.
        exam (ForeignKey): Relationship to an ``Exam``.
        registration_type (CharField): Type of registration (Regular or Retake).
        registration_date (DateField): Date of registration.
        status (CharField): Status of the registration (Pending, Verified, or Rejected).
        payment_status (CharField): Status of payment (Pending, Completed, or Failed).
        payment_method (CharField): Payment method used.
        ineligibility_reasons (TextField): Reasons for ineligibility.
        admit_card_generated (BooleanField): Indicates if admit card has been generated.
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
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='registrations', null=True, blank=True)
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES)
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    ineligibility_reasons = models.TextField(null=True, blank=True)
    admit_card_generated = models.BooleanField(default=False)

    def __str__(self):
        """
        Returns the string representation of the exam registration.

        Returns:
            str: Details of the registration including student name, course code, exam date, and registration type.
        """
        return (
            f"Registration {self.id} by {self.student.name} for "
            f"{self.exam.course.course_code} on {self.exam.exam_date} as {self.registration_type}"
        )

class Result(models.Model):
    """
    Model representing the result of a student for a specific exam registration.

    Attributes:
        registration (OneToOneField): Relationship to an ``ExamRegistration``.
        marks (IntegerField): Marks obtained by the student in the exam.
    """
    registration = models.OneToOneField(
        ExamRegistration, on_delete=models.CASCADE, related_name='result', null=True, blank=True
    )
    marks = models.IntegerField(null=True, blank=True)

    def __str__(self):
        """
        Returns the string representation of the result.

        Returns:
            str: Details of the result including student name, course code, and marks obtained.
        """
        return (
            f"Result {self.id} - {self.registration.student.name} for "
            f"{self.registration.exam.course.course_code}: {self.marks} marks"
        )

class MarksheetApplication(models.Model):
    """
    Model representing a student's application for a marksheet.

    Attributes:
        STATUS_CHOICES (list of tuples): Status options for the application.
        PAYMENT_STATUS_CHOICES (list of tuples): Payment status options.
        PAYMENT_METHOD_CHOICES (list of tuples): Payment method options.
        student (ForeignKey): Relationship to a ``Student``.
        exam (ForeignKey): Relationship to an ``Exam``.
        application_date (DateField): Date of application.
        status (CharField): Status of the application (Pending, Approved, or Rejected).
        payment_status (CharField): Status of payment (Pending, Completed, or Failed).
        payment_method (CharField): Payment method used.
        token (CharField): Unique token for the application.
    """
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

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marksheet_applications')
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='marksheet_applications')
    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    token = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique token if not already set.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.token:
            self.token = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the marksheet application.

        Returns:
            str: Details of the application including student name and application ID.
        """
        return f"Marksheet Application {self.id} by {self.student.name}"

class CertificateApplication(models.Model):
    """
    Model representing a student's application for a certificate.

    Attributes:
        DEGREE_CHOICES (list of tuples): Degree options for the certificate.
        STATUS_CHOICES (list of tuples): Status options for the application.
        PAYMENT_STATUS_CHOICES (list of tuples): Payment status options.
        PAYMENT_METHOD_CHOICES (list of tuples): Payment method options.
        student (ForeignKey): Relationship to a ``Student``.
        degree (CharField): Degree for which the certificate is applied.
        application_date (DateField): Date of application.
        status (CharField): Status of the application (Pending, Approved, or Rejected).
        payment_status (CharField): Status of payment (Pending, Completed, or Failed).
        payment_method (CharField): Payment method used.
        token (CharField): Unique token for the application.
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
    token = models.CharField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Overrides the save method to generate a unique token if not already set.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if not self.token:
            self.token = uuid.uuid4().hex[:10].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Returns the string representation of the certificate application.

        Returns:
            str: Details of the application including student name and application ID.
        """
        return f"Certificate Application {self.id} by {self.student.name}"

class TeacherRemuneration(models.Model):
    """
    Model representing remuneration for teachers for different exam roles.

    Attributes:
        ROLE_CHOICES (list of tuples): Role options for the teacher.
        STATUS_CHOICES (list of tuples): Status options for the remuneration.
        teacher (ForeignKey): Relationship to a ``Teacher``.
        exam (ForeignKey): Relationship to an ``Exam``.
        role (CharField): Role of the teacher in the exam.
        amount (DecimalField): Remuneration amount.
        status (CharField): Status of the payment (Pending or Paid).
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
        Returns the string representation of the teacher remuneration.

        Returns:
            str: Details of the remuneration including teacher name and role.
        """
        return f"Remuneration {self.id} for {self.teacher.name} as {self.role}"

class ExamMaterials(models.Model):
    """
    Model representing materials used for an exam.

    Attributes:
        MATERIAL_TYPE_CHOICES (list of tuples): Type options for the materials.
        exam (ForeignKey): Relationship to an ``Exam``.
        material_type (CharField): Type of material (e.g., Answer Scripts, Pens).
        quantity (IntegerField): Quantity of materials.
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
        Returns the string representation of the exam materials.

        Returns:
            str: Details of the materials including type and associated exam.
        """
        return f"{self.material_type} for {self.exam}"

class Attendance(models.Model):
    """
    Model representing attendance for an exam.

    Attributes:
        ROLE_CHOICES (list of tuples): Role options for the attendee.
        exam (ForeignKey): Relationship to an ``Exam``.
        student (ForeignKey): Relationship to a ``Student``, optional.
        teacher (ForeignKey): Relationship to a ``Teacher``, optional.
        attendance_date (DateField): Date of attendance.
        role (CharField): Role of the attendee (Student or Invigilator).
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
        Returns the string representation of the attendance.

        Returns:
            str: Details of the attendance including attendee name, role, and date.
        """
        if self.role == 'Student':
            return f"Attendance {self.id} - {self.student.name} as {self.role} on {self.attendance_date}"
        else:
            return f"Attendance {self.id} - {self.teacher.name} as {self.role} on {self.attendance_date}"
