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
    path("<str:class_id>/attendance", views.staff_attendance , name="staff-attendance"),
    path("<str:class_id>/timetable", views.staff_timetable , name="staff-timetable"),
    path("<str:class_id>/ia-result", views.staff_ia_result , name="staff-ia-result"),
    path("<str:class_id>/model-result", views.staff_model_result , name="staff-model-result"),
    path("<str:class_id>/sem-result", views.staff_sem_result , name="staff-sem-result"),
    path("<str:class_id>/notes", views.staff_notes , name="staff-notes"),
    path("<str:class_id>/add-timetable-form", views.add_timetable_form, name="add-timetable-form"),
    path("login", views.user_login , name="login"),

]