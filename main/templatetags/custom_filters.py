from django import template
from .. import models
import calendar

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