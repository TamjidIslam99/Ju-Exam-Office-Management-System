from django.contrib import admin
from .models import (
    User, Department, Student, Teacher, ExamOfficeOrAdmin, Course, Exam,
    ExamSchedule, ExamRegistration, Result, MarksheetApplication,
    CertificateApplication, TeacherRemuneration, ExamMaterials, Attendance
)

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(ExamOfficeOrAdmin)
admin.site.register(Course)
admin.site.register(Exam)
admin.site.register(ExamSchedule)
admin.site.register(ExamRegistration)
admin.site.register(Result)
admin.site.register(MarksheetApplication)
admin.site.register(CertificateApplication)
admin.site.register(TeacherRemuneration)
admin.site.register(ExamMaterials)
admin.site.register(Attendance)
