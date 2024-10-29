# accounts/urls.py

from django.urls import path
from .views import (
    RegisterExamOfficeView,
    RegisterDepartmentView,
    RegisterTeacherView,
    RegisterStudentView,
    HomePageView,
    LoginView
)

urlpatterns = [
    path('home', HomePageView.as_view(), name='home'),  # Homepage at '/accounts/'
    path('register/exam_office/', RegisterExamOfficeView.as_view(), name='register_exam_office'),
    path('register/department/', RegisterDepartmentView.as_view(), name='register_department'),
    path('register/teacher/', RegisterTeacherView.as_view(), name='register_teacher'),
    path('register/student/', RegisterStudentView.as_view(), name='register_student'),
    path('login/', LoginView.as_view(), name='login'),


]
