from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
import calendar

def class_dropdown(staff):
    subjects = models.Subject.objects.filter(staff = staff)
    class_attending = []
    for subject in subjects:
        class_attending.append(subject.class_related)
    return class_attending

# Login & SignUp
def user_login(request):   
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
                login(request, user)
                try:
                    staff = models.Staff.objects.get(user=user)
                except:
                    staff = None
                if(staff!=None):
                    return redirect("staff-timetable")
                else:
                    return redirect("attendance")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "student/common/login.html")

def student_signup(request):
    pass

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

#For Staffs
def staff_timetable(request):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    context ={
        "staff":staff,
        "user":user,
    }
    return render(request, "staff/staff-timetable.html", context)

def add_timetable_form(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        subject_name = request.POST.get('period')
        subject = get_object_or_404(models.Subject, name=subject_name)     
        models.TimeTable.objects.create(
            day=day,
            start_time=start_time,
            end_time=end_time,
            subject=subject
        )
    if 'save_and_next' in request.POST:
        return render(request, "staff/add-timetable-form.html")
    elif 'save_and_exit' in request.POST:
        return render(request, "staff/staff-timetable.html")
    return render(request, "staff/add-timetable-form.html")

def staff_attendance(request):
    return render(request, "staff/class/staff-attendance.html")

def staff_notes(request):
    return render(request, "staff/class/staff-notes.html")



