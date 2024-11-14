# Answer_Script_Management/admin.py
from django.contrib import admin
from .models import AnswerScript, ScriptEvaluationLog, ScriptEvaluationLog

admin.site.register(AnswerScript)
admin.site.register(ScriptEvaluationLog)
