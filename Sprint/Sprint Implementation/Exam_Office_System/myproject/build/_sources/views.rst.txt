Views Documentation
===================

ExamCalendarListView
---------------------
This view lists all the exam calendars. It fetches all the `ExamCalendar` objects from the database
and passes them to the `exam_calendar_list.html` template.

CreateExamCalendarView
-----------------------
This view handles both displaying the form for creating an exam calendar and processing the form submission.
It saves both the `ExamCalendar` and `Exam` objects upon successful form submission.

ExamCalendarDetailView
-----------------------
This view displays the details of a specific `ExamCalendar`. It fetches the `ExamCalendar` by its primary key and
renders the `exam_calendar_detail.html` template.
