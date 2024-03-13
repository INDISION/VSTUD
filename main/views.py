from django.shortcuts import render,redirect
from django.shortcuts import get_object_or_404
from . import models
from django.core.mail import send_mail
from django.conf import settings
from datetime import datetime, timedelta
import calendar
from django.contrib.auth.models import User
import random,string

def user_role(user):
    try:
        student = models.Student.objects.get(user=user)
        staff = False
    except:
        staff = models.Staff.objects.get(user=user)
        student = False
    role = {"student":student, "staff":staff}
    return role
# Login & SignUp
def user_login(request):
    return render(request, "staff/class/base.html")
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
    student = models.Student.objects.get(user=user)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)
    timetable = models.TimeTable.objects.filter(subject__class_related=student.class_attending)
    sem_start_date = student.class_attending.start_date
    sem_end_date = student.class_attending.end_date

    # Academic Calendar
    cal = {}
    date_pointer = sem_start_date
    while date_pointer <= sem_end_date:
        year = date_pointer.year
        month = date_pointer.month
        month_name = calendar.month_name[month]
        if month_name not in cal:
            cal[month_name] = calendar.monthcalendar(year, month)
        date_pointer += timedelta(days=1)
    _holidays = {}
    for holiday in holidays:
        month = holiday.date.month
        if month not in _holidays:
            _holidays[month] = []
        else:
            _holidays[month].append(holiday.date.day)
    
    # Timetable
    _timetable = {}
    for each in timetable:
        day = each.day
        if day not in _timetable:
            _timetable[day] = []
        _timetable[day].append(each)
    context = {
        "user":user,
        "student":student, 
        "cal":cal, 
        "holidays":_holidays, 
        "timetable":_timetable
        }
    return render(request, "student/class/timetable.html", context)

def notes(request):
    user = request.user
    student = models.Student.objects.get(user=user)
    subjects = models.Subject.objects.filter(class_related=student.class_attending)
    _notes = []
    for subject in subjects:
        _notes.append(models.Note.objects.filter(subject=subject))
    for subject_note in _notes:
        for note in subject_note:
            print(note.title)
    context = {
        "subjects":subjects,
        "all_notes":_notes,
    }
    return render(request, "student/class/notes.html", context)


# Result
def ia_result(request):
    user = request.user
    student = models.Student.objects.get(user=user)
    ia1 = models.Result.objects.filter(exam__name="ia1", student=student, class_related=student.class_attending)
    ia2 = models.Result.objects.filter(exam__name="ia2", student=student, class_related=student.class_attending)
    ia3 = models.Result.objects.filter(exam__name="ia3", student=student, class_related=student.class_attending)
    context = {
        "user":user,
        "student":student,
        "ia1":ia1,
        "ia2":ia2,
        "ia3":ia3
    }
    return render(request, "student/result/ia.html", context)

def model_result(request):
    user = request.user
    student = models.Student.objects.get(user=user)
    model_exam = models.Result.objects.filter(exam__name="model", student=student, class_related=student.class_attending)
    context = {
        "user":user,
        "student":student,
        "model":model_exam,
    }
    return render(request, "student/result/model.html", context)

def sem_result(request):
    user = request.user
    student = models.Student.objects.get(user=user)
    semesters_data = []
    for i in range(1,9):
        sem = "semester-"+str(i)
        semesters_data.append(models.Result.objects.filter(exam__name=sem, student=student))
    print(semesters_data)
    context = {
        "user":user,
        "student":student,
        "semesters_data":semesters_data
    }
    return render(request, "student/result/sem.html", context)
