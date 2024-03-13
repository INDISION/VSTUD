from django.shortcuts import render,HttpResponse,redirect
from . import models
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import calendar
from django.contrib.auth.models import User
import random,string

# Login & SignUp
def user_login(request):
    return render(request, "common/login.html")
def add_student(request):
    if request.method == 'POST':
        first_name = request.POST.get("first-name")
        last_name = request.POST.get("last-name")
        email = request.POST.get("email")
        register_no = request.POST.get("register-no")
        class_attending = request.POST.get("class")
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        transport = request.POST.get("transport")
        phone_no = request.POST.get("phone-no")
        mentor = request.POST.get("mentor")
        username =f"{class_attending[:5]}{register_no[-3:]}"

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        staff_user = models.User.objects.get(username=mentor)
        class_attending = models.Class.objects.get(class_id=class_attending)
        mentor=models.Staff.objects.get(user=staff_user)
        user = User.objects.create_user(first_name=first_name,last_name=last_name,email=email,username=username , password=password)
        user.save()
        message = f'''
Hello {first_name}, Welcome To VSTUD.
We are from Velammal Institute Of Technology!!!
Username : {username}
password : {password}

Disclaimer : **Dont forget to change your password on website**
'''
        send_mail(
                'VSTUD',message,'settings.EMAIL_HOST_USER',[email],fail_silently=False

            )        
        if user:
            student = models.Student(user=user, name=first_name,register_number=register_no,class_attending=class_attending,date_of_birth=dob,gender=gender,phone=phone_no,mentor=mentor)
            student.save()
            return redirect('attendance')
            
    return render(request , "staff/add-student-form.html")

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
    user = request.user
    student = models.Student.objects.get(user = user)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)
    sem_start_date = student.class_attending.start_date
    sem_end_date = student.class_attending.end_date
    cal = {}
    date_pointer = sem_start_date
    while date_pointer <= sem_end_date:
        year = date_pointer.year
        month = date_pointer.month
        month_name = calendar.month_name[month]
        if month_name not in cal:
            cal[month_name] = calendar.monthcalendar(year, month)
        date_pointer += timedelta(days=1)

    context = {"cal":cal, "holidays":holidays}
    return render(request, "student/class/timetable.html", context)

# Result
def ia_result(request):
    return render(request, "student/result/ia.html")
def model_result(request):
    return render(request, "student/result/model.html")
def sem_result(request):
    return render(request, "student/result/sem.html")
