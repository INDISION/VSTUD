from django.shortcuts import render
from . import models
from datetime import datetime
import calendar

# Login & SignUp
def user_login(request):
    return render(request, "common/login.html")
def student_signup(request):
    pass

def cal_attendance(start_date, attendance, holidays):
    completed_holidays = []
    for holiday in holidays:
        print(holiday.date, holiday.date <= datetime.now().date() and holiday.date >= start_date)
        if holiday.date <= datetime.now().date() and holiday.date >= start_date:
            completed_holidays.append(holiday)
    days = (datetime.now().date() - start_date).days + 1
    working_days = days - len(completed_holidays)
    present_days = []
    for day in attendance:
        if day.date <= datetime.now().date() and day.date >= start_date:
            present_days.append(holiday)
    attendance_percent = int(len(present_days)/working_days*100)
    return attendance_percent

# Class
def attendance(request):
    month = datetime.now().month
    year = datetime.now().year
    user = request.user
    student = models.Student.objects.get(user=user)
    user_attendance = models.Attendance.objects.filter(student=student)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)

    month_percent = cal_attendance(start_date=datetime(year, month, 1).date(), attendance=user_attendance, holidays=holidays)

    sem_percent = cal_attendance(start_date=student.class_attending.start_date, attendance=user_attendance, holidays=holidays)

    data = {
        "sem_percent" : sem_percent,
        "month_percent" : month_percent,
        "student" : student,
    }
    return render(request, "student/class/attendance.html", data)

def timetable(request):
    return render(request, "student/class/timetable.html")

# Result
def ia_result(request):
    return render(request, "student/result/ia.html")
def model_result(request):
    return render(request, "student/result/model.html")
def sem_result(request):
    return render(request, "student/result/sem.html")
