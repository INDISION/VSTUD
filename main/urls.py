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
    path("staff/attendance", views.staff_attendance , name="staff-attendance"),
    path("staff/timetable", views.staff_timetable , name="staff-timetable"),
    path("staff/ia-result", views.staff_ia , name="staff-ia-result"),
    path("staff/model-result", views.model_result , name="staff-model-result"),
    path("staff/sem-result", views.sem_result , name="staff-sem-result"),
    path("staff/notes", views.staff_notes , name="staff-notes"),
    path("login", views.user_login , name="login"),
    path("staff/timetable", views.staff_timetable, name="staff-timetable"),
    path("staff/add-timetable-form", views.add_timetable_form, name="add-timetable-form"),

]