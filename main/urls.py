from django.urls import path
from . import views
urlpatterns = [
    path("student/attendance", views.attendance , name="attendance"),
    path("student/timetable", views.timetable , name="timetable"),
    path("student/ia-result", views.ia_result , name="ia-result"),
    path("student/model-result", views.model_result , name="model-result"),
    path("student/sem-result", views.sem_result , name="sem-result"),
    path("student/notes", views.notes , name="notes"),
    path("staff/attendance", views.staff_attendance , name="staff-attendance"),
    path("staff/timetable", views.staff_timetable , name="staff-timetable"),
    path("staff/ia-result", views.staff_ia , name="staff-ia-result"),
    path("staff/model-result", views.model_result , name="staff-model-result"),
    path("staff/sem-result", views.sem_result , name="staff-sem-result"),
    path("staff/notes", views.staff_notes , name="staff-notes"),
    path("login", views.user_login , name="login"),
    path("staff/timetable", views.staff_timetable, name="staff-timetable"),
    path("staff/add-timetable-form", views.add_timetable_form, name="add-timetable-form"),
    path("staff/add-notes-form", views.add_notes_form , name="add-notes-form"),
    path("staff/add-staff-form", views.add_staff_form , name="add-staff-form"),
    path("staff/add-subject-form", views.add_subject_form , name="add-subject-form"),
    path("<str:class_id>/add-holiday-form", views.add_holiday_form , name="add-holiday-form"),
    path("staff/add-attendance-form", views.add_attendance_form , name="add-attendance-form"),
    path("staff/add-marks-ia-form", views.add_marks_ia_form , name="add-marks-ia-form"),
    path("staff/add-marks-model-form", views.add_marks_model_form , name="add-marks-model-form"),
    path("staff/add-marks-semester-form", views.add_marks_semester_form , name="add-marks-semester-form"),
    path("staff/add-student-form", views.add_student_form , name="add-student-form"),



]