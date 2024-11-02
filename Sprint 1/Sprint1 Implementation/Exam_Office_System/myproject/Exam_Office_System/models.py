from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Custom User Manager
class UserManager(BaseUserManager):
    """Manager for custom User model with create_user and create_superuser methods."""

    def create_user(self, username, email, password=None, role=None, **extra_fields):
        """
        Create a regular user with specified username, email, and role.

        Args:
            username (str): Username of the user.
            email (str): Email of the user.
            password (str, optional): User's password.
            role (str): User's role (e.g., Teacher, Student).

        Raises:
            ValueError: If email or role is not provided.

        Returns:
            User: Created User instance.
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
        Create a superuser with admin privileges and a specified role.

        Args:
            username (str): Username of the superuser.
            email (str): Email of the superuser.
            password (str): Password for the superuser.
            role (str): Role of the superuser (default is 'Exam_Office').

        Raises:
            ValueError: If an invalid role is specified.
        
        Returns:
            User: Created superuser instance.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if role not in ['Exam_Office', 'Teacher', 'Department', 'Student']:
            raise ValueError('Superuser must have a valid role')
        return self.create_user(username, email, password, role, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model with username, email, and role fields.

    Attributes:
        ROLE_CHOICES (list of tuples): Available roles for the user.
        username (CharField): Unique username for the user.
        email (EmailField): Unique email address.
        role (CharField): Role of the user (e.g., Teacher, Student).
        is_active (BooleanField): Indicates if the user account is active.
        is_staff (BooleanField): Indicates if the user has staff permissions.
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

    def _str_(self):
        """
        Returns the string representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


# Department Model
class Department(models.Model):
    """
    Model representing a department with a unique name.

    Attributes:
        user (OneToOneField): Linked User instance for department profile.
        name (CharField): Name of the department.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='department_profile')
    name = models.CharField(max_length=255)

    def _str_(self):
        """
        Returns the string representation of the department.

        Returns:
            str: The name of the department.
        """
        return self.name


# Student Model
class Student(models.Model):
    """
    Model representing a student, linked to a user, with department and clearance information.

    Attributes:
        user (OneToOneField): Linked User instance for student profile.
        registration_number (CharField): Unique registration number.
        department (ForeignKey): Associated department.
        hall_clearance (BooleanField): Indicates if hall clearance is done.
        library_clearance (BooleanField): Indicates if library clearance is done.
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

    def _str_(self):
        """
        Returns the string representation of the student.

        Returns:
            str: The name of the student.
        """
        return self.name


# Teacher Model
class Teacher(models.Model):
    """
    Model representing a teacher, linked to a user and a department.

    Attributes:
        user (OneToOneField): Linked User instance for teacher profile.
        department (ForeignKey): Associated department.
        name (CharField): Name of the teacher.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='teachers')
    name = models.CharField(max_length=255)

    def _str_(self):
        """
        Returns the string representation of the teacher.

        Returns:
            str: The name of the teacher.
        """
        return self.name


# Exam Office or Admin Model
class ExamOfficeOrAdmin(models.Model):
    """
    Model for the exam office or admin user with contact information.

    Attributes:
        user (OneToOneField): Linked User instance for office profile.
        office_name (CharField): Name of the office.
        contact_number (CharField): Contact number.
        address (TextField): Address of the office.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='exam_office_profile')
    office_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.TextField()

    def _str_(self):
        """
        Returns the string representation of the exam office or admin.

        Returns:
            str: The office name.
        """
        return self.office_name


# Course Model
class Course(models.Model):
    """
    Model representing a course offered by a department.

    Attributes:
        department (ForeignKey): Associated department.
        course_code (CharField): Unique course code.
        course_title (CharField): Title of the course.
    """
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    course_code = models.CharField(max_length=50, unique=True)
    course_title = models.CharField(max_length=255)

    def _str_(self):
        """
        Returns the string representation of the course.

        Returns:
            str: The course code and title.
        """
        return f"{self.course_code} - {self.course_title}"


# Exam Model
class Exam(models.Model):
    """
    Model representing an exam linked to a course, department, and invigilators.

    Attributes:
        department (ForeignKey): Associated department.
        course (ForeignKey): Course for which the exam is held.
        exam_date (DateField): Date of the exam.
        batch (CharField): Batch for which the exam is conducted.
        session (CharField): Academic session of the exam.
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

    def _str_(self):
        """
        Returns the string representation of the exam.

        Returns:
            str: Details of the exam including course code and date.
        """
        return f"Exam {self.id} for {self.course.course_code} on {self.exam_date}"


# Exam Schedule Model
class ExamSchedule(models.Model):
    """
    Model for an exam schedule with publication and modification dates.

    Attributes:
        exam (OneToOneField): Associated exam.
        published_date (DateField): Publication date of the schedule.
        modified_date (DateField): Date of any modification.
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

    def _str_(self):
        """
        Returns the string representation of the exam schedule.

        Returns:
            str: Details of the schedule including associated exam.
        """
        return f"Schedule for {self.exam}"


