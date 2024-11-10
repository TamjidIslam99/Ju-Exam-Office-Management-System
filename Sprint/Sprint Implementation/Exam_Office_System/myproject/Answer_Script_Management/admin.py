# Answer_Script_Management/admin.py
from django.contrib import admin
from .models import AnswerScript, GradingDiscrepancy, FinalizedAnswerScript

admin.site.register(AnswerScript)
admin.site.register(GradingDiscrepancy)
admin.site.register(FinalizedAnswerScript)
