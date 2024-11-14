from django.urls import path
from . import views
app_name = 'exam'
urlpatterns = [
    path('attendance/record/', views.record_attendance, name='record_attendance'),
    path('attendance/statistics/<int:attendance_id>/', views.attendance_statistics, name='attendance_statistics'),
]


