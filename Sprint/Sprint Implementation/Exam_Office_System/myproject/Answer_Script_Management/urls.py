from django.urls import path
from .views import manage_answer_scripts, view_attendance_and_scripts, evaluate_script, finalize_management

urlpatterns = [
    path('manage/', manage_answer_scripts, name='manage_answer_scripts'),
    path('exam/<int:exam_id>/attendance/', view_attendance_and_scripts, name='view_attendance_and_scripts'),
    path('evaluate/<int:script_id>/', evaluate_script, name='evaluate_script'),
    path('finalize/', finalize_management, name='finalize_management'),
]