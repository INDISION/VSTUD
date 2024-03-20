from django import template
from .. import models
import calendar
from datetime import datetime, date

register = template.Library()


@register.filter(name='set_user')
def set_user(user):
    global current_user
    current_user = user
    return ""

@register.filter(name='check_holiday')
def check_holiday(month,day):
    student = models.Student.objects.get(user=current_user)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)
    for holiday in holidays:
        holiday_month = calendar.month_name[holiday.date.month]
        holiday_day = holiday.date.day
        if holiday_month==month and  holiday_day==day:
            return True
    return False

@register.filter(name='set_class_id')
def set_user(classID):
    global class_id
    class_id = classID
    return ""

@register.filter(name='staff_check_holiday')
def check_holiday(month,day):
    class_related = models.Class.objects.get(class_id=class_id)
    holidays = models.Holiday.objects.filter(class_related=class_related)
    for holiday in holidays:
        holiday_month = calendar.month_name[holiday.date.month]
        holiday_day = holiday.date.day
        if holiday_month==month and  holiday_day==day:
            return True
    return False

@register.filter(name='calculate_attendance')
def calculate_attendance(student, start_date=None):
    if start_date==None:
        start_date = student.class_attending.start_date
    attendance = models.Attendance.objects.filter(student=student)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)
    completed_holidays = []
    for holiday in holidays:
        if holiday.date <= datetime.now().date() and holiday.date >= start_date:
            completed_holidays.append(holiday)
    days = (datetime.now().date() - start_date).days + 1
    working_days = days - len(completed_holidays)
    present_days = []
    for day in attendance:
        if day.date <= datetime.now().date() and day.date >= start_date:
            present_days.append(day)
    attendance_percent = int(len(present_days)/working_days*100)
    return attendance_percent

@register.filter(name='calculate_leaves')
def calculate_leaves(student, start_date=None):
    if start_date==None:
        start_date = student.class_attending.start_date
    attendance = models.Attendance.objects.filter(student=student)
    holidays = models.Holiday.objects.filter(class_related=student.class_attending)
    completed_holidays = []
    for holiday in holidays:
        if holiday.date <= datetime.now().date() and holiday.date >= start_date:
            completed_holidays.append(holiday)
    days = (datetime.now().date() - start_date).days + 1
    working_days = days - len(completed_holidays)
    present_days = []
    for day in attendance:
        if day.date <= datetime.now().date() and day.date >= start_date:
            present_days.append(day)
    leaves = working_days - len(present_days)
    return leaves

@register.filter(name='class_strength')
def class_strength(class_related):
    students = models.Student.objects.filter(class_attending=class_related)
    return len(students)

@register.filter(name='class_present_count')
def class_present_count(class_related):
    attendance = models.Attendance.objects.filter(class_related=class_related, present_status=True, date=date.today())
    return len(attendance)

@register.filter(name='class_absent_count')
def class_absent_count(class_related):
    attendance = models.Attendance.objects.filter(class_related=class_related, present_status=False, date=date.today())
    return len(attendance)