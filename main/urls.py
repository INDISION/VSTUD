from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("student/attendance", views.attendance , name="attendance"),
    path("student/timetable", views.timetable , name="timetable"),
    path("student/ia-result", views.ia_result , name="ia-result"),
    path("student/model-result", views.model_result , name="model-result"),
    path("student/sem-result", views.sem_result , name="sem-result"),
    path("student/notes", views.notes , name="notes"),
    path("attendance/<str:class_id>/", views.staff_attendance , name="staff-attendance"),
    path("timetable/<str:class_id>", views.staff_timetable , name="staff-timetable"),
    path("ia-result/<str:class_id>", views.staff_ia_result , name="staff-ia-result"),
    path("model-result/<str:class_id>", views.staff_model_result , name="staff-model-result"),
    path("sem-result/<str:class_id>", views.staff_sem_result , name="staff-sem-result"),
    path("notes/<str:class_id>", views.staff_notes , name="staff-notes"),
    path("add-timetable-form/<str:class_id>", views.add_timetable_form, name="add-timetable-form"),
    path("add-attendance-form/<str:class_id>/<str:_date>", views.add_attendance_form, name="add-attendance-form"),
    path("add-student", views.add_student, name="add-attendance-form"),
    path("login", views.user_login , name="login"),
]