from django.shortcuts import render

# Login & SignUp
def user_login(request):
    return render(request, "common/login.html")
def student_signup(request):
    pass

# Class
def attendance(request):
    return render(request, "student/attendance.html")
def timetable(result):
    pass

# Result
def ia_result(result):
    pass
def model_result(result):
    pass
def sem_result(result):
    pass
