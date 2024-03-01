from django.urls import path
from . import views
urlpatterns = [
    path("", views.attendance , name="attendance"),
    path("timetable", views.timetable , name="timetable"),
    path("ia-result", views.ia_result , name="ia-result"),
    path("model-result", views.model_result , name="model-result"),
    path("sem-result", views.sem_result , name="sem-result"),
]