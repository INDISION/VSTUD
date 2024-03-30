from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.user_login , name="login"),
    path("student/attendance", views.attendance , name="attendance"),
    path("student/timetable", views.timetable , name="timetable"),
    path("student/ia-result", views.ia_result , name="ia-result"),
    path("student/model-result", views.model_result , name="model-result"),
    path("student/sem-result", views.sem_result , name="sem-result"),
    path("student/notes", views.notes , name="notes"),
    path("<str:class_id>/attendance", views.staff_attendance , name="staff-attendance"),
    path("<str:class_id>/timetable", views.staff_timetable , name="staff-timetable"),
    path("<str:class_id>/ia-result", views.staff_ia_result , name="staff-ia-result"),
    path("<str:class_id>/model-result", views.staff_model_result , name="staff-model-result"),
    path("<str:class_id>/sem-result", views.staff_sem_result , name="staff-sem-result"),
    path("staff-notes/<str:class_id>", views.staff_notes , name="staff-notes"),
    path("add-timetable-form/<str:class_id>", views.add_timetable_form, name="add-timetable-form"),
    path("add-notes-form/<str:class_id>", views.add_notes_form , name="add-notes-form"),
    path("add-staff-form/<str:class_id>", views.add_staff_form , name="add-staff-form"),
    path("add-subject-form/<str:class_id>", views.add_subject_form , name="add-subject-form"),
    path("add-holiday-form/<str:class_id>", views.add_holiday_form , name="add-holiday-form"),
    path("add-attendance-form/<str:class_id>/<str:_date>", views.add_attendance_form , name="add-attendance-form"),
    path("staff/add-marks-ia-form", views.add_marks_ia_form , name="add-marks-ia-form"),
    path("staff/add-marks-model-form", views.add_marks_model_form , name="add-marks-model-form"),
    path("staff/add-marks-semester-form", views.add_marks_semester_form , name="add-marks-semester-form"),
    path("staff/add-student-form", views.add_student_form , name="add-student-form"),
    path("add-department-form/<str:class_id>", views.add_department_form , name="add-department-form"),
    path("password-reset-form", views.password_reset_form , name="password-reset-form"),
    path("check-mail-notfiication", views.check_mail_notification , name="check-mail-notification"),
    path("logout", views.user_logout , name="logout"),
    path("mail-form", views.mail_form , name="mail-form"),

    
]