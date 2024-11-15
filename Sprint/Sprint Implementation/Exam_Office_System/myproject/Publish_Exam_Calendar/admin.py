from django.contrib import admin
from .models import ExamCalendar

@admin.register(ExamCalendar)
class ExamCalendarAdmin(admin.ModelAdmin):
    list_display = ('system_type', 'exam_start_date', 'exam_end_date', 'approval_status', 'created_at')
    search_fields = ('system_type', 'exam_start_date', 'exam_end_date')
    list_filter = ('approval_status', 'system_type')
