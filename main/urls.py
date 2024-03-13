from django.urls import path
from . import views
urlpatterns = [
    path("", views.attendance , name="attendance"),
    path("student/timetable", views.timetable , name="timetable"),
    path("student/ia-result", views.ia_result , name="ia-result"),
    path("student/model-result", views.model_result , name="model-result"),
    path("student/sem-result", views.sem_result , name="sem-result"),
    path("login", views.user_login , name="login"),
    path("staff/timetable", views.staff_timetable, name="staff-timetable"),
    path("staff/add-timetable-form", views.add_timetable_form, name="add-timetable-form"),
]