from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from . import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta, date
import calendar
from .templatetags.custom_filters import calculate_attendance

# Basic
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

def class_dropdown(staff):
    subjects = models.Subject.objects.filter(staff = staff)
    class_attending = []
    for subject in subjects:
        class_attending.append(subject.class_related)
    return class_attending


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

def staff_attendance(request, class_id=None):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    context = {
        "user":user,
        "staff":staff,
        "date" : date.today(),
        "classes":class_attending_list,
        "class_id":class_id,
    }
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
    try:
        holiday = models.Holiday.objects.get(date=date.today(), class_related__class_id=class_id)
    except:
        holiday = False
    
    context["present"] = len(class_present_students)
    context["absent"] = len(class_absent_students)
    context["strength"] = len(class_absent_students) + len(class_present_students)
    context["absentees"] = class_absent_students
    context["holiday"] = holiday
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

def staff_timetable(request, class_id=None):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list and class_attending.class_id!=class_id:
            class_attending_list.append(class_attending)
    class_related = models.Class.objects.get(class_id=class_id)
    holidays = models.Holiday.objects.filter(class_related=class_related)
    timetable = models.TimeTable.objects.filter(subject__class_related=class_related)
    sem_start_date = class_related.start_date
    sem_end_date = class_related.end_date
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
    context ={
        "staff":staff,
        "user":user,
        "class_id":class_related,
        "classes":class_attending_list,
        "cal":cal, 
        "holidays":_holidays, 
        "timetable":_timetable,
    }
    return render(request, "staff/class/staff-timetable.html", context)

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
    print(_notes[4])
    return render(request, "student/class/notes.html", context) 

def staff_notes(request, class_id=None):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    subject = models.Subject.objects.get(staff=staff, class_related__class_id=class_id)
    subject_notes = models.Note.objects.filter(subject=subject)
    context = {
        'user': user,
        'staff': staff,
        "class_id":class_id,
        "classes": class_attending_list,
        'subject': subject,
        "subject_notes":subject_notes,
    }

    return render(request, "staff/class/staff-notes.html", context)

    
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

def staff_ia_result(request, class_id=None):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    subject = models.Subject.objects.get(class_related__class_id = class_id, staff=staff)
    ia1_results = models.Result.objects.filter(class_related__class_id=class_id, exam__name = 'ia1', exam__subject = subject)
    ia2_results = models.Result.objects.filter(class_related__class_id=class_id, exam__name = 'ia2', exam__subject = subject)
    ia3_results = models.Result.objects.filter(class_related__class_id=class_id, exam__name = 'ia3', exam__subject = subject)
    context = {
        "user":user,
        "staff":staff,
        "classes":class_attending_list,
        "class_id":class_id,
        "ia1_results" : ia1_results,
        "ia2_results" : ia2_results,
        "ia3_results" : ia3_results,
    }
    return render(request, "staff/result/staff-ia.html", context)

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

def staff_model_result(request, class_id=None):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    subject = models.Subject.objects.get(class_related__class_id = class_id, staff=staff)
    model_results = models.Result.objects.filter(class_related__class_id=class_id, exam__name = 'model', exam__subject = subject)
    context = {
        "user":user,
        "staff":staff,
        "classes":class_attending_list,
        "class_id":class_id,
        "model_results" : model_results,
    }
    return render(request, "staff/result/staff-model.html", context)

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

def staff_sem_result(request, class_id=None):
    user = request.user
    staff = models.Staff.objects.get(user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)
    subject = models.Subject.objects.get(class_related__class_id = class_id, staff=staff)
    semester_results = models.Result.objects.filter(class_related__class_id=class_id, exam__name = 'semester', exam__subject = subject)
    print(semester_results)
    context = {
        "user":user,
        "staff":staff,
        "classes":class_attending_list,
        "class_id":class_id,
        "semester_results" : semester_results,
    }
    return render(request, "staff/result/staff-sem.html", context)

# Forms
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

def add_notes_form(request):
    if request.method == 'POST':
        note_name = request.POST.get('note_name')
        note_file = request.POST.get('note_file')
        models.Note.objects.create(
            title = note_name,
            file = note_file,    
        )
        return redirect("staff-notes")

    return render(request, "staff/class/add-notes-form.html")

def add_staff_form(request):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        staff_name = first_name + ' ' +  last_name
        staff_number = request.POST.get('staff_number')
        staff_email = request.POST.get('staff_email')
        staff_reg = request.POST.get('staff_reg')

        
        user_name = staff_reg
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        new_user = User.objects.create_user(first_name=first_name,last_name=last_name,email=staff_email,username=user_name,password=password)
        new_user.is_staff = True
        new_user.save()

        models.Staff.objects.create(
            user = new_user,
            name = staff_name,
            phone = staff_number,    
        )
        if 'save-and-exit' in request.POST:
            return redirect("staff-attendance")
        elif 'next' in request.POST:
            return redirect("add-staff-form")
    context = {
        'user': user,
        'staff': staff,
        'subjects': subjects,
        "classes": class_attending_list,
    }
        
    return render(request, "staff/class/add-staff-form.html", context)

def add_subject_form(request):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    staff_members = models.Staff.objects.get("name")
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
        'staff_members': staff_members,
    }
    

    if request.method == 'POST':
        subject_name = request.POST.get('subject_name')
        subject_code = request.POST.get('subject_code')
        subject_credit = request.POST.get('subject_credit')

        

    return render(request, "staff/class/add-subject-form.html", context)

def add_holiday_form(request,class_id=None):
    user = request.user
    staff = get_object_or_404(models.Staff, user=user)
    subjects = models.Subject.objects.filter(staff=staff)
    class_attending_list = []
    for subject in subjects:
        class_attending = subject.class_related
        if class_attending not in class_attending_list:
            class_attending_list.append(class_attending)

    if request.method == 'POST':
        class_id = request.POST.get("class-related")
        class_related = models.Class.objects.get(class_id = class_id)
        date = request.POST.get('date')
        description = request.POST.get('description')
        print(date)
        print(description)
        models.Holiday.objects.create(
            class_related = class_related,
            date = date,
            description = description,  
        )

        print("---------------")
        if 'save-and-exit' in request.POST:
            return redirect("staff-attendance")
        elif 'next' in request.POST:
            return redirect("add-holiday-form", class_id)
    context = {
        'user': user,
        'staff': staff,
        'subjects': subjects,
        "classes": class_attending_list,
        "class_id": class_id,
    }
    return render(request, "staff/class/add-holiday-form.html" ,context)

def add_attendance_form(request):
    return render(request, "staff/class/add-attendance-form.html")

def add_marks_ia_form(request):
    return render(request, "staff/result/add-marks-ia-form.html")

def add_marks_model_form(request):
    return render(request, "staff/result/add-marks-model-form.html")

def add_marks_semester_form(request):
    return render(request, "staff/result/add-marks-sem-form.html")\
    
def add_student_form(request):
    return render(request, "staff/class/add-student-form.html")



