from django.urls import path
from . import views

urlpatterns = [
    # Registration URLs
    path('register/exam_office/', views.ExamOfficeRegisterView.as_view(), name='register_exam_office'),
    path('register/student/', views.StudentRegisterView.as_view(), name='register_student'),
    path('register/teacher/', views.TeacherRegisterView.as_view(), name='register_teacher'),
    path('register/department/', views.DepartmentRegisterView.as_view(), name='register_department'),
    
    # Login and Logout URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]
