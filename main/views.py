from django.shortcuts import render

# Login & SignUp
def user_login(request):
    return render(request, "common/login.html")
def student_signup(request):
    pass

# Class
def attendance(request):
    return render(request, "student/class/attendance.html")
def timetable(request):
    return render(request, "student/class/timetable.html")

# Result
def ia_result(request):
    return render(request, "student/result/ia.html")
def model_result(request):
    return render(request, "student/result/model.html")
def sem_result(request):
    return render(request, "student/result/sem.html")