# Exam Registration Model
class ExamRegistration(models.Model):
    """
    Model representing exam registrations by students with status and payment information.

    Attributes:
        student (ForeignKey): The student who registers for the exam.
        exams (ManyToManyField): Exams registered by the student.
        registration_type (CharField): Type of registration (Regular or Retake).
        registration_date (DateField): Date of the registration.
        status (CharField): Current registration status (Pending, Verified, or Rejected).
        payment_status (CharField): Payment status for the application.
        payment_method (CharField): Method of payment used.
        ineligibility_reasons (TextField): Reasons if registration is ineligible.
        admit_card_generated (BooleanField): Indicates if admit card is generated.
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
    registration_type = models.CharField(max_length=20, choices=REGISTRATION_TYPE_CHOICES)
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    ineligibility_reasons = models.TextField(null=True, blank=True)
    admit_card_generated = models.BooleanField(default=False)

    def _str_(self):
        """
        Returns the string representation of the exam registration.

        Returns:
            str: Details of the registration including student name and registration ID.
        """
        return f"Registration {self.id} by {self.student.name}"


# Results Model
class Result(models.Model):
    """
    Model representing the result of an exam for a specific student.

    Attributes:
        exam (ForeignKey): The exam associated with this result.
        student (ForeignKey): The student who took the exam.
        marks (IntegerField): Marks obtained by the student.
    """
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='results')
    marks = models.IntegerField()

    class Meta:
        unique_together = ('exam', 'student')

    def _str_(self):
        """
        Returns the string representation of the result.

        Returns:
            str: Details of the result including student name and marks obtained.
        """
        return f"Result {self.id} - {self.student.name}: {self.marks} marks"


# Marksheet Application Model
class MarksheetApplication(models.Model):
    """
    Model representing an application for obtaining a marksheet.

    Attributes:
        student (ForeignKey): The student applying for the marksheet.
        exam (ForeignKey): The exam associated with the marksheet.
        application_date (DateField): Date of application submission.
        status (CharField): Application status (Pending, Approved, or Rejected).
        payment_status (CharField): Payment status for the application.
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
    token = models.CharField(max_length=100, unique=True)

    def _str_(self):
        """
        Returns the string representation of the marksheet application.

        Returns:
            str: Details of the application including student name and application ID.
        """
        return f"Marksheet Application {self.id} by {self.student.name}"


# Certificate Application Model
class CertificateApplication(models.Model):
    """
    Model representing an application for a certificate.

    Attributes:
        student (ForeignKey): The student applying for the certificate.
        degree (CharField): Degree associated with the certificate.
        application_date (DateField): Date of application submission.
        status (CharField): Status of the application.
        payment_status (CharField): Payment status for the application.
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
    token = models.CharField(max_length=100, unique=True)

    def _str_(self):
        """
        Returns the string representation of the certificate application.

        Returns:
            str: Details of the application including student name and application ID.
        """
        return f"Certificate Application {self.id} by {self.student.name}"


# Teacher Remuneration Model
class TeacherRemuneration(models.Model):
    """
    Model for tracking teacher remuneration for different roles in exams.

    Attributes:
        teacher (ForeignKey): The teacher receiving remuneration.
        exam (ForeignKey): The associated exam.
        role (CharField): Role of the teacher for the remuneration.
        amount (DecimalField): Amount paid to the teacher.
        status (CharField): Status of the remuneration (Pending or Paid).
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

    def _str_(self):
        """
        Returns the string representation of the teacher remuneration.

        Returns:
            str: Details of the remuneration including teacher name and role.
        """
        return f"Remuneration {self.id} for {self.teacher.name} as {self.role}"


# Exam Materials Model
class ExamMaterials(models.Model):
    """
    Model representing materials needed for an exam.

    Attributes:
        exam (ForeignKey): The exam associated with the materials.
        material_type (CharField): Type of material (Answer Scripts, Pens, Question Papers).
        quantity (IntegerField): Quantity of the material.
    """
    MATERIAL_TYPE_CHOICES = [
        ('AnswerScripts', 'Answer Scripts'),
        ('Pens', 'Pens'),
        ('QuestionPapers', 'Question Papers'),
    ]

    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='materials')
    material_type = models.CharField(max_length=50, choices=MATERIAL_TYPE_CHOICES)
    quantity = models.IntegerField()

    def _str_(self):
        """
        Returns the string representation of the exam materials.

        Returns:
            str: Details of the materials including type and associated exam.
        """
        return f"{self.material_type} for {self.exam}"


# Attendance Model
class Attendance(models.Model):
    """
    Model to track attendance of students and invigilators for an exam.

    Attributes:
        exam (ForeignKey): The exam associated with the attendance record.
        student (ForeignKey): The student who attended, if applicable.
        teacher (ForeignKey): The teacher who attended, if applicable.
        attendance_date (DateField): Date of attendance.
        role (CharField): Role of the person in the exam (Student or Invigilator).
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

    def _str_(self):
        """
        Returns the string representation of the attendance.

        Returns:
            str: Details of the attendance including attendee name, role, and date.
        """
        if self.role == 'Student':
            return f"Attendance {self.id} - {self.student.name} as {self.role} on {self.attendance_date}"
        else:
            return f"Attendance {self.id} - {self.teacher.name} as {self.role} on {self.attendance_date}"