from django.urls import path
from . import views
urlpatterns = [
    path("", views.home, name="home"),
    path("student/attendance/<str:student_id>", views.attendance , name="attendance"),
    path("student/timetable/<str:student_id>", views.timetable , name="timetable"),
    path("student/ia-result/<str:student_id>", views.ia_result , name="ia-result"),
    path("student/model-result/<str:student_id>", views.model_result , name="model-result"),
    path("student/sem-result/<str:student_id>", views.sem_result , name="sem-result"),
    path("student/notes/<str:student_id>", views.notes , name="notes"),

    path("staff/attendance/<str:class_id>/", views.staff_attendance , name="staff-attendance"),
    path("staff/timetable/<str:class_id>", views.staff_timetable , name="staff-timetable"),
    path("staff/ia-result/<str:class_id>", views.staff_ia_result , name="staff-ia-result"),
    path("staff/model-result/<str:class_id>", views.staff_model_result , name="staff-model-result"),
    path("staff/sem-result/<str:class_id>", views.staff_sem_result , name="staff-sem-result"),
    path("staff/notes/<str:class_id>", views.staff_notes , name="staff-notes"),
    path("staff/add-timetable-form/<str:class_id>", views.add_timetable_form, name="add-timetable-form"),
    path("staff/add-attendance-form/<str:class_id>/<str:_date>", views.add_attendance_form, name="add-attendance-form"),
    path("staff/add-student", views.add_student, name="add-student"),
    path("admin/attendance/<str:class_id>", views.admin_attendance, name="admin-attendance"),
    path("admin/notes/<str:class_id>", views.admin_notes, name="admin-notes"),
    path("admin/timetable/<str:class_id>", views.admin_timetable, name="admin-timetable"),
    path("admin/results/<str:class_id>", views.admin_results, name="admin-results"),
    path("admin/exams/<str:class_id>", views.admin_exams, name="admin-exams"),
    path("login", views.user_login , name="login"),
    path("logout", views.user_logout , name="logout"),
    path("admin/<str:class_id>", views.staff_admin , name="admin"),
]