from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from datetime import datetime, timedelta, date
import calendar
from .templatetags.custom_filters import calculate_attendance

# Home
def home(request):
    user = request.user
    student=staff=None
    try:
        student = models.Student.objects.get(user=user)
    except:
        staff = models.Staff.objects.get(user=user)
    if student:
        return redirect("attendance")
    elif staff:
        return redirect("staff-attendance")
    else:
        return redirect("login")
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
                    return redirect("staff-attendance")
                else:
                    return redirect("attendance")
        else:
            messages.error(request, "Invalid username or password.")
            return redirect("login")
    return render(request, "student/common/login.html")

def student_signup(request):
    pass

# Class
def attendance(request):
    month = datetime.now().month
    year = datetime.now().year
    user = request.user
    student = models.Student.objects.get(user=user)

    month_percent = calculate_attendance(student=student, start_date=datetime(year, month, 1).date())

    sem_percent = calculate_attendance(student=student, start_date=student.class_attending.start_date)

    data = {
        "sem_percent" : sem_percent,
        "month_percent" : month_percent,
        "student" : student,
    }
    return render(request, "student/class/attendance.html", data)

def staff_attendance(request):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    # Absentees List
    absent_students = []
    present_students = []
    extra_details = {}
    context = {
        "user":user,
        "staff":staff,
        "date" : date.today(),
        "details":extra_details,
        "classes":class_attending_list,
        "absentees":absent_students,
    }
    for class_attending in class_attending_list:
        class_id = class_attending.class_id
        class_absent_students = []
        class_present_students = []
        students = models.Student.objects.filter(class_attending=class_attending)
        for student in students:
            try:
                student_attendance = models.Attendance.objects.get(student=student, class_related=class_attending, date=date.today())
            except:
                student_attendance = None
            if student_attendance!=None and student_attendance.present_status:
                class_present_students.append(student)
            else:
                class_absent_students.append(student)
            context[student.user.username] = calculate_attendance(start_date=student.class_attending.start_date, student=student)
        absent_students.append(class_absent_students)
        present_students.append(class_present_students)
        extra_details[class_id+"_strenth"] = len(students)
    print(extra_details)
    return render(request, "staff/class/attendance.html", context)

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
        "user":user,
        "student":student,
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
    return render(request, "staff/class/staff-timetable.html", context)

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
    return render(request, "staff/class/add-timetable-form.html")

def staff_notes(request):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    context = {
        'user': user,
        'staff': staff,
        'subjects': subjects,
        "classes": class_attending_list,
    }
    print(subjects)

    return render(request, "staff/class/staff-notes.html", context)

def staff_ia(request):
    return render(request, "staff/result/staff-ia.html")
