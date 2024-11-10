# Answer_Script_Management/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('assign_answer_script/<int:exam_id>/', views.assign_answer_script, name='assign_answer_script'),
    path('grade_answer_script/<int:answer_script_id>/', views.grade_answer_script, name='grade_answer_script'),
    path('finalize_answer_script/<int:answer_script_id>/', views.finalize_answer_script, name='finalize_answer_script'),
]
